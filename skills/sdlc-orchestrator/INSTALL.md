# SDLC Skill 包 — 安裝指南

> 這一頁給拿到包的人照做。這套流程的內容完全領域中立——不假設任何語言、框架或產業，任何技術棧的專案都適用。

## 包內容

| 內容 | 數量 | 安裝後的位置 |
|------|------|-------------|
| 9 個 phase/分診 skill 目錄（`product-discovery`、`requirement-scoping`、`system-design`、`dev-setup`、`implementation-handoff`、`qa-handoff`、`release-handoff`、`ops-feedback`、`change-request`，含各自 `references/`） | 9 | Claude Code：`<scope>/.claude/skills/`；Codex：`<scope>/.agents/skills/` |
| 角色檔 `sdlc-implementer.md` / `sdlc-reviewer.md` / `sdlc-verifier.md` | 3 | Claude Code：`<scope>/.claude/agents/`；Codex：`<scope>/.agents/agents/` |
| 共用參照 `agent-teams.md` + `severity-format.md` | 2 | 上述 `skills/sdlc-orchestrator/references/` |
| 流程源頭文件 `SDLC_主流程版_IAO.md`（8 階段 35 步驟原文，各 skill 檔頭都引用它） | 1 | 上述 `skills/sdlc-orchestrator/` |
| Entry Protocol 文字段（見 `DESIGN.md`「Entry Protocol」區塊） | 1 | 貼進你自己的 `CLAUDE.md` 或 `AGENTS.md` |

## 安裝（主路徑）

在包的根目錄執行：

```
python install.py
```

安裝程式分 4 步完成（前三步詢問，第四步才寫入）：

1. **安裝範圍** —— 選個人／全域或單一專案。只有專案安裝會要求選擇專案／工作區根目錄。若誤選 `.claude`、`.codex`、`.agents` 或其中的子資料夾，程式會拒絕並要求重選。
2. **流程入口寫進哪個檔** —— 選項會跟安裝範圍一致：
   - 個人：`~/.claude/CLAUDE.md`（Claude Code）或 `$CODEX_HOME/AGENTS.md`（Codex；未設定 `CODEX_HOME` 時為 `~/.codex/AGENTS.md`）
   - 專案：`<專案>/CLAUDE.md`（Claude Code）或 `<專案>/AGENTS.md`（Codex）
3. **skill 與角色檔各自放哪裡** —— 先問 skill，再問角色檔。每題都有三個選項：與第 2 步規則檔相符的標準位置（排第一且是預設）、另一工具的標準位置、依個人習慣輸入其他精確目錄：
   - Claude Code：個人 `~/.claude/{skills,agents}`；專案 `<專案>/.claude/{skills,agents}`
   - Codex：個人 `~/.agents/{skills,agents}`；專案 `<專案>/.agents/{skills,agents}`
4. **開始安裝** —— 安全檢查全部通過後才一次建立所需的完整父目錄與安裝內容。

Entry Protocol 會直接寫入第 3 步實際選定的完整 skill 與角色根目錄，因此可以混搭兩種工具的標準位置或自訂位置，不會再假設兩者必須同層。

已存在的檔案怎麼處理：

- **`CLAUDE.md` / `AGENTS.md`**：原有內容一律保留，流程入口附加在最後面；動到之前會先備份。已經裝過的話會**先問你**要不要更新，答 n 就完全不動。即使你當初是手動貼的（沒有標記），安裝程式也會認出內容並停下來問，不會貼出第二份。
- **skill 目錄與角色檔**：自動判斷，不會逐項問你。你若原本就有同名的 skill（這 9 個名字很通用，容易撞名），它會被完整移到所選 skill 根目錄旁的 `sdlc-replaced-backups/` 保留，安裝結束時列出清單請你確認。**不會放在 `skills/` 裡面**——那會讓它被當成第二個同名 skill 載入。
- **重複執行**：安全。沒改過的檔案直接覆蓋、不留備份；改過的才會保留舊版。

**同時用 Claude Code 和 Codex**：一次只會寫入一個檔案。兩個都要就跑兩次 `install.py`，第二次選另一個工具即可（不會產生重複內容）。

