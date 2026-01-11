# 🔍 PushGuardian Performance Benchmark Report

**Generated:** 2026-01-09 17:14:22
**Total Test Cases:** 9

---

## 📊 Overall Summary

- **Average Total Duration:** 17.42s
- **Average Search Time:** 4754.80ms
- **Average LLM Calls:** 0.0 per test
- **Average Query Length:** 6.1 words
- **Total Searches Performed:** 37
- **Average Principle Links:** 5.4
- **Average Example Links:** 2.8

### Decision Distribution

- **ALLOW:** 3 cases
- **BLOCK:** 6 cases

### Severity Distribution

- **CRITICAL:** 1 cases
- **HIGH:** 5 cases
- **LOW:** 2 cases
- **MEDIUM:** 1 cases

---

## 📋 Detailed Test Case Results

### 1. Test: `block`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\block.txt`
**Timestamp:** 2026-01-09T17:11:58.164211

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 12763.53ms (12.76s) |
| **Search Time** | 2808.75ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `critical` |
| **Findings** | 2 |
| **Principle Links** | 7 |
| **Example Links** | 2 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `prevent secrets in git commits API keys environment variables best practices`
- **Query Length:** 11 words
- **Latency:** 795.42ms
- **Total Results:** 5
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 3
- **Example Links:** 2

  **Top Principle Links:**
  - https://github.com/orgs/community/discussions/183126
  - https://graphite.com/guides/best-practices-for-github-action-secrets-management
  - https://cybersierra.co/blog/prevent-api-key-breach/

  **Top Example Links:**
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad

**Search #2 (serper, Iteration 1)**

- **Query:** `prevent secrets in git commits API keys environment variables best practices`
- **Query Length:** 11 words
- **Latency:** 795.42ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 3 (33%)
- **Principle Links:** 7
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙과 예시 모두 부족합니다. OWASP와 같은 신뢰할 수 있는 출처에서 원칙 링크를 확보하고, GitHub 또는 Stack Overflow와 같은 플랫폼에서 실용적인 예시 링크를 찾아야 합니다. 따라서, 검색 쿼리를 개선하여 더 나은 자료를 찾기 ...

  **Top Principle Links:**
  - https://cybersierra.co/blog/prevent-api-key-breach/
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://github.com/orgs/community/discussions/183126

  **Top Example Links:**
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad

**Search #3 (serper, Iteration 1)**

- **Query:** `best practices for managing secrets in code repositories`
- **Query Length:** 8 words
- **Latency:** 1217.91ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 3 (33%)
- **Principle Links:** 7
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙과 예시 모두 부족합니다. OWASP와 같은 신뢰할 수 있는 출처에서 원칙 링크를 확보하고, GitHub 또는 Stack Overflow와 같은 플랫폼에서 실용적인 예시 링크를 찾아야 합니다. 따라서, 검색 쿼리를 개선하여 더 나은 자료를 찾기 ...

  **Top Principle Links:**
  - https://cybersierra.co/blog/prevent-api-key-breach/
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://github.com/orgs/community/discussions/183126

  **Top Example Links:**
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad

---

### 2. Test: `medium_risk_auth`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_auth.txt`
**Timestamp:** 2026-01-09T17:12:17.220281

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 19055.55ms (19.06s) |
| **Search Time** | 3201.36ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 6 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 781.09ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://www.wiz.io/academy/application-security/code-review-best-practices
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/

**Search #2 (serper, Iteration 1)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 781.09ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 6
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙에 대한 링크는 있지만, 실제 예시 링크가 부족합니다. 하드코딩된 비밀 키와 관련된 실용적인 예시를 찾기 위해 GitHub나 Stack Overflow에서 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.wiz.io/academy/application-security/code-review-best-practices
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://stackoverflow.com/questions/14570989/best-practice-for-storing-and-protecting-private-api-keys-in-applications

  **Top Example Links:**
  - https://stackoverflow.com/questions/68685462/how-to-securely-store-a-hardcoded-api-key-on-android
  - https://stackoverflow.com/questions/44695274/how-to-avoid-hardcoding-keys-for-encryption-objective-c
  - https://stackoverflow.com/questions/31490275/how-to-protect-a-site-wide-secret-key

**Search #3 (serper, Iteration 1)**

