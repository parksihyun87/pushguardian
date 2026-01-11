# PushGuardian 성능 최적화 가이드

## 현재 병목 분석

### 전체 워크플로우 실행 시간 (예상)
```
1. load_config: ~10ms
2. scope_classify: ~50ms
3. hard_policy_check: ~100ms (secrets 검사)
4. soft_llm_judge: ~2000ms (LLM 호출) ⚠️ 병목
5. research_tavily: ~1500ms (검색 API + LLM annotation) ⚠️ 병목
6. observation_validate: ~1500ms (LLM 호출) ⚠️ 병목
7. research_serper: ~1500ms (검색 API + LLM annotation) ⚠️ 병목
8. observation_validate: ~1500ms (LLM 호출) ⚠️ 병목
9. [HITL] research_naver: ~3000ms (LLM 쿼리 생성 + 검색 + LLM 필터링) ⚠️ 병목
10. write_report: ~500ms (LLM 호출)
11. persist_report: ~50ms

총: ~12초 (HITL 없으면 ~9초, HITL 있으면 ~12초)
```

### 주요 병목
1. **LLM 호출**: 6-7회 (각 1-2초) = 총 6-14초
2. **검색 API**: 2-3회 (각 0.5-1.5초) = 총 1.5-4.5초
3. **순차 실행**: 병렬화 가능한 작업도 순차 실행 중

---

## ✅ 최적화 방안

### 1. 즉시 적용 가능 (Low Hanging Fruit)

#### A. Streamlit sleep 제거
**현재**: `time.sleep(1)` - 불필요한 1초 대기
**개선**: 제거
```python
# streamlit_app.py:189
# time.sleep(1)  # 제거
st.rerun()
```
**효과**: -1초

#### B. LLM 모델 최적화
**현재**: 모든 곳에서 gpt-4o-mini (동일 품질)
**개선**: 간단한 작업은 더 빠른 모델 사용
- 네이버 쿼리 생성: gpt-4o-mini → gpt-3.5-turbo (-30%)
- 네이버 필터링: gpt-4o-mini 유지 (품질 중요)

**효과**: -500ms

#### C. 네이버 검색 개수 줄이기
**현재**: 10개 검색 → LLM 필터링
**개선**: 5개 검색 (이미 1차 필터링으로 충분)
```python
# graph.py
results = search_naver(query_ko, max_results=5)  # 10 → 5
```
**효과**: -200ms

---

### 2. 병렬화 (중간 난이도)

#### A. 검색 API 병렬 실행
**현재**: Tavily → Observation → Serper (순차)
**개선**: Tavily + Serper 동시 실행 → Observation (1회만)

**구현**:
```python
# 새로운 노드: research_parallel
async def research_parallel_node(state: GuardianState) -> GuardianState:
    """Tavily와 Serper를 병렬로 실행"""
    import asyncio

    async def tavily_search():
        return gather_research(...)

    async def serper_search():
        return gather_research(..., search_engine="serper")

    # 병렬 실행
    tavily_result, serper_result = await asyncio.gather(
        tavily_search(),
        serper_search()
    )

    # 결과 병합
    merged = merge_evidence(tavily_result, serper_result)
    return state
```

**효과**: -1500ms (50% 단축)

#### B. LLM 배치 처리
**현재**: Link annotation을 순차적으로 1개씩 처리
**개선**: 모든 링크를 한 번에 LLM에게 전달

```python
# research/link_annotator.py
def annotate_links_batch(links: List[str]) -> List[Dict]:
    """모든 링크를 한 번에 LLM에게 전달"""
    prompt = f"""다음 {len(links)}개 링크들을 분석하세요:
    {json.dumps(links, ensure_ascii=False)}
    """
    # 1회 LLM 호출로 모두 처리
```

**효과**: -1000ms

---

### 3. 아키텍처 개선 (고난이도)

#### A. LLM 스트리밍
**현재**: LLM 응답을 기다림 (blocking)
**개선**: 스트리밍으로 즉시 표시

```python
# streamlit_app.py
for chunk in llm.stream(prompt):
    st.write(chunk)  # 즉시 표시
```

