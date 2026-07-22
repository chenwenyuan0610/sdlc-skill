---
name: debug
description: 'Trigger when the user mentions debugging, investigating errors, finding root cause, tracing bugs, or diagnosing unexpected behavior. Uses systematic evidence-based approach — never guess or change code without proof.'
---

## /debug — 系統性除錯

### 核心原則

**Evidence before action** — 沒有證據不改 code。

### 流程

#### Phase 1: 理解問題

1. 整理 symptom（錯誤訊息、log、stack trace、Apollo config dump）
2. 列出 minimal reproduction steps（3-7 步）
3. 明確 expected vs actual
4. **環境定位**：dev / sit / sit-sg / jmeter / poc / prod / prod-sg？哪個 GKE cluster？

#### Phase 2: 找 Root Cause

1. 列出 3-5 個可能的 root cause 假設
2. 逐一驗證（grep、read file、跑小實驗）
3. 每個假設標記 ✅ confirmed / ❌ ruled out，附 file:line 證據
4. 複雜問題 → spawn sub-agent 平行驗證多個假設

#### Phase 3: 修復

1. 寫 failing test 重現問題（Java：JUnit 5；Vue：Vitest）
2. 最小改動修復（只改必要的）
3. 確認 test 通過 + 無 regression

#### Phase 4: 驗證

1. 所有測試通過
2. 原問題不再發生
3. 無新的 side effect
4. 輸出 diff 給 user 決定

### 輸出格式

每個 phase 完成時輸出摘要：

- **Root Cause**: 一句話 + file:line
- **Fix**: 改了什麼 + 為什麼
- **Verification**: 測試結果（附 command output）

### 何時用 sub-agent

- 同時驗證多個 root cause 假設
- 需要搜尋大範圍 codebase（13 個 Maven module）
- 改動涉及多個模組，需要平行確認影響範圍

### _hitrust 常見除錯切入點

| Symptom | 第一個檢查 |
|---------|----------|
| HTTP 401/403 | Spring Security filter chain (`SecurityConfig.java`) + JWT 驗證 |
| Connection pool 耗盡 | HikariCP 設定（4 datasource：settings/transaction/logs/permanent）|
| Apollo config 沒生效 | `apollo.bootstrap.namespaces` + 確認 namespace publish |
| Cloud SQL 連不上 | `./cloud-sql-proxy` 是否啟動 + IAM SA 權限 |
| GKE pod CrashLoopBackOff | `kubectl describe pod` + check JRE17 vs JRE21 image mismatch |
| GitLab pipeline 失敗 | 對應 `cicd-*` repo 的 `.remote-gitlab-ci.yml` + runner tag `shareconnect-gke-runner` |
