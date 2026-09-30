---
name: qa-handoff
description: TRIGGER when 開發實作完成，要進入測試（對應原 SDLC 步驟25-28：單元測試/整合測試/驗收測試/Bug修正回歸測試）。DO NOT TRIGGER when 開發還沒完成（→ implementation-handoff）。
---

> ⚠️ 修改本檔案前後，MUST 依 `../sdlc-orchestrator/CHANGELOG.md` 的規則記錄異動。

# QA Handoff — SDLC Phase 6 測試

依 `../sdlc-orchestrator/SDLC_主流程版_IAO.md` 步驟 25-28。**Lead 依範圍直接執行或派工，範圍達門檻 MUST 派工**（完整分級表 + 審查角度定義 → `../sdlc-orchestrator/references/agent-teams.md`）。

**測試撰寫責任（步驟 25-27 一體適用）**：驗收相關測試（單元測試以外，涉及驗收/spec 對齊的測試）MUST 由本 skill 獨立撰寫，`implementation-handoff` 的開發者不得自行撰寫或修改。撰寫依據是 `dev-setup` 產出的自然語言測試描述（草稿），但 MUST 對照 `requirements-spec.md` 原始需求規格書覆核，不能只信 `dev-setup` 的措辭直接照抄。⚠ **專案沒有 `requirements-spec.md` 時**（例如從 `change-request` 的「在既有範圍內」那條路進來，該路徑不產生正式需求規格，也不經過 `dev-setup`）→ **改以該路徑產出的輕量 spec ＋ 程式碼現況基線為覆核依據**，並在測試文件註明依據來源；**不得因為缺檔就跳過覆核**——避免 `dev-setup` 寫的時候用詞不小心貼近某種特定實作方式，這裡照抄等於沒有真的獨立驗證。開發者自己補測試容易不自覺照著自己寫的 code 邏輯走，變成「一定會過的測試」，這正是本規則要堵的漏洞。

**綁定層優先**：使用環境的 CLAUDE.md / AGENTS.md 若對本 phase 定義了工具綁定（例如「Phase 6 → 走某某既有審查流程」的綁定表），一律照綁定走；本 skill 的內建做法只是「無綁定專案」的 fallback。

## 觸發條件
- 所有票的開發已完成（來自 implementation-handoff）
- 不適用：開發還沒做完 → 先回 implementation-handoff

## 完成條件（Phase Exit Criteria）
4 個步驟的 Output 都產出，**並且下列七項完成條件全部通過**（完整條目 → `references/phase-exit-criteria.md`；第 5～7 項不是可選的附加檢查）：
1. 單元測試結果
2. 整合測試結果 + **可重複執行的整合測試腳本**
3. 驗收結果 + **UAT 操作文件**（讓使用者能自己照著操作驗一次）
4. 修正後穩定的版本
5. **UAT 操作文件已由非撰寫者完整照著跑過一次**，確認步驟、預期結果與成功／失敗判定跟得上；執行者與結果 MUST 記在 `docs/handoff-log.md` 的 `## Phase 6 — Testing` 分節，或該分節明確指向的 Phase 6 證據檔。
6. **程式碼安全審查已由非原作者完成**，記錄審查者與範圍；若本次變更確實不涉及安全面而標 N/A，仍 MUST 記錄具體理由、非原作者確認者與確認範圍，位置同上。第 5～7 項均須有可核對的證據，才可把 Phase 6 標成完成。
7. **測試有效性的改壞實驗已完成**：依 `../sdlc-orchestrator/references/test-case-coverage.md` 規則四，由獨立覆核者選題並實跑，留下正常通過、改壞後目標斷言失敗、還原後通過的證據；未做、阻塞或測試缺口未修正均不得收關。

⚠ **本 phase 不可裁剪**：實作與測試是流程裁剪的下限，**`## Phase 6` 分節永遠不得標 `狀態：不適用`**，不論專案宣告哪一種模式（裁剪規則 → `../sdlc-orchestrator/references/tailoring.md`）。

**測試結果只能標四種狀態**：`PASS`／`BLOCKED`／`NEEDS WORK`／`FAIL`（定義與防假綠燈三條 → `../sdlc-orchestrator/references/severity-format.md`）。**同一項目重跑 ≥2 次才綠 = NEEDS WORK 不是 PASS**；跑不動 = `BLOCKED` 不是 PASS；禁止自創「未要求／略過」這類豁免標記。

