# SDLC Skill 包 — 異動記錄（實際內容）

> 記錄格式與規則見 `CHANGELOG.md`，這裡只放異動摘要表與逐筆詳細記錄。查歷史才需要打開本檔；平常編輯規則檔案前只需要看 `CHANGELOG.md`。

---

## 異動摘要

| 票號 | 類別 | 項目 | 狀態 |
|---|---|---|---|
| `SKC-20260930-03` | 規則調整 | 白話回報、具體動作提問與既有授權接續 | 已落地 |
| `SKC-20260930-02` | 規則調整 | 外部環境狀態責任與產品入口整合驗證 | 已落地 |
| `SKC-20260930-01` | 規則調整 | 複審重新取得改壞證據，並掃描跨檔換寫殘留 | 已落地 |
| `SKC-20260924-02` | 規則調整 | 子 agent 逐項 checkpoint、可接續派工與提問邊界 | 已落地 |
| `SKC-20260924-01` | 規則調整 | Phase 6 納入獨立改壞實驗、隔離副本權限與收關證據 | 已落地 |
| `SKC-20260923-05` | 規則調整 | 模式宣告移至 Phase 7 上線交接，Phase 8 接手補查 | 已落地 |
| `SKC-20260923-04` | 規則調整 | fixed 僅由覆核者標記；PASS 後限改同一工單 ID 的結案與覆核紀錄 | 已落地 |
| `SKC-20260923-03` | 規則調整 | 將 Phase 6 的 UAT 非撰寫者實跑與非原作者安全審查提升為明確收關條件 | 已落地 |
| `SKC-20260923-01` | 規則調整 | 入口承認合法不適用狀態，補合法略過與無效狀態的路由 | 已落地 |
| `SKC-20260922-01` | 規則調整 | 分卷保留階段定位資訊，同步共用入口與分卷入口 | 已落地 |
| `SKC-20260814-01` | 規則調整（建立機制） | 建立 `CHANGELOG.md`/`CHANGELOG-ENTRIES.md` 異動追蹤機制，25 份規則檔案加上編輯前提示行 | 已落地 |
| `SKC-20260814-02` | 規則調整（範圍限縮） | 把品質門禁「MUST 0 issues」限定為「這次異動新增/修改的程式碼」，範圍外既有問題 MUST 記錄不強制修——即使經過三輪獨立稽核，這個缺口仍未被發現 | 已落地 |
| `SKC-20260814-03` | 規則調整（新增機制） | 建立「回歸」通用規則（`sdlc-entry.md`）：區分回歸與普通bug、狀態回寫、連鎖回開（含例外論證要求）、跟框架缺陷的界線；`traceability.md` 補內容修正規則；12 份檔案同步 | 已落地 |
| `SKC-20260814-04` | 規則調整（補顆粒度，分兩步完成） | `REQ-nn` 補驗收標準子編號機制（`REQ-nn-AC1`/`AC2`……）；步驟二修正 grep pattern 過期、補拆分判準、補回歸情境下的舊引用處理、補 reviewer/verifier 涵蓋 | 已落地 |
| `SKC-20260815-01` | 規則調整（新增機制） | `implementation-handoff`（Phase 5）完成條件新增第5項橫切檢查：測試所需的資料/帳號/外部相依 MUST 主動盤點並備妥或回報缺口，不再只靠 Phase 6 跑到一半才發現的 `BLOCKED`；`sdlc-implementer`/`sdlc-reviewer`/`sdlc-verifier` 三個角色檔同步補對應檢查項 | 已落地 |
| `SKC-20260908-01` | 規則調整（改寫，分兩步完成） | `DESIGN.md` 的 Entry Protocol 區塊（＝`install.py` 貼進使用環境 `CLAUDE.md` 的那段）由條列改寫為定位表，補上 Phase 1-8 階段名與原步驟編號（43 → 32 行，承重判定一條未減）；步驟二修正舊版就存在、窮舉才抓到的 Phase 4 路由洞（`dev-setup` 那列條件寫反且被上一列吃掉，永遠命中不到）＋三處可讀性 | 已落地 |
| `SKC-20260815-02` | 規則調整（新增規則檔案） | 新增 `references/tooling-reuse.md`：專案文件（不含skill包自身）裡重複性機械檢查優先寫成可重跑腳本、省 LLM 重新推導 token 的 MAY 原則，含跟 `sdlc-entry.md`「治理保證不得只靠腳本」的分工、`framework-defects.md` 登記簿資料列的邊界判準；`qa-handoff`/`ticket-spec.md`/`framework-defects.md`/`CHANGELOG.md` 同步引用/更新 | 已落地 |

---

## SKC-20260930-03

- 時間戳：2026-09-30
- 類別：規則調整
- 項目：白話回報、具體動作提問與既有授權接續
- 狀態：已落地
- 觸發原因：使用者確認 lessons 第十點改善方向並要求修改。
- 異動：共用入口新增「對使用者回報與提問」；以功能現況、動作及影響說明，內部角色程序由主對話處理；看不懂時重新從功能解釋。
- 原文「MUST 用明確選項提問」「每一輪新的完工都要重新觸發」改為先判授權，範圍內必要工作接續，真正缺新決定才問；停止／暫緩指示保留。
- implementation-handoff 與 qa-handoff 同步；部署仍需適用授權。
- 驗證：兩個 skill 的 quick_validate 通過、五組來源／發行副本 SHA256 一致、git diff --check 通過；文字檢查涵蓋已有完整授權、僅要求檢查、明確暫緩及未授權部署四種情境，未執行外部動作。

---

## SKC-20260930-02

- 時間戳：2026-09-30
- 類別：規則調整
- 項目：外部環境狀態責任與產品入口整合驗證
- 狀態：已落地
- 觸發原因：使用者確認 lessons 第九點的三項改善，要求修改。

### 異動內容與證據

- 原先 QA 步驟 26 只要求「測模組間、前後端互動」；新增指標要求「從產品入口驗證實際環境狀態及失敗後行為」。
- test-case-coverage 新增規則五，規定預期狀態、責任者、確認方式與失敗行為；產品負責切換與使用者／維運負責準備分別驗證。
- 測試須觀察外部實際狀態，直接 import 共用函式僅能證明元件，不能替代產品入口；腳本不得代做待驗切換。
- requirement-scoping、system-design、change-request、dev-setup、qa-handoff 與 QA 收關清單引用同一規則。
- 驗證：五個修改的 skill 均通過 quick_validate，八組來源／發行副本 SHA256 一致，git diff --check 通過。
- 文字情境檢查：產品切換失敗須查後續操作；使用者負責時不自行切換；腳本預切與只呼叫 helper 均不能證明入口行為；mock 與外部整合證據分開。此次未執行產品外部整合，沒有宣稱產品測試通過。

---

## SKC-20260930-01

- 時間戳：2026-09-30
- 類別：規則調整
- 項目：複審重新取得改壞證據，並掃描跨檔換寫殘留
- 狀態：已落地；情境 E1–E8 與反向檢查 R1–R5 全部 PASS。
- 觸發原因：檢視 `docs/sdlc-lessons.md` 第八點時，確認既有第五點只明訂「測試缺口修正後」重驗，未完整處理產品／fixture 修正後沿用舊證據，以及跨檔換寫只修已知 finding 的問題。

### 異動內容

- `test-case-coverage.md` 規則四新增版本綁定：改壞證據識別產品、測試、fixture／設定版本；相關內容再修改後，受影響舊證據失效，複審在最終候選版本重跑，不得只看 diff。
- 複審重新評估風險，重跑仍適用的既有選題並補新風險；維持風險選題，不設固定 mutation 數量，也不因無關歷史註記重跑不相干情境。
- `traceability.md` 新增跨檔換寫殘留掃描，把命中分為現況事實、歷史證據、刻意相容／無關；禁止不判讀語意的全域取代。
- 全面換寫若仍有有效現況殘留，不得只另開後續票就讓原票 PASS；只有原始範圍明訂分階段／部分模組時才能記界線後另開票。
- `qa-handoff`、Phase 6 收關清單與 reviewer／verifier 角色同步引用共用規則。

