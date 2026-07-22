---
name: release-handoff
description: TRIGGER when 測試通過，要確認可以部署（對應原 SDLC 步驟29-32：部署前檢查/staging/production/煙霧測試）。DO NOT TRIGGER when 測試還沒過（→ qa-handoff）。部署動作一律人工手動觸發，Claude 不自動化。
---

# Release Handoff — SDLC Phase 7 部署

依 `../sdlc-orchestrator/SDLC_主流程版_IAO.md` 步驟 29-32。**Lead 只負責檢查清單與唯讀驗證，實際部署動作 MUST 由使用者手動觸發**（不可越過的安全紅線）。

**綁定層優先**：使用環境的 CLAUDE.md / AGENTS.md 若對本 phase 定義了工具綁定（例如「Phase 7 → 走某某既有部署稽核流程」的綁定表），一律照綁定走；本 skill 的內建做法只是「無綁定專案」的 fallback。

## 觸發條件
- 驗收結果已通過（來自 qa-handoff）
- 不適用：測試還沒過 → 先回 qa-handoff

## 完成條件（Phase Exit Criteria）
4 個步驟的 Output 都產出，且通過本階段專屬檢查（完整條目 → `references/phase-exit-criteria.md`）：
1. 部署檢查清單（通過）
2. staging 運行
3. production 上線
4. 煙霧測試結果（綠燈/退版）

## 持久化
交接結果 MUST 記進 `docs/handoff-log.md`（部署檢查結果、目標環境、煙霧測試結果），**用固定標頭 `## Phase 7 — Release` 分節**。分節的第一行 MUST 是狀態行 `狀態：進行中` 或 `狀態：完成`——**標頭存在不等於做完**，沒有這一行的話下一個接手的人／agent 會誤判本階段已結束而跳過（原因同 `implementation-handoff` 的「## Phase 5」標頭）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。

## 流程

### 步驟 29：部署前檢查
- Action：檢查環境、設定、資料就緒（環境變數/憑證/資料庫 migration 已跑）
- 誰做：Lead 列出檢查清單，逐項確認
- Output：部署檢查清單（通過）

### 步驟 30：部署到測試環境（staging）
- Action：部署到 staging
- 誰做：Lead 列出部署步驟，**使用者手動執行**，Lead 不自動觸發
- Output：staging 運行

### 步驟 31：部署到正式環境（production）
- Action：部署到 production
- 誰做：同上，**使用者手動執行**，Lead 不自動觸發
- Output：production 上線

### 步驟 32：上線後煙霧測試
- Action：快速測核心功能是否活著
- 誰做：Lead 可協助執行唯讀檢查（健康檢查端點、關鍵頁面回應等），不涉及任何寫入/部署動作
- Output：煙霧測試結果（綠燈/退版）

## 停止條件
- 使用者要求 Lead 直接觸發部署 → 拒絕，這是人工手動觸發的範圍，Lead 只能協助檢查
- 部署前檢查發現前面階段（`qa-handoff`）的產出有問題 → 明確告知使用者要回 `qa-handoff` 重新確認，不要在已知有問題的情況下放行部署

## 下一步
煙霧測試綠燈 → 提示使用者可以接著用 `ops-feedback` 開始維運監控。**不自動呼叫**，只是提醒。
