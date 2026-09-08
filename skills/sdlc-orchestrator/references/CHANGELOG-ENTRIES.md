# SDLC Skill 包 — 異動記錄（逐筆詳細記錄）

> 規則說明見 `../CHANGELOG.md`；本檔只放實際記錄，累加、不覆蓋歷史。

## 異動摘要

| 票號 | 日期 | 類別 | 項目 |
|---|---|---|---|
| SKC-20260818-01 | 2026-08-18 | 規則調整（新增） | 新增 `test-case-coverage.md`，要求測試描述/測試案例 MUST 涵蓋正向+反向情境，綠地專案 MUST 額外涵蓋紅軍測試；`dev-setup`/`system-design`/`change-request`/`qa-handoff` 四份 SKILL.md 加上指向該規則的條款 |
| SKC-20260818-02 | 2026-08-18 | 規則調整（新增） | 新增 `phase-transition-reminders.md`，要求「下一步」提醒 MUST 選項化呈現、未回應時 MUST 重新提出、每輪完工都要重新觸發；`implementation-handoff`/`qa-handoff` 兩份 SKILL.md 加上指向該規則的條款 |
| SKC-20260818-03 | 2026-08-18 | 規則調整（修訂） | `traceability.md` 規則二新增「change-request → 需要新設計決策 → system-design」演進支線的 REQ-nn 表放置規則（比照既有 change-specs 條款）；`system-design/SKILL.md` 完成條件表加第四項 REQ-nn 表、測試描述段落加上每條 MUST 掛 `[REQ-nn]` 的要求 |

---

## SKC-20260818-01

- 時間戳：2026-08-18
- 類別：規則調整（新增）
- 項目：新增 `references/test-case-coverage.md`，並在 `dev-setup`、`system-design`、`change-request`、`qa-handoff` 四份 `SKILL.md` 加上指向該規則的條款
- 狀態：已落地
- 觸發原因：cloud-oa-system 專案 ISSUE-5（框架缺陷登記簿 `FD-02`，使用者 Jesse Meng 於對話中標記 `accepted` 並提出具體規則內容）——`implementation-handoff` 完工三關全過、300+ 單元/整合測試全綠、Lead 執行的 end-to-end 驗證也全部通過，但使用者手動測試仍發現至少 6 項真實缺陷。根本原因：測試描述與測試案例只涵蓋「照規格操作」的正向路徑，沒有系統性要求反向/誤用情境，也沒有綠地專案的紅軍測試要求。

### 異動內容

**新增檔案** `sdlc-orchestrator/references/test-case-coverage.md`：定義三條規則——(1) 測試描述/測試案例 MUST 同時包含正向與反向情境，並列出最低涵蓋類別表（邊界數量／重複衝突輸入／錯誤修正路徑／資料一致性）；(2) 綠地專案（`dev-setup` 觸發）MUST 額外涵蓋紅軍測試（繞過防呆／偽造竄改信號／偵測與通報）；(3) 每個功能的測試 MUST 同時驗證前端提示、後端阻擋、修正路徑三層。

**`dev-setup/SKILL.md`**「附加產出：測試描述」段，原文：
```
- Action：對任務清單裡每個項目，用白話文寫「這個功能應該怎麼運作」...
```
改為在該段句尾加上：
```
**MUST 同時涵蓋正向與反向情境（含綠地專案的紅軍測試），規則與最低涵蓋類別 → `../sdlc-orchestrator/references/test-case-coverage.md`**——只寫正向案例視為本項未完成
```
Output 一行同步加註「正向+反向情境皆須涵蓋」。

**`system-design/SKILL.md`**「下一步」段「演進支線 MUST 一併產出測試描述」那句，句尾加上同樣的指向條款（正向+反向，不含紅軍測試字樣，因該支線是演進模式）。

**`change-request/SKILL.md`** 步驟 2 表格「在既有範圍內」那列，句尾加上指向條款，並註明 Tier 0-1 的一句話測試描述也要優先挑反向情境寫（若該次異動本身是在補防呆邏輯）。

**`qa-handoff/SKILL.md`** 步驟 25（單元測試）Action 加一句：測試描述若只涵蓋正向案例，MUST 先回補反向案例再往下寫測試，不得照單全收。步驟 27（驗收測試）新增一條：反向案例與紅軍測試 MUST 依該規則檔逐類確認涵蓋，且 MUST 驗證三層（前端提示/後端阻擋/修正路徑）；「誰做」一併新增：紅軍測試案例（適用時）MUST 加派 `sdlc-verifier`（target=security）覆核。