### 證據

- 規則情境與反向檢查：工作區 `sdlc-rereview-eval.md`。
- 六組來源／發行副本 SHA256 一致；`python -m unittest discover -s tests -q`：40 tests，OK，7 skipped；qa-handoff quick_validate 通過；`git diff --check` 通過。

### 已知待辦

- 無。

---


## SKC-20260924-02

- 時間戳：2026-09-24
- 類別：規則調整
- 項目：子 agent 逐項 checkpoint、可接續派工與提問邊界
- 狀態：已落地；獨立覆核 E1–E7、R1–R5 全部 PASS。
- 觸發原因：檢視 `docs/sdlc-lessons.md` 第六點時，使用者明確排除工具呼叫次數上限、只做前 N 項與正常完成後的重複彙整；要求用清楚標記已完成工作的方式，讓 session／token 中止後可由下一個 agent 接續。

### 異動內容

- `references/agent-teams.md` 原本只有「同一 agent 修正 1 次」的 retry 原則；新增「可接續的委派與溝通」，要求 Lead 先建立穩定編號清單，agent 每完成一項立即回報編號、結果、證據與必要解讀。
- 新規則明文禁止以工具呼叫數、前 N 項或用量為由自行縮小範圍；正常完成只使用既有角色報告，不再重列 checkpoint 或另做未檢查項目總結。
- session／token 突然中止時，新文由 Lead 將「無 checkpoint 的編號」視為未完成，恢復同一 agent 或只改派剩餘編號，且不要求已無輸出能力的 agent 補標 `BLOCKED`。
- 新增歧義邊界：影響結果或範圍的歧義回報 Lead、不直接詢問使用者；獨立項目繼續。小歧義可採保守解讀，但須在該項 checkpoint 揭露。
- 三份 `sdlc-*` 角色檔增加共用規則指標；`INSTALL.md` 修正 reviewer／verifier Bash 與自動核准模式的過時文字。

### 證據

- 規則情境與反向檢查記錄：工作區 `sdlc-agent-continuation-eval.md`。
- 來源與發行副本六組對應檔案 SHA256 一致；`python -m unittest discover -s tests -q`：40 tests，OK，7 skipped。

### 已知待辦

- 無。

---

## SKC-20260924-01

- 時間戳：2026-09-24
- 類別：規則調整
- 項目：產品測試有效性的獨立改壞實驗
- 狀態：已落地；獨立覆核八個情境與文字反向檢查完成，結果及既有工單規則待辦見驗證紀錄。
- 觸發原因：使用者確認 lessons 第五點的改善流程，要求實作。

### 異動內容與證據

- qa-handoff 原文「下列六項完成條件全部通過」→「下列七項完成條件全部通過」，新增「測試有效性的改壞實驗已完成」並連至 test-case-coverage 規則四。
- 規則四定義正常基線、獨立選題、單一改壞點、確認位置與執行路徑、目標斷言失敗、測試作者修正及還原重驗；要求指令／退出碼／輸出而非文字推演。
- reviewer 新增 Bash、verifier 明確允許隔離實驗；原專案唯讀與工單列 PASS 例外保持分離，agent-teams、ticket-spec 同步邊界。
- Phase 6 詳細收關條件與 severity-format 同步：預期紅燈不等於交付失敗，不把環境／語法失敗算成功。
- 驗證紀錄：工作區 `sdlc-mutation-review-eval.md`（規則情境覆核，非產品 mutation 實跑）。

---

## SKC-20260923-05

- 時間戳：2026-09-23
- 類別：規則調整
- 項目：模式宣告的建立時機移至上線後交接
- 狀態：已落地
- 觸發原因：使用者指出 lessons 第四點的建立時機錯置，指定 Phase 7／8 交接處理。

### 異動內容與證據

- change-request 原文：「模式宣告（第一次用本 skill 時做一次就好）」；改為：「本 skill 只讀取 `docs/sdlc-mode.md`，不在首次分診後自動建立或切換模式。」
- tailoring 新增：「主責在 Phase 7 成功上線、交接 Phase 8 時，補查在 Phase 8 接手時；不等到第一次 change-request，也不等維運結束。」
- release-handoff 完成條件新增模式交接；ops-feedback 接手先補查。兩份 phase-exit-criteria 同步要求宣告完整與交接紀錄。
- 規則情境檢查：成功上線且已確認演進模式→建立；缺決定→記錄交接待辦；退版／未部署→不自動切換；既有 regulated→保留；full→evolution 須有明確決定；Phase 8 缺檔→先補查再分流。此次為規則文字檢查，未執行部署或修改任何專案模式檔。

---

## SKC-20260923-01

- 時間戳：2026-09-23
- 類別：規則調整
- 項目：三值狀態與合法不適用後的入口路由（FD-06）
- 狀態：已落地；2026-09-23 獨立覆核 PASS，FD-06 由覆核者標為 fixed
- 觸發原因：前次分卷覆核發現入口只接受兩值，與 tailoring 三值矛盾；使用者已明確要求修正。

### 異動內容與證據

- `sdlc-entry.md`「階段完成狀態的判定」原文：`第一行 MUST 是 狀態：進行中 或 狀態：完成`；新文：`第一行 MUST 使用三值之一`，包括帶理由與決定者的不適用。原兩值段改成「先校驗狀態 → 續作進行中 → 合法略過後查必要輸入 → Phase 7 不適用的去向」。
- 新文：`Phase 5／6 永遠不能標不適用`、`不適用表示合法略過，不是完成證據`。缺欄位、未知狀態與未授權裁剪不能被已上線或下游完成掩蓋。
- `DESIGN.md` Entry Protocol、`claude_sdlc.md` 與使用環境入口同步三值與路由。新增定位列：`Phase 7 合法不適用，且本次 Phase 5／6 已完成、無其他未做／進行中階段`；未上線且無適用待辦時結束本次工作，不宣稱部署完成。
- `release-handoff/SKILL.md` 原本同段先限定兩值、下一段又允許第三值；第一段現明列符合下段條件的不適用。
- `references/tailoring.md` 指回入口路由，並明確連接部署階段既有不部署例外。未新增裁剪模式或放寬 Phase 5／6 下限。

### 驗證

- 五份修改規則在使用版本與來源包 SHA256 一致；使用環境入口與安裝器 render_entry_protocol 輸出一致。
- 安裝器測試 40 項：33 通過、7 跳過；release-handoff 通過 quick_validate.py；git diff --check 通過。
- 獨立覆核：Archimedes（01a0cc5a-3ba1-7310-a373-7810f7776490）重放根目錄 `sdlc-state-eval.md` 全部指定場景並判 PASS；未操作實際 handoff-log、分卷檔或部署環境。
- 後續同步：implementation-handoff、qa-handoff 與 tooling-reuse 的舊兩值描述已改成明確說明「全域三值、Phase 5／6 禁用不適用」；兩份規則包相關檔案 SHA256 一致，殘留掃描無舊全域兩值文字。
- 本地反向驗證：三種合法狀態通過；裸不適用、缺理由、缺決定者、未知狀態被拒絕。獨立覆核另確認移除三值、欄位檢查、Phase 5／6 禁用或 Phase 7 例外都會造成錯誤路由。

---

## SKC-20260923-04

- 時間戳：2026-09-23
- 類別：規則調整
- 項目：覆核者 PASS 後的唯一窄化寫入例外（ticket-spec 硬規則 5）
- 狀態：已落地；2026-09-24 後續獨立覆核 PASS，AI 狀態權限、四種工單保存位置、拆表寫入與同步流程均可執行。
- 觸發原因：唯讀覆核者無法親自標記 fixed，與「fixed 只能由覆核者標記」互相卡住。

### 初始異動（2026-09-23）

- ticket-spec.md 明定覆核過程唯讀；只有 PASS 後可修改對應工單列的 in-progress → fixed、完成日期與覆核者／覆核紀錄。
- NEEDS WORK／FAIL 完全不得寫入；不得修改程式碼、測試、需求、設計、其他工單或其他列；寫入後必須檢查 diff。
- qa-handoff 與 sdlc-reviewer 角色同步權限邊界；來源包與使用版同步。

