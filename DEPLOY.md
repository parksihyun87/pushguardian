# 🚀 PushGuardian 배포 가이드

다른 사람이 접속할 수 있도록 PushGuardian을 배포하는 방법입니다.

## 방법 1: Streamlit Cloud (추천 - 무료, 가장 쉬움)

### 준비사항
- GitHub 계정
- OpenAI API Key
- Tavily API Key

### 배포 단계

1. **GitHub에 코드 푸시**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/pushguardian.git
   git push -u origin main
   ```

2. **Streamlit Cloud 접속**
   - https://share.streamlit.io 방문
   - GitHub 계정으로 로그인

3. **앱 배포**
   - "New app" 클릭
   - Repository: `your-username/pushguardian` 선택
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - "Deploy!" 클릭

4. **Secrets 설정**
   - 배포된 앱 → Settings → Secrets
   - `.streamlit/secrets.toml.example` 내용을 복사
   - 실제 API 키로 수정해서 붙여넣기
   ```toml
   OPENAI_API_KEY = "sk-proj-실제키"
   TAVILY_API_KEY = "tvly-실제키"
   ```

5. **완료!**
   - 앱 URL: `https://your-username-pushguardian-xxx.streamlit.app`
   - 이 URL을 다른 사람에게 공유

---

## 방법 2: Railway (유료, 더 많은 제어)

### 장점
- 더 많은 리소스
- Custom domain 지원
- 더 빠른 성능

### 배포 단계

1. **Railway 계정 생성**
   - https://railway.app 방문
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   - "New Project" → "Deploy from GitHub repo"
   - `pushguardian` 레포지토리 선택

3. **환경 변수 설정**
   - 프로젝트 → Variables 탭
   - 다음 변수 추가:
     ```
     OPENAI_API_KEY=sk-proj-실제키
     TAVILY_API_KEY=tvly-실제키
     ```

4. **배포 설정**
   - Railway가 `Procfile` 자동 감지
   - 또는 Start Command: `streamlit run streamlit_app.py --server.port=$PORT`

5. **도메인 설정**
   - Settings → Domains
   - Railway 제공 도메인 사용 또는 커스텀 도메인 연결

---

## 방법 3: Render (무료 티어 있음)

### 배포 단계

1. **Render 계정 생성**
   - https://render.com 방문

2. **New Web Service**
   - GitHub 레포지토리 연결
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

3. **환경 변수 설정**
   - Environment → Add Environment Variable
   - API 키들 추가

---

## 배포 전 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 있는지 확인 (API 키 유출 방지)
- [ ] `requirements.txt`에 모든 dependencies 있는지 확인
- [ ] API 키 사용량 제한 설정 (OpenAI, Tavily)
- [ ] 테스트 diff 파일로 로컬에서 먼저 테스트

## 보안 주의사항

⚠️ **중요:** API 키를 절대 GitHub에 커밋하지 마세요!
- `.env` 파일은 로컬에만
- Secrets는 배포 플랫폼의 환경 변수로만 설정
- GitHub public repository라면 API 사용량 모니터링 필수

## 비용 예상

**Streamlit Cloud:**
- 무료: Public app, 1GB RAM, 공유 CPU
- 제한: 동시 사용자 수 제한 있음

**Railway:**
- $5/month 크레딧 무료
- 초과 시 사용량 기반 과금

**Render:**
- 무료: 512MB RAM, 750시간/월
- 15분 비활성화 시 sleep

## 성능 최적화

배포 후 느리다면:
1. LLM 모델을 `gpt-4o-mini`로 변경 (이미 설정됨)
2. Research iteration 제한 (현재 2회로 설정됨)
3. 캐싱 추가 고려

## 문제 해결

**배포 실패:**
- Logs 확인
- `requirements.txt` dependencies 확인
- Python 버전 호환성 (`runtime.txt`로 지정 가능)

**API 에러:**
- Secrets 올바르게 설정됐는지 확인
- API 키 유효한지 확인
- 사용량 제한 확인

## 도메인 연결 (선택)

무료 도메인: Streamlit/Railway/Render 제공
커스텀 도메인: DNS 설정 → CNAME 레코드 추가

예시:
```
pushguardian.yourdomain.com → your-app.streamlit.app
```
