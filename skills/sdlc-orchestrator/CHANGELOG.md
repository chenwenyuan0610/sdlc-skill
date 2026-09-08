# SDLC Skill 包 — 異動記錄規則

> ⚠️ 修改本檔案前後，MUST 依本檔規則記錄異動（本檔自己也適用這條規則）。

這份文件是**規則本身**，說明修改本規則包內「會被實際讀取執行的規則檔案」時要怎麼記錄異動。範圍：13 份 `SKILL.md`（9 個 phase skill + `bug-fix`/`converge`/`debug`/`rule-eval`）、`sdlc-orchestrator/references/` 下 10 份規則檔（`agent-teams.md`/`framework-defects.md`/`questioning-sufficiency.md`/`severity-format.md`/`tailoring.md`/`ticket-spec.md`/`traceability.md`/`tooling-reuse.md`/`test-case-coverage.md`/`phase-transition-reminders.md`）、`agents/` 下 3 份角色檔、`sdlc-entry.md`、`DESIGN.md`，共 28 份。**不含** `claude_sdlc.md`（它是衍生自 `sdlc-entry.md` 的速查摘要，不是規則正本，異動應跟著 `sdlc-entry.md` 走，不用另外追蹤）與 `DESIGN-RATIONALE.md`/`SDLC_Agent_優化設計.md`/`SDLC_Agent協作版.md`/`SDLC_主流程版_IAO.md`/`DISTRIBUTION.md`/`INSTALL.md`（依 `KNOWN-ISSUES.md` 的說明，這些是開發討論紀錄或已作廢文件，不是實際執行時會讀的規則）。

**實際的異動摘要表與逐筆詳細記錄放在 `CHANGELOG-ENTRIES.md`，不放在這裡**——這份規則檔會在每次編輯規則檔前被讀到，刻意保持精簡，避免內容隨記錄筆數增加而膨脹、消耗不必要的 token；想查歷史記錄時才去開 `CHANGELOG-ENTRIES.md`。

## 為什麼這個 repo 已經有 git 還需要這套機制

`git log` 記錄「改了什麼」，但目前的 commit message（例：`feat: skill new version`）沒有「為什麼改」的敘事，也沒有「這是同一個交付物分幾步做完」的合併判斷——這套機制記的是決策脈絡（觸發原因、取捨、跟其他規則的關係），跟 git 的逐次快照互補，不是重複建設。**兩者分工**：想知道「這個檔案現在長怎樣、什麼時候被誰改過」→ 看 `git log`/`git blame`；想知道「為什麼決定這樣改、跟其他規則的關係、有沒有回頭改過主意」→ 看 `CHANGELOG-ENTRIES.md`。

## 為什麼要有這個機制

純文字宣稱「已經改好了」容易跟檔案實際內容脫鉤，不是理論風險——本機制在另一份（未納入 git 管理的）安裝副本上就出過這個問題：異動記錄宣稱某份文件已同步改到新版，實際去讀檔案卻沒改到，直到之後重新核對才發現落差。

所以每筆記錄的「異動內容」段 MUST 附實際的 before/after 原文片段或指令輸出當證據，不接受「已完成」「已同步」這種沒有對照依據的空話——跟 `sdlc-verifier` agent「no evidence = unverified」的立場一致，同一套系統不該對自己的規則檔異動採用比對專案程式碼更寬鬆的證據標準。

## 範圍不是固定清單，新增規則檔案時 MUST 同步涵蓋

上面「範圍」段列的 25 份是建立本機制當下（`SKC-20260814-01`）的快照，**不是永久清單**。之後任何新增的規則檔案——新 skill 的 `SKILL.md`、`sdlc-orchestrator/references/` 下新的規則檔、新角色檔——判斷準則是「這份檔案在流程中會被實際讀取執行」（跟本檔開頭排除 `claude_sdlc.md`／討論紀錄文件的判準相同），符合的話：