### 驗證

- 初始獨立反向驗證：Poincare（01a0ccba-de1e-7b32-a3e2-596a6ab5119d）確認當時列出的五個情境；2026-09-24 後續覆核發現未涵蓋 AI 狀態權限、BUG／FB 保存位置與主表／角色表拆列，因此該次 PASS 不再代表完整規則已驗證。

### 後續修正（2026-09-24）

- 硬規則 2 將「AI 只能寫 proposed」限縮到提案／決策階段：AI 不得自行決定 accepted／rejected；人已標 accepted 後可由認領者標 in-progress，未參與修正的 AI reviewer 可依硬規則 5 在 PASS 後標 fixed。
- 硬規則 5 的寫入位置改為「四種工單」表指定的位置：工作票的工單系統與 handoff-log 狀態回寫、BUG 的 handoff-log、FB 的 feedback-log、FD 的框架缺陷登記簿。外部系統仍需既有權限。
- 寫入單位改為同一工單 ID 的結案紀錄：狀態／日期／變更摘要，以及角色／覆核紀錄。欄位拆成主表與角色表時可更新同一 ID 的兩列；其他 ID、其他欄位與非指定位置仍禁止。
- qa-handoff、phase-exit-criteria、agent-teams、test-case-coverage 與 sdlc-reviewer 的權限描述同步。
- 後續驗證：Hegel（01a0d154-7d58-72b3-a59d-53064fbcdb7d）獨立重放 12 個狀態／權限情境及兩個反向刪除情境；確認原三項矛盾與後續五個執行缺口均已關閉，未發現新的直接矛盾。覆核提出的兩個輕微文字風險（待編號 ID、FB accepted 前置）亦已對齊。

---

## SKC-20260923-03

- 時間戳：2026-09-23
- 類別：規則調整
- 項目：Phase 6 收關條件明文化
- 狀態：已落地；2026-09-23 獨立覆核通過，四個缺證據情境均被拒絕，完整情境 PASS
- 觸發原因：sdlc-lessons.md 第二點指出，四份 Output 完成後容易漏掉非原作者安全審查與非撰寫者 UAT 實跑。

### 異動內容

- qa-handoff/SKILL.md 的完成條件由四份 Output 改為六項全部通過，新增 UAT 非撰寫者實跑及安全審查／N/A 證據。
- phase-exit-criteria.md 補上 UAT 執行者、日期、結果，以及安全審查或 N/A 確認者、範圍、結果的持久化要求。
- skill/ 與 sdlc-skill/skills/ 兩份規則來源同步。

### 驗證

- 驗證案例：sdlc-phase6-exit-eval.md。
- 獨立反向驗證：Chandrasekhar（01a0cc65-878e-71a1-a68e-3bcdb8ddd40e）確認移除第 5、6 項會重現原缺口；六項證據全齊 PASS。四個負向案例回報 FAIL 是預期的拒絕結果。

---


## SKC-20260922-01

- 時間戳：2026-09-22
- 類別：規則調整
- 項目：handoff-log 時間分卷保留階段定位資訊
- 狀態：已落地；2026-09-23 獨立覆核分卷範圍 PASS，FD-05 由覆核者標為 fixed
- 觸發原因：使用者依專案踩坑紀錄要求修正分卷造成階段定位失真的問題。

### 異動內容

- `sdlc-entry.md`「handoff-log 分卷時保留階段定位資訊」為共用規則：保留原標頭、緊接下一行的原狀態、有效分卷連結；再次分卷仍保留，回歸更新主檔狀態。
- 五份分卷入口：`implementation-handoff`、`qa-handoff`、`release-handoff`、`change-request`、`ops-feedback` 的 `SKILL.md` 同步引用共用規則。
- `DESIGN.md` Entry Protocol 與 `claude_sdlc.md` 同步，避免安裝或手動複製入口時漏掉此要求；使用環境的既有入口同步。
- 使用環境與來源規則包的上述八份檔案逐檔 SHA256 比對一致。缺陷登記與情境驗證紀錄留在使用環境，不複製使用環境的登記資料進來源包。

### 證據

原分卷文字：`超過 200 行時把舊內容整段移到`，只要求 `主檔保留最近期內容 ＋ 一行分卷索引`。

新分卷文字：`handoff-log.md` 另 `MUST 保留既有階段標頭、原狀態行與分卷連結`。

共用規則原文（`sdlc-entry.md:100`）：`分卷本身不得改狀態、改階段順序或新增原本不存在的階段`。
分卷後核對原文（`sdlc-entry.md:112`）：`依同一份定位表判出的下一步與分卷前相同（包括「進行中優先」）`。

### 驗證

- 差異空白檢查通過；八份規則檔在使用版本與來源版本完全相同。
- 安裝器測試：`python -m unittest discover -s tests -q`，40 項，33 通過、7 跳過。首次在工作區根目錄執行時找不到 tests；改至來源包根目錄後完成測試。
- 五份修改的 SKILL.md 均通過 quick_validate.py；安裝器 render_entry_protocol 產生的入口與工作區 CLAUDE.md 相符；git diff --check 通過。
- 獨立情境覆核：Kuhn（01a0c894-2052-7aa1-94d7-393c232eda5d）於 2026-09-23 回報分卷範圍 PASS：7 正向案例通過、23 反向破壞案例全部抓到，含合法不適用狀態首次與再次分卷；覆核者確認規則 SHA256 未變，並自行將使用環境的 FD-05 標 fixed、填覆核紀錄。
- 驗證界線：連結與錨點以記憶體模型驗證，未做 Markdown 渲染器實測。入口兩值狀態與 tailoring 三值狀態的既存矛盾仍保留；本次只修分卷保留合法原狀態，不宣稱解決該矛盾。

---


## SKC-20260814-01

- 時間戳：2026-08-14
- 類別：規則調整（建立機制，分三步完成）
- 項目：建立 `CHANGELOG.md`（規則）+ `CHANGELOG-ENTRIES.md`（記錄）異動追蹤機制，25 份規則檔案加上編輯前提示行，並補上「新增規則檔案時範圍要同步更新」的規則
- 狀態：已落地

> 依「合併規則」：步驟二是在補完步驟一還沒做完的同一個交付物——一個只涵蓋「現有 25 份檔案」、沒講「以後新增檔案怎麼辦」的異動追蹤機制，只看步驟一會誤以為未來新增的 skill/規則檔會自動被涵蓋，這個認知在步驟二之前是錯的，合併成同一票號記錄。

### 步驟一：建立機制本體（2026-08-14）
- 觸發原因：這套機制先前在另一份（未納入 git 管理的）安裝副本上已經驗證過必要性——純文字宣稱「已同步」跟檔案實際內容脫鉤是真實發生過的問題。這個 repo 雖然本身有 git，但 commit message 目前很精簡（例如 `feat: skill new version`），沒有「為什麼改」的敘事、也沒有「同一交付物分幾步做完」的合併判斷，兩者互補，決定補上。

### 異動內容
新建 `skills/sdlc-orchestrator/CHANGELOG.md`（規則說明：合併規則、票號格式、跟 git commit 的分工）與 `CHANGELOG-ENTRIES.md`（本檔，從空表開始，不回填偽造歷史）。在以下 25 份檔案的 frontmatter 結尾／H1 正下方各加一行 `> ⚠️ 修改本檔案前後，MUST 依 \`<相對路徑>/CHANGELOG.md\` 的規則記錄異動。`（相對路徑依檔案位置調整）：

- 13 份 `SKILL.md`：`bug-fix`／`change-request`／`converge`／`debug`／`dev-setup`／`implementation-handoff`／`ops-feedback`／`product-discovery`／`qa-handoff`／`release-handoff`／`requirement-scoping`／`rule-eval`／`system-design`
- `sdlc-orchestrator/references/` 下 7 份：`agent-teams.md`／`framework-defects.md`／`questioning-sufficiency.md`／`severity-format.md`／`tailoring.md`／`ticket-spec.md`／`traceability.md`
- 3 份角色檔：`agents/sdlc-implementer.md`／`sdlc-reviewer.md`／`sdlc-verifier.md`
- `sdlc-orchestrator/sdlc-entry.md`、`DESIGN.md`

