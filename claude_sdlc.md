## 開發工作入口（Step 0 先定位）

**Step 0 速查**（先查專案 `docs/` 現況，不要憑「問題清不清楚」跳關；完整判斷規則＝`.claude/sdlc-orchestrator/sdlc-entry.md`，語意衝突以該檔為準）：

| 現況 | 入口 |
|------|------|
| `docs/` 已有任一 SDLC 產出物 | 已在 pipeline——按下表對 `docs/` 現況定位，不可跳 phase |
| `docs/` 無產出物＋全新構想（還沒有系統＝創世） | 問題／使用者／方案任一不確定 → `product-discovery`；三者都明確 → Phase 5 表 |
| `docs/` 無產出物＋既有運行系統（演進；**別因缺 docs/ 退回 Phase 1**） | 瑣碎變更（constant／log／既有模組內小修）→ Phase 5 表；需新設計決策（新 schema/API/元件/模組）或範圍不確定 → `change-request` |

| SDLC Phase | `docs/` 現況 | skill |
|-----------|------|-------|
| 1 需求發想 | 無 `product-discovery.md` | `product-discovery` |
| 2 需求分析 | 有 product-discovery.md，無 requirements-spec.md | `requirement-scoping` |
| 3 設計 | 有 requirements-spec.md，無 design.md（拆分檔判定：architecture.md + db-schema.md/api-spec.md 至少兩份同時存在才算完成，單獨一份 architecture.md 不算） | `system-design` |
| 4 開發前準備 | 有設計文件，無 dev-setup.md | `dev-setup` |
| 5 開發實作 | 有 dev-setup.md，`handoff-log.md` 無「## Phase 5」記錄或記錄未完成 | `implementation-handoff` |
| 6 測試 | `handoff-log.md` 有「## Phase 5」完成記錄，無「## Phase 6」記錄 | `qa-handoff` |
| 7 部署 | `handoff-log.md` 有「## Phase 6」通過記錄，無「## Phase 7」記錄 | `release-handoff` |
| 8 維運 | 有 `feedback-log.md` 或已上線 | `ops-feedback` |
| 跨 phase | 既有規格／設計上的新變更，範圍不確定是否在內 | `change-request` |

**SDLC Phase 5-8 綁定**（_hitrust 專屬；無綁定專案的 fallback 與 dev skill 附帶清單、跨包變更 → `.claude/docs/sdlc-entry.md`）：

| Phase | Skill | 綁定工具 |
|-------|-------|------------------------|
| 5 開發實作 | `implementation-handoff` | 上方「Phase 5 開發實作」表 |
| 6 測試 | `qa-handoff` | Three-Army Review Team（編制 → `.claude/rules/model-dispatch-binding.md` §4）|
| 7 部署 | `release-handoff` | `hitrust-cicd-audit` + 對應 cicd-* repo，一律人工手動觸發 |
| 8 維運 | `ops-feedback` | Elasticsearch metrics（`.claude/docs/architecture.md`）|
