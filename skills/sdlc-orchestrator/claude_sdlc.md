# 開發工作入口 — 貼進你的 CLAUDE.md / AGENTS.md

> 這是表格版的流程入口，比 `DESIGN.md` 裡的 Entry Protocol 純文字版更好查。**兩者擇一即可**，不要兩份都貼。
> `install.py` 預設貼的是 Entry Protocol 純文字版；想改用這份表格版，把下面整段複製進你的 `CLAUDE.md`（Claude Code）或 `AGENTS.md`（Codex）取代它。
> 完整判斷規則 → `sdlc-entry.md`，語意衝突以該檔為準。

---

## 開發工作入口（Step 0 先定位）

**Step 0 速查**（**由上而下，第一個命中的那一列勝**；先查專案 `docs/` 現況，不要憑「問題清不清楚」跳關）：

| 現況 | 入口 |
|------|------|
| **問題本身講不清楚**（不確定是新構想還是既有系統的問題／bug 不知根因或需求在哪／還沒決定要不要做）→ **先收斂再分流**；**優先於 `docs/` 現況** | `converge`（pipeline 外，不計入 9 份編制；純討論、唯讀調查 OK，**MUST NOT 改 DB／code**；收斂完再回本表定位）|
| `docs/` 有 **`product-discovery.md`** | 已在 pipeline——按下表對 `docs/` 現況定位，不可跳 phase |
| `docs/` 無 `product-discovery.md`＋全新構想（還沒有系統＝創世） | 問題／使用者／方案任一不確定 → `product-discovery`；三者都明確 → 直接進開發實作 |
| `docs/` 無 `product-discovery.md`＋既有運行系統（演進；**別因缺 docs/ 退回 Phase 1**） | 瑣碎變更（constant／log／既有模組內小修）→ 直接進開發實作；需新設計決策（新 schema/API/元件/模組）或範圍不確定 → `change-request` |

⚠ **第 2 列的判定只看 `product-discovery.md` 一個檔。** 其餘 SDLC 檔名（`design.md`／`architecture.md`／`requirements-spec.md`／`change-log.md`／`change-specs/`／`handoff-log.md`／`converge-summary.md`／`feedback-log.md`）**演進模式也會產生**，拿它們判會把老專案誤送 Phase 1 重做需求發想、或誤送 Phase 7 部署一個還沒動工的變更。理由 → `sdlc-entry.md`「演進模式的例外」。

| SDLC Phase | `docs/` 現況 | skill |
|-----------|------|-------|
| 1 需求發想 | **Step 0 判定為創世模式**且無 `product-discovery.md` | `product-discovery` |
| 2 需求分析 | 有 product-discovery.md，無 requirements-spec.md | `requirement-scoping` |
| 3 設計 | 有 requirements-spec.md，設計文件未齊（有 design.md；或 architecture.md 加上 db-schema.md／api-spec.md／components.md／modules.md 任一份；或 architecture.md 內明寫不涉及資料庫／對外介面 → 才算完成）。**此判定只適用創世模式**——演進模式只補單一面向是正常的 | `system-design` |
| 4 開發前準備（**限創世**）| 有設計文件、無 dev-setup.md，**且骨架尚未建立** | `dev-setup`；**既有專案不走此關**（骨架／版控／排程恆為既存），其唯一不能丟的「測試描述」改由 `change-request`／`system-design` 演進支線產出 |
| 5 開發實作 | 創世：有 dev-setup.md；**演進：有 `change-specs/` 或 design-delta 即可，不需 dev-setup.md**。兩者皆須 `handoff-log.md` 無「## Phase 5」分節或該分節狀態非「完成」 | `implementation-handoff` |
| 6 測試 | `handoff-log.md` 有「## Phase 5」完成記錄，無「## Phase 6」記錄 | `qa-handoff` |
| 7 部署 | `handoff-log.md` 有「## Phase 6」通過記錄，無「## Phase 7」記錄 | `release-handoff` |
| 8 維運 | 有 `feedback-log.md` 或已上線，**且沒有任何進行中的階段** | `ops-feedback` |
| 跨 phase | 既有規格／設計上的新變更，範圍不確定是否在內 | `change-request` |

**階段完成的判定**：`handoff-log.md` 每個 `## Phase N` 分節第一行是 `狀態：進行中` 或 `狀態：完成`。先掃有沒有「進行中」的分節，有就是目前階段（測試失敗退回開發也走這條）；都沒有才按產出物比對。**標頭存在不等於做完。**

不確定現在在哪個階段時，先看 `docs/` 裡實際有哪些檔案，不要憑對話印象判斷。

⚠ **跳過 Phase 3-4 不包含跳過測試**：演進模式跳掉的是設計與開發前準備，開發完成一律 MUST 接 `qa-handoff`（Phase 6）。既有專案的改動落在別人寫的、還在跑的程式碼上，回歸測試的價值比新專案更高。

**Phase 5-8 工具綁定**（依你的環境自行填寫；沒有就刪掉這張表，skill 會走內建通用 fallback）：

| Phase | Skill | 綁定你環境的工具 |
|-------|-------|------------------|
| 5 開發實作 | `implementation-handoff` | 例：你既有的開發規範 skill／流程 |
| 6 測試 | `qa-handoff` | 例：你既有的審查編制／測試流程 |
| 7 部署 | `release-handoff` | 例：你既有的 CI/CD 稽核流程 |
| 8 維運 | `ops-feedback` | 例：你既有的監控／metrics 系統 |