刻意不含 `claude_sdlc.md`（衍生自 `sdlc-entry.md` 的速查摘要，非規則正本）與 `DESIGN-RATIONALE.md`/`SDLC_Agent_優化設計.md`/`SDLC_Agent協作版.md`/`SDLC_主流程版_IAO.md`/`DISTRIBUTION.md`/`INSTALL.md`（依 `KNOWN-ISSUES.md` 說明為討論紀錄或已作廢文件）。

### 證據（步驟一）
`git status --short` 於 repo 根目錄確認 25 個既有檔案標記 `M`（modified）+ 2 個新檔案標記 `??`（`CHANGELOG.md`／`CHANGELOG-ENTRIES.md`）；`grep -rl "修改本檔案前後" skills agents` 命中 26 個檔案（25 份目標檔案 + `CHANGELOG.md` 自身的同款提示行，與規則說明段一致）；抽查 `agents/sdlc-implementer.md`（多行 YAML frontmatter，含 `tools:` 清單）與 `skills/sdlc-orchestrator/DESIGN.md`（同層相對路徑）確認插入位置正確、相對路徑正確。

### 步驟二：補「新增規則檔案時範圍要同步更新」規則（2026-08-14）
- 觸發原因：使用者追問「有確保這個機制對這個 repo 新增的 skill 也有效嗎」——查證發現步驟一寫的是「現在這 25 份」的靜態清單，沒有規則講「以後這個 repo 又新增一個 skill/規則檔時，要不要比照辦理」。這是機制本身的完整性缺口：範圍會隨時間跟實際檔案脫鉤，而這正是本機制存在的理由要防的那種脫鉤，只是這次脫鉤的是「範圍」而不是「內容」。
- `CHANGELOG.md` 新增「範圍不是固定清單，新增規則檔案時 MUST 同步涵蓋」整節，三條規則：①新規則檔案建立當下就要加提示行，不是之後有空再補；②MUST 回來更新本檔「範圍」段的清單與份數；③新增動作本身也要開一筆 `CHANGELOG-ENTRIES.md` 記錄

### 證據（步驟二）
`Read` 核對 `CHANGELOG.md`，確認新增段落插入在「為什麼要有這個機制」與「首次使用檢查」之間，語意銜接正確。

### 步驟三：異動摘要表移除「時間戳」欄（2026-08-14）
- 觸發原因：使用者指出票號本身（`SKC-<8碼日期>-<序號>`）已經帶日期，摘要表另外放一欄「時間戳」是重複資訊
- `CHANGELOG-ENTRIES.md` 異動摘要表從 5 欄（票號／時間戳／類別／項目／狀態）改為 4 欄（票號／類別／項目／狀態），同步調整既有的 `SKC-20260814-01` 那一列
- **不動的部分**：每筆記錄詳細區塊裡的「時間戳：YYYY-MM-DD」欄位維持不變——多步驟票（例如日後可能出現的跨日期票）詳細區塊的時間戳可以是日期區間（比照舊安裝副本 `SKC-20260811-01` 的先例：`2026-08-11 → 2026-08-13`），這個資訊票號本身放不下，只有摘要表那欄才是純重複

### 證據（步驟三）
`Read` 核對 `CHANGELOG-ENTRIES.md` 異動摘要表，確認表頭與資料列都已改成 4 欄。

### 已知待辦
- 本次異動皆為 working tree 修改，**尚未 commit**——是否要 commit／commit message 怎麼寫，留給使用者決定
- Hook 機制（PreToolUse 攔截提醒）目前只在 `CHANGELOG.md`「首次使用檢查」段說明，尚未實際安裝，待使用者另外核准
- 這是本次「把 `.claude\skills` 上已確認的健檢成果搬進這個 git 版本」系列工作的第一項（對應原編號 ①），後續還有 ⑥（AC 顆粒度概念，需要用這個 repo 的 `[REQ-nn]` 格式重新設計，不是直接搬）跟⑨（測試資料與環境準備，仍是這個 repo 也沒解決的缺口）待處理
- 「新增規則檔案時 MUST 同步涵蓋」目前只是文字規則，沒有機制強制執行（例如沒有 git hook 檢查新增的 `SKILL.md` 是否帶有提示行）——跟本機制本身「先寫規則、hook 是選配」的既有設計一致，不算本次遺漏

---

## SKC-20260814-02

- 時間戳：2026-08-14
- 類別：規則調整（範圍限縮）
- 項目：把品質門禁「MUST 0 issues」限定為「這次異動新增/修改的程式碼」，範圍外既有問題 MUST 記錄不強制修
- 狀態：已落地
- 觸發原因：這是「把另一份安裝副本（`.claude\skills`）上已確認的健檢成果搬進這個 git 版本」系列工作的第二項。查證發現：`implementation-handoff/SKILL.md`「完工關卡」表第1關、`references/phase-exit-criteria.md` 步驟22/23、`agents/sdlc-implementer.md` Step 3 三處的品質門禁規則都只寫「MUST 0 issues」，沒界定範圍是「這次異動」還是「整個專案」。`sdlc-implementer.md` Step 1 教實作者去讀專案設定檔找**全專案**掃描指令；演進模式（既有系統，尤其是成立多年、從沒走過這套 SDLC 的舊專案）通常帶有既有 lint/type 問題，字面執行「MUST 0 issues」會逼實作者把沒碰過的舊程式碼一併清乾淨才能結案。**這個缺口即使經過 `KNOWN-ISSUES.md` 記載的三輪獨立稽核（走劇本／對抗性破壞／跨檔逐項比對）也沒被抓到**——另外查了全 repo 的「既有問題/技術債/legacy」相關字眼，沒有任何地方處理這個情境。

### 異動內容

**`agents/sdlc-implementer.md`**：Step 3 標題下加範圍說明段落（「0 issues」指這次異動新增/修改的程式碼，範圍外既有問題不算阻塞項但 MUST 列進報告）；Step 4 自我驗證清單加一條；Step 5 報告格式加「## 範圍外的既有問題」區塊。

**`skills/implementation-handoff/SKILL.md`**：「完工關卡」表第1關品質門禁的內容加「這次異動新增／修改的程式碼 0 issues」與範圍說明；持久化規則的 `handoff-log.md` 記錄欄位加「範圍外的既有問題」。

**`skills/implementation-handoff/references/phase-exit-criteria.md`**：步驟22、23 與「完工三關」第1關的「0 issues」都改為「這次異動新增/修改的程式碼 0 issues」，並加註範圍外問題已列進 `handoff-log.md`。

### 證據
`Grep "範圍外的既有問題|這次異動新增/修改的程式碼|這次異動新增／修改的程式碼"` 於 `agents/sdlc-implementer.md`、`skills/implementation-handoff/SKILL.md`、`skills/implementation-handoff/references/phase-exit-criteria.md` 三個檔案，共命中 8 處，覆蓋 Step 3/4/5（implementer）、完工關卡表+持久化規則（SKILL.md）、步驟22/23+完工三關第1關（exit-criteria）。

### 已知待辦
- 本次異動皆為 working tree 修改，尚未 commit

---

## SKC-20260814-03

