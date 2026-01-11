# 🔍 PushGuardian Performance Benchmark Report

**Generated:** 2026-01-09 17:00:41
**Total Test Cases:** 9

---

## 📊 Overall Summary

- **Average Total Duration:** 13.54s
- **Average Search Time:** 4411.00ms
- **Average LLM Calls:** 0.0 per test
- **Average Query Length:** 6.4 words
- **Total Searches Performed:** 34
- **Average Principle Links:** 5.8
- **Average Example Links:** 2.6

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
**Timestamp:** 2026-01-09T16:58:49.471994

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 10236.42ms (10.24s) |
| **Search Time** | 2853.26ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `critical` |
| **Findings** | 2 |
| **Principle Links** | 7 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `prevent secrets in git commits API keys environment variables best practices`
- **Query Length:** 11 words
- **Latency:** 782.17ms
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
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730

**Search #2 (serper, Iteration 1)**

- **Query:** `prevent secrets in git commits API keys environment variables best practices`
- **Query Length:** 11 words
- **Latency:** 782.17ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (20%)
- **Principle Links:** 7
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, and there are no practical ex...

  **Top Principle Links:**
  - https://docs.github.com/en/get-started/learning-to-code/storing-your-secrets-safely
  - https://github.com/orgs/community/discussions/168661
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

  **Top Example Links:**
  - https://medium.com/@alameerashraf/protecting-your-code-how-to-prevent-and-fix-sensitive-data-exposure-on-github-e1934611847f
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730

**Search #3 (serper, Iteration 1)**

- **Query:** `best practices for managing secrets in GitHub and preventing sensitive file exposure`
- **Query Length:** 12 words
- **Latency:** 1288.92ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (20%)
- **Principle Links:** 7
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, and there are no practical ex...

  **Top Principle Links:**
  - https://docs.github.com/en/get-started/learning-to-code/storing-your-secrets-safely
  - https://github.com/orgs/community/discussions/168661
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

  **Top Example Links:**
  - https://medium.com/@alameerashraf/protecting-your-code-how-to-prevent-and-fix-sensitive-data-exposure-on-github-e1934611847f
  - https://medium.com/@kcfreepress/stop-committing-secrets-to-github-how-to-avoid-it-and-how-to-fix-it-if-you-already-did-3a78fbdfbaad
  - https://community.latenode.com/t/just-learned-the-proper-way-to-store-api-keys-in-commits/8730

---

### 2. Test: `medium_risk_auth`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_auth.txt`
**Timestamp:** 2026-01-09T16:59:07.986428

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 18514.43ms (18.51s) |
| **Search Time** | 5102.97ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 3 |
| **Principle Links** | 6 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 1653.66ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://www.wiz.io/academy/application-security/code-review-best-practices

**Search #2 (serper, Iteration 1)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 1653.66ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 6
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have gathered some principle links, I still lack practical examples that demonstrate how to handle hardcoded secret keys effectively. Searchin...

  **Top Principle Links:**
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.wiz.io/academy/application-security/code-review-best-practices

  **Top Example Links:**
  - https://stackoverflow.com/questions/68685462/how-to-securely-store-a-hardcoded-api-key-on-android
  - https://stackoverflow.com/questions/17832462/how-to-hardcode-private-key-which-can-be-used-to-encrypt-once-and-decrypt-many-t
  - https://stackoverflow.com/questions/31490275/how-to-protect-a-site-wide-secret-key

**Search #3 (serper, Iteration 1)**

- **Query:** `hardcoded secret key security best practices site:github.com OR site:stackoverflow.com`
- **Query Length:** 9 words
- **Latency:** 1795.65ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 6
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have gathered some principle links, I still lack practical examples that demonstrate how to handle hardcoded secret keys effectively. Searchin...

  **Top Principle Links:**
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.wiz.io/academy/application-security/code-review-best-practices

  **Top Example Links:**
  - https://stackoverflow.com/questions/68685462/how-to-securely-store-a-hardcoded-api-key-on-android
  - https://stackoverflow.com/questions/17832462/how-to-hardcode-private-key-which-can-be-used-to-encrypt-once-and-decrypt-many-t
  - https://stackoverflow.com/questions/31490275/how-to-protect-a-site-wide-secret-key

