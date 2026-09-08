# SDLC Skill 包 — 異動記錄（實際內容）

> 記錄格式與規則見 `CHANGELOG.md`，這裡只放異動摘要表與逐筆詳細記錄。查歷史才需要打開本檔；平常編輯規則檔案前只需要看 `CHANGELOG.md`。

---

## 異動摘要

| 票號 | 類別 | 項目 | 狀態 |
|---|---|---|---|
| `SKC-20260814-01` | 規則調整（建立機制） | 建立 `CHANGELOG.md`/`CHANGELOG-ENTRIES.md` 異動追蹤機制，25 份規則檔案加上編輯前提示行 | 已落地 |
| `SKC-20260814-02` | 規則調整（範圍限縮） | 把品質門禁「MUST 0 issues」限定為「這次異動新增/修改的程式碼」，範圍外既有問題 MUST 記錄不強制修——即使經過三輪獨立稽核，這個缺口仍未被發現 | 已落地 |
| `SKC-20260814-03` | 規則調整（新增機制） | 建立「回歸」通用規則（`sdlc-entry.md`）：區分回歸與普通bug、狀態回寫、連鎖回開（含例外論證要求）、跟框架缺陷的界線；`traceability.md` 補內容修正規則；12 份檔案同步 | 已落地 |
| `SKC-20260814-04` | 規則調整（補顆粒度，分兩步完成） | `REQ-nn` 補驗收標準子編號機制（`REQ-nn-AC1`/`AC2`……）；步驟二修正 grep pattern 過期、補拆分判準、補回歸情境下的舊引用處理、補 reviewer/verifier 涵蓋 | 已落地 |
| `SKC-20260815-01` | 規則調整（新增機制） | `implementation-handoff`（Phase 5）完成條件新增第5項橫切檢查：測試所需的資料/帳號/外部相依 MUST 主動盤點並備妥或回報缺口，不再只靠 Phase 6 跑到一半才發現的 `BLOCKED`；`sdlc-implementer`/`sdlc-reviewer`/`sdlc-verifier` 三個角色檔同步補對應檢查項 | 已落地 |
| `SKC-20260815-02` | 規則調整（新增規則檔案） | 新增 `references/tooling-reuse.md`：專案文件（不含skill包自身）裡重複性機械檢查優先寫成可重跑腳本、省 LLM 重新推導 token 的 MAY 原則，含跟 `sdlc-entry.md`「治理保證不得只靠腳本」的分工、`framework-defects.md` 登記簿資料列的邊界判準；`qa-handoff`/`ticket-spec.md`/`framework-defects.md`/`CHANGELOG.md` 同步引用/更新 | 已落地 |

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