- 時間戳：2026-08-14
- 類別：規則調整（新增機制）
- 項目：建立通用「回歸」規則——發現前面 phase 的產出本身錯了（不是普通 bug）時，要能區分兩者、狀態要能回寫、連鎖回開受影響的中間 phase，且跟框架缺陷（`FD-nn`）的界線要講清楚
- 狀態：已落地
- 觸發原因：這是系列工作第三項。原始問題是「另一份安裝副本上做過的回歸機制能不能搬過來」——查證發現 `release-handoff` 步驟32（煙霧測試退版）已經是這個情境的一個範例，但只是個案，其他 phase 的「發現前面階段有問題」停止條件都只講「告知使用者回哪個phase」沒有下文；`traceability.md` 的 `REQ-nn` 明文「永不變、不重用、不補洞」，容易被誤讀成「內容也不能改」。使用者過程中提出五點修正：①明確定義「回歸」＝根因需要回頭改一份更早 phase 已定案的產出物（例如需求文件），區別於普通 bug；②**連鎖回開是必須處理的漏洞**——只回開最早出錯的 phase，中間建立在錯誤內容上的 phase 會被判斷演算法誤判為「已完成」而漏掉重新檢查，是比沒有機制更危險的假象；③要求檢查 git 版本新增的 `bug-fix`/`debug`/`converge`/`rule-eval` 四個 skill 有沒有相關情境；④「回查下游」要給具體做法不能只講「MUST回查」；⑤要講清楚跟框架缺陷（`FD-nn`）的界線，兩者可能同時成立不是互斥。

### 異動內容

**`sdlc-orchestrator/sdlc-entry.md`**：在「階段完成狀態的判定」與「跨包變更」之間新增「## 回歸」整節——區分回歸與普通bug的判準（修正落點在哪一個phase的產出物）、狀態回寫規則、連鎖回開規則（含「明確論證才能不回開」的例外條款）、跟 `traceability.md` 的分工、跟框架缺陷的界線（可能同時成立）。

**`sdlc-orchestrator/references/traceability.md`**：新增「規則五：內容修正 ≠ 重新編號」——澄清「永不變」指編號不指內容，原地修訂＋不重新編號；內容修正後 MUST `grep [REQ-nn]` 回查下游，站不住的部分依 `ticket-spec.md` 開新工單，證據欄寫明源自哪個 REQ 修正。

**`sdlc-orchestrator/references/ticket-spec.md`**：FD-nn 排除清單「需求不清→回上一個phase」加指回 `sdlc-entry.md`「回歸」段；新增一句「兩者可能同時成立，不是二選一」。

**`release-handoff/SKILL.md`**：步驟32（煙霧測試退版）改為指回通用規則（含連鎖回開判斷）而非只描述 Phase 5 單獨處理；停止條件的通用句加同樣的指回。

**6 份 SKILL.md 的既有「停止條件」**（`requirement-scoping`/`system-design`/`dev-setup`/`implementation-handoff`/`qa-handoff`/`ops-feedback`）：句尾加「確認要回頭後依 `sdlc-entry.md`『回歸』段回寫狀態（含連鎖回開判斷），不能只在對話裡講一講」。

**`debug/SKILL.md`**：Phase 3 修復段加提醒——Root Cause 若是需求理解有誤而非程式邏輯錯誤，轉走回歸而非硬修出掩蓋問題的 patch。

**`bug-fix/SKILL.md`**：步驟1分診的既有「根因是設計缺陷→不是修bug是設計變更」擴充，加入「根因是需求沒釐清→也不是修bug、也不透過change-request，是回歸情境」。

`converge`／`rule-eval` 查過後確認不需要改：`converge` 是 pipeline 外的討論前哨站，不產出 phase 分節，沒有「更早 phase」可回歸；`rule-eval` 驗的是規則本身有沒有效，跟內容判斷錯誤是不同維度。

### 證據
`Grep "回歸」段"` 於 `skills` 目錄命中 11 個檔案；`git status --short` 確認共 12 個檔案標記 `M`（含 `sdlc-entry.md` 本身）。抽查 `sdlc-entry.md` 新增段落與 `traceability.md`「規則五」的插入位置與銜接文字正確。

### 已知待辦
- 連鎖回開的「例外」條款（論證某中間phase不受影響可以不回開）目前只要求「寫明論證過程」，沒有規定要不要找獨立角色確認這個論證——跟 `severity-format.md` 的 N/A 條款「實作者以外的角度確認」比，這條的把關比較鬆，之後可能要補
- 本次異動皆為 working tree 修改，尚未 commit

---

## SKC-20260814-04

- 時間戳：2026-08-14
- 類別：規則調整（補顆粒度，分兩步完成）
- 項目：`REQ-nn` 補驗收標準子編號機制（`REQ-nn-AC1`/`AC2`……），並延伸 `[REQ-07]` 引用格式支援 `[REQ-07-AC2]` 精確變體
- 狀態：已落地

> 依「合併規則」：步驟二是使用者主動追問「這個調整有什麼不完善之處」後補完步驟一還沒做完的同一個交付物——只看步驟一會誤以為子編號機制已經自洽，實際上跟同一 session 剛建的規則五有格式不一致的真 bug，合併成同一票號記錄。

### 步驟一：建立 AC 子編號機制（2026-08-14）
- 觸發原因：另一份安裝副本（`.claude\skills`）上曾查出這個缺口：一條需求（`REQ-nn`）可能包含多條可獨立驗證的業務規則（例如「登入功能」底下「帳號不存在」「密碼錯誤」「連續失敗鎖帳號」三條規則），但追溯只做到 REQ 層級——只要有一條規則被測到，整條 REQ 在 `qa-handoff` 步驟27 的窮舉表上就能顯示「已覆蓋」，其餘規則完全沒測到卻看不出來。查證確認這個缺口在 git 版本上一樣存在且未被發現：`requirement-scoping/SKILL.md` 步驟9 的 REQ 是按「功能」發號，`questioning-sufficiency.md` 沒有任何維度要求拆到規則層級，`qa-handoff` 步驟27 的窮舉表也只到 REQ 層級。討論三個選項（A. REQ 底下加 AC 子編號，不開新表／B. 不加子編號、只用文字列出每條規則／C. 從源頭要求每條規則各發一個 REQ-nn）後選 A——B 沒有穩定 ID 無法 grep 對帳，違背 `traceability.md` 規則三自己的理由；C 會把需求規格書拆得過碎，不利 Phase 2 跟業務方在功能層級溝通範圍/優先序，且要連帶改掉 `requirement-scoping` 步驟9「把每個功能寫成正式規格」的既有定位。A 不違反規則二（唯一真相源、不開第二張表——子編號仍在 `requirements-spec.md` 同一張表裡）也不違反規則三（`[REQ-07-AC2]` 是同一格式家族的精確變體，不是第二種格式），且跟 `SKC-20260814-03` 剛建的「內容修正後回查下游」機制銜接得上（能精確指到哪條規則被改，不用整條 REQ 打回重驗）。

### 異動內容（步驟一）

**`requirement-scoping/SKILL.md`**：步驟9 Action 加「一條 `REQ-nn` 若包含多條可獨立驗證的業務規則/情境，MUST 逐條列出並各自編號（`REQ-nn-AC1`、`REQ-nn-AC2`……）；只有單一情境時不需要編號」。

**`sdlc-orchestrator/references/traceability.md`**：規則三標題改為「引用格式只有一種（含驗收標準子編號變體）」，內文說明 `[REQ-07-AC2]` 是精確變體不是第二種格式，並加一句「REQ 有拆 AC 時，測試 MUST 掛到 AC 這一層」；規則四正向窮舉加「REQ 有拆 AC 的 MUST 逐條 AC 分別列出、分別回答，不能只在 REQ 層級打勾」，並說明不這樣做會讓「已覆蓋」的宣稱失真。

**`qa-handoff/SKILL.md`**：步驟27 Action 加對應的 AC 逐條窮舉要求，措辭與 `traceability.md` 規則四一致。

### 證據（步驟一）
`Grep "REQ-nn-AC|REQ-07-AC2|驗收標準子編號"` 於三個檔案命中 5 處，涵蓋需求發號規則（`requirement-scoping`）、引用格式與窮舉規則（`traceability.md` 規則三/四）、測試關窮舉檢查（`qa-handoff` 步驟27）。