---

### 3. Test: `medium_risk_dto`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_dto.txt`
**Timestamp:** 2026-01-09T16:59:20.770084

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 12783.66ms (12.78s) |
| **Search Time** | 2954.31ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 1 |
| **Principle Links** | 8 |
| **Example Links** | 1 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 805.26ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

**Search #2 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 805.26ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (22%)
- **Principle Links:** 8
- **Example Links:** 1
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have found several principle links related to input validation, there are no practical examples available. To meet the research requirements, ...

  **Top Principle Links:**
  - https://z0enix.medium.com/owasp-mobile-top-10-m4-insufficient-input-output-validation-8a511c5ff918?source=rss------technology-5
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://cwe.mitre.org/data/definitions/20.html

  **Top Example Links:**
  - https://learn.snyk.io/lesson/improper-input-validation/

**Search #3 (serper, Iteration 1)**

- **Query:** `missing input validation examples in API security`
- **Query Length:** 7 words
- **Latency:** 1343.79ms
- **Total Results:** 9
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (22%)
- **Principle Links:** 8
- **Example Links:** 1
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have found several principle links related to input validation, there are no practical examples available. To meet the research requirements, ...

  **Top Principle Links:**
  - https://z0enix.medium.com/owasp-mobile-top-10-m4-insufficient-input-output-validation-8a511c5ff918?source=rss------technology-5
  - https://www.fyld.pt/blog/api-security-10-practices-developers/
  - https://cwe.mitre.org/data/definitions/20.html

  **Top Example Links:**
  - https://learn.snyk.io/lesson/improper-input-validation/

---

### 4. Test: `medium_risk_sql`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\medium_risk_sql.txt`
**Timestamp:** 2026-01-09T16:59:35.610812

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 14840.22ms (14.84s) |
| **Search Time** | 2450.14ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 4 |
| **Example Links** | 3 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 798.88ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 0

  **Top Principle Links:**
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://www.wiz.io/academy/application-security/code-review-best-practices

**Search #2 (serper, Iteration 1)**

- **Query:** `structure security best practices code review`
- **Query Length:** 6 words
- **Latency:** 798.88ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have gathered some principle links, I lack practical examples that demonstrate SQL Injection risks. To meet the research requirements, I need ...

  **Top Principle Links:**
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://www.wiz.io/academy/application-security/code-review-best-practices

  **Top Example Links:**
  - https://github.com/topics/sql-injection-attack
  - https://github.com/topics/sqli-injection
  - https://github.com/topics/sql-injection-attacks

**Search #3 (serper, Iteration 1)**

- **Query:** `SQL Injection Risk examples GitHub`
- **Query Length:** 5 words
- **Latency:** 852.38ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 3
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* While I have gathered some principle links, I lack practical examples that demonstrate SQL Injection risks. To meet the research requirements, I need ...

  **Top Principle Links:**
  - https://devcom.com/tech-blog/secure-code-review-best-practices-to-protect-your-applications/
  - https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review
  - https://www.wiz.io/academy/application-security/code-review-best-practices

  **Top Example Links:**
  - https://github.com/topics/sql-injection-attack
  - https://github.com/topics/sqli-injection
  - https://github.com/topics/sql-injection-attacks

---

