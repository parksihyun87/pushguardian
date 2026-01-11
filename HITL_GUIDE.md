# HITL (Human-in-the-Loop) 기능 가이드

## 개요

PushGuardian의 HITL (Human-in-the-Loop) 기능은 자동 연구 과정에서 **한글 자료가 부족할 때** 사용자에게 네이버 검색 API를 통한 추가 검색 여부를 묻는 기능입니다.

## 작동 원리

```
1. Tavily 검색 (1차)
   ↓
2. LLM 품질 평가
   ↓
3. Serper 검색 (2차, 필요 시)
   ↓
4. LLM 품질 평가 (2회 완료)
   ↓
5. 자료 부족 판단 (총 링크 < 3개)
   ↓
6. ⏸️  HITL 승인 화면 표시
   ↓
7. 사용자 선택:
   - 🔍 네이버 검색 추가 → 한글 자료 검색 → 리포트 작성
   - ✅ 현재 자료로 계속 → 바로 리포트 작성
   - ⏭️  건너뛰기 → 바로 리포트 작성
```

## 설정 방법

### 1. 네이버 검색 API 키 발급

1. [네이버 개발자 센터](https://developers.naver.com/) 접속
2. "Application" > "애플리케이션 등록" 클릭
3. 애플리케이션 정보 입력:
   - 애플리케이션 이름: 원하는 이름 (예: PushGuardian)
   - 사용 API: **검색** 선택
   - 비로그인 오픈 API 서비스 환경: **WEB 설정** 추가 (URL: http://localhost)
4. 등록 완료 후 **Client ID**와 **Client Secret** 확인

### 2. 환경 변수 설정

`.env` 파일에 네이버 API 키를 추가합니다:

```bash
# 네이버 검색 API (한글 자료 검색용)
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
```

**참고**: 네이버 API 키가 없어도 PushGuardian은 정상 작동합니다. HITL 화면에서 네이버 검색을 선택하지 않으면 됩니다.

## 사용 방법

### Streamlit Web UI

```bash
streamlit run streamlit_app.py
```

1. Diff 텍스트 입력 또는 Git 레포 경로 지정
2. "🔍 Diff 분석하기" 클릭
3. 분석 진행 (Tavily → Serper 검색)
4. **자료가 부족하면 HITL 승인 화면 표시**:

```
⏸️  한글 자료 추가 검색이 필요합니다 (HITL)

현재 수집된 자료:
- 원칙 링크: 1개
- 예시 링크: 0개

자료가 부족할 수 있습니다. 네이버 검색 API로 한글 자료를 추가로 검색하시겠습니까?

[🔍 네이버 검색 추가] [✅ 현재 자료로 계속] [⏭️  건너뛰기]
```

5. 선택지:
   - **🔍 네이버 검색 추가**: 네이버에서 한글 자료 추가 검색 (API 키 필요)
   - **✅ 현재 자료로 계속**: 현재 수집된 자료로 리포트 작성
   - **⏭️  건너뛰기**: 추가 검색 없이 리포트 작성

## 기술 구조

### LangGraph Checkpointer

HITL 기능은 LangGraph의 `MemorySaver` checkpointer를 사용하여 구현됩니다:

```python
from langgraph.checkpoint.memory import MemorySaver

# 그래프 빌드 시 checkpointer 전달
checkpointer = MemorySaver()
graph = build_graph(checkpointer=checkpointer)

# interrupt_before로 human_approval 노드 전에 중단
workflow.compile(checkpointer=checkpointer, interrupt_before=["human_approval"])
```

### 저장되는 상태 (GuardianState)

Checkpointer는 다음 정보를 저장합니다:

- **diff_text**: 분석 대상 Git diff
- **findings**: 발견된 보안 이슈 (hard_findings + soft_findings)
- **evidence**: 수집된 연구 자료 (principle_links, example_links, search_queries 등)
- **research_plan**: LLM 플래너 출력
- **recheck_count**: 연구 반복 횟수
- **human_approval_needed**: HITL 트리거 여부
- **human_decision**: 사용자 선택 (approve/search_naver/skip)
- 기타 모든 워크플로우 상태

### 상태 재개

```python
# 사용자가 선택한 후
graph.update_state(config, {"human_decision": "search_naver"})

# 그래프 재개 (interrupt 지점부터 계속)
for chunk in graph.stream(None, config=config):
    # 네이버 검색 → 리포트 작성
    pass
```

## HITL 트리거 조건

현재 HITL은 다음 조건에서 트리거됩니다:

1. **2회 연구 완료**: Tavily(0) + Serper(1) = recheck_count >= 1
2. **자료 부족**: 총 링크 수 < 3개 (principle_links + example_links)

이 조건은 [graph.py:394-399](pushguardian/graph.py#L394-L399)에서 수정할 수 있습니다:

```python
if recheck_count >= 1:
    total_links = len(evidence.principle_links) + len(evidence.example_links)
    if total_links < 3:  # 이 조건을 조정 가능
        state["human_approval_needed"] = True
```

## 네이버 검색 쿼리 생성

네이버 검색 시 다음 우선순위로 한글 쿼리를 생성합니다:

1. **보안 이슈 발견**: `{finding.kind} 보안 취약점 예제`
   - 예: "XSS 보안 취약점 예제"
2. **약점 스택 감지**: `{weak_stack} 튜토리얼`
   - 예: "Docker 튜토리얼"
3. **기본 쿼리**: "보안 모범 사례"

쿼리 생성 로직은 [graph.py:422-429](pushguardian/graph.py#L422-L429)에서 수정 가능합니다.

## 제한 사항

### 네이버 API 할당량

- **무료**: 일 25,000건
- **유료**: 추가 사용 시 과금
- 자세한 내용은 [네이버 검색 API 가격 정책](https://www.ncloud.com/product/applicationService/search) 참고

### CLI 모드 미지원

현재 HITL 기능은 **Streamlit Web UI에서만** 사용 가능합니다. CLI 모드 (`pushguardian.cli`)에서는 자동으로 건너뜁니다.

CLI에서 HITL을 지원하려면 터미널 입력을 처리하는 추가 구현이 필요합니다.

## 디버깅

### Checkpointer 상태 확인

```python
# 현재 저장된 상태 확인
snapshot = graph.get_state(config)
print(snapshot.values)  # GuardianState 전체
print(snapshot.next)    # 다음 실행할 노드
```

### HITL 로그

HITL 노드 실행 시 다음 로그가 출력됩니다:

```
⏸️  사람의 승인 대기 중... (human_approval_node)
🔍 네이버 검색 시작: XSS 보안 취약점 예제
네이버 검색 완료: 5개 결과
✅ 네이버 검색 완료: 5개 결과
```

## FAQ

### Q1. HITL 화면이 표시되지 않아요

**A**: 다음을 확인하세요:
1. 2회 연구가 완료되었는지 (Tavily + Serper)
2. 총 링크 수가 3개 미만인지
3. Streamlit Web UI를 사용하고 있는지 (CLI는 미지원)

### Q2. 네이버 검색을 선택했는데 결과가 없어요

**A**: 다음을 확인하세요:
1. `.env` 파일에 `NAVER_CLIENT_ID`와 `NAVER_CLIENT_SECRET`이 올바르게 설정되었는지
2. 네이버 API 할당량을 초과하지 않았는지
3. 터미널 로그에 에러 메시지가 있는지 확인 (`네이버 검색 API 호출 실패: ...`)

### Q3. HITL 없이 항상 네이버 검색을 실행하고 싶어요

**A**: [graph.py](pushguardian/graph.py)를 수정하여 네이버 검색을 기본 워크플로우에 추가할 수 있습니다:

```python
# observation_validate 후 항상 네이버 검색
workflow.add_edge("observation_validate", "research_naver")
workflow.add_edge("research_naver", "write_report")
```

### Q4. HITL 트리거 조건을 변경하고 싶어요

**A**: [graph.py:394-399](pushguardian/graph.py#L394-L399)를 수정하세요:

```python
# 예: 총 링크 5개 미만일 때 트리거
if recheck_count >= 1:
    total_links = len(evidence.principle_links) + len(evidence.example_links)
    if total_links < 5:  # 3 → 5로 변경
        state["human_approval_needed"] = True
```

## 참고 자료

- [LangGraph Checkpointer 문서](https://langchain-ai.github.io/langgraph/concepts/persistence/)
- [네이버 검색 API 문서](https://developers.naver.com/docs/serviceapi/search/web/web.md)
- [PushGuardian 메인 README](README.md)