### 步驟二：修正格式不一致與補判準（2026-08-14）
- 觸發原因：使用者追問步驟一的設計有沒有不完善之處，逐項檢視後發現四個問題：①**規則五的 grep pattern 是真 bug**——`SKC-20260814-03` 寫的 `grep -rn "\[REQ-<nn>\]"` 精確比對收尾括號，不會匹配步驟一才新增的 `[REQ-07-AC2]` 變體，內容修正後回查下游會漏掉所有用精確 AC 格式標註的引用，直接違反規則三自己「格式唯一、任何grep都能對帳」的存在理由；②「這條規則算不算獨立情境」沒有給判準，會因人而異拆得不一致；③沒講已經在用的裸 `[REQ-07]` 標籤事後才發現要拆 AC 時怎麼處理舊引用；④`sdlc-reviewer.md`／`sdlc-verifier.md` 完全沒有跟 `REQ-nn`/追溯機制掛勾的檢查項（非步驟一造成，是 git 版本原本就沒有，但既然查到了一併補）。

### 異動內容（步驟二）

**`sdlc-orchestrator/references/traceability.md`**：規則五的回查下游 grep 改成只比對前綴 `\[REQ-<nn>`（不釘死收尾括號），才能同時抓到裸引用跟所有 AC 變體；新增一段處理「事後才拆分子編號」的回歸情境——比照內容修正，回查下游時 MUST 逐一判斷每個既有裸引用原本指哪個新 AC，且說明拆分本身該在撰寫需求規格當下做，事後拆分要有明確觸發理由。

**`requirement-scoping/SKILL.md`**：步驟9 補拆分判準——「把這條規則整句拿掉，剩下的描述還能不能單獨判斷做對了沒有」，能就該拆；卡住時傾向拆（代價可回收），不傾向不拆（代價是實際測試覆蓋缺口，不可回收）。

**`agents/sdlc-reviewer.md`**：Step 1 加「若專案有 `requirements-spec.md`，先查這張票對應哪些 `REQ-nn`（含拆了 AC 子編號的），逐一確認程式碼都有涵蓋」。

**`agents/sdlc-verifier.md`**：target=evidence 清單加「追溯窮舉表每一列宣稱都適用同一條規則，REQ 拆了 AC 子編號的要逐條 AC 分別查，不能因為其中一條 AC 有證據就假設其他 AC 也算過」。

### 證據（步驟二）
`Grep "只比對前綴|判準（這條規則算不算獨立情境）|逐一確認每個 AC|逐條 AC 分別查"` 於四個檔案（`traceability.md`、`requirement-scoping/SKILL.md`、`sdlc-reviewer.md`、`sdlc-verifier.md`）逐一命中確認；`git status --short` 確認共 6 個檔案標記 `M`（含步驟一未變動但因為步驟二又被改到的 `traceability.md`/`requirement-scoping/SKILL.md`）。

### 已知待辦
- 沒有實際案例驗證這個子編號機制在真實需求上好不好用（例如子編號會不會讓 `requirements-spec.md` 的單一產出物 ≤200 行限制更容易被觸發，需要更早拆檔）
- 系列工作最後一項（⑨測試資料與環境準備，git 版本目前也沒解決的真缺口）尚未處理
- 本次異動皆為 working tree 修改，尚未 commit

---

## SKC-20260815-01

- 時間戳：2026-08-15
- 類別：規則調整（新增機制）
- 項目：`implementation-handoff` 完成條件新增「測試資料與環境準備」第5項橫切檢查，`sdlc-implementer`/`sdlc-reviewer`/`sdlc-verifier` 同步補對應檢查項
- 狀態：已落地
- 觸發原因：系列工作最後一項（原編號⑨），是 git 版本三輪獨立稽核都沒抓到的真缺口。查證確認：`severity-format.md` 把「缺測試資料」列為 `BLOCKED` 的合法原因——這是 Phase 6 測試跑到一半才被動發現；`release-handoff` 的檢查是上線前把測試資料**清掉**，跟「一開始有沒有備妥」是相反方向；`implementation-handoff` 步驟21只管資料庫**結構**該不該動、動去哪，不管**內容**（seed/fixture）；`qa-handoff` 步驟25-27 的測試撰寫依據（`dev-setup`/`change-request` 產出的測試描述）從沒被人換算成「所以需要準備哪些資料狀態」。三個修法選項（A. Phase 5 完成條件新增獨立第5項／B. Phase 6 加前置盤點步驟／C. 分兩段——測試描述撰寫時盤點＋Phase 5執行準備）跟使用者討論後選 A：B 的問題是這時候 Phase 5 三關已經跑完宣告完成，若盤點後發現 schema 不支援造測試資料，要整個打回「回歸」流程比A多繞一圈；C 要動三個檔案（`dev-setup`／`change-request`／`implementation-handoff`）且演進模式本來就不走 `dev-setup`，等於盤點邏輯要分別寫兩次，一致性維護成本較高。A 選獨立第5項而不是掛在步驟21底下，是因為步驟21對沒有資料庫的專案會標 N/A，掛在它底下等於這項檢查對非持久化儲存專案會一併消失；獨立成第5項則不管有沒有DB都適用，且創世/演進兩條入場路徑都會經過 Phase 5，涵蓋兩邊入口。

### 異動內容

**`skills/implementation-handoff/SKILL.md`**：
- 完成條件清單新增第5項：「Phase 6 測試所需的資料/帳號/外部相依已備妥，或已識別缺口並回報使用者」，並註明**不適用** N/A 豁免（真的不需要準備時要寫理由記錄，不是套用N/A流程省略記錄）
- 流程段步驟24之後新增「附加檢查：測試資料與環境準備」（Action/誰做/Output 三欄），Action 講明依測試描述反推資料狀態需求、外部sandbox憑證確認、MUST NOT用正式環境資料頂替
- 持久化段：新增測試資料/環境準備結果的記錄要求，並明訂**這是全票一次性記錄，不是每個子項目各自重複**（避免掛在「每個工作項目」清單裡造成顆粒度不一致——這是內部自我檢查時發現的，寫進正式異動前已修正，不是事後另開票修的瑕疵）

**`skills/implementation-handoff/references/phase-exit-criteria.md`**：新增「測試資料與環境準備（全步驟一體適用）」整節，四條檢查項，位置在步驟24與「基礎安全」之間。

**`agents/sdlc-implementer.md`**：Step 1 discovery 加第4點（原第4點「讀取開發規範skill」順延為第5點）；Step 4 自我驗證清單加一條；Step 5 報告格式加「## 測試資料與環境準備」區塊。

**`agents/sdlc-reviewer.md`**：Step 2 審查清單加一條——若本票屬於 Phase 5，檢查報告的測試資料/環境準備段落是否具體，不是隨便寫「已備妥」。

**`agents/sdlc-verifier.md`**：target=evidence 清單加一條——`handoff-log.md` 宣稱已備妥的，要看到 seed script/fixture/缺口清單等實際證據；target=security 清單加一條——檢查測試/種子資料有沒有誤用正式環境的真實個資或憑證。

### 證據
`Grep "測試資料與環境準備|測試資料／環境準備結果|附加檢查：測試資料"` 於 `implementation-handoff/SKILL.md`、`implementation-handoff/references/phase-exit-criteria.md`、`agents/sdlc-implementer.md`、`agents/sdlc-reviewer.md`、`agents/sdlc-verifier.md` 五個檔案逐一命中確認插入位置正確；`wc -l` 確認五個檔案均遠低於200行長度治理上限（45/101/91/53/75行）；`git status --short` 確認 6 個檔案標記 `M`（`agents/sdlc-implementer.md`、`agents/sdlc-reviewer.md`、`agents/sdlc-verifier.md`、`skills/implementation-handoff/SKILL.md`、`skills/implementation-handoff/references/phase-exit-criteria.md`、本檔），與異動內容段列出的檔案一致。

### 已知待辦
- `severity-format.md` 的 `BLOCKED`「缺測試資料」條目沒有回頭加註「這應該是 Phase 5 沒做好才會撞到的殘餘情況，不是本來就該發生的常態」——不影響正確性（BLOCKED仍是合法的保底狀態，例如缺口已回報但使用者還沒申請到sandbox帳號），純粹是可讀性的順手補強，決定不在本票一併做，避免範圍蔓延
- 系列工作（把另一份安裝副本上已確認的健檢成果搬進這個git版本）的原編號①③④⑥⑨至此全數處理完畢
- 本次異動皆為 working tree 修改，尚未 commit

---

## SKC-20260815-02