### 5. Test: `pass`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\pass.txt`
**Timestamp:** 2026-01-09T16:59:36.642004

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 1031.19ms (1.03s) |
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
**Timestamp:** 2026-01-09T16:59:39.475087

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 2821.25ms (2.82s) |
| **Search Time** | 1708.12ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 1 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `allow` |
| **Severity** | `low` |
| **Findings** | 0 |
| **Principle Links** | 3 |
| **Example Links** | 1 |
| **Tools Used** | tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `nextjs beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1708.12ms
- **Total Results:** 4
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 3
- **Example Links:** 1

  **Top Principle Links:**
  - https://nextjs.org/learn/react-foundations
  - https://welearncode.com/beginners-guide-nextjs/
  - https://medium.com/@elanaolson/a-beginners-guide-to-building-a-react-nextjs-app-7463120389f0

  **Top Example Links:**
  - https://nextjs.org/learn

---

### 7. Test: `soft_medium_xss`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\soft_medium_xss.txt`
**Timestamp:** 2026-01-09T16:59:57.237591

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 17762.50ms (17.76s) |
| **Search Time** | 5251.96ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 2 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 787.52ms
- **Total Results:** 5
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 1

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://nextjs.org/learn

**Search #2 (tavily, Iteration 0)**

- **Query:** `nextjs beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 822.29ms
- **Total Results:** 5
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 1

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://nextjs.org/learn

**Search #3 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 787.52ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (10%)
- **Principle Links:** 8
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from platforms like GitH...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/andrea-acampora/nestjs-ddd-devops
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://github.com/spiral/json-schema-generator
  - https://nextjs.org/learn

**Search #4 (serper, Iteration 1)**

- **Query:** `nextjs beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 822.29ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (10%)
- **Principle Links:** 8
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from platforms like GitH...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/andrea-acampora/nestjs-ddd-devops
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://github.com/spiral/json-schema-generator
  - https://nextjs.org/learn

**Search #5 (serper, Iteration 1)**

- **Query:** `DTO schema bypass security best practices site:owasp.org OR site:github.com`
- **Query Length:** 9 words
- **Latency:** 844.07ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (10%)
- **Principle Links:** 8
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from platforms like GitH...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/andrea-acampora/nestjs-ddd-devops
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://github.com/spiral/json-schema-generator
  - https://nextjs.org/learn

**Search #6 (serper, Iteration 1)**