## 持久化
測試結果 MUST 記進 `docs/handoff-log.md`（各層級測試通過率、發現的 bug 清單、**每個 bug 的修正狀態與回歸重測結果**——bug 沒有「已修正 + 回歸重測通過」的記錄不算結案）。**每個 bug MUST 帶編號與證據欄，格式照 `../sdlc-orchestrator/references/ticket-spec.md`**（缺陷型 `BUG-nn`；證據欄空白不受理），**用固定標頭 `## Phase 6 — Testing` 分節**。分節的第一行 MUST 是狀態行 `狀態：進行中` 或 `狀態：完成`；Phase 6 不適用，這裡只接受這兩值——**標頭存在不等於做完**，沒有這一行的話下一個接手的人／agent 會誤判本階段已結束而跳過（原因同 `implementation-handoff` 的「## Phase 5」標頭——讓下一個接手的人/agent 單靠檢查檔案就能判斷目前在哪個 phase）；專案尚無 `docs/` 資料夾就直接建立，不用先問使用者。

**⚠ 產出物長度治理**：**單一 `docs/` 產出物 MUST ≤200 行**。超過 MUST 按段落語意拆檔，且**主檔 MUST 保留一頁式索引**（哪一段在哪個檔）。**拆檔 MUST NOT 改變既有段落編號**，否則上下游文件的交叉引用會全斷。**天生會長大的段落一開始就獨立成檔**：原始需求清單、維度覆蓋表／提問記錄／自決與猜測（檔名固定 `docs/<phase>-evidence.md`）、風險清單。
⚠ **累加型紀錄例外**（`change-log.md`／`handoff-log.md`／`feedback-log.md`）：超過 200 行時改用**時間分卷**，把舊詳細紀錄移到 `<原檔名>-<年份或期別>.md`，主檔保留最近期內容與分卷索引。**`handoff-log.md` 另 MUST 保留既有階段標頭、原狀態行與分卷連結**，完整規則與分卷後核對 → `../sdlc-orchestrator/sdlc-entry.md`「handoff-log 分卷時保留階段定位資訊」。**NEVER 為了守行數而刪除歷史。**

## 流程

**⚠ 既有專案沒有既有測試時，Phase 6 的工作是「補本次變更」不是「回溯補齊舊專案」**（演進模式常態，MUST 依此調整步驟 25-27）：

| 情況 | 這一關要做什麼 |
|---|---|
| **沒有可跑的測試框架** | **先把它建起來**——最小可跑即可（一個測試檔、一條能執行的指令），不必一次補齊整套。這是本 phase 的第一件事，不是前置條件；缺它就卡住等於整個既有專案永遠進不了測試關 |
| **要動的程式碼原本沒有測試覆蓋** | **針對這次異動的那段邏輯補測試**：①改完之後的新行為 ②那段邏輯原本就有、而這次不該被改掉的行為——後者是回歸保護。改完才補測試很正常，重點是**補完之後這段邏輯下次再被改時有東西接住** |

**⚠ 補測試的範圍 ＝ 這次異動的邏輯，不多不少。**

補測試會讀到大量既有程式碼，這是正常的——**但讀到不等於要改它，也不等於要替它補測試**。三件事 MUST NOT 做：

- **MUST NOT 改動原本沒有要改的邏輯**。包括「補測試時順手看到寫得不好的」「看起來可以一起優化的」「跟本次無關但很快就能修的」。要改另開一張票。
- **MUST NOT 為了讓測試好寫而重構既有程式碼**。測試難寫通常代表那段邏輯本身有問題，但那是另一件工作——這次的目標是「這段邏輯下次被改時有東西接住」，不是「把它改好」。
- **MUST NOT 把測試範圍擴大到整個模組或整個舊專案**。以「這次動到的那段邏輯」為界。

理由：一旦補測試的過程夾帶了本次沒有要做的改動，**回歸測試就變成「測我剛改的版本」**，失去它存在的意義——它應該證明的是「我沒有改壞原本會動的東西」。這與完工第 3 關「最小改動確認」是同一條原則的兩面。