- 時間戳：2026-08-15
- 類別：規則調整（新增規則檔案）
- 項目：新增 `sdlc-orchestrator/references/tooling-reuse.md`——專案文件（不含skill包自身）裡重複性機械檢查優先寫成可重跑腳本、省 LLM 重新推導 token 的 MAY 原則
- 狀態：已落地
- 觸發原因：使用者提出構想——希望 skill 能在任務中把重複性、可用腳本取代的工作寫成腳本，省下每次都要 AI 重新耗 token 推導的成本。討論過程有幾個關鍵取捨：①查證發現 `sdlc-entry.md` 已有「治理保證必須寫在規則文字裡，不得依賴本機自動化」，字面上有摩擦——釐清後確認 `sdlc-entry.md` 那條擋的是**規則包自己的治理保證**（不能只靠不隨包發送的腳本才算數），本檔講的是**專案執行過程中的效率優化**（腳本是專案自己的產出物），兩者層次不同不衝突；②討論要不要寫成新 skill——skill是「情境觸發」設計，這個原則橫跨所有phase、沒有乾淨的觸發邊界，形狀跟 `severity-format.md`/`traceability.md` 這類通用原則一致，選擇走 `references/` 而非新增 skill；③使用者糾正一開始的範圍誤解——最初的候選清單普查混進了「檢查skill包自己25-26份檔案」的項目（跨檔重複樣板文字、CHANGELOG提醒行覆蓋檢查），使用者指出腳本要對付的是**skill所產的專案文件**，不是skill本身——理由是防止「用這套流程」的專案例行工作滲透成「改這套流程」的無人把關自動化動作，修改規則檔案需要走CHANGELOG治理、需要使用者核准；④普查專案文件層級的候選後選出六個（REQ/AC追溯窮舉、docs長度治理、handoff-log固定標頭+狀態行、工單證據欄空白、severity-format四種狀態值、工單編號格式），並發現 `ticket-spec.md`/`framework-defects.md` 兩份檔案裡已經有作者自己預留的「使用環境可另加機械檢查輔助」措辭，尚未正式連結；⑤使用者追問「REQ追溯核對真的整個都是機械性的嗎」，查證發現這條違反本檔案自己判準第2條（驗收標準是否做對需要語意判斷）——只有「有沒有被測試標籤引用到」可腳本化，「測試是否真的驗證到位」不行，整包貼「機械性」標籤是過度宣稱，已修正拆分；⑥使用者追問「MAY寫成腳本這句話，有沒有可能讓AI誤判成要對skill本身寫腳本」——查證發現 `framework-defects.md` 是唯一的邊界案例：這份 `references/*.md` 檔案依 `ticket-spec.md` 定義**可能就是FD-nn的實際登記簿本身**，登記簿表格裡的資料列即使物理上放在references檔案裡仍屬於專案執行資料，適用本檔案；但同一份檔案定義欄位規則的文字本身不適用——已在「適用範圍」段補上這個判準說明。**過程中曾經commit過一版（`839a8e1`）但只包含部分檔案、且措辭還沒吸收⑤⑥的修正，使用者主動決定 `git stash` + `git revert 839a8e1` 後重新一次做完整版**，本票記錄的是revert後重寫的最終狀態，不是逐次修正的過程（決策脈絡仍完整保留在本段落，只是不再拆成多個步驟小節）。

### 異動內容

**新增 `skills/sdlc-orchestrator/references/tooling-reuse.md`**：適用範圍段（限專案文件，含 `framework-defects.md` 資料列例外的判準）＋三條判準（會重複做／判斷機械性／腳本比LLM推導省時，並註明「同一檢查項目可能只有一部分機械性」）＋不適合腳本化的反例＋跟 `sdlc-entry.md` 的分工說明＋包內既有先例（`dev-setup`一鍵啟動／品質門禁指令、`qa-handoff`整合測試腳本）＋六個建議套用的檢查點（REQ追溯窮舉那條已正確拆分成「可腳本化的引用比對」與「不可腳本化的語意驗證」兩部分；工單編號格式那條已排除`REQ-nn`與未定義的`CR-nn`）。

**`skills/qa-handoff/SKILL.md`**：步驟27在既有 `traceability.md` 引用後加一句，同樣正確拆分成可腳本化與需語意判斷兩部分，指向 `tooling-reuse.md`。

**`skills/sdlc-orchestrator/references/ticket-spec.md`**：兩處既有的「使用環境可另加機械檢查輔助」措辭（第61條「證據欄空白=不受理」、第65條「`fixed` MUST由非修正者標記」）補上指向 `tooling-reuse.md` 的連結。

**`skills/sdlc-orchestrator/references/framework-defects.md`**：「覆核者欄空白＝該筆不得標`fixed`」註記段補上同樣的機械檢查輔助說明，指向 `tooling-reuse.md`。

**`skills/sdlc-orchestrator/CHANGELOG.md`**：依自己「新增規則檔案時 MUST 同步涵蓋」的規則，範圍段的 references 清單從 7 份補到 8 份（加入 `tooling-reuse.md`），總數 25→26。

### 證據
`git status --short` 於 repo 根目錄確認 `tooling-reuse.md` 標記 `??`，`qa-handoff/SKILL.md`／`ticket-spec.md`／`framework-defects.md`／`CHANGELOG.md`／本檔標記 `M`；`Grep "判準與做法 → \`tooling-reuse.md\`|判準與做法 → \`\.\./sdlc-orchestrator/references/tooling-reuse\.md\`"` 於四個引用檔案逐一命中確認連結位置正確；`Read` 核對 `tooling-reuse.md` 全文，確認「適用範圍」段的 `framework-defects.md` 例外說明、REQ追溯條目的拆分措辭、工單編號格式排除`REQ-nn`/`CR-nn`的註記都已包含在單次寫入的版本裡，不需要再事後修正。

### 已知待辦
- 只挑了 `qa-handoff` 步驟27、`ticket-spec.md`兩條、`framework-defects.md`一條做示範連結，`severity-format.md`的四種狀態值段落、多份`SKILL.md`裡的`handoff-log`固定標頭段落，沒有逐一補上反向指回 `tooling-reuse.md` 的連結——這幾處在 `tooling-reuse.md` 自己的清單裡已經有描述，缺的是反向連結，決定不在本票一併做，避免範圍蔓延
- `docs/` 長度治理段落逐字重複出現在多份 `SKILL.md`，這次沒有逐一補上引用——那是既有的內容重複（DRY）問題，範圍比這張票大，決定不在本票一併處理
- 本次異動皆為 working tree 修改，尚未 commit（先前的 `839a8e1` 已由使用者 revert，git 歷史上不會留下那次不完整的commit）

---

## SKC-20260908-01

- 時間戳：2026-09-08
- 類別：規則調整（改寫）
- 項目：`DESIGN.md` 的 Entry Protocol 圍籬區塊改寫為定位表，補上 Phase 1-8 階段名與原步驟編號
- 狀態：已落地
- 觸發原因：`install.py` 只抽 `DESIGN.md` 裡 `### Entry Protocol` 那一個圍籬區塊貼進使用環境的 `CLAUDE.md`（`extract_entry_protocol()`，靠標題文字定位）。該區塊只寫路由條件，DESIGN.md 另一張「Phase → Skill 對應」表（含 Phase 1-8 與步驟 1-35）不在圍籬內，永遠不會被貼出去。結果是裝好之後的 `CLAUDE.md` 只出現 Phase 5／6／7 三個字串（而且只當 `handoff-log.md` 的分節標頭在用），Phase 1-4 零提及、「步驟」零出現——讀那份檔的人或 agent 看不出這條流程總共有 8 關。這一段是承重的：13 份 SKILL.md 的 `description` 只能讓 Claude 觸發到「某一支 skill」，判斷「現在在第幾關」必須讀 `docs/handoff-log.md`，那正是這段入口的工作；Codex 端更沒有 description 自動配對（本檔第九輪已載明），完全依賴這段文字。

### 異動內容

`DESIGN.md` 第 145-189 行的圍籬區塊，整段改寫。

