---
name: ops-feedback
description: TRIGGER when 系統已上線，要建立監控、收集回饋、規劃下一輪迭代（對應原 SDLC 步驟33-35：監控日誌/回饋收集/修正優化）。DO NOT TRIGGER when 還沒上線（→ release-handoff）。
---

# Ops Feedback — SDLC Phase 8 維運

依 `../sdlc-orchestrator/SDLC_主流程版_IAO.md` 步驟 33-35。**Lead 對話彙整為主，發現新需求時接回 `product-discovery` 形成迴圈。**

**綁定層優先**：使用環境的 CLAUDE.md / AGENTS.md 若對本 phase 定義了工具綁定（例如「Phase 8 → 用某某既有監控系統」的綁定表），一律照綁定走；本 skill 的內建做法只是「無綁定專案」的 fallback。

## 觸發條件
- 系統已上線（來自 release-handoff）
- 不適用：還沒上線 → 先回 release-handoff

## 完成條件（Phase Exit Criteria）
3 個步驟的 Output 都產出，且通過本階段專屬檢查（完整條目 → `references/phase-exit-criteria.md`）：
1. 監控儀表板 / 日誌
2. 回饋 / 問題清單
3. 改善後的系統（若有修正）

## 持久化
回饋/問題清單 MUST 寫成 `docs/feedback-log.md`（累加記錄，不覆蓋歷史；**每條回饋帶狀態欄位：`open` / `routed-to-<去處>` / `resolved`**，步驟35 處理完 MUST 回寫狀態——沒回寫就無法追蹤哪條已結案）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。監控儀表板/日誌若為外部系統，**把連結記進 `docs/feedback-log.md` 的固定標頭 `## Monitoring` 分節**，不用複製內容。

## 流程

### 步驟 33：系統監控與日誌
- Action：建立監控、收集日誌
- 誰做：Lead 協助確認既有監控是否涵蓋新功能（監控工具依專案自己的選擇）
- Output：監控儀表板 / 日誌

### 步驟 34：收集回饋與問題
- Action：蒐集使用者行為與回報，彙整
- 誰做：Lead 對話彙整
- Output：回饋 / 問題清單

### 步驟 35：修正與優化
- Action：修正、優化；有新需求時視性質分流
- 誰做：不影響既有規格/設計的小修正 → Lead-direct 修正（依步驟21-24同樣的 Lead-direct/派工判斷標準）；影響既有規格/設計但不是全新方向 → 用 `change-request` 分診；完全是全新方向 → 回到 `product-discovery` 重跑整個流程。**分流結果向使用者確認時 MUST 選項化**（比照 `change-request`：三條路做成可勾選項、你判斷的放第一個標「建議」附一句理由；自由補充永遠允許）
- Output：改善後的系統 + `docs/feedback-log.md` 對應條目的狀態回寫（`resolved` 或 `routed-to-<去處>`）

## 停止條件
- 回饋內容混雜多個不相關問題 → 先分類，一次只處理一條，避免 scope creep
- 發現上線的問題其實源自更早的階段（例如需求規格本身就有誤）→ 明確告知使用者要回哪個 phase 重新確認，不要只在維運層面打補丁

## 下一步
發現需要新一輪需求發想（全新方向）→ 接回 `product-discovery`，形成迴圈；發現是既有規格內的變更 → 接 `change-request` 分診，不進 phase 迴圈。**不自動呼叫**，只是提醒；`product-discovery` 這條是 8 個 phase 唯一的「循環」邊，其餘 7 個 phase 都是線性單向，`change-request` 是額外的旁路，不算在 8 phase 迴圈內。