**효과**: 체감 속도 대폭 개선 (실제 시간은 동일하지만 UX 향상)

#### B. 캐싱
**현재**: 동일한 diff도 매번 새로 분석
**개선**: 최근 분석 결과 캐싱 (Redis/메모리)

```python
@lru_cache(maxsize=100)
def analyze_diff(diff_hash: str):
    ...
```

**효과**: 재분석 시 -10초

#### C. Incremental Research
**현재**: 2회 검색 후 HITL → 추가 검색
**개선**: 백그라운드에서 3개 검색 엔진 모두 실행, 필요시 즉시 사용

```python
# 백그라운드 작업
tavily_future = executor.submit(search_tavily)
serper_future = executor.submit(search_serper)
naver_future = executor.submit(search_naver)

# 필요한 것만 기다림
result1 = tavily_future.result()
if needs_more:
    result2 = serper_future.result()  # 이미 실행 중
```

**효과**: HITL 대기 시간 -3초

---

### 4. 인프라 최적화

#### A. 로컬 LLM 캐시
```bash
# .env
LANGCHAIN_CACHE=true
```

#### B. HTTP/2 멀티플렉싱
검색 API 호출 시 HTTP/2 사용

#### C. CDN/프록시
검색 결과를 CDN에 캐싱 (동일 쿼리 재사용)

---

## 🎯 권장 적용 순서

### Phase 1: Quick Wins (1-2시간)
1. ✅ Streamlit sleep 제거 (-1초)
2. ✅ 네이버 검색 5개로 줄이기 (-200ms)
3. ✅ 간단한 LLM 작업 gpt-3.5-turbo 사용 (-500ms)

**예상 개선**: -1.7초 (12초 → 10.3초)

### Phase 2: 병렬화 (1-2일)
1. ⚠️ 검색 API 병렬 실행 (-1.5초)
2. ⚠️ LLM 배치 처리 (-1초)

**예상 개선**: -2.5초 (10.3초 → 7.8초)

### Phase 3: 아키텍처 개선 (1주)
1. 🔄 LLM 스트리밍 (체감 속도 대폭 개선)
2. 🔄 캐싱 (재분석 시 -10초)
3. 🔄 Incremental research (HITL -3초)

**예상 개선**: 체감 속도 50% 향상, 재분석 80% 향상

---

## 📊 최종 목표

| 시나리오 | 현재 | Phase 1 | Phase 2 | Phase 3 |
|---------|------|---------|---------|---------|
| 기본 (HITL 없음) | 9초 | 7.3초 | 5.8초 | 2-3초 (스트리밍) |
| HITL 포함 | 12초 | 10.3초 | 7.8초 | 4-5초 (스트리밍) |
| 재분석 | 12초 | 10.3초 | 7.8초 | 1-2초 (캐싱) |

---

## 💡 구현 예시

### Phase 1 적용

```python
# 1. streamlit_app.py:189
# time.sleep(1)  # 제거
st.rerun()

# 2. graph.py:453
results = search_naver(query_ko, max_results=5)  # 10 → 5

# 3. research/naver_query_generator.py:84
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)  # gpt-4o-mini → gpt-3.5-turbo
```

### Phase 2 적용 (병렬화)

```python
# graph.py에 새 노드 추가
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def research_parallel_node(state: GuardianState) -> GuardianState:
    """Tavily와 Serper 병렬 실행"""
    loop = asyncio.get_event_loop()

    def tavily_task():
        return gather_research(state, search_engine="tavily")

    def serper_task():
        return gather_research(state, search_engine="serper")

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            loop.run_in_executor(executor, tavily_task),
            loop.run_in_executor(executor, serper_task)
        ]
        results = await asyncio.gather(*futures)

    # 결과 병합
    merged = merge_evidence(results[0], results[1])
    state["evidence"] = merged
    state["recheck_count"] = 1  # 2회 검색 완료

    return state

# workflow 수정
workflow.add_node("research_parallel", research_parallel_node)
workflow.add_conditional_edges(
    "soft_llm_judge",
    should_do_research,
    {"research": "research_parallel", "write_report": "write_report"}
)
workflow.add_edge("research_parallel", "observation_validate")
```