原文（節錄，條列式，只出現 Phase 5/6/7）：

- docs/handoff-log.md 有「## Phase 7」而且那一節是「狀態：完成」，或系統已經上線 → 讀 ops-feedback，照做。
- docs/handoff-log.md 有「## Phase 6」而且那一節是「狀態：完成」，但沒有「## Phase 7」→ 讀 release-handoff，照做。

新文（節錄，表格式，Phase 名與原步驟編號入表）：

| 條件（看 docs/） | Phase（原步驟） | 讀哪個 skill |
|---|---|---|
| handoff-log.md 有「## Phase 7」且完成，或系統已上線 | 8 維運（33-35） | `ops-feedback` |
| 有「## Phase 6」且完成，無 Phase 7 | 7 部署（29-32） | `release-handoff` |

其餘結構性調整：①開頭「先確認有沒有 docs/ 資料夾」改為「先看 docs/ 實際有哪些檔」，與檔尾原本重複的同義句合併，省一段；②四條散落的 ⚠ 提醒（標頭≠做完／只看 product-discovery.md／既往不溯／改完回本表重判＋rule-eval）收攏成「四條硬規則」一節；③「設計文件未齊」的三項判定從表格列裡抽成表後註腳，避免撐爆欄寬。`{{SKILLS_ROOT}}`／`{{AGENTS_ROOT}}` 兩個佔位符保留（`render_entry_protocol()` 缺任一個會丟 `ValueError`）。

### 證據

`python3 -c` 直接呼叫 `install.extract_entry_protocol()` 與 `install.render_entry_protocol()` 的輸出：

    抽取成功: True
    新版行數: 32 （舊版 43）
    佔位符替換 OK: True

    === 承重規則保留檢查 ===
    ✅ converge 優先        ✅ 狀態：進行中          ✅ Phase 7 → ops-feedback
    ✅ Phase 6 → release-handoff   ✅ Phase 5 → qa-handoff   ✅ change-specs 入場
    ✅ 設計完成三判定        ✅ dev-setup 限創世      ✅ 只看 product-discovery.md
    ✅ 既往不溯              ✅ sdlc-mode/tailoring   ✅ rule-eval
    ✅ bug-fix               ✅ 標頭≠做完

    === 新增的（舊版沒有）===
    ✅ 1 需求發想  ✅ 2 需求分析  ✅ 3 設計      ✅ 4 開發前準備
    ✅ 5 開發實作  ✅ 6 測試      ✅ 7 部署      ✅ 8 維運

14 條承重判定逐條命中、8 個階段名全部新增、行數 43 → 32。已用 `inject_entry_protocol()` 相同的組裝與接合方式回寫測試安裝副本 `/Users/waynechen/_test/CLAUDE.md`（49 行 → 38 行，含 BEGIN/END 標記與 H2 標題）。

### 步驟二：修正 Phase 4 路由洞（步驟一漏抓，非步驟一造成）

改成表格之後對 `_test` 做安裝後驗收，把 11 列條件照字面編碼、窮舉所有 `docs/` 狀態組合跑一次，發現 **第 9 列（Phase 4 開發前準備 → `dev-setup`）在所有組合下都命中不到**。兩個原因疊加：

1. **條件寫反**：入口寫「**有** dev-setup.md 但骨架還沒建起來」，但 `dev-setup` 這一關的產出物就是 `dev-setup.md`——等於要求先有產物才准去生產物。同一包另外兩處寫的都是相反的：`claude_sdlc.md:27`「有設計文件、**無** dev-setup.md，且骨架尚未建立」、本檔 `DESIGN.md:203` 自己記載的白紙測試結果「正確判定 Phase 4（有設計文件、**缺** dev-setup.md）並進 `dev-setup`」。
2. **順序被上一列吃掉**：第 6 列（→ `implementation-handoff`）條件是「無 `## Phase 5` 分節 **且** 有 dev-setup.md」。原第 9 列要求「有 dev-setup.md」，只有在「已存在 `## Phase 5` 分節」時才輪得到；但那時分節狀態必為「進行中」或「完成」，第 2 列或第 5 列早已先命中。

**實際後果**：創世專案設計做完、還沒做開發前準備時，前 9 列全部落空，掉到第 10 列被送回 Phase 1 重做需求發想。

**這個洞是舊版就有的**——舊版條列同樣寫「有 docs/dev-setup.md 但骨架還沒建起來」，步驟一改寫時原文照抄，沒有加大也沒有縮小它，是步驟二的驗收才抓到。

修法：條件改為「**設計文件已齊，但沒有 dev-setup.md，且骨架尚未建立**」，並依「越後面的階段排越前面」把該列從第 9 位移到第 7 位（Phase 5 之後、Phase 3 之前）——原位置在 Phase 2 之後，本身就違反該原則。

同批處理的三處可讀性問題：①`rule-eval` 是入口裡唯一沒加反引號的 skill 名，補上，12 個 skill 名寫法一致；②Phase 5 那列三個 OR 條件擠成全表最長的一格，壓成「有 dev-setup.md（創世）或 change-specs/ 輕量規格或 design-delta（演進，經 change-request 分診）」；③Phase 欄原本混了數字階段、「流程外」、「該分節那一關」三種東西，後兩者改成 `—`，說明移進第三欄。

### 步驟二證據

修正前後各跑一次窮舉（15 個 `docs/` 狀態布林、排除「分節存在但無狀態」等不可能組合）：

    修正前： 永遠命中不到的列： ['9']
    修正後： 永遠命中不到的列： 無
             1 converge 7680 / 2 續作該關 4608 / 3 ops-feedback 2304 / 4 release-handoff 384
             5 qa-handoff 192 / 6 implementation-handoff 168 / 7 dev-setup(Phase 4) 4
             8 system-design 8 / 9 requirement-scoping 4 / 10 product-discovery 4 / 11 change-request 4

`DESIGN.md:203` 白紙測試那個情境（有設計文件、缺 dev-setup.md、骨架未建）重跑 → 命中 `dev-setup`，與該行記載的預期一致。`python3 -m unittest discover -s tests` → 40 tests OK。路由順序索引 ops-feedback 4 → release-handoff 5 → qa-handoff 6 → implementation-handoff 7 → system-design 8 → requirement-scoping 10，嚴格遞增；「狀態：進行中」在第 3 列（最小）。反引號一致性檢查：12 個 skill 名皆已加，未加者 0。

### 已知待辦
- `claude_sdlc.md` 開頭原本寫「`install.py` 預設貼的是 Entry Protocol 純文字版；想改用這份表格版……」，本票之後兩邊都是表格、那句話會變成假的，已一併改成「加詳版 vs 精簡版」的區分。該檔不在本機制範圍內（`CHANGELOG.md` 明文排除），此處僅記其連帶更動。
- `tests/test_install.py` 的 `EntryProtocolRoutingTests.entry_lines()` 原本只認 `- ` 開頭的條列列，表格列 `| … |` 認不到而誤報「入口文字沒有任何一條規則指向 ops-feedback」。已放寬為同時認兩種格式——這三個測試守的是 first-hit-wins 的比對順序，跟排版無關。放寬後以「在圍籬區塊內對調 `ops-feedback` 與 `requirement-scoping` 兩列」反向驗證，測試確實報 `ops-feedback 必須排在 release-handoff 之前`，還原後 40 tests OK，不變式沒有被鬆掉。
- Phase 5 那一列原本寫「經 change-request → system-design」，字串 `system-design` 使 `first_index()` 把該列同時算成「指向 system-design 的規則」，兩個階段索引相同而測試失敗。改用本包既有詞彙 `design-delta` 指稱那份產出物，語意不變。
- 本包目前有兩份內容不重疊的 `CHANGELOG-ENTRIES.md`（本檔含 `SKC-20260814-*`／`SKC-20260815-*`，`references/CHANGELOG-ENTRIES.md` 含 `SKC-20260818-*`），兩份在同一個 commit 落地。`CHANGELOG.md` 的「寫在哪」只寫檔名不寫路徑，字面解讀指向同層的本檔，故本票記在本檔。合併與否未決，未在本票處理。