⚠ **不得因為「這次有改動的程式碼本來就沒測試」而跳過本 phase。** 但遵守「既往不溯」：本 phase 只補本次異動及其直接受影響的行為，不要求替未修改、與本次無關的舊程式碼補測試。

### 步驟 25：單元測試
- Action：依 `dev-setup` 的測試描述、對照 `requirements-spec.md` 覆核後，針對單一函式/模組/元件獨立撰寫測試並執行。**測試描述若只涵蓋正向案例（違反 `../sdlc-orchestrator/references/test-case-coverage.md` 規則一），MUST 先回補反向案例再往下寫測試，不得照單全收直接動手**——這是本 phase「獨立撰寫」職責的一部分，不是 `dev-setup` 沒寫全就跟著漏
- 誰做：範圍大（多模組/新框架）→ MUST 派 `sdlc-implementer` agent（角色定義檔 `sdlc-implementer.md`，在你的角色檔目錄下）撰寫測試——**MUST 是與實作者不同的 agent 實例**，且派工 prompt 不要附上實作者的思路說明，只給需求規格與驗收標準（避免同一視角自己測自己）；範圍小 → Lead-direct。測試寫完後派 `sdlc-reviewer` 覆核測試本身是否測到重點；原專案唯讀，依規則四在隔離副本執行改壞實驗
- Output：單元測試結果

### 步驟 26：整合測試
- 涉及外部狀態設定時，MUST 依 `../sdlc-orchestrator/references/test-case-coverage.md` 規則五，從產品入口驗證實際環境狀態及失敗後行為；測試腳本不得代做待驗的產品切換。
- Action：依同一份測試描述，測模組間、前後端互動。**MUST 寫成可重複執行的腳本**（不是手動點過一遍就算），下次變更能直接重跑當回歸測試
- 誰做：同上判斷標準
- Output：整合測試結果 + 測試腳本（含怎麼跑的說明）

### 步驟 27：功能/驗收測試
- Action：對照需求規格（`requirement-scoping` 產出的 `requirements-spec.md`）逐條驗收。**MUST 逐條列出所有 `REQ-nn`，每條回答「哪個測試覆蓋它」；`REQ-nn` 有拆驗收標準子編號（`REQ-nn-AC1`/`AC2`……）的，MUST 逐條 AC 分別列出、分別回答，不能只在 REQ 這一層打勾**——沒有覆蓋的 MUST 寫理由（例：`REQ-09｜無自動化測試｜理由：純視覺調整，改以 UAT 步驟 3 人工確認`），**不得留空**；留空的表視同本關未完成。**再反向抽查一次**：這輪改動的檔案有沒有哪個不屬於任何 REQ（要嘛漏掛、要嘛夾帶了本票範圍外的改動）。規則與豁免條件 → `../sdlc-orchestrator/references/traceability.md`。**這項窮舉裡「REQ/AC有沒有被任何測試標籤引用到」的部分屬於機械性比對，MAY 寫成可重用的腳本先抓出零引用的候選清單加速——但「那個測試是否真的驗證到這條規則」「沒覆蓋的理由是否合理」仍需語意判斷，腳本只能縮小要覆核的範圍，不能取代這兩項判斷。判準與做法 → `../sdlc-orchestrator/references/tooling-reuse.md`**。**`system-design` 步驟16 標記為同一驗收批次的子項目（有依賴關係，如前端依賴後端），MUST 等批次內所有子項目都完工才能一起驗收，不能對批次裡其中一個子項目單獨宣告驗收通過**
- **反向案例與紅軍測試** MUST 依 `../sdlc-orchestrator/references/test-case-coverage.md` 逐類確認涵蓋（規則一不分綠地棕地；規則二紅軍測試限創世模式，見該檔判準），且 MUST 驗證三層（前端提示／後端阻擋／修正路徑）——**只驗證前端提示、沒驗證後端本身擋不擋得住，視為未完成**，因為前端驗證永遠可被繞過
- 誰做：MUST 至少一個獨立角度覆核，不是實作者自己勾自己的驗收項；範圍大或涉及安全/共用資料 → 加派 `sdlc-verifier`（角色定義檔 `sdlc-verifier.md`，在你的角色檔目錄下；target=security 或 evidence，依風險挑選）；**紅軍測試案例（適用時）MUST 加派 `sdlc-verifier`（target=security）覆核，不得只由撰寫測試的同一角色自行判定通過**
- Output：驗收結果 + **UAT 操作文件**——驗收通過後 MUST 產出一份使用者能自己照著跑的操作文件（前置條件／逐步操作／每步預期看到什麼／怎麼判定成功失敗），寫給不熟系統的人看，不是內部測試筆記。**檔名固定 `docs/uat-<批次或變更名>.md`**（例 `docs/uat-ISSUE-42.md`），並在 `docs/handoff-log.md` 的 `## Phase 6` 分節寫一行指過去。⚠ 沒有明文檔名的話，Phase 7／Phase 8 要引用時找不到——`handoff-log.md` 只放測試結果與 bug 清單，不放操作步驟

