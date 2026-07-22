# SDLC 開發工作入口 — Step 0 完整判斷規則

> 本檔是「開發工作入口 Step 0 判斷表」（`claude_sdlc.md`，貼進你 `CLAUDE.md`/`AGENTS.md` 的那份）的完整版：該表是速查摘要，**語意衝突以本檔為準**。設計依據 → `DESIGN.md`。

## Step 0 — 先判斷現在在 SDLC 哪個階段

**先查專案 `docs/` 現況，不要只憑「問題現在清不清楚」判斷** —— Phase 1-4 產出的正是「清楚的問題/方案」，這是進 Phase 5-8 的前提，不是跳過 Phase 1-4 的理由。

**先分兩種生命週期**（一次性「創世」vs 重複用「演進」——技術選型/整體架構這類創世工作只做一次，舊專案早已定案不重做；每個新功能走的是演進迴圈）：

1. 專案 `docs/` 已有任一 SDLC 產出物（`product-discovery.md`/`requirements-spec.md`/`design.md`（或拆分的 `architecture.md` 等）/`dev-setup.md`/`handoff-log.md`/`feedback-log.md`）→ **已在 SDLC pipeline 裡**，用 Phase 表依 `docs/` 現況判斷目前哪個 phase，不可跳過
2. `docs/` 沒有產出物，且**這是全新構想、還沒有任何既有系統**（創世模式）→ 問題本質/使用者/方案任一不確定，從 Phase 1（`product-discovery`）；三者都已明確，直接進開發實作
3. `docs/` 沒有產出物，但**專案是既有運行中的系統**（老專案採用這套流程；演進模式，**別因為缺 `docs/` 就當成新專案退回 Phase 1**）：
   - 一看就知道改哪的瑣碎變更（改 constant / 補 log / 既有模組內小修）→ 直接開發實作
   - 需要新設計決策（新 schema/API/元件/模組）、或範圍不確定是否在既有範圍內 → `change-request`（它用程式碼現況當基線分診，會轉去只做該面向的 `system-design` design-delta 或直接開發，並順手替舊專案補上 `docs/design.md` 基線）

Phase 3 設計完成的判定（三者任一成立即算完成）：

1. 有 `docs/design.md`
2. 有 `architecture.md`，且 `db-schema.md`／`api-spec.md`／`components.md`／`modules.md` 至少再有一份
3. 有 `architecture.md`，且檔內明確寫出本專案不涉及資料庫／不提供對外介面

只有單獨一份 `architecture.md` 又沒有第 3 點的聲明 → 不算完成（可能是專案原有的無關文件）。

## 階段完成狀態的判定

`docs/handoff-log.md` 的每個 `## Phase N` 分節，第一行 MUST 是 `狀態：進行中` 或 `狀態：完成`。**標頭存在不等於做完** —— 只看標頭會把做到一半的階段誤判成已結束而跳過。判斷順序：先掃有沒有任何分節是「進行中」，有的話那就是目前階段（Phase 6 測試失敗要退回 Phase 5 也走這條路）；都沒有才往下按產出物比對。

## 跨包變更（變更橫跨 ≥2 個 repo 時）

需求級的單一真相記錄放「發起變更的主 repo」的 `docs/change-log.md`（與 `change-request` skill 實際寫入的檔案一致），內含：規格 delta + 涉及的 repo 清單 + 各 repo 狀態表。各 repo 各自走完整 pipeline、完成後回寫狀態。順序原則 = **API 供應方先行**（先做提供介面的那一端，再做消費端）。

## Phase 5-8 的工具綁定（依你的環境自行定義）

這 9 份 skill 是**領域中立**的通用流程，不假設任何特定技術棧或工具。Phase 5-8（開發/測試/部署/維運）在各團隊往往已有既有工具與規範，因此：

- **你的環境若已有既有流程**（既有的開發規範 skill、審查編制、部署稽核流程、監控系統）→ 在你自己的 `CLAUDE.md`/`AGENTS.md` 寫一張「Phase → 對應工具」的綁定表，skill 會優先照綁定走
- **沒有綁定** → skill 內建的通用 fallback 接手（品質門禁、獨立審查精神、部署前檢查清單、監控盤點），不會卡住

**設計原則（勿破壞）**：skill 檔案本身**不寫死任何工具名稱**，只講「依既有流程/若無則走通用 fallback」；「這個 phase 轉交去哪個工具」的實際綁定只放在你自己的 `CLAUDE.md`/`AGENTS.md`。未來簡化這些 skill 時 **NEVER 把特定環境的工具名硬編進 skill 本體**（會破壞可攜性，讓這包無法給下一個團隊用）。

各 skill 完整的 TRIGGER / DO NOT TRIGGER 條件見其 `SKILL.md` 的 frontmatter description。