**`CHANGELOG.md`** 開頭「範圍」段同步更新：references 從 8 份改為 9 份（加入 `test-case-coverage.md`），總數從 26 份改為 27 份。

### 證據

- 新檔案：`sdlc-orchestrator/references/test-case-coverage.md`（本次建立，內容見上）
- `framework-defects.md` 登記簿 `FD-02` 列，證據欄記錄了具體觸發的 6 項缺陷（少於2份檔案未擋下、重複檔案未擋下、無法移除已選檔案、Show Result 顯示 issuer OID、列表顏色被簡化、responseCode 編輯頁 issuer 應下拉選單卻是自由輸入）
- 四份 `SKILL.md` 的實際 diff：可用 `grep -n "test-case-coverage" dev-setup/SKILL.md system-design/SKILL.md change-request/SKILL.md qa-handoff/SKILL.md` 核對四處引用皆已落地

### 已知待辦（若有）

- `framework-defects.md` 的 `FD-02` 列，`status` 欄按規則不能由修正者（Claude）自己標 `fixed`，需使用者或另一角色覆核後標記；本次先標記為修正完成、等待覆核。
- `~/.claude/settings.json` 尚未設定攔截 skill 規則檔編輯的 PreToolUse hook（`CHANGELOG.md`「首次使用檢查」段提到的機制），已告知使用者，使用者尚未決定是否要加。

## SKC-20260818-02

- 時間戳：2026-08-18
- 類別：規則調整（新增）
- 項目：新增 `references/phase-transition-reminders.md`，並在 `implementation-handoff`、`qa-handoff` 兩份 `SKILL.md` 加上指向該規則的條款
- 狀態：已落地
- 觸發原因：cloud-oa-system 專案 ISSUE-5（框架缺陷登記簿 `FD-03`，使用者 Jesse Meng 於對話中標記 `accepted`）——`implementation-handoff` 完工後「下一步」提醒只寫進完工總結的一段文字，不是獨立是非題；使用者沒有特別回應，後續兩輪 bug 修復都沒有重新提出，直到使用者自己主動問「為什麼不執行 qa-handoff」才發現 Phase 6 從頭到尾沒有真的被觸發過。根因：「下一步」規則只要求「提醒使用者」，沒有規定提醒要用什麼機制呈現、沒人回應時要不要重新提出。

### 異動內容

**新增檔案** `sdlc-orchestrator/references/phase-transition-reminders.md`：定義三條規則——(1) 明講「不是可選項」的下一步提醒 MUST 用選項化提問呈現，不能只是文字提醒；(2) 沒有得到明確回應前 MUST 在下一輪回覆重新提出，不得被後續新工作蓋過；(3) 同一工單號底下每一輪新的完工（含後續 bug 修復輪）都要重新觸發，不是只問第一次。

**`implementation-handoff/SKILL.md`**「下一步」段，原文：
```
所有票開發完成 → **MUST 接 `qa-handoff`（Phase 6）**。**不自動呼叫**，只是提醒使用者——但要明講這不是可選項。
```
句尾加上：
```
**提醒的呈現與重複觸發規則 → `../sdlc-orchestrator/references/phase-transition-reminders.md`**：MUST 用明確選項提問呈現，不能只寫進完工總結的一段文字；沒有得到明確回應前 MUST 在下一輪回覆重新提出；每一輪新的完工（含後續 bug 修復輪）都要重新觸發，不是只問第一次。
```

**`qa-handoff/SKILL.md`**「下一步」段同樣句尾加上指向條款（省略「每一輪完工重新觸發」那句，因 Phase 6→7 通常只發生一次）。

**`CHANGELOG.md`** 開頭「範圍」段同步更新：references 從 9 份改為 10 份（加入 `phase-transition-reminders.md`），總數從 27 份改為 28 份。

### 證據

- 新檔案：`sdlc-orchestrator/references/phase-transition-reminders.md`（本次建立，內容見上）
- `framework-defects.md` 登記簿 `FD-03` 列，證據欄記錄了具體觸發脈絡
- 兩份 `SKILL.md` 的實際 diff：可用 `grep -n "phase-transition-reminders" implementation-handoff/SKILL.md qa-handoff/SKILL.md` 核對兩處引用皆已落地

### 已知待辦（若有）

