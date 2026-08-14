---
name: debug
description: 'Trigger when the user mentions debugging, investigating errors, finding root cause, tracing bugs, or diagnosing unexpected behavior. Uses systematic evidence-based approach — never guess or change code without proof.'
---

## /debug — 系統性除錯

### 核心原則

**Evidence before action** — 沒有證據不改 code。

### 流程

#### Phase 1: 理解問題

1. 整理 symptom（錯誤訊息、log、stack trace、相關設定值）
2. 列出 minimal reproduction steps（3-7 步）
3. 明確 expected vs actual
4. **環境定位**：哪個環境／哪個部署實例？只在特定環境重現，還是到處都有？
5. **停止條件**：symptom／repro steps／expected-vs-actual 這些問不出來 → 停下來，轉 `converge`，不要直接滑進 Phase 2 開始瞎猜 root cause

#### Phase 2: 找 Root Cause

1. 列出 3-5 個可能的 root cause 假設
2. 逐一驗證（grep、read file、跑小實驗）
3. 每個假設標記 ✅ confirmed / ❌ ruled out，附 file:line 證據
4. 複雜問題 → spawn sub-agent 平行驗證多個假設

#### Phase 3: 修復

1. 用該專案既有的測試框架寫一個 failing test 重現問題
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
- 需要搜尋大範圍 codebase（跨多個模組／套件）
- 改動涉及多個模組，需要平行確認影響範圍

### 常見切入點對照表（依你的環境自行維護，本 skill 不內建）

「這個 symptom 先查哪裡」高度依賴技術棧與部署方式，寫進本 skill 會讓它綁死在某個環境。
你的環境若已有程式碼導航索引或除錯手冊，**Phase 2 列假設之前先查它**，比從零猜快得多。
