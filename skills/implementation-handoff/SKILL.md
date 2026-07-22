---
name: implementation-handoff
description: TRIGGER when 開發前準備已完成（設計文件/骨架/排程都就緒），要開始實際開發（對應原 SDLC 步驟21-24：資料庫建置/後端API開發/前端元件開發/頁面組裝）。DO NOT TRIGGER when 準備工作還沒做完（→ dev-setup）。
---

# Implementation Handoff — SDLC Phase 5 開發實作

依 `../sdlc-orchestrator/SDLC_主流程版_IAO.md` 步驟 21-24。**Lead 依票直接執行或派工，範圍達門檻 MUST 派工**（判斷標準見步驟內「誰做」；分級表 / 模型選擇 / 派工 prompt 附帶 dev skill 規則 → `../sdlc-orchestrator/references/agent-teams.md`）。

**綁定層優先**：使用環境的 CLAUDE.md / AGENTS.md 若對本 phase 定義了工具綁定（例如「Phase 5 → 走某某既有開發流程」的綁定表），一律照綁定走；本 skill 的內建做法只是「無綁定專案」的 fallback。

## 觸發條件
- 開發排程已定（來自 dev-setup），要開始實際寫程式
- 不適用：還沒排開發前準備 → 先回 dev-setup

## 完成條件（Phase Exit Criteria）
4 個步驟的 Output 都產出，且通過本階段專屬檢查（完整條目 → `references/phase-exit-criteria.md`）：
1. 可用的資料庫（若專案不涉及持久化儲存 → 標 N/A 並註明理由）
2. 可運行的後端 API（若專案不提供對外介面 → 標 N/A 並註明理由）
3. 完成的前端元件（若專案無使用者介面 → 標 N/A 並註明理由）
4. 可用的前端頁面（同上）

**標 N/A 的項目不算未完成。** 四項中至少一項有實質產出即可進 Phase 6——資料分析、CLI 工具、函式庫、韌體等非 web 專案，用該領域的等價產出（分析腳本與輸出、可執行檔、可安裝套件、可燒錄映像）替換對應項目並註明。

## 持久化
每張票完工狀態 MUST 記進 `docs/handoff-log.md`（票號、完成日期、品質門禁結果），**用固定標頭 `## Phase 5 — Implementation` 分節**。分節的第一行 MUST 是狀態行 `狀態：進行中` 或 `狀態：完成`——**標頭存在不等於做完**，沒有這一行的話下一個接手的人／agent 會誤判本階段已結束而跳過（`handoff-log.md` 由 Phase 5-7 共用，固定標頭讓下一個接手的人/agent 能單靠檢查這個檔案判斷目前在哪個 phase，不用回想對話）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。

## 流程

### 步驟 21：資料庫建置
- Action：依 DB schema 建立資料庫、資料表
- 誰做：單一票 ≤20 行/單檔/無新依賴 → Lead-direct；範圍較大（多檔/新模組）→ MUST 派 `sdlc-implementer` agent（角色定義在 Entry Protocol 的 `<agents-root>/sdlc-implementer.md`），多張範圍獨立的票平行派，不要序列一張張自己做
- Output：可用的資料庫

### 步驟 22：後端 API 開發
- Action：依 API 規格實作後端邏輯與端點
- 誰做：同上判斷標準
- Output：可運行的後端 API

### 步驟 23：前端元件開發
- Action：依元件清單實作元件（可跨頁重用，先用假資料）
- 誰做：同上判斷標準
- Output：完成的前端元件

### 步驟 24：前端頁面組裝與串接
- Action：把元件組裝成頁面，接上步驟 22 的真實 API
- 誰做：同上判斷標準
- Output：可用的前端頁面

**品質門禁**：每張票完工 MUST 有明確的品質門禁（該語言/框架慣用的型別檢查/lint/測試/build，具體指令依專案自己的工具鏈），0 issues 才算過。

## 停止條件
- 前置條件沒確認就想開始開發 → 停下來，指出缺哪個前置條件
- 開發過程中發現前面階段（`system-design`/`dev-setup`）的產出有問題 → 明確告知使用者要回哪個 phase 重新確認，不要在已知有問題的情況下繼續往下做

## 下一步
所有票開發完成 → 提示使用者可以接著用 `qa-handoff` 確認測試前置條件。**不自動呼叫**，只是提醒。