- **Query:** `nextjs beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1188.27ms
- **Total Results:** 10
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (10%)
- **Principle Links:** 8
- **Example Links:** 2
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from platforms like GitH...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/andrea-acampora/nestjs-ddd-devops
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://github.com/spiral/json-schema-generator
  - https://nextjs.org/learn

---

### 8. Test: `weak_stack_docker`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\weak_stack_docker.txt`
**Timestamp:** 2026-01-09T17:00:17.393541

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 20155.95ms (20.16s) |
| **Search Time** | 8462.10ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `block` |
| **Severity** | `high` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 6 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `file permissions security access control configuration`
- **Query Length:** 6 words
- **Latency:** 1533.58ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (14%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://docs.docker.com/build/building/best-practices/
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34

  **Top Example Links:**
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://www.datacamp.com/tutorial/docker-tutorial

**Search #2 (tavily, Iteration 0)**

- **Query:** `docker beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1421.89ms
- **Total Results:** 7
- **Spam Filtered:** 0
- **High-Quality Domains:** 1 (14%)
- **Principle Links:** 4
- **Example Links:** 3

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://docs.docker.com/build/building/best-practices/
  - https://medium.com/@mtran0989/a-comprehensive-guide-to-understanding-and-managing-file-permissions-in-windows-file-explore-be9c8e352c34

  **Top Example Links:**
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/
  - https://www.datacamp.com/tutorial/docker-tutorial

**Search #3 (serper, Iteration 1)**

- **Query:** `file permissions security access control configuration`
- **Query Length:** 6 words
- **Latency:** 1533.58ms
- **Total Results:** 14
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (14%)
- **Principle Links:** 8
- **Example Links:** 6
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, as well as practical examples...

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights
  - https://docs.docker.com/build/building/best-practices/

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/

**Search #4 (serper, Iteration 1)**

- **Query:** `docker beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1421.89ms
- **Total Results:** 14
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (14%)
- **Principle Links:** 8
- **Example Links:** 6
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, as well as practical examples...

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights
  - https://docs.docker.com/build/building/best-practices/

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/

**Search #5 (serper, Iteration 1)**

- **Query:** `best practices for running as root and hardcoded credentials security`
- **Query Length:** 10 words
- **Latency:** 1240.97ms
- **Total Results:** 14
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (14%)
- **Principle Links:** 8
- **Example Links:** 6
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, as well as practical examples...

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights
  - https://docs.docker.com/build/building/best-practices/

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/

**Search #6 (serper, Iteration 1)**

- **Query:** `docker beginner tutorial best practices examples`
- **Query Length:** 6 words
- **Latency:** 1310.19ms
- **Total Results:** 14
- **Spam Filtered:** 0
- **High-Quality Domains:** 2 (14%)
- **Principle Links:** 8
- **Example Links:** 6
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP or official documentation, as well as practical examples...

  **Top Principle Links:**
  - https://www.linuxjournal.com/content/understanding-ownership-and-access-control-enhanced-security
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights
  - https://docs.docker.com/build/building/best-practices/

  **Top Example Links:**
  - https://medium.com/@nomannayeem/the-one-docker-tutorial-every-beginner-developer-actually-needs-f94a5774da27
  - https://princeton.service-now.com/service?id=kb_article&sys_id=662a27064f9ca20018ddd48e5210c775
  - https://www.ninjaone.com/blog/change-permissions-in-windows-10/

---

### 9. Test: `weak_stack_react`

**File:** `C:\workplace\code\python\langraph\pushguardian\examples\test_file\weak_stack_react.txt`
**Timestamp:** 2026-01-09T17:00:41.126324

#### ⏱️ Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Duration** | 23732.78ms (23.73s) |
| **Search Time** | 10916.15ms |
| **LLM Calls** | 0 |
| **Research Iterations** | 2 |

#### 🎯 Results Summary

| Metric | Value |
|--------|-------|
| **Decision** | `allow` |
| **Severity** | `medium` |
| **Findings** | 2 |
| **Principle Links** | 8 |
| **Example Links** | 4 |
| **Tools Used** | serper, tavily |

#### 🔍 Search Quality Analysis

**Search #1 (tavily, Iteration 0)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 793.36ms
- **Total Results:** 6
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471

**Search #2 (tavily, Iteration 0)**

- **Query:** `react useState hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1267.45ms
- **Total Results:** 6
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471

**Search #3 (tavily, Iteration 0)**

- **Query:** `react useEffect hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1358.05ms
- **Total Results:** 6
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 4
- **Example Links:** 2

  **Top Principle Links:**
  - https://www.soliantconsulting.com/blog/api-first-data-security-schema-validators/
  - https://www.pynt.io/learning-hub/api-security-guide/api-security-best-practices
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471

**Search #4 (serper, Iteration 1)**

- **Query:** `DTO schema validation backend API security best practices`
- **Query Length:** 8 words
- **Latency:** 793.36ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

**Search #5 (serper, Iteration 1)**

- **Query:** `react useState hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1267.45ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

**Search #6 (serper, Iteration 1)**

- **Query:** `react useEffect hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1358.05ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

**Search #7 (serper, Iteration 1)**

- **Query:** `DTO schema security best practices site:owasp.org OR site:github.com`
- **Query Length:** 8 words
- **Latency:** 1410.52ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

**Search #8 (serper, Iteration 1)**

- **Query:** `react useState hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1130.04ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

**Search #9 (serper, Iteration 1)**

- **Query:** `react useEffect hook tutorial examples`
- **Query Length:** 5 words
- **Latency:** 1537.87ms
- **Total Results:** 12
- **Spam Filtered:** 0
- **High-Quality Domains:** 0 (0%)
- **Principle Links:** 8
- **Example Links:** 4
- **LLM Assessment:** ✗ Needs refinement
  - *Reasoning:* The current evidence lacks high-quality principle links from authoritative sources like OWASP and relevant practical examples from GitHub or Stack Ove...

  **Top Principle Links:**
  - https://github.com/Sairyss/domain-driven-hexagon/blob/master/README.md
  - https://github.com/axotion/class-validator-security-enhancer
  - https://www.fyld.pt/blog/api-security-10-practices-developers/

  **Top Example Links:**
  - https://blog.logrocket.com/useeffect-react-hook-complete-guide/
  - https://medium.com/@titoadeoye/react-hooks-usestate-with-practical-examples-64abd6df6471
  - https://www.w3schools.com/react/react_useeffect.asp

---

## 📈 Comparative Analysis

### Search Performance Comparison

| Test Case | Total Time (s) | Search Time (ms) | Queries | Query Avg Length | Links Found |
|-----------|----------------|------------------|---------|------------------|-------------|
| `block` | 10.24 | 2853 | 3 | 11.3 | 10 |
| `medium_risk_auth` | 18.51 | 5103 | 3 | 7.0 | 9 |
| `medium_risk_dto` | 12.78 | 2954 | 3 | 7.7 | 9 |
| `medium_risk_sql` | 14.84 | 2450 | 3 | 5.7 | 7 |
| `pass` | 1.03 | 0 | 0 | 0.0 | 0 |
| `soft_low_style` | 2.82 | 1708 | 1 | 6.0 | 4 |
| `soft_medium_xss` | 17.76 | 5252 | 6 | 7.2 | 10 |
| `weak_stack_docker` | 20.16 | 8462 | 6 | 6.7 | 14 |
| `weak_stack_react` | 23.73 | 10916 | 9 | 6.0 | 12 |

### Search Engine Usage

- **SERPER:** Used in 7 test(s)
- **TAVILY:** Used in 8 test(s)

---

## 💡 Performance Optimization Opportunities

### 📝 Query Length Optimization Candidates

*Queries with 10+ words (may benefit from keyword extraction):*

- **block** (12 words)
  - `best practices for managing secrets in GitHub and preventing sensitive file exposure`
- **block** (11 words)
  - `prevent secrets in git commits API keys environment variables best practices`
- **block** (11 words)
  - `prevent secrets in git commits API keys environment variables best practices`

### 🎯 Search Quality Improvements Needed

*Searches with <50% high-quality domains:*

- **block** (tavily): 0% trusted domains
- **block** (serper): 20% trusted domains
- **block** (serper): 20% trusted domains
- **medium_risk_auth** (tavily): 0% trusted domains
- **medium_risk_auth** (serper): 0% trusted domains
- **medium_risk_auth** (serper): 0% trusted domains
- **medium_risk_dto** (tavily): 0% trusted domains
- **medium_risk_dto** (serper): 22% trusted domains
- **medium_risk_dto** (serper): 22% trusted domains
- **medium_risk_sql** (tavily): 0% trusted domains
- **medium_risk_sql** (serper): 0% trusted domains
- **medium_risk_sql** (serper): 0% trusted domains
- **soft_low_style** (tavily): 0% trusted domains
- **soft_medium_xss** (tavily): 0% trusted domains
- **soft_medium_xss** (tavily): 0% trusted domains
- **soft_medium_xss** (serper): 10% trusted domains
- **soft_medium_xss** (serper): 10% trusted domains
- **soft_medium_xss** (serper): 10% trusted domains
- **soft_medium_xss** (serper): 10% trusted domains
- **weak_stack_docker** (tavily): 14% trusted domains
- **weak_stack_docker** (tavily): 14% trusted domains
- **weak_stack_docker** (serper): 14% trusted domains
- **weak_stack_docker** (serper): 14% trusted domains
- **weak_stack_docker** (serper): 14% trusted domains
- **weak_stack_docker** (serper): 14% trusted domains
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