- **Query:** `hardcoded secret key security best practices site:github.com OR site:stackoverflow.com`
- **Query Length:** 9 words
- **Latency:** 1639.18ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 6
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙에 대한 링크는 있지만, 실제 예시 링크가 부족합니다. 하드코딩된 비밀 키와 관련된 실용적인 예시를 찾기 위해 GitHub나 Stack Overflow에서 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.wiz.io/academy/application-security/code-review-best-practices
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://stackoverflow.com/questions/14570989/best-practice-for-storing-and-protecting-private-api-keys-in-applications

  **Top Example Links:**
  - https://stackoverflow.com/questions/68685462/how-to-securely-store-a-hardcoded-api-key-on-android
  - https://stackoverflow.com/questions/44695274/how-to-avoid-hardcoding-keys-for-encryption-objective-c
  - https://stackoverflow.com/questions/31490275/how-to-protect-a-site-wide-secret-key

---

### 3. Test: `medium_risk_dto`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_dto.txt`
**Timestamp:** 2026-01-09T17:12:37.088892

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 19868.61ms (19.87s) |
| **Search Time** | 3199.77ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 1 |
| **Principle Links** | 4 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 803.06ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

**Search #2 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 803.06ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 원칙 링크는 충분하지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성에 대한 실질적인 예제를 찾기 위해 GitHub에서 관련 자료를 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://github.com/nomasystems/ndto
  - https://github.com/stepan-anokhin/dto-schema
  - https://github.com/Jivkomg/dto-validation-demo

**Search #3 (serper, Iteration 1)**

- **Query:** `DTO schema validation examples GitHub`
- **Query Length:** 5 words
- **Latency:** 1593.65ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 원칙 링크는 충분하지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성에 대한 실질적인 예제를 찾기 위해 GitHub에서 관련 자료를 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://github.com/nomasystems/ndto
  - https://github.com/stepan-anokhin/dto-schema
  - https://github.com/Jivkomg/dto-validation-demo

---

### 4. Test: `medium_risk_sql`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_sql.txt`
**Timestamp:** 2026-01-09T17:12:57.927888

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 20839.00ms (20.84s) |
| **Search Time** | 3596.95ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 7 |
| **Example Links** | 2 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 786.85ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

**Search #2 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 786.85ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 7
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 원칙 링크는 충분하지만, 실제 예제 링크가 부족합니다. SQL 인젝션 취약점과 관련된 DTO/Schema 규약 무시 가능성을 다룬 실용적인 예제를 찾기 위해 Serper를 통해 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://www.baeldung.com/sql-injection
  - https://brightsec.com/blog/sql-injection-attack/

**Search #3 (serper, Iteration 1)**

- **Query:** `DTO schema validation SQL injection examples`
- **Query Length:** 6 words
- **Latency:** 2023.25ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 7
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 원칙 링크는 충분하지만, 실제 예제 링크가 부족합니다. SQL 인젝션 취약점과 관련된 DTO/Schema 규약 무시 가능성을 다룬 실용적인 예제를 찾기 위해 Serper를 통해 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://www.baeldung.com/sql-injection
  - https://brightsec.com/blog/sql-injection-attack/

---

### 5. Test: `pass`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\pass.txt`
**Timestamp:** 2026-01-09T17:12:59.704368

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 1775.48ms (1.78s) |
| **Search Time** | 0.00ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 0 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `allow` |
| **Severity** | `low` |
| **Findings** | 0 |
| **Principle Links** | 0 |
| **Example Links** | 0 |
| **Tools Used** | None |

---

### 6. Test: `soft_low_style`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\soft_low_style.txt`
**Timestamp:** 2026-01-09T17:13:02.034606

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 2330.24ms (2.33s) |
| **Search Time** | 783.13ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 1 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `allow` |
| **Severity** | `low` |
| **Findings** | 0 |
| **Principle Links** | 1 |
| **Example Links** | 2 |
| **Tools Used** | tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `react beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 783.13ms
- **Total Results:** 3
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 1
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.uxpin.com/studio/blog/react-best-practices/

  **Top Example Links:**
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

---

### 7. Test: `soft_medium_xss`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\soft_medium_xss.txt`
**Timestamp:** 2026-01-09T17:13:21.724442

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 19689.84ms (19.69s) |
| **Search Time** | 5965.01ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 832.78ms
- **Total Results:** 6
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

**Search #2 (tavily, Iteration 0)**

- **Query:** `react beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 782.37ms
- **Total Results:** 6
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

**Search #3 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 832.78ms
- **Total Results:** 11
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙 링크는 있지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성과 관련된 실제 사례를 찾기 위해 Serper를 통해 추가 검색을 진행해야 합니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/learn/tutorial-tic-tac-toe
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

**Search #4 (serper, Iteration 1)**

- **Query:** `react beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 782.37ms
- **Total Results:** 11
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙 링크는 있지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성과 관련된 실제 사례를 찾기 위해 Serper를 통해 추가 검색을 진행해야 합니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/learn/tutorial-tic-tac-toe
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

**Search #5 (serper, Iteration 1)**

