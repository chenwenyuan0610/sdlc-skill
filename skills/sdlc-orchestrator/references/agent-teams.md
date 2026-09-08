# Agent Teams — SDLC 派工分級（領域中立）

> ⚠️ 修改本檔案前後，MUST 依 `../CHANGELOG.md` 的規則記錄異動。

用途：`implementation-handoff`/`qa-handoff`/`system-design` 決定「這件事該 Lead 自己做、派一個 agent、還是派一組平行 agent」時查這份文件。角色定義檔 `sdlc-implementer.md`／`sdlc-reviewer.md`／`sdlc-verifier.md`，安裝在你選定的**角色檔目錄**下（不綁定任何特定技術棧）。

## 角色檔對應

| 角色檔 | 用途 | 唯讀 |
|--------|------|------|
| `sdlc-implementer.md` | 實作票（`implementation-handoff` 用） | 否，會寫檔（`Read/Edit/Write/Glob/Grep/Bash`）|
| `sdlc-reviewer.md` | 建設性審查：功能正確性/設計品質（`qa-handoff` 用） | **是，工具層真的擋住**（只有 `Read/Glob/Grep`）|
| `sdlc-verifier.md` | 對抗性驗證：安全性 or 證據查核，依 target 參數（`qa-handoff` 用） | **否——它有 `Bash`**（`target=evidence` 要重跑指令）。⚠ **不得在自動核准權限模式下派它**；唯讀是靠角色檔的自我約束，不是工具層限制 |

**派工方式分兩種環境**：Claude Code 會把角色檔目錄下的 `sdlc-*.md` 自動註冊成可派的 agent 型別——直接用該型別派工（frontmatter 的唯讀 tools 限制才會真正生效）；無自訂 agent 型別的環境（如 Codex）才用 embed——把角色檔內容讀進 generic worker/explorer 的 prompt，並註明「讀角色檔目錄下的 `sdlc-<角色>.md` 取得完整角色定義」。兩種方式都不要即興重寫角色設定。

## Tier 分級

⚠ **只有當使用環境的綁定層明文指定「SDLC pipeline 用哪張 Tier 表」時才改用它**，否則一律用本表。**兩套判準並存會讓同一個變更得到不同 Tier，而多個 MUST 關卡靠 Tier 判定**——所以只能有一個生效。
⚠ **使用環境為別條路線（例如自己的功能開發流程）定義的 Tier 表，不自動套用到 SDLC**——那類表往往綁著該路線自己的審查編制，套過來會派出 SDLC 明文禁派的角色。判斷方式：那張表指名的是誰？指名 SDLC 角色才適用，指名別條路線的角色就不是。

| Tier | 判斷標準 | 誰實作 | 完工覆核（**沒有「免審」這一格**）|
|------|---------|------|------|
| 0 Lead-direct | 單一改動 ≤20 行、單檔、無新依賴、無新對外介面 | Lead 直接做，**不用派工** | **1 個 `sdlc-reviewer`**（唯讀）|
| 1 單一 agent | 單一票，範圍明確，不涉及安全/共用資料/新架構決策 | 派 1 個 `sdlc-implementer` | **1 個 `sdlc-reviewer`**（唯讀）|
| 2 平行多 agent | 多張獨立票、或單票跨多個檔案/模組 | 每張獨立票各派 1 個 `sdlc-implementer`，平行執行 | 1 個 `sdlc-reviewer` ＋ 依風險加 1 個 `sdlc-verifier`（挑最相關角度）|
| 3 高風險全套 | 涉及安全/認證/共用資料寫入/跨模組架構變更/外部整合 | 平行實作 | `sdlc-reviewer` ＋ `sdlc-verifier`(target=security) ＋ `sdlc-verifier`(target=evidence) 三者都派，任一 NEEDS WORK 就不算過 |

**覆核 MUST 由實作者以外的角色做，所有 Tier 一體適用。** 環境有 agent 機制就派唯讀 agent；沒有就由另一個人看。⚠ **「Lead 覆核輸出」不算獨立覆核**——Lead 是派工、定範圍、決定怎麼做的人，讓他驗自己派的活，等於實作者自己勾自己的驗收項。**改動小不是免審的理由**：越小的改動越容易夾帶沒人注意的副作用，而它剛好也是最便宜的審查。

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
4. **最小改動**（**所有 Tier 一體適用；演進模式 MUST 逐項查**）：這次的 diff 有沒有超出票的範圍——順手重構了無關的程式碼、改了別的模組、調整了沒人要求的格式或 import 順序、動到與本票無關的設定或依賴版本。**判準是「這一行如果拿掉，本票的驗收條件會不會不過」**，答案是「不會」就該拿掉。既有專案的每一行多餘改動都是別人要回歸測試的成本，**「順便修一下」是既有系統最常見的災難來源**；真的該修就另開一張票，不要夾帶。

Tier 3 前三個角色都要派；Tier 2 至少派 1 個，依風險挑最相關的；**第 4 項不分 Tier，由該票的覆核者一併看**（它查的是 diff 範圍，不需要額外派人）。

## 卡住時的處理（retry 而非重派）

- Agent 執行卡住/回報有問題 → 先讓同一個 agent 修正 1 次，不要立刻換人重派
- 修正後仍卡住 → 停下來跟使用者確認方向，不要無限重試
- 不要對同一件事同時派多個 agent「平行試」比較結果——那是資源浪費，不是本文件說的「平行派工」（平行派工的前提是任務彼此獨立，不是同一任務跑多次）
