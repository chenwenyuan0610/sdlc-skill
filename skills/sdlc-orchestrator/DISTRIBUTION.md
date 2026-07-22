# SDLC Skill 包 — 分發與安裝指南（整包目錄複製）

> **⚠ 已作廢，改看 `INSTALL.md`。** 本檔記載的是 2026-07-10 的手動複製流程，當時還沒有 `install.py`。內容保留供對照，安裝請勿照這份做。

> 分發方式 2026-07-10 拍板：**整包目錄複製**。這一頁給拿到包的同事照做；給分發者的打包清單在最下方。
> 這套流程的內容完全領域中立——不假設 Java/Vue/既有業務領域，任何技術棧的專案都適用。

## 包內容（共 15 個檔案單位）

| 內容 | 數量 | 放到你環境的哪裡 |
|------|------|-----------------|
| 9 個 phase/分診 skill 目錄（`product-discovery`、`requirement-scoping`、`system-design`、`dev-setup`、`implementation-handoff`、`qa-handoff`、`release-handoff`、`ops-feedback`、`change-request`，含各自 `references/`） | 9 | `<你的專案>/.claude/skills/` |
| 角色檔 `sdlc-implementer.md` / `sdlc-reviewer.md` / `sdlc-verifier.md` | 3 | `<你的專案>/.claude/agents/` |
| 共用參照 `sdlc-orchestrator/references/agent-teams.md` + `references/severity-format.md` | 2 | `<你的專案>/.claude/skills/sdlc-orchestrator/references/`（保持這個路徑，skill 內引用寫的是它） |
| 流程源頭文件 `SDLC_主流程版_IAO.md`（8 階段 35 步驟原文，各 skill 檔頭都引用它） | 1 | `<你的專案>/.claude/skills/sdlc-orchestrator/` |
| Entry Protocol 文字段（見 `DESIGN.md`「Entry Protocol」區塊） | 1 | 貼進你自己的 `CLAUDE.md` 或 `AGENTS.md`（見下） |

## 安裝 — 用 Claude Code 的同事

1. 把上表前四列複製進你專案的 `.claude/` 對應位置（第四列 `SDLC_主流程版_IAO.md` 放 `skills/sdlc-orchestrator/` 下，9 份 skill 檔頭都引用它）。
2. 打開 `DESIGN.md`，把「Entry Protocol」整段程式碼區塊貼進你專案的 `CLAUDE.md`（沒有就建一個）。
3. 驗證：問 Claude「我想開發一個新工具」——它應該先檢查專案 `docs/` 資料夾、而不是直接開始寫程式。skill 的自動觸發（description 配對）是加分，Entry Protocol 是保底：兩條路都會把它帶到正確的 SKILL.md。

## 安裝 — 用 Codex 的同事

1. 同樣把前四列複製進專案的 `.claude/` 位置（Codex 沒有 skill 自動配對，但這些只是路徑固定的 markdown 檔，Codex 讀得到）。
2. 把「Entry Protocol」整段貼進你專案的 `AGENTS.md`（沒有就建一個）。Entry Protocol 的動作全部寫成「打開並讀取某路徑的 SKILL.md 照做」——不依賴任何 Claude 專屬機制。
3. 驗證：對 Codex 說「我想開發一個新工具」——它應該照 AGENTS.md 的 Entry Protocol 先查 `docs/`。

## 使用起點（安裝完之後）

- 全新構想 → 從 `product-discovery` 開始，每個階段的產出都會寫成專案 `docs/` 下的 md 檔。
- 專案已經走過部分流程 → 看 `docs/` 裡已有哪些檔案，Entry Protocol 的對照表會告訴你現在該進哪個階段。
- 隨時想確認「現在在哪、下一步是什麼」→ 打開 `docs/handoff-log.md` 與 `docs/` 檔案清單，不要憑印象。

## Phase 5/6 派工說明（權限與模型）

- 票量大時 `implementation-handoff`（Phase 5）/`qa-handoff`（Phase 6）會依 `agent-teams.md` 分級表**自動派** `sdlc-implementer`/`sdlc-reviewer`/`sdlc-verifier` subagent——這是設計行為，不用另外下指令；日常單人跑流程不會派。Codex 等沒有自訂 agent 型別的環境改用 embed 方式（見 `agent-teams.md`）。
- **權限**：派工動作本身不跳提示，但 subagent 動手（Write/Edit、跑品質門禁指令）在 Claude Code 預設權限模式下會逐項請你批准——**卡在權限提示不是流程壞掉**，人在場按批准即可。想無人值守跑完：開 session 用 acceptEdits 模式（Shift+Tab 切換或 `--permission-mode acceptEdits`），或在專案 `.claude/settings.json` 的 `permissions` 設 `"defaultMode": "acceptEdits"` 並補你工具鏈的 allow 規則（如 `Bash(npm *)`）。
- **模型**：三支角色檔都預設 sonnet；只有高複雜票才升 opus，升級條件與判斷軸 → `agent-teams.md`「模型選擇」段。
- **技術棧 dev skill**：你的環境若有自己的開發規範 skill（如 `typescript-dev`），派工 prompt 附上路徑，worker 會讀取遵循；沒有也能跑（本包刻意不含任何技術棧 skill，保持領域中立）。

## 給分發者：打包命令

```bash
SRC=<你的專案>/.claude
OUT=~/sdlc-pack
mkdir -p $OUT/skills $OUT/agents
for s in product-discovery requirement-scoping system-design dev-setup \
         implementation-handoff qa-handoff release-handoff ops-feedback change-request; do
  cp -R $SRC/skills/$s $OUT/skills/
done
mkdir -p $OUT/skills/sdlc-orchestrator/references
cp $SRC/skills/sdlc-orchestrator/references/agent-teams.md \
   $SRC/skills/sdlc-orchestrator/references/severity-format.md \
   $OUT/skills/sdlc-orchestrator/references/
cp $SRC/agents/sdlc-implementer.md $SRC/agents/sdlc-reviewer.md $SRC/agents/sdlc-verifier.md $OUT/agents/
cp $SRC/skills/sdlc-orchestrator/DESIGN.md $SRC/skills/sdlc-orchestrator/DISTRIBUTION.md \
   "$SRC/skills/sdlc-orchestrator/SDLC_主流程版_IAO.md" $OUT/skills/sdlc-orchestrator/
echo "pack ready: $OUT"
```

打包時**不要**帶入：`SDLC_Agent協作版.md`（內部決策史/報告稿）、`DESIGN-RATIONALE.md`（內部討論記錄）、`<你的專案>/CLAUDE.md` 的 Phase 5-8 綁定段（那是既有專案專屬綁定層，各團隊要綁自己的工具就仿照該段自己寫）。

## 更新機制（整包複製的代價與對策）

複製出去的包不會自動更新。約定：包的版本以本檔頂部的拍板日期為準；有重大修訂時由分發者重新打包通知，同事整包覆蓋（`docs/` 產出物在各自專案裡，覆蓋 skill 包不影響它們）。