- **Query:** `DTO schema validation security best practices examples`
- **Query Length:** 7 words
- **Latency:** 1275.71ms
- **Total Results:** 11
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙 링크는 있지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성과 관련된 실제 사례를 찾기 위해 Serper를 통해 추가 검색을 진행해야 합니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/learn/tutorial-tic-tac-toe
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

**Search #6 (serper, Iteration 1)**

- **Query:** `react beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1459.00ms
- **Total Results:** 11
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 원칙 링크는 있지만, 실제 예제 링크가 부족합니다. DTO/Schema 규약 무시 가능성과 관련된 실제 사례를 찾기 위해 Serper를 통해 추가 검색을 진행해야 합니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://medium.com/paysafe-bulgaria/springboot-dto-validation-good-practices-and-breakdown-fee69277b3b0
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/learn/tutorial-tic-tac-toe
  - https://dev.to/philipwalsh/react-best-practices-with-examples-ao0
  - https://medium.com/@devsamiubaidi/react-tutorial-for-beginners-2025-step-by-step-guide-with-examples-setup-commands-best-8daa75369c33

---

### 8. Test: `weak_stack_docker`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\weak_stack_docker.txt`
**Timestamp:** 2026-01-09T17:13:53.621829

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 31897.39ms (31.90s) |
| **Search Time** | 11023.04ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 5 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `file permissions security access control configuration`
- **Query Length:** 6 words
- **Latency:** 781.71ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (14%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775

**Search #2 (tavily, Iteration 0)**

- **Query:** `docker FROM tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1310.00ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (14%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775

**Search #3 (tavily, Iteration 0)**

- **Query:** `docker WORKDIR tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1265.22ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (14%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775

**Search #4 (serper, Iteration 1)**

- **Query:** `file permissions security access control configuration`
- **Query Length:** 6 words
- **Latency:** 781.71ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

**Search #5 (serper, Iteration 1)**

- **Query:** `docker FROM tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1310.00ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

**Search #6 (serper, Iteration 1)**

- **Query:** `docker WORKDIR tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1265.22ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

**Search #7 (serper, Iteration 1)**

- **Query:** `root user execution security best practices site:owasp.org OR site:github.com`
- **Query Length:** 9 words
- **Latency:** 1419.58ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

**Search #8 (serper, Iteration 1)**

- **Query:** `docker FROM tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1702.34ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

**Search #9 (serper, Iteration 1)**

- **Query:** `docker WORKDIR tutorial examples`
- **Query Length:** 4 words
- **Latency:** 1187.26ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (8%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 자료는 루트 사용자 실행과 하드코딩된 비밀번호에 대한 충분한 원칙 및 예제를 제공하지 않습니다. OWASP와 GitHub와 같은 고품질 출처에서 더 많은 정보를 찾아야 합니다. 따라서 검색을 통해 더 나은 자료를 확보하는 것이 필요합니다....

  **Top Principle Links:**
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34
  - https://github.com/Exa-Networks/exabgp/wiki/Security-Best-Practices
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights

  **Top Example Links:**
  - https://docker-curriculum.com/
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27

---

### 9. Test: `weak_stack_react`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\weak_stack_react.txt`
**Timestamp:** 2026-01-09T17:14:22.178262

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 28555.91ms (28.56s) |
| **Search Time** | 12215.15ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `allow` |
| **Severity** | `medium` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 5 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 770.86ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://daveceddia.com/useeffect-hook-examples/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://legacy.reactjs.org/docs/hooks-state.html

**Search #2 (tavily, Iteration 0)**

- **Query:** `react useState 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1656.91ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://daveceddia.com/useeffect-hook-examples/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://legacy.reactjs.org/docs/hooks-state.html

**Search #3 (tavily, Iteration 0)**

- **Query:** `react useEffect 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1376.20ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://www.openappsec.io/post/how-we-deployed-open-appsec-api-security-schema-validation-to-protect-our-own-backend-systems
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://daveceddia.com/useeffect-hook-examples/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://legacy.reactjs.org/docs/hooks-state.html

**Search #4 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 770.86ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

**Search #5 (serper, Iteration 1)**

- **Query:** `react useState 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1656.91ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

**Search #6 (serper, Iteration 1)**

- **Query:** `react useEffect 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1376.20ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

**Search #7 (serper, Iteration 1)**

- **Query:** `DTO security best practices site:owasp.org OR site:github.com`
- **Query Length:** 7 words
- **Latency:** 1179.99ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

**Search #8 (serper, Iteration 1)**

- **Query:** `react useState 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1407.07ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

**Search #9 (serper, Iteration 1)**

- **Query:** `react useEffect 훅 tutorial examples`
- **Query Length:** 5 words
- **Latency:** 2020.15ms
- **Total Results:** 13
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 5
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* 현재 수집된 증거는 DTO 규약 무시 가능성과 관련된 고품질 원칙 링크와 실용적인 예시 링크가 부족합니다. 따라서 OWASP와 GitHub에서 더 많은 정보를 찾기 위해 Serper를 사용하여 검색할 필요가 있습니다....

  **Top Principle Links:**
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://github.com/upleveled/security-vulnerability-examples-next-js-postgres/issues/29
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices

  **Top Example Links:**
  - https://react.dev/reference/react/useEffect
  - https://legacy.reactjs.org/docs/hooks-state.html
  - https://daveceddia.com/useeffect-hook-examples/

---

## 📈 Comparative Analysis

### Search Performance Comparison

| Test Case | Total Time (s) | Search Time (ms) | Queries | Query Avg Length | Links Found |
|-----------|----------------|------------------|---------|------------------|-------------|
| `block` | 12.76 | 2809 | 3 | 10.0 | 9 |
| `medium_risk_auth` | 19.06 | 3201 | 3 | 7.0 | 9 |
| `medium_risk_dto` | 19.87 | 3200 | 3 | 7.0 | 7 |
| `medium_risk_sql` | 20.84 | 3597 | 3 | 7.3 | 9 |
| `pass` | 1.78 | 0 | 0 | 0.0 | 0 |
| `soft_low_style` | 2.33 | 783 | 1 | 6.0 | 3 |
| `soft_medium_xss` | 19.69 | 5965 | 6 | 6.8 | 11 |
| `weak_stack_docker` | 31.90 | 11023 | 9 | 5.0 | 13 |
| `weak_stack_react` | 28.56 | 12215 | 9 | 5.9 | 13 |

### Search Engine Usage

- **SERPER:** Used in 7 test(s)
- **TAVILY:** Used in 8 test(s)

---

## 💡 Performance Optimization Opportunities

### 📝 Query Length Optimization Candidates

*Queries with 10+ words (may benefit from keyword extraction):*

- **block** (11 words)
  - `prevent secrets in git commits API keys environment variables best practices`
- **block** (11 words)
  - `prevent secrets in git commits API keys environment variables best practices`

### 🎯 Search Quality Improvements Needed

*Searches with <50% high-quality domains:*

- **block** (tavily): 0% trusted domains
- **block** (serper): 33% trusted domains
- **block** (serper): 33% trusted domains
- **medium_risk_auth** (tavily): 0% trusted domains
- **medium_risk_auth** (serper): 0% trusted domains
- **medium_risk_auth** (serper): 0% trusted domains
- **medium_risk_dto** (tavily): 0% trusted domains
- **medium_risk_dto** (serper): 0% trusted domains
- **medium_risk_dto** (serper): 0% trusted domains
- **medium_risk_sql** (tavily): 0% trusted domains
- **medium_risk_sql** (serper): 0% trusted domains
- **medium_risk_sql** (serper): 0% trusted domains
- **soft_low_style** (tavily): 0% trusted domains
- **soft_medium_xss** (tavily): 0% trusted domains
- **soft_medium_xss** (tavily): 0% trusted domains
- **soft_medium_xss** (serper): 0% trusted domains
- **soft_medium_xss** (serper): 0% trusted domains
- **soft_medium_xss** (serper): 0% trusted domains
- **soft_medium_xss** (serper): 0% trusted domains
- **weak_stack_docker** (tavily): 14% trusted domains
- **weak_stack_docker** (tavily): 14% trusted domains
- **weak_stack_docker** (tavily): 14% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_docker** (serper): 8% trusted domains
- **weak_stack_react** (tavily): 0% trusted domains
- **weak_stack_react** (tavily): 0% trusted domains
- **weak_stack_react** (tavily): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains
- **weak_stack_react** (serper): 0% trusted domains

---

## 📌 Next Steps

### Recommended Improvements:

1. **Query Optimization**
   - Implement keyword extraction (TF-IDF or LLM-based)
   - Reduce query length by 30-50% while maintaining relevance
   - Target: Average query length < 8 words

2. **Search Quality Enhancement**
   - Add `site:` operator for trusted domains (OWASP, NIST, GitHub)
   - Implement domain whitelisting in query construction
   - Target: >70% results from high-quality sources

3. **Latency Reduction**
   - Consider parallel search execution for independent queries
   - Implement caching for common security topics
   - Target: Reduce search time by 20-30%

4. **Search Engine Selection**
   - Analyze Tavily vs Serper quality differences
   - Consider direct fallback strategy based on query type
   - Optimize retry logic based on LLM confidence

---

*Report generated by PushGuardian Benchmark Suite*