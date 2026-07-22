# Agent Teams — SDLC 派工分級（領域中立）

用途：`implementation-handoff`/`qa-handoff`/`system-design` 決定「這件事該 Lead 自己做、派一個 agent、還是派一組平行 agent」時查這份文件。角色定義檔在 Entry Protocol 指定的 `<agents-root>/sdlc-*.md`，不假設它與 `<skill-root>` 同層。

## 角色檔對應

| 角色檔 | 用途 | 唯讀 |
|--------|------|------|
| `<agents-root>/sdlc-implementer.md` | 實作票（`implementation-handoff` 用） | 否，會寫檔 |
| `<agents-root>/sdlc-reviewer.md` | 建設性審查：功能正確性/設計品質（`qa-handoff` 用） | 是 |
| `<agents-root>/sdlc-verifier.md` | 對抗性驗證：安全性 or 證據查核，依 target 參數（`qa-handoff` 用） | 是 |

**派工方式分兩種環境**：角色檔選在 Claude Code 會自動發現的標準 `agents/` 目錄時，直接用註冊後的 `sdlc-*` agent 型別派工（frontmatter 的唯讀 tools 限制才會真正生效）；Codex 標準位置、自訂位置，或其他無自訂 agent 型別的環境則用 embed——從 Entry Protocol 的 `<agents-root>` 讀取 `sdlc-<角色>.md`，把完整角色定義放進 generic worker/explorer 的 prompt。兩種方式都不要即興重寫角色設定。

## Tier 分級

| Tier | 判斷標準 | 誰做 |
|------|---------|------|
| 0 Lead-direct | 單一改動 ≤20 行、單檔、無新依賴、無新對外介面 | Lead 直接做，不用派工、不用額外審查 |
| 1 單一 agent | 單一票，範圍明確，不涉及安全/共用資料/新架構決策 | 派 1 個 `sdlc-implementer`，Lead 覆核輸出 |
| 2 平行多 agent | 多張獨立票、或單票跨多個檔案/模組 | 每張獨立票各派 1 個 `sdlc-implementer`，平行執行；完工後派 1 個 `sdlc-reviewer` 或 `sdlc-verifier`（依風險挑最相關角度）|
| 3 高風險全套 | 涉及安全/認證/共用資料寫入/跨模組架構變更/外部整合 | 平行實作 + `sdlc-reviewer` + `sdlc-verifier`(target=security) + `sdlc-verifier`(target=evidence) 三者都派，任一 NEEDS WORK 就不算過 |

**判斷時機**：進 `implementation-handoff` 拆票、進 `qa-handoff` 排審查、進 `system-design` 派多面向設計時，都用這張表決定規模，不要憑感覺判斷。`system-design` 派多面向時用 `general-purpose`（設計不是實作，不套用 `sdlc-implementer`），角色紀律見 `system-design/SKILL.md` 本體的 Core rule。

## 模型選擇（派工時）

- 預設照角色檔 frontmatter 的 `model` 派（三支 `sdlc-*` 都已釘 sonnet），派工時不額外指定
- 單票同時命中 **≥2 個高複雜信號**才升 opus，且派工說明 MUST 寫明理由：跨模組架構決策要在實作中現場做 / 安全關鍵路徑（認證、授權、金流、密鑰處理）/ 大範圍改動（≥10 檔或核心共用模組重構）/ 驗收標準高度依賴推理（複雜演算法、併發正確性）
- Tier 管「派幾個、怎麼審」，模型管「單票多難」——兩軸獨立判斷；NEVER 為求保險整批升 opus
- 環境綁定：Claude Code 派工用 Agent 的 `model` 參數覆寫；無此機制的環境（如 Codex）直接選對應等級的模型開 worker

## 派工 prompt 附帶技術棧 dev skill

你的環境裡若有對應本票技術棧的開發規範 skill（如果有的話——看已安裝的 skill 目錄裡有沒有針對該語言/框架的開發規範），派工 prompt MUST 附上該 SKILL.md 路徑，worker 依角色檔 Step 1 讀取遵循；環境沒有就省略，不阻塞派工、不要求先補 skill（本包刻意不含任何技術棧 skill，保持領域中立）。

## 平行派工原則

- 多張範圍互相獨立的票（改動不共用同一批檔案）→ MUST 平行派，不要序列一張張做——序列做法在等待時間上沒有任何好處，純粹浪費
- 設計面向（架構/資料庫/API/前端/模組）互相獨立時 → 同理平行派，每個 agent 只做一個面向，不跨面向擴張
- 平行派出去的 agent 之間互不依賴、互不通訊——若某個面向的產出需要等另一個面向先決定（例如 API 設計需要先知道 DB schema），則那兩者不算獨立，要序列

## 審查角度（Tier 2-3 適用）

不是「派幾個一樣的 reviewer 各看一遍」，是每個角色專門看不同的失敗模式（角色定義 + 嚴重度格式見 `severity-format.md`）：

1. **功能正確性**（`sdlc-reviewer`）：邏輯有沒有做對，符不符合驗收標準
2. **安全性**（`sdlc-verifier`, target=security）：有沒有引入常見弱點（injection、權限繞過、敏感資料外洩）
3. **證據驗證**（`sdlc-verifier`, target=evidence）：宣稱「測試過了」「跑過了」的地方，有沒有實際 command output 佐證，不接受口頭宣稱

Tier 3 三個角色都要派；Tier 2 至少派 1 個，依風險挑最相關的。

## 卡住時的處理（retry 而非重派）

- Agent 執行卡住/回報有問題 → 先讓同一個 agent 修正 1 次，不要立刻換人重派
- 修正後仍卡住 → 停下來跟使用者確認方向，不要無限重試
- 不要對同一件事同時派多個 agent「平行試」比較結果——那是資源浪費，不是本文件說的「平行派工」（平行派工的前提是任務彼此獨立，不是同一任務跑多次）
