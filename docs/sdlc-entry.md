# SDLC 開發工作入口 — Step 0 完整判斷規則（唯一 owner）

> 本檔是 CLAUDE.md「開發工作入口 Step 0 判斷表」的完整版：該表是速查摘要，**語意衝突以本檔為準**（發現衝突→GREEN 級修正摘要並回報）。本文為 2026-07-11 從 CLAUDE.md 原封不動外移（sdlc-orchestrator 歷經第八/九/十一輪除錯的定案語意，改動屬 YELLOW 級）。設計依據 → `.claude/skills/sdlc-orchestrator/DESIGN.md`。

## Step 0 — 先判斷現在在 SDLC 哪個階段

（sdlc-orchestrator D2/E1/第九輪 Entry Protocol/第十一輪創世-演進決策，**先查 `docs/` 現況，不要只憑「問題現在清不清楚」判斷**——Phase 1-4 產出的正是「清楚的問題/方案」，這是進 Phase 5-8 的前提，不是跳過 Phase 5-8 的理由）：

**先分兩種生命週期**（一次性「創世」vs 重複用「演進」——技術選型/整體架構這類創世工作只做一次，舊專案早已定案不重做；每個新功能走的是演進迴圈）：

1. 專案 `docs/` 已有任一 SDLC 產出物（`product-discovery.md`/`requirements-spec.md`/`design.md`（或拆分的 `architecture.md` 等）/`dev-setup.md`/`handoff-log.md`/`feedback-log.md`）→ **已在 SDLC pipeline 裡**，用 CLAUDE.md Phase 表依 `docs/` 現況判斷目前哪個 phase，不可跳過
2. `docs/` 沒有產出物，且**這是全新構想、還沒有任何既有系統**（創世模式）→ 問題本質/使用者/方案任一不確定，從 Phase 1（`product-discovery`）；三者都已明確，直接用 CLAUDE.md「Phase 5 開發實作」表
3. `docs/` 沒有產出物，但**專案是既有運行中的系統**（老專案採用這套流程；演進模式，**別因為缺 `docs/` 就當成新專案退回 Phase 1**）：
   - 一看就知道改哪的瑣碎變更（改 constant / 補 log / 既有模組內小修）→ 直接 CLAUDE.md「Phase 5 開發實作」表
   - 需要新設計決策（新 schema/API/元件/模組）、或範圍不確定是否在既有範圍內 → `change-request`（它用程式碼現況當基線分診，會轉去只做該面向的 `system-design` design-delta 或直接開發，並順手替舊專案補上 `docs/design.md` 基線）

Phase 3 拆分檔判定：`architecture.md` + `db-schema.md`/`api-spec.md` **至少兩份同時存在**才算設計已完成，單獨一份 architecture.md 不算。

## 跨包變更綁定（_hitrust 專屬，供 change-request 步驟 2.5 查）

變更橫跨 ≥2 個 repo 時，需求級單一真相記錄放 `_hitrust/doc/change-requests/<需求名>.md`（規格 delta + 涉及包清單 + 各包狀態表）；各包各自走 pipeline、完成回寫；順序 = API 供應方先行（threedsserver-v3 → admin-frontend / acs-simulate-cloud / integrator-tester）。

## 無綁定專案（獨立技術棧、非 _hitrust 既有模組）

CLAUDE.md「SDLC Phase 5-8 綁定」表不適用——SDLC skill 內建通用 fallback 接手（品質門禁/獨立審查精神/部署前檢查清單/監控盤點），不假設任何特定工具存在。

**設計原則（為何綁定與 skill 分離，勿破壞）**：9 份 SDLC skill 是**領域中立**的通用流程，可移植給其他專案/團隊——skill 檔案本身**不寫死任何工具名稱**，只講「依既有流程/若無則走通用 fallback」；「這個 phase 轉交去哪個工具」的實際綁定只放 CLAUDE.md「SDLC Phase 5-8 綁定」表與本檔。未來「簡化」SDLC skill 時 **NEVER 把 _hitrust 專屬工具名硬編進 skill 本體**（會破壞可攜性）。

**無綁定專案的 dev skill 附帶清單**（本環境專屬，供 `agent-teams.md`「派工 prompt 附帶技術棧 dev skill」查表）：Node.js/TypeScript 票 → `typescript-dev`；React/通用 UI 票 → `frontend-uiux-universal`；安全敏感前端票（auth/輸入驗證/token）→ 加 `frontend-security`；Python 票 → `python-dev`。⚠ `frontend-engineer` 是 Vue/admin-frontend 專屬綁定，React 專案不要附。

各 skill 完整 TRIGGER / DO NOT TRIGGER 見其 SKILL.md description；skill 觸發詳表 → `.claude/rules/skill-trigger-matrix.md`。