1. **建立該檔案的同時**，MUST 在 frontmatter 結尾／H1 正下方加上跟其他 25 份一樣的提示行——不是「先建立，之後有空再補」
2. MUST 回來更新本檔開頭「範圍」段的清單與份數，不是加了提示行就算數——清單本身也要對得上實際檔案，否則下一個讀這份規則的人會誤以為範圍還是舊的
3. 這個新增動作本身也要依下方「記錄格式」開一筆 `CHANGELOG-ENTRIES.md` 記錄（類別可以是「規則調整（新增）」），不因為是「順手加的」就跳過

**為什麼不能省略**：這個機制存在的理由就是防止「宣稱涵蓋」跟「實際涵蓋」脫鉤——如果新增檔案沒有人記得補提示行，這份檔案本身就成為機制的第一個破口，而且是**靜默的破口**（沒有人會因為漏加一行提示而報錯），往往要等到下次稽核才會發現，那時候這份檔案可能已經被改過好幾次卻完全沒被追蹤。

## 首次使用檢查（給第一次遇到這條規則的 AI 或使用者）

在依本規則記錄異動之前，先確認目前環境是否已有機制主動提醒／攔截對規則檔案的編輯，而不是只能靠「記得看這行提示」：

1. **Claude Code 環境**：檢查 `~/.claude/settings.json`（或專案層 `.claude/settings.json`）的 `hooks.PreToolUse` 裡，是否已有一條攔截 Edit/Write、目標路徑符合本檔範圍段列出的 25 份檔案（`skills/**/SKILL.md`、`skills/sdlc-orchestrator/references/*.md`、`skills/sdlc-orchestrator/DESIGN.md`、`skills/sdlc-orchestrator/sdlc-entry.md`、`agents/*.md`）的規則。
2. **沒有的話**：向使用者說明現況，**問是否要新增**——`~/.claude/settings.json` 與 `~/.claude/hooks/*` 屬於需要使用者明確同意才能修改的等級，NEVER 自己動手安裝。
3. **非 Claude Code 環境**（例如 Codex，沒有對等的 PreToolUse hook 機制）→ 略過此步，只靠檔案開頭的提示行運作，這是已知的機制落差，不是遺漏。

## 合併規則（同一個交付物分多步完成時）

**判斷標準**：只看前一票，會不會對「這件事現在的真實狀態」有錯誤或過時的認知？會的話，兩票 MUST 合併成同一個票號記錄，不要拆成獨立票——票號沿用最早那一步的日期，內容依時間序拆成多個小節（例如「### 原始異動」「### 後續復原」，或「### 步驟一：...」「### 步驟二：...」，依實際情況命名）。

這個標準涵蓋兩種常見情況，不限於其中一種：
- **撤銷**：新增又復原，淨效果等於沒改
- **延續/補完**：後一票是在完成、修正或重構前一票還沒做完/做對的同一個交付物

**真正該分開的情況**：後一票是獨立、不相關的新交付物，不會讓人對前一票的內容產生錯誤認知。

## 記錄格式

**票號規則**：`SKC-<8碼日期>-<2碼序號>`，例如 `SKC-20260814-01`。同一天多筆用序號遞增區分。

**寫在哪**：打開 `CHANGELOG-ENTRIES.md`，在最上面的「異動摘要」表加一列，並在下面新增對應票號的區塊，累加記錄，不覆蓋歷史。每個票號區塊 MUST 包含：

```markdown
## SKC-<日期>-<序號>

- 時間戳：YYYY-MM-DD
- 類別：規則調整 / 規則調整（復原）/ 規則調整（新增）...
- 項目：一句話說明改了什麼
- 狀態：已落地 / 進行中
- 觸發原因：為什麼要改

### 異動內容
[具體改了哪個檔案的哪一段，原文 → 新文；多檔同一模式可只舉一個完整範例 + 條列其餘檔案]

### 證據
[實際 diff、Grep/Read 輸出，或明確指向可核對的來源；不接受純文字摘要]

### 已知待辦（若有）
[例如：尚未同步到其他安裝副本]
```

**與 git commit 的關係**：完成一筆 `CHANGELOG-ENTRIES.md` 記錄後，對應的 git commit message 可以只放簡短摘要並指回票號（例如 `feat: 補品質門禁範圍限縮（SKC-20260814-01）`），細節不必重複寫進 commit message——票號是連接兩邊的鍵。
