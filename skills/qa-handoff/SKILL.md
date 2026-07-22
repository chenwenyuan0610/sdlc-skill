---
name: qa-handoff
description: TRIGGER when 開發實作完成，要進入測試（對應原 SDLC 步驟25-28：單元測試/整合測試/驗收測試/Bug修正回歸測試）。DO NOT TRIGGER when 開發還沒完成（→ implementation-handoff）。
---

# QA Handoff — SDLC Phase 6 測試

依 `../sdlc-orchestrator/SDLC_主流程版_IAO.md` 步驟 25-28。**Lead 依範圍直接執行或派工，範圍達門檻 MUST 派工**（完整分級表 + 審查角度定義 → `../sdlc-orchestrator/references/agent-teams.md`）。

**綁定層優先**：使用環境的 CLAUDE.md / AGENTS.md 若對本 phase 定義了工具綁定（例如「Phase 6 → 走某某既有審查流程」的綁定表），一律照綁定走；本 skill 的內建做法只是「無綁定專案」的 fallback。

## 觸發條件
- 所有票的開發已完成（來自 implementation-handoff）
- 不適用：開發還沒做完 → 先回 implementation-handoff

## 完成條件（Phase Exit Criteria）
4 個步驟的 Output 都產出，且通過本階段專屬檢查（完整條目 → `references/phase-exit-criteria.md`）：
1. 單元測試結果
2. 整合測試結果
3. 驗收結果
4. 修正後穩定的版本

## 持久化
測試結果 MUST 記進 `docs/handoff-log.md`（各層級測試通過率、發現的 bug 清單、**每個 bug 的修正狀態與回歸重測結果**——bug 沒有「已修正 + 回歸重測通過」的記錄不算結案），**用固定標頭 `## Phase 6 — Testing` 分節**。分節的第一行 MUST 是狀態行 `狀態：進行中` 或 `狀態：完成`——**標頭存在不等於做完**，沒有這一行的話下一個接手的人／agent 會誤判本階段已結束而跳過（原因同 `implementation-handoff` 的「## Phase 5」標頭——讓下一個接手的人/agent 單靠檢查檔案就能判斷目前在哪個 phase）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。

## 流程

### 步驟 25：單元測試
- Action：針對單一函式/模組/元件寫測試並執行
- 誰做：範圍大（多模組/新框架）→ MUST 派 `sdlc-implementer` agent（角色定義在 Entry Protocol 的 `<agents-root>/sdlc-implementer.md`）撰寫測試——**MUST 是與實作者不同的 agent 實例**，且派工 prompt 不要附上實作者的思路說明，只給需求規格與驗收標準（避免同一視角自己測自己）；範圍小 → Lead-direct。測試寫完後派 `sdlc-reviewer`（唯讀）覆核測試本身是否測到重點
- Output：單元測試結果

### 步驟 26：整合測試
- Action：測模組間、前後端互動
- 誰做：同上判斷標準
- Output：整合測試結果

### 步驟 27：功能/驗收測試
- Action：對照需求規格（`requirement-scoping` 產出）逐條驗收
- 誰做：MUST 至少一個獨立角度覆核，不是實作者自己勾自己的驗收項；範圍大或涉及安全/共用資料 → 加派 `sdlc-verifier`（角色定義在 Entry Protocol 的 `<agents-root>/sdlc-verifier.md`，target=security 或 evidence，依風險挑選）
- Output：驗收結果

### 步驟 28：Bug 修正與回歸測試
- Action：修 bug、重測確認沒弄壞其他功能
- 誰做：修正動作 MUST 由能寫檔的角色執行——範圍大 → 派 `sdlc-implementer`（角色定義在 Entry Protocol 的 `<agents-root>/sdlc-implementer.md`）；範圍小 → Lead-direct。修完後由 `sdlc-reviewer` 或 `sdlc-verifier`（皆唯讀）覆核，**唯讀角色不負責修改，只負責判定**
- Output：修正後穩定的版本

## 停止條件
- 品質門禁（型別檢查/lint/build）沒過就想進測試 → 停下來，先修到 0 issues
- 測試中發現前面階段（`requirement-scoping`/`system-design`/`implementation-handoff`）的產出有問題 → 明確告知使用者要回哪個 phase 重新確認，不要在已知有問題的情況下把測試做完當作沒事

## 下一步
驗收結果通過 → 提示使用者可以接著用 `release-handoff` 確認部署前置條件。**不自動呼叫**，只是提醒。