- `framework-defects.md` 的 `FD-03` 列，`status` 欄同樣需要非修正者覆核後才能標 `fixed`。
- 本檔範圍刻意只涵蓋 `implementation-handoff`/`qa-handoff` 兩個轉換點，其餘 7 個 phase skill 的「下一步」段是否也有同樣問題，尚未逐一檢查，留待之後實際遇到再補（見 `phase-transition-reminders.md`「落在哪個 skill」段的說明）。

## SKC-20260818-03

- 時間戳：2026-08-18
- 類別：規則調整（修訂）
- 項目：`traceability.md` 規則二新增演進支線（`change-request → 需要新設計決策 → system-design`）的 REQ-nn 表放置規則；`system-design/SKILL.md` 完成條件表與測試描述段落同步補條款
- 狀態：已落地（規則本身＋ISSUE-5 回頭補表皆完成，見下方「已知待辦」更新）
- 觸發原因：cloud-oa-system 專案 ISSUE-5（框架缺陷登記簿 `FD-01`，使用者 Jesse Meng 於對話中標記 `accepted`，並指定範圍：先只改 skill 規則，暫不回頭補 ISSUE-5 自己的 REQ-nn 表）——ISSUE-5 走完整個 system-design 演進支線，全程沒有 REQ-nn 表，`docs/5-merge-html/handoff-log.md` 的驗收只能拿 `design.md` 的 11 條白話測試描述當替代追溯單位，無法用 `[REQ-nn]` grep 全專案反查對帳。

### 異動內容

**`traceability.md`** 規則二，原文只有一句涵蓋 `change-request`「在既有範圍內」那條路（`docs/change-specs/<變更名>.md`）。新增一段，句型與既有條款一致：
```
**演進模式從 `change-request` 分診為「需要新設計決策」、轉去 `system-design` 的支線，同樣沒有 `requirements-spec.md`**（這條支線也不經過 `requirement-scoping`）→ 該次變更的 REQ 表放 **`system-design` 產出的設計文件索引檔第一段**：單一檔案彙整時是 `docs/design.md`（或依變更分資料夾時的 `docs/<變更資料夾>/design.md`）；依面向拆成多檔時，放在扮演一頁式索引角色的那份主檔第一段（`system-design/SKILL.md`「持久化」段落定義了哪一份是索引）。**它就是該次變更的唯一真相源**，規則完全相同——設計文件裡的 `architecture.md`/`api-spec.md`/`db-schema.md`/`logic-flow.md` 等其他檔案只能引用 `[REQ-nn]`，不得另開一張需求表。
```

**`system-design/SKILL.md`** 完成條件表「演進」列，原文「只要三項」改成「只要四項」，新增第④項 REQ-nn 表，句尾附 `../sdlc-orchestrator/references/traceability.md` 規則二的指標。

**`system-design/SKILL.md`**「⚠ 演進支線 MUST 一併產出「測試描述」」那段，句尾加上：
```
每條測試描述 MUST 掛上它驗證的 [REQ-nn]（REQ-nn 表放哪 → ../sdlc-orchestrator/references/traceability.md 規則二），不是自由文字散寫；沒有 REQ-nn 可掛代表該條需求本身還沒編號，先回頭補進 REQ-nn 表再繼續寫測試描述。
```

### 證據

- `traceability.md` 規則二實際 diff：可用 `grep -n "system-design 的支線" traceability.md` 核對
- `system-design/SKILL.md` 兩處 diff：可用 `grep -n "只要四項\|MUST 掛上它驗證的" system-design/SKILL.md` 核對

### 已知待辦（若有）

- `framework-defects.md` 的 `FD-01` 列，`status` 欄同樣需要非修正者覆核後才能標 `fixed`。
- cloud-oa-system 專案 ISSUE-5 本身的 REQ-nn 表已於 2026-08-18 回頭補齊（使用者指示「照著skill回頭補表」後執行）：①`docs/5-merge-html/design.md` 新增 REQ-01~REQ-11 表（REQ-11 標記已廢止，編號保留不重用）、11 條原始測試描述＋後續三輪補充的測試描述皆掛上 `[REQ-nn]` ②`architecture.md`/`api-spec.md`/`db-schema.md`/`logic-flow.md` 的section標題補上對應 `[REQ-nn]` ③`handoff-log.md` 的引用已改成 `[REQ-nn]` 格式。**已知例外**：`docs/uat-ISSUE-5.md` 尚未補 `[REQ-nn]` 標籤，使用者已接受此為次要缺口，留待之後有空再補。