### 測試寫完後、驗收通過前：獨立覆核測試有效性

MUST 依 `../sdlc-orchestrator/references/test-case-coverage.md` 規則四完成改壞實驗。委派時提供需求／AC、待驗版本、測試指令與範圍；由未參與本次產品及測試修改的覆核者自行選題。測試缺口交測試作者修正，再由覆核者重驗；實驗證據由 Lead 彙整進 Phase 6 分節或其指向的證據檔。工具不足時交由另一個具備隔離執行能力的獨立角色，不能只讀程式碼就宣稱實跑通過。

**複審仍是新版本的完整證據關，不是 diff 確認。** 步驟 28 或任何 finding 修正若改到相關產品行為、測試、fixture／設定，先前受影響情境的改壞證據失效；MUST 依規則四在最終候選版本重跑仍適用的選題，並補上修正新增的風險。宣稱跨檔換寫舊契約時，同時依 `../sdlc-orchestrator/references/traceability.md` 規則六掃描殘留並逐筆分類。

### 步驟 28：Bug 修正與回歸測試
- Action：修 bug、重測確認沒弄壞其他功能；若修正使既有改壞證據失效，必須在最終候選版本重新完成受影響情境的正常 → 改壞 → 還原，不能只複查修正 diff
- 誰做：修正動作 MUST 由能寫檔的角色執行——範圍大 → 派 `sdlc-implementer`（角色定義檔 `sdlc-implementer.md`，在你的角色檔目錄下）；範圍小 → Lead-direct。修完後由 `sdlc-reviewer` 或 `sdlc-verifier` 覆核；覆核對原專案維持唯讀；改壞實驗僅限規則四的隔離副本。原專案只有 `sdlc-reviewer` 判 PASS 後，依 `ticket-spec.md` 硬規則 5 更新同一工單 ID 的狀態／日期／變更摘要及角色／覆核紀錄；欄位拆表時可更新同一 ID 的兩列
- Output：修正後穩定的版本

**⚠ 版控邊界（本 phase 一體適用，派出去的 agent 也適用）**：**NEVER 自動 `git commit`／`git push`／建立或切換 branch／開 MR**。步驟 28 修 bug 同樣受此限制——輸出 diff 交由使用者提交。

## 停止條件
- 品質門禁（型別檢查/lint/build）沒過就想進測試 → 停下來，先修到 0 issues
- 測試中發現前面階段（`requirement-scoping`/`system-design`/`implementation-handoff`）的產出有問題 → 明確告知使用者要回哪個 phase 重新確認，不要在已知有問題的情況下把測試做完當作沒事；確認要回頭後依 `../sdlc-orchestrator/sdlc-entry.md`「回歸」段回寫狀態（含連鎖回開判斷），不能只在對話裡講一講
- 卡住的原因是**流程規則本身**（規則寫死了不適用本專案的做法／兩條規則矛盾／判準模糊到判不出來／缺一步接不上）→ **不要就地改規則、不要停工**：append 一列到**框架缺陷登記簿**（status=`proposed`，**證據欄必填**）。登記簿位置 → `../sdlc-orchestrator/references/framework-defects.md`；**該檔可能是登記簿本身，也可能是指向使用環境實際登記簿的指標檔，打開照它說的走**，然後用最接近的合理解讀把工作做完

## 下一步
驗收結果通過 → 依使用者授權範圍接續 `release-handoff` 的部署前置確認；若部署不在既有授權內，說明測試結果及預定部署環境，再詢問具體部署動作。授權、暫緩與提醒判準依 `../sdlc-orchestrator/references/phase-transition-reminders.md`；驗收通過本身不授予部署權限。
