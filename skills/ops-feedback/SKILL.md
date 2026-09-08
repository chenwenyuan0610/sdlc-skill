---
name: ops-feedback
description: TRIGGER when 系統已上線，要建立監控、收集回饋、規劃下一輪迭代（對應原 SDLC 步驟33-35：監控日誌/回饋收集/修正優化）。DO NOT TRIGGER when 還沒上線（→ release-handoff）。
---

> ⚠️ 修改本檔案前後，MUST 依 `../sdlc-orchestrator/CHANGELOG.md` 的規則記錄異動。

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
回饋/問題清單 MUST 寫成 `docs/feedback-log.md`（累加記錄，不覆蓋歷史；**每條回饋帶編號 `FB-nn` 與狀態欄位**，格式照 `../sdlc-orchestrator/references/ticket-spec.md`；步驟35 處理完 MUST 回寫狀態——沒回寫就無法追蹤哪條已結案）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。監控儀表板/日誌若為外部系統，**把連結記進 `docs/feedback-log.md` 的固定標頭 `## Monitoring` 分節**，不用複製內容。

**⚠ 產出物長度治理**：**單一 `docs/` 產出物 MUST ≤200 行**。超過 MUST 按段落語意拆檔，且**主檔 MUST 保留一頁式索引**（哪一段在哪個檔）。**拆檔 MUST NOT 改變既有段落編號**，否則上下游文件的交叉引用會全斷。**天生會長大的段落一開始就獨立成檔**：原始需求清單、維度覆蓋表／提問記錄／自決與猜測（檔名固定 `docs/<phase>-evidence.md`）、風險清單。
⚠ **累加型紀錄例外**（`change-log.md`／`handoff-log.md`／`feedback-log.md`）：流水帳**沒有「段落語意」可拆、也沒有段落編號可保留**，而本 phase 的 `feedback-log.md` 明文「累加記錄，不覆蓋歷史」，兩個 MUST 會相撞。改用**時間分卷**——超過 200 行時把舊內容整段移到 `<原檔名>-<年份或期別>.md`，主檔保留最近期內容 ＋ 一行分卷索引。**NEVER 為了守行數而刪除歷史。**

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
- Output：改善後的系統 + `docs/feedback-log.md` 對應條目的狀態回寫，**狀態值一律用 `ticket-spec.md` 的狀態機，不得自創**：

| 這次怎麼處理 | 狀態 | 備註欄要寫什麼 |
|---|---|---|
| 自己修掉了 | **先寫 `in-progress`**，由非修正者覆核後才由**覆核者**改成 `fixed` | 改了什麼（照 `ticket-spec.md` 對 `fixed` 的要求）|
| 分流給 `change-request`／`product-discovery` 接手 | **仍是 `in-progress`** | `routed-to-<去處>` ＋ 承接的單號 |
| 決定不做 | `rejected`——**MUST 由人拍板**，執行者不得自行標 | 為什麼不做 |

⚠ **分流不是結案。** 把回饋轉出去之後，事情還在別的地方跑——標成終態會讓這條回饋從追蹤清單消失，而承接方那邊掛掉時沒有人會發現。**只有真的修好、或明確決定不做，才是終態。**
⚠ **終態不得由自己標**（`ticket-spec.md` 硬規則 5 結案權與執行權分離、硬規則 2 `rejected` 必須由人決定）：Lead-direct 修完後**留 `in-progress`**，由**非修正者**確認才改 `fixed`；`rejected` MUST 由人拍板，執行者不得自行標。

## 停止條件
- 回饋內容混雜多個不相關問題 → 先分類，一次只處理一條，避免 scope creep
- 發現上線的問題其實源自更早的階段（例如需求規格本身就有誤）→ 明確告知使用者要回哪個 phase 重新確認，不要只在維運層面打補丁；確認要回頭後依 `../sdlc-orchestrator/sdlc-entry.md`「回歸」段回寫狀態（含連鎖回開判斷），不能只在對話裡講一講
- 卡住的原因是**流程規則本身**（規則寫死了不適用本專案的做法／兩條規則矛盾／判準模糊到判不出來／缺一步接不上）→ **不要就地改規則、不要停工**：append 一列到**框架缺陷登記簿**（status=`proposed`，**證據欄必填**）。登記簿位置 → `../sdlc-orchestrator/references/framework-defects.md`；**該檔可能是登記簿本身，也可能是指向使用環境實際登記簿的指標檔，打開照它說的走**，然後用最接近的合理解讀把工作做完

## 下一步
發現需要新一輪需求發想（全新方向）→ 接回 `product-discovery`，形成迴圈；發現是既有規格內的變更 → 接 `change-request` 分診，不進 phase 迴圈。**不自動呼叫**，只是提醒；`product-discovery` 這條是 8 個 phase 唯一的「循環」邊，其餘 7 個 phase 都是線性單向，`change-request` 是額外的旁路，不算在 8 phase 迴圈內。
