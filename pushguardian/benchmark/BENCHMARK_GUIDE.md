# 🔍 PushGuardian 벤치마크 가이드

## 개요

이 벤치마크 시스템은 PushGuardian의 성능과 검색 품질을 측정하고 개선하기 위해 만들어졌습니다.

## 📊 측정 지표

### 1. Performance Metrics (성능 지표)
- **Total Duration**: 전체 워크플로우 실행 시간 (ms, sec)
- **Search Time**: 순수 검색 API 호출 시간
- **LLM Calls Count**: LLM API 호출 횟수
- **Node-by-node Duration**: 각 노드별 실행 시간 분석

### 2. Search Quality Metrics (검색 품질 지표)
- **Query Length**: 검색 쿼리 단어 수 (짧을수록 latency 감소)
- **High-Quality Domains Ratio**: 신뢰할 만한 도메인 비율 (OWASP, NIST, GitHub 등)
- **Spam Filtered Count**: 필터링된 스팸 결과 수
- **Links Found**: 발견된 Principle/Example 링크 수
- **LLM Assessment**: LLM이 평가한 검색 결과 충분성

### 3. Workflow Metrics (워크플로우 지표)
- **Research Iterations**: 검색 반복 횟수 (Tavily → Serper)
- **Tools Used**: 사용된 검색 엔진 (tavily, serper, duckduckgo)
- **Decision & Severity**: 최종 판단 및 위험도
- **Findings Count**: 탐지된 보안 이슈 개수

## 🚀 사용법

### 1. 벤치마크 실행

```bash
# Conda 환경 활성화
conda activate p_guard

# 벤치마크 실행
python run_benchmark.py
```

### 2. 실행 과정

벤치마크는 다음 단계로 진행됩니다:

1. `examples/test_file/` 디렉토리의 모든 `.txt` 파일 스캔
2. 각 테스트 케이스마다:
   - LangGraph 워크플로우 실행
   - 각 노드별 실행 시간 측정
   - 검색 API 호출 추적
   - LLM 호출 카운트
   - 검색 품질 지표 수집
3. 모든 결과를 통합하여 마크다운 리포트 생성
4. `benchmark_reports/` 디렉토리에 저장

### 3. 테스트 케이스 (총 9개)

```
examples/test_file/
├── block.txt                # Hard block (secrets)
├── pass.txt                 # Clean code (pass)
├── medium_risk_dto.txt      # DTO validation issues
├── medium_risk_sql.txt      # SQL injection risk
├── medium_risk_auth.txt     # Auth implementation issues
├── soft_medium_xss.txt      # XSS vulnerability
├── soft_low_style.txt       # Low severity style issues
├── weak_stack_react.txt     # React learning mode
└── weak_stack_docker.txt    # Docker learning mode
```

## 📄 리포트 구조

생성된 마크다운 리포트는 다음 섹션들을 포함합니다:

### 1. Overall Summary (전체 요약)
- 평균 실행 시간
- 평균 검색 시간
- 평균 LLM 호출 수
- 평균 쿼리 길이
- Decision/Severity 분포

### 2. Detailed Test Case Results (테스트별 상세 결과)
각 테스트 케이스마다:
- **Performance Metrics**: 실행 시간, 검색 시간, LLM 호출
- **Results Summary**: Decision, Severity, Findings, Links
- **Node Execution Timeline**: 각 노드별 실행 시간
- **Search Quality Analysis**:
  - 쿼리 내용 및 길이
  - 검색 엔진 및 latency
  - 결과 개수 및 스팸 필터링
  - 고품질 도메인 비율
  - LLM 평가 (sufficient/needs refinement)
  - 실제 링크 목록 (top 3)

### 3. Comparative Analysis (비교 분석)
- 모든 테스트의 성능 비교 테이블
- 검색 엔진 사용 통계
- 가장 느린 컴포넌트 분석

### 4. Performance Optimization Opportunities (개선 기회)
- **Slowest Components**: 가장 느린 노드 top 3
- **Query Length Optimization Candidates**: 10단어 이상의 긴 쿼리 목록
- **Search Quality Improvements Needed**: 고품질 도메인 비율 50% 미만인 검색

### 5. Next Steps (다음 단계 권장사항)
- Query Optimization 방안
- Search Quality Enhancement 방안
- Latency Reduction 방안
- Search Engine Selection 최적화

## 💡 개선 전/후 비교 방법

### 1. Baseline 측정
```bash
# 개선 전 벤치마크 실행
python run_benchmark.py
# → benchmark_reports/benchmark_20260109_143000.md 생성
```

