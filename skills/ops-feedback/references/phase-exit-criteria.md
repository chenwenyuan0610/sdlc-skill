# Ops Feedback — Phase Exit Criteria 詳細清單

每個步驟的具體檢查項，全部確認才算 Phase 8 完成（本階段完成後，若有新需求則接回 Phase 1，形成迴圈）。

## 接手時的模式補查
- 已依 `../../sdlc-orchestrator/references/tailoring.md`「宣告檔建立與維運交接時機」檢查 `docs/sdlc-mode.md`；缺漏已補建／補正，模式、理由、決定者完整，`docs/feedback-log.md` 有連結與決定依據。
- 此檢查在分流下一筆維護工作前完成，已有合法宣告未被自行覆寫。

## 步驟 33 系統監控與日誌
- 監控涵蓋新功能的關鍵路徑，不是只沿用舊功能的既有監控
- 監控工具依專案自己的選擇，沒有另建一套跟既有監控不一致的機制
- 監控儀表板/日誌的連結已記進 `docs/feedback-log.md`「## Monitoring」分節（外部系統記連結即可）

## 步驟 34 收集回饋與問題
- 回饋/問題清單已分類，不是混雜多個不相關問題的流水帳
- 每條回饋標明來源（使用者回報/監控告警/日誌異常）

## 步驟 35 修正與優化
- 每條問題已明確決定路徑：小修正 → Lead-direct 修正；影響既有規格但非全新方向 → `change-request`；全新方向 → 回 `product-discovery`
- 沒有「先放著」的問題沒被分類就結案
- 每條處理結果已回寫 `docs/feedback-log.md` 對應條目的狀態欄，**值一律用 `../../sdlc-orchestrator/references/ticket-spec.md` 的狀態機**：自己修掉＝**先留 `in-progress`**，由非修正者覆核後才由覆核者改 `fixed`（註明改了什麼）／分流出去＝**仍是 `in-progress`** ＋備註 `routed-to-<去處>` 與承接單號／決定不做＝`rejected`（寫為什麼）。⚠ **分流不是結案**——標成終態會讓這條回饋從追蹤清單消失，承接方那邊掛掉時沒人會發現。**`resolved`／`routed-to-` 不是合法狀態值**，本檔先前用它們，已改。
- **`fixed` 與 `rejected` 不得由修正者自己標**（`ticket-spec.md` 硬規則 5：結案權與執行權分離；硬規則 2：`rejected` 必須由人決定）。Lead-direct 修完後留 `in-progress`，由**非修正者**確認才改 `fixed`

## 與既有機制的關係
本階段是新內容，不涉及分工問題。