裝完驗證：對你的 AI 說「我想開發一個新的小工具」。裝對的話它**不會**直接開始寫程式，而是先問你需求、或先去看專案的 `docs/` 資料夾。如果它直接跳去寫 code，代表 Entry Protocol 沒進到規則檔裡（見附錄手動補上）。

## 使用起點（安裝完之後）

- 全新構想 → 從 `product-discovery` 開始，每個階段的產出都會寫成專案 `docs/` 下的 md 檔。
- 專案已經走過部分流程 → 看 `docs/` 裡已有哪些檔案，Entry Protocol 的對照表會告訴你現在該進哪個階段。
- 隨時想確認「現在在哪、下一步是什麼」→ 打開 `docs/handoff-log.md` 與 `docs/` 檔案清單，不要憑印象。

## Phase 5/6 派工說明（權限與模型）

- 票量大時 `implementation-handoff`（Phase 5）/`qa-handoff`（Phase 6）會依 `references/agent-teams.md` 分級表**自動派** `sdlc-implementer`/`sdlc-reviewer`/`sdlc-verifier` subagent——這是設計行為，不用另外下指令；日常單人跑流程不會派。沒有自訂 agent 型別的環境（如 Codex）改用 embed 方式（見 `agent-teams.md`）。
- **權限**：派工動作本身不跳提示，但 subagent 動手（Write/Edit、跑品質門禁指令）在 Claude Code 預設權限模式下會逐項請你批准——**卡在權限提示不是流程壞掉**，人在場按批准即可。想無人值守跑完：開 session 用 acceptEdits 模式（Shift+Tab 切換或 `--permission-mode acceptEdits`），或在專案 `.claude/settings.json` 的 `permissions` 設 `"defaultMode": "acceptEdits"` 並補你工具鏈的 allow 規則。
- **模型**：三支角色檔都預設 sonnet；只有高複雜票才升 opus，升級條件與判斷軸 → `references/agent-teams.md`「模型選擇」段。
- **技術棧開發規範**：你的環境若有自己的開發規範 skill，派工 prompt 附上路徑，worker 會讀取遵循；沒有也能跑（本包刻意不含任何技術棧 skill，保持領域中立）。

## 附錄：手動安裝

不想跑安裝程式、或想確認它到底動了哪些檔案時照這個做。

**skill 要放在工具的標準位置**：Claude Code 使用專案 `<你的專案>/.claude/skills/` 或個人 `~/.claude/skills/`；Codex 使用專案 `<你的專案>/.agents/skills/` 或個人 `~/.agents/skills/`。以下先用 Claude Code 專案層示範；Codex 請把 `.claude/` 換成 `.agents/`。

1. 把包裡的 `skills/` 全部內容複製進 `<你的專案>/.claude/skills/`，`agents/` 全部內容複製進 `<你的專案>/.claude/agents/`（沒有這些資料夾就自己建）：

   ```
   <你的專案>/
     .claude/
       skills/    ← 本包 skills/ 的全部內容（含 sdlc-orchestrator/）
       agents/    ← 本包 agents/ 的全部內容
   ```

   `sdlc-orchestrator/references/` 與 `sdlc-orchestrator/SDLC_主流程版_IAO.md` 要保持這個相對路徑——9 份 skill 檔頭與內文引用寫的就是它。

2. 打開 `skills/sdlc-orchestrator/DESIGN.md`，把「Entry Protocol」整段程式碼區塊複製貼進你專案根目錄的規則檔：用 Claude Code 貼進 `CLAUDE.md`，用 Codex 貼進 `AGENTS.md`（沒有那個檔就新建一個）。把其中的 `{{SKILLS_ROOT}}` 與 `{{AGENTS_ROOT}}` 分別換成你實際複製到的完整 `skills/` 與 `agents/` 路徑。

3. 驗證同上節。Claude Code 與 Codex 都支援從各自標準目錄發現 skill，並可依 description 隱式啟用；Entry Protocol 是 deterministic fallback，會用明確路徑要求 AI 打開對應的 SKILL.md，因此不依賴隱式配對是否命中。

## 更新機制

複製出去的包不會自動更新。有重大修訂時會重發整包，整包覆蓋即可——`docs/` 產出物在你自己專案裡，覆蓋 skill 包不影響它們。