### 2. 개선 사항 적용
예: Query optimization, Domain filtering 등

### 3. 개선 후 측정
```bash
# 개선 후 벤치마크 실행
python run_benchmark.py
# → benchmark_reports/benchmark_20260109_150000.md 생성
```

### 4. 비교 분석
두 리포트를 비교하여 다음 지표들의 변화 확인:

#### 목표 지표:
- **Query Length**: 30-50% 감소 (목표: 평균 8단어 이하)
- **Search Time**: 20-30% 감소
- **High-Quality Domain Ratio**: 70% 이상
- **Total Duration**: 전체 실행 시간 단축

#### 품질 지표:
- **Links Found**: 유지 또는 증가 (품질 저하 방지)
- **LLM Assessment**: "Sufficient" 비율 증가
- **Findings Detection**: 동일 (보안 탐지 정확도 유지)

## 🔧 코드 구조

```
pushguardian/benchmark/
├── __init__.py
├── metrics.py              # 메트릭 데이터 클래스 및 수집기
├── runner.py               # 벤치마크 실행 로직
└── report_generator.py     # 마크다운 리포트 생성

run_benchmark.py            # 메인 실행 스크립트
```

### 주요 클래스:

#### `MetricsCollector`
워크플로우 실행 중 실시간으로 메트릭 수집:
```python
collector = MetricsCollector()
collector.start_workflow()
collector.start_node("research_tavily")
collector.end_node("research_tavily", state)
collector.add_search_metrics(...)
result = collector.finalize(test_name, test_file, final_state)
```

#### `BenchmarkResult`
하나의 테스트 케이스 결과를 담는 데이터 클래스:
- Performance metrics
- Node-by-node breakdown
- Search quality metrics
- Final results

#### `generate_markdown_report()`
여러 `BenchmarkResult`를 받아 종합 리포트 생성

## 📈 예상 개선 효과

### Query Optimization (TF-IDF 기반 키워드 추출)
- **Before**: `"prevent secrets in git commits API keys environment variables best practices"` (10 words)
- **After**: `"prevent secrets git commits API keys"` (6 words, 40% 감소)
- **Latency 개선**: 15-20% 예상

### Domain Filtering (site: operator)
- **Before**: 일반 검색 → 스팸 필터링 → 고품질 도메인 40%
- **After**: `site:owasp.org OR site:github.com` → 고품질 도메인 85%+
- **Search Quality**: 2배 이상 개선

### Combined Effect
- **Total Latency**: 25-35% 감소 예상
- **Search Quality**: 신뢰도 높은 링크 비율 70%+ 달성
- **User Experience**: 더 빠르고 정확한 보안 가이드 제공

## 🎯 벤치마크 활용 시나리오

### 1. 성능 회귀 테스트
- 새로운 기능 추가 시 성능 저하 여부 확인
- CI/CD 파이프라인에 통합 가능

### 2. A/B 테스팅
- 다른 검색 전략 비교 (Tavily vs Serper vs Hybrid)
- Query optimization 알고리즘 비교 (TF-IDF vs LLM vs Rule-based)

### 3. Cost Analysis
- LLM API 호출 수 최적화
- 검색 API 사용량 분석

### 4. 사용자 경험 개선
- End-to-end latency 개선
- 검색 결과 품질 향상

## 📝 주의사항

1. **API 키 필요**: `.env` 파일에 `OPENAI_API_KEY`, `TAVILY_API_KEY`, `SERPER_API_KEY` 설정 필요
2. **실행 시간**: 9개 테스트 × 평균 20-30초 = 약 3-5분 소요 예상
3. **비용**: OpenAI GPT-4o-mini 및 검색 API 호출 비용 발생
4. **재현성**: 동일 조건에서 실행해야 공정한 비교 가능

## 🚀 다음 단계

벤치마크 리포트를 확인한 후:

1. **병목 지점 파악**: 가장 느린 노드 및 검색 단계 확인
2. **개선 우선순위 선정**: Query length, Search quality, Latency 중 집중할 영역 결정
3. **개선 사항 구현**:
   - [research/gather.py](pushguardian/research/gather.py)에 query optimization 추가
   - [research/tavily_client.py](pushguardian/research/tavily_client.py), [research/serper_client.py](pushguardian/research/serper_client.py)에 domain filtering 추가
4. **재측정 및 비교**: 개선 효과 검증

---

**문의 및 개선 제안은 이슈로 등록해주세요!**
