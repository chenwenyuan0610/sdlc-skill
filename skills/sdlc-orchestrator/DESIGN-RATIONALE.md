# SDLC Orchestrator — 決策細節與被否決方案

> **讀者：本包維護者。** 這是設計過程的內部記錄，不是使用說明。
> 要知道**怎麼裝** → 包根目錄的 `README-給同事.md`；**怎麼用** → `INSTALL.md`；**設計摘要** → `DESIGN.md`。
> 本檔提到的部分檔案路徑（如 `agents/sa.md`、`.claude/rules/*`）屬於維護者自己的環境，**不在這個包裡**，點不開是正常的。

> 這是 `DESIGN.md` 的附錄，只在需要回顧「為什麼當初選這個」時查。日常介紹用 `DESIGN.md` 就夠。

## 背景

來源：`SDLC_主流程版_IAO.md`。

User 提供的設計出發點：

> Agent 協作開發 SDLC · 通用設計原則
> 提煉自一套實戰框架的設計與校準經驗：15+ 個交付切片、60+ 處流程缺陷的修復史。
> 原則領域中立，適用於任何導入 agent 開發的軟體組織。

**結構性發現**：35 步驟中，步驟 21-32（Phase 5-7：開發實作/測試/部署）在既有專案已有成熟對應物（`feature`/`fix`、多角色審查 review、`CI/CD 稽核工具`）。真正沒有 skill 覆蓋的是 Phase 1-4（步驟 1-20）。新 skill 的價值集中在前 20 步；後 15 步轉交既有 skill，避免製造第二套 review/gate 真相源。

## D1 — Skill 定位與範圍：全流程包裹

| 未選方案 | 說明 | 未選原因 |
|---|---|---|
| 上層規劃層 | 只管 Phase 1-4，產出 spec/tickets 交給 feature skill | 與 user 選擇的「全流程」方向不同；其洞察（前段是新內容）仍保留進設計 |
| 純 checklist 參考文件 | 不觸發 agent dispatch | 不符合「Agent 協作開發」定位 |
| 部門級 SOP 文件（非 skill） | 人類可讀流程文件 | user 明確要「設計出 skill」 |

## D2 — 檔案架構：單一 orchestrator + phase references（**已於下一輪討論推翻，見「D2 修訂」**）

```
.claude/skills/sdlc-orchestrator/
├── SKILL.md                              (≤200行：8階段狀態機骨架、觸發條件、gate 呼叫點)
└── references/
    ├── phase-1-4-discovery-design.md
    ├── phase-5-implementation.md         (轉交 feature/fix，不重寫)
    ├── phase-6-7-test-deploy.md          (轉交多角色審查 + check + CI/CD 專案 audit)
    └── phase-8-ops-feedback.md
```

| 未選方案 | 優點 | 未選原因（當下） |
|---|---|---|
| 8 個獨立 phase skill | 模組化、可漸進採用 | 無單一入口，跨 phase 狀態要外部追蹤；互相引用會違反 EVAL-A-003「不要 skill calling skills」 |
| Workflow-script 全程驅動 | 密集 fan-out 步驟可用 judge panel | 多數步驟需 user 即時判斷，Workflow 無法中途暫停等真人輸入；且需 user 明確 opt-in |

### D2 修訂 — 改回 8 個獨立 phase skill，不加前綴命名

User 重新拍板：改採「8 個獨立 phase skill，每階段一個，即使 Phase 5-8 只是轉交既有 skill 也獨立成檔」，理由是希望之後能設計一層「agent teams 協作」機制依情況引用不同 skill——這需要 skill 本身先是獨立、可被外部引用的單位，而不是綁在單一 orchestrator 內部的 references。

命名規則同時修訂：**不加 `sdlc-` 前綴，跟現有 skill（`feature`/`fix`/`debug`）同風格**，短動詞/名詞 + 必要時 hyphen 限定領域：

| Phase | 步驟 | Skill 名稱 |
|---|---|---|
| 一、需求發想 | 1-5 | `product-discovery` |
| 二、需求分析 | 6-10 | `requirement-scoping` |
| 三、設計 | 11-17 | `system-design` |
| 四、開發前準備 | 18-20 | `dev-setup` |
| 五、開發實作 | 21-24 | `implementation-handoff`（轉交 `feature`/`fix`） |
| 六、測試 | 25-28 | `qa-handoff`（轉交多角色審查 review） |
| 七、部署 | 29-32 | `release-handoff`（轉交 `CI/CD 稽核工具`） |
| 八、維運 | 33-35 | `ops-feedback` |

**風險與解決狀態（沿用原本否決 8-skill 方案的理由）**：
1. ✅ 已反轉（第六輪）：跨 phase 狀態本身仍不由 skill 集中追蹤（8 個獨立 skill 的既有設計不變），但每個 phase 的 Output **MUST** 持久化寫成專案 `docs/` 下的 md 檔——原本「對話式交接、團隊自行保存」的政策已被 user 否決，完整討論 → 本文件末「Follow-up 決策 5」。
2. ✅ 已解決：`implementation-handoff` / `qa-handoff` / `release-handoff` 若內部直接呼叫 `feature`/`fix`/多角色審查/`CI/CD 稽核工具`，屬於 skill 呼叫 skill，違反 EVAL-A-003；解法是這三個 skill 只負責「檢查前置條件是否齊備＋提示 user 去用哪個既有 skill」，不在 skill 內部真的程式化呼叫。這跟現有 `debug` skill「找到根因了，去用 `fix` skill」是同一種銜接模式，既有專案本來就這樣運作，不是新發明的變通，是既有模式的延伸套用。
3. ✅ 已做最小雛形：「agent teams 協作 workflow」完整範圍仍未設計，但已在 `system-design` 步驟 11 做了限定範圍的雛形（Workflow tool 多角度並行評估），細節見本檔末「Follow-up 決策」E4。

## D3 — Gate 機制：獨立 Phase Exit Criteria

| 未選方案 | 說明 | 未選原因 |
|---|---|---|
| 延伸既有 既有的品質關卡（assistant 原推薦） | 步驟11-17映射到 既有的品質關卡 五問，不新造 gate | 能避免兩份判準漂移，但 user 選了獨立方案 |
| 輕量無正式 gate | 不設 checklist | 沒有「這階段真的做完了嗎」的驗證力道 |

**⚠️ 遺留風險（已解決，見下）**：獨立 Phase Exit Criteria 與 既有的品質關卡 有內容重疊（尤其設計階段的 invariants / edge case / rollback 判準）。

**解決方案**：不做「內容分工」（曾考慮過 既有的品質關卡 管派工前 gate、Phase Exit Criteria 管階段輸出完整度，但覺得兩邊都要維護、容易改一邊漏改另一邊），改成**依路徑決定用哪一套**：
- 走完整 SDLC 流程（經過 `system-design` skill）：只用 Phase Exit Criteria，不再套用 既有的品質關卡，避免重複檢查同一件事
- 沒走完整 SDLC 流程（小型 bug fix、個人非正式專案、小工具開發，直接用 `feature`/`fix` skill）：維持現況繼續用 既有的品質關卡，不受本次設計影響，保留原有開發彈性

撰寫 `phase-1-4-discovery-design.md`／`system-design` skill 時，需在觸發條件裡明確寫出「進入本 skill 視為走完整 SDLC 流程，後續派工不再重新跑 既有的品質關卡」，避免兩邊都被觸發。

## D4 — 可移植性：不分層，直接綁既有專案

| 未選方案 | 說明 | 未選原因 |
|---|---|---|
| 分層：域中性原則 + 既有專案綁定層（比照 user 全域 CLAUDE.md 的「正本 vs 綁定層」模式） | 日後跨專案可直接重用 | user 評估現在要先定分界線設計成本過高，選擇先不分層 |

**初步驗證測試時的澄清**：用一個跟 既有業務領域 完全無關的專案構想當測試提示詞，客觀判斷後發現 9 份 skill 的 TRIGGER 條件都沒有限定「必須跟 既有業務領域 相關」，任何全新專案構想都會觸發。一度以為是漏洞，user 確認這是**預期行為**：「綁既有專案」只是指技術上接既有專案現有工具鏈，不是限定領域——公司任何要開發的項目都要走這套流程。D4 的決策本身不用改，只是文件沒把這點講清楚，已在 `SDLC_Agent協作版.md` D4 段補上澄清。

---

## Follow-up 決策：4 個未決事項收斂（8 份 skill 建立後的第二輪討論）

用 `first-principles-thinking` + `pursue-excellence` 兩個框架分析，逐項列選項、Lead 分析、user 最終選擇。

### E1 — 觸發條件分工

**Lead 分析過程中的自我修正**：原本提議「用既有 Agent Budget Table（Tier 0-3）判斷要不要走 SDLC」，但發現這有循環依賴——Tier（規模）是需求發想做完才會知道的東西，拿最終規模去決定要不要做「決定規模之前的步驟」邏輯不通。

| 選項 | 判斷依據 | 問題 |
|---|---|---|
| A. 綁定 Tier 系統 | 規模 | 循環依賴，已被 Lead 自己否決 |
| B. 用「確定性」判斷（✅ user 選中） | 問題本質/目標使用者/解決方案是否已明確 | 邏輯自洽，且跟原文 Phase 1 存在理由一致（Phase 1 的意義就是「還不知道要做什麼」） |
| C. 不額外設計 | 現有 TRIGGER 描述 | 「需求已經明確」沒有明確定義，等於沒解決 |

**落地**：`product-discovery` 的 TRIGGER/DO NOT TRIGGER 改成「問題/情境/方案任一不確定→走本 skill；都已明確→不論規模大小直接跳後面 phase」；`system-design` 補一句説明「用範圍判斷在這裡不循環，因為需求規格書已存在，範圍是已知資訊」，避免讀者誤以為跟 E1 的結論矛盾。

### E2 — 中途例外處理

**驗證（實際 grep，非印象）**：`system-design`／`requirement-scoping` 已有部分回頭語句，其餘 5 份完全沒有，行為不一致。

| 選項 | 說明 | 未選原因 |
|---|---|---|
| A. 8 份都補一行回頭規則（✅ user 選中） | 停止條件統一加「發現前面階段有問題→明確告知回哪個 phase」 | — |
| B. 只在高風險後段補 | 只加 system-design 之後 | 不一致，Phase 1-2 出問題時沒規則 |
| C. 不特別設計 | 依賴 global CLAUDE.md「三次失敗即停」 | 那條講的是重試次數，不是跨 phase 倒退，情境不同 |
| D. 建共用 reference 文件 | 8 skill 共用一份 | 違反已鎖定的 D2「8 個獨立不互相依賴」原則 |

**落地**：8 份 SKILL.md 的「停止條件」都補一行，措辭依各自上一階段調整（例如 `dev-setup` 寫「回 `system-design`」，`qa-handoff` 寫「回 `requirement-scoping`/`system-design`/`implementation-handoff`」）。

### E3 — 其他 phase 要不要補正式 exit criteria

**Lead 原本的分析與推薦**：Phase 1/2/4 是概念性產出、Phase 5-8 已有既有 quality gate 把關，覺得沒有 concrete failure 支持「全部比照 Phase 3」，**推薦選項 A「全部不補」**；分析過程中也列過「只給 requirement-scoping 補」（選項 B，因為需求規格書是後面所有階段的地基）當備選，但不是最終推薦。

**user 最終選擇「C. 全部比照 Phase 3 補齊」**——覆蓋 Lead 的選項 A 建議，選擇一致性/完整性優先。

**落地時的處理方式**：Phase 1/2/4/8（新內容型）比照 Phase 3 給出步驟級具體檢查項；Phase 5-8 中的 handoff 三份（implementation/qa/release-handoff）刻意寫成「檢查交接有沒有做對」而非「重複既有 skill 的品質標準」，避免違反 D3 已定案的「不重複檢查」原則——這是在 user 選擇的方向內，兼顧不跟 D3 自我矛盾的做法。

### E4 — Agent teams 協作 workflow

**Lead 原本的分析**：目前沒有正在發生的具體失敗（跳 phase 已被各 skill 自己的觸發條件支援；多 agent 即時協作在單一 Lead 對話模型下沒有具體案例），傾向完全延後。

**user 最終選擇「C. 現在就做最小雛形」**——覆蓋 Lead 的延後建議。

**落地**：範圍限定在 `system-design` 步驟 11（架構設計最容易有多方案分岔的地方），用 Workflow tool 做 3 個視角（效能/成本/維護性）並行產出 + 綜合評分，雙重觸發限制（步驟11 + user 明確同意用 Workflow）。**不是**完整的「8 個 phase skill 依情況彈性引用」機制——那個完整範圍的問題還沒有具體失敗案例，仍然延後，只是先在最明顯的單點做雛形。細節見 `system-design/references/agent-teams-workflow.md`。

---

## Follow-up 決策 2：Agent 派工方式（8 份 skill 建立後的第三輪討論）

觸發：user 問「agent 這邊預計可以怎麼派工」，Lead 檢查後發現既有 `agents/sa.md` 的 scope 跟 `system-design` 步驟11-15 想用的方式對不上。

### F1 — SA agent scope 落差

**發現**（實際 Read `agents/sa.md`，非印象）：`sa.md` 定位是「橋接模糊需求 → 單一 PR 可執行 spec」，輸出模板是 Goal/Scope/Acceptance Criteria/Data Contracts/Risk flags/Self-verification checklist——這是給 engineer 派工前用的，不是設計系統架構圖、ER 圖、API 規格這種多產出物的工具。但 `system-design/SKILL.md` 原本寫「SA agent 主力」，等於暗示直接沿用，格式對不上。

**第一輪 Lead 提案**（user 一度選中，後推翻）：新建一個 `system-design` 專用角色檔（比照 `sa.md` 但 scope 涵蓋架構/DB/API 設計），跟 `sa.md` 並存。

**user 推翻理由**：「感覺要特地為了 SDLC 弄一組員工，但我一樣不想要分太細，AI Agent 的設計應該不用過多員工」——擔心新角色檔造成 agent 角色數量膨脹、增加維護成本。

**重新列選項**：

| 選項 | 說明 | 未選原因 |
|---|---|---|
| 不建角色檔，設計提示詞寫進 system-design skill 本身 | 零新增 agents/*.md，prompt 範本活在 skill 的 references 裡 | user 沒選，可能覺得跟 sa.md 的既有紀律（never assume/read-only/列ambiguities）重複定義一次不划算 |
| 擴充既有 sa.md，不新建檔（✅ user 選中） | 同一個 `sa` 角色，加一個 mode 參數：mode=pr-spec（原本的）／mode=system-design（新的，5 種設計面向的輸出模板） | — |
| 接受 sa.md 原封不動的落差 | 不改任何東西，PR-spec 模板硬套在架構設計上 | 沒選，落差是真實問題（架構設計不會有「Data Contracts」這種 PR-scoped 欄位） |

**落地**：`agents/sa.md` 從 126 行擴充到 148 行，加了「Mode 選擇」段（Lead 派工時必須指定 mode）+「Step 2（system-design mode）」的緊湊表格式輸出模板（5 種設計面向：架構/DB/API/前端元件/模組拆分，每次只產出一種，不跨面向擴張）。`system-design/SKILL.md` 的流程表同步更新：步驟11-15 用 `sa`(system-design mode)，步驟16（拆分任務/開票）改用 `sa`(**pr-spec mode**)——因為票級 spec 正是 `sa.md` 原本就在做的事，不需要另外設計。

### F2 — Phase 1/2 派工邊界模糊

**問題**：`product-discovery` 步驟5、`requirement-scoping` 步驟10 原本寫「可選派 agent」，沒講明是什麼 agent、能不能改檔案。

**決定**：明確定義成 `general-purpose` + 唯讀（只給 Read/Glob/Grep/WebSearch，不給 Edit/Write）——這兩步驟都還在「調查」階段，不是真的要動手實作，agent 只做調查不做決策也不能改檔案。

---

## Follow-up 決策 3：一次性 vs 重複用維度 + Change Request Skill（第四輪討論）

觸發：user 提出一個新維度——SDLC 35 步驟裡，有些只會在專案剛開始做一次（例如蒐集原始需求，之後漏掉的東西是走 CR，不會回頭重做整段需求發想），有些則是每次新任務都要重複用（例如系統架構、資料庫設計、程式元件應該綁在一起，一次一整套）。

### G1 — 35 步驟重新逐一分類

對照原文 `SDLC_主流程版_IAO.md` 逐步過一遍：

| 步驟 | 性質 |
|---|---|
| 1-5 需求發想 | 純一次性——專案奠基，之後不會整段重跑 |
| 6-8 需求分析前半（功能清單/範圍/優先序） | 一次性為主（初版路線圖），但功能清單會隨時間增補 |
| 9 需求規格書 | **雙重性質**——初版重量級（整個第一版），之後每個新功能/CR 也要寫規格，但規模小很多 |
| 10 風險盤點 | 雙重性質，跟步驟9同理 |
| 11 系統架構 | 純一次性——不會每個功能重選技術棧 |
| 12-14 DB/API/元件設計 | 純重複用——每個新功能幾乎都會碰到這三個之一（這是 user 原本舉的例子） |
| 15 模組拆分 | 一次性為主，邊界很少變動 |
| 16 開票 | 純重複用——每個功能都要開票 |
| 17 設計文件 | **雙重性質**——初版完整文件，之後是文件的增補 |
| 18 建骨架 | 純一次性 |
| 19-20 版控策略/排程 | 策略一次性，但排程動作每次都做 |
| 21-35（開發實作→維運） | 純重複用，已經是既有 feature/fix/多角色審查/CI/CD 專案 audit 的天性 |

**關鍵發現**：問題核心不是「整個 skill 是一次性還是重複用」，而是**步驟9（需求規格書）與步驟17（設計文件）是雙重性質**——這是 CR（change request）流程真正要接住的東西。

### G2 — CR Skill 怎麼設計

**user 決定**：這個維度要真的拿來改架構（不只是加標籤），且雙重性質的部分（步驟9、17）全部收進一個新的 CR skill，`requirement-scoping`/`system-design` 保持現狀只負責專案初期的重量級版本。

三個 CR skill 定位方案：

| 方案 | 說明 | 未選原因 |
|---|---|---|
| B. 自己做輕量設計 | CR skill 內建範圍界定 + 輕量設計（`sa` system-design mode）+ 開票，是 Lead 最初的草案 | **Pattern-match 否決**：這場討論已經發生過 3 次「差點重複造第二套邏輯」——既有的品質關卡 vs Phase Exit Criteria、sa.md 差點多開角色檔、8 個 skill 的回頭規則差點又建共用文件。每次最終解法都是「別重複造，用路由/轉交」。CR 若自己做設計，會變成第二個縮小版 `system-design`，未來要再處理一次分工重疊問題 |
| C. 不開新 skill，比照 sa.md 模式在 requirement-scoping/system-design 內加 mode=light | 跟 sa.md「同角色多 mode」解法邏輯最一致 | 跟 user 已決定要開新 CR skill 的方向不一致 |
| A. 純路由/分診（✅ 選中） | CR skill 自己不做設計，核心價值是「對照既有需求規格/設計文件檢查一致性」——這件事目前沒有任何 skill 在做。判斷後分派到三條路之一：既有範圍內瑣碎變更→`sa`(pr-spec mode)寫輕量spec+開票→提醒轉`feature`/`fix`；需要新設計決策→提醒轉`system-design`只做「那一個面向」；其實是新方向→提醒轉`product-discovery` | — |

**落地**：`change-request/SKILL.md`（43 行，eval 過）。不派新 agent，沿用既有 `sa` agent 的 pr-spec mode（開票時）；不持久化既有文件，比照其餘 8 個 skill 的 Input/Output 交接原則，使用者需自行提供既有需求規格/設計文件內容才能對照。

---

## Follow-up 決策 4：外部路由文件缺口與驗證（第五輪討論）

觸發：9 份 skill 建立完成、內部一致性也複查過後，user 實際用一句新提示詞測試，結果完全沒有走到 SDLC pipeline，直接被導去舊的 `feature` 流程——這是第一次從「skill 之外」的角度檢視這套設計，而不是檢查 9 份 skill 彼此之間對不對得起來。

### H1 — 為什麼 9 份 Skill 建好了，Lead 還是不會用

**發現過程（實際 grep，非印象）**：`CLAUDE.md`「開發工作入口」表跟 `.claude/rules/skill-trigger-matrix.md`（自稱「決定要不要 invoke 某 skill 的 single reference」）兩份文件，從 9 份 Skill 建立以來就沒有任何一行提到它們，grep 兩份文件結果都是 0 命中。

**根因**：D2 決策選了「8 個獨立 phase skill，不做程式化中央 orchestrator」，路由邏輯設計上本該交給每份 Skill 自己的 TRIGGER 說明；但 Lead 實際運作時，`CLAUDE.md` 是「MUST 遵守、覆蓋預設行為」的最上層指令，`skill-trigger-matrix.md` 又自稱是唯一路由依據。兩份文件同時對新 9 個 Skill 沉默時，Lead 會直接套用舊表「新功能 → `feature`」這條最短路徑——這條路徑在文件裡是無條件陳述，沒有任何前提子句，等於把 CLAUDE.md「MUST 遵守」的權威套在一條過時的捷徑上，蓋過了 skill 自身更細緻的 TRIGGER 判斷。

**跟前四輪的差異**：D2/E1-E4/F1-F2/G1-G2 檢查的都是 9 份 Skill 彼此之間的一致性（內部一致性）；這次找到的是「skill 之外、Lead 實際依賴的路由入口文件」沒同步（外部一致性）——是不同層次的缺口，前四輪的複查方法論不會抓到這個。

**修法**：
- `CLAUDE.md`「開發工作入口」表前補一段 Step 0：問題本質/使用者/方案任一不確定 → 走 SDLC pipeline；都明確 → 直接用（現在降級為條件式子表的）Phase 5 執行層表格，並新增 SDLC Phase 1-8 + `change-request` 的路由表
- `skill-trigger-matrix.md` 新增「SDLC Pipeline Skills」表（9 列，Trigger/Should NOT trigger/Context budget 比照既有 User-Invocable Skills 表格式），Skill Priority Rules 補第 6 條（確定性判斷優先於規模判斷）

### H2 — 修復後怎麼驗證，而不是「聲稱修好了」

修完文件後直接說「應該修好了」不夠——文件寫得通不通順，跟 Lead 實際會不會照著做，是兩回事，這正是本輪一開始發現問題的根源。所以真的跑了一次測試。

**測試設計**：Lead 自己沒辦法真的重開一個 session（這輪對話已經知道全部討論脈絡，自己判斷不算冷測試，context 已被污染），改派一個完全沒有對話記憶的 fresh agent（subagent_type=`claude`），把 user 原始提示詞（含「開始開發」——比第一輪 smoke test 多出的更強行動指令詞，用來測試修復後的路由會不會還是被字面指令蓋過）原封不動餵給它。

**安全設計**：提示詞真的叫 agent「開始開發」，若路由沒修好，fresh agent 可能會真的建資料夾、寫檔案、跑 git、派 engineer，在 `既有專案` repo 裡生出一個無關的假專案。解法：判斷過程要求完全自然產生，不因為知道是測試刻意選特定答案；但判斷完之後——落在純對話型 skill（如 `product-discovery`，本身無副作用）就正常往下走，落在有副作用的 skill/動作就說明理由後立刻停手，不准真的執行。安全閘只作用在決策之後，不影響判斷過程本身。

**結果**：正確觸發 `product-discovery`，正確排除 `feature`（scope 限定既有既有專案 codebase）、`dev-setup`/`requirement-scoping`/`system-design`（各自前提條件都不滿足）。安全閘沒被觸發（product-discovery 本身無副作用），agent 正常執行 Step 1-3（產出需求清單 + 示範釐清問題）。

**誠實的保留（不 overclaim）**：agent 回報引用的判斷依據主要是 `product-discovery` 自身既有的 TRIGGER 文字，以及 CLAUDE.md 原本就有的「需求模糊→中斷問 user」自主執行原則——都是修復前就存在的機制，不是這輪新增的 Step 0 文字被逐字引用。合理推測是新結構把舊表格從「無條件頂層入口」降級成「Phase 5 條件式子表」，解除了它蓋過 skill 自身 TRIGGER 的效果，但這次測試沒辦法完全切割證明是哪個具體改動起作用；而且測試用 subagent 模擬，並非真正重開一個全新 session。若要更高確定性，需要 user 實際關閉此 session、開新 session 貼上同一句提示詞驗證。

---

## Follow-up 決策 5：Output 持久化政策反轉（第六輪討論）

觸發：user 拿一個獨立的測試專案實測整套 9 份 SDLC skill，在 `product-discovery`/`requirement-scoping` 階段主動要求把每階段討論產出寫成 `docs/` 下的 md 檔。跑完 Phase 1-2 後，user 回頭問「這是因為我要求你，還是 skill 有說要做」，Lead 如實回答：兩份 skill 的 Output 說明本來就允許純對話（例如 `product-discovery` 步驟1明寫「條列式即可，不用正式文件」），這次持久化純粹是 user 這次臨時要求，不是 skill SOP 規定。

### I1 — 是否要把「必須持久化」寫回 skill 本身

**發現**（實際 Read 三份設計文件，非印象）：`DESIGN.md`/`SDLC_Agent協作版.md`/`DESIGN-RATIONALE.md` 三份文件都白紙黑字寫著「對話式交接，skill 不負責持久化...這是給部門團隊用的公司開發流程，不綁定任何個人 MCP 工具或 Claude 專屬機制」——這是刻意的設計決策，不是遺漏。

| 選項 | 說明 | 選中 |
|---|---|:---:|
| A. 有 agentic tool 時預設持久化，手動時仍用舊管道 | 保留部門通用性，只在 Claude Code 這類場景加預設行為 | 提供但未選 |
| B. 全面改成必須持久化，刪掉部門通用性説法（✅ user 選中） | 直接把 9 份 SKILL.md 的規則改成 MUST 持久化到 docs/，不再保留「不綁定個人工具」的考量 | ✅ |
| C. 只改 product-discovery/requirement-scoping（今天實際用到的兩份） | 範圍最小 | 未選 |

**user 選擇 B 的取捨**：放棄「部門任何人（含沒裝 agentic coding tool 的同事）都能走這套流程」的原始設計目標，換取「用 Claude Code 實際跑這套流程時，產出物不會隨對話消失、可被下一輪/下一個 phase 直接引用」的實際價值。這是 user 在真實使用後的明確反轉，Lead 有先引用三份文件的原文提醒衝突，不是被動照做也不是自作主張推翻。

### I2 — docs/ 資料夾路徑要不要寫死

**發現**：Lead 第一版edit直接假設專案內有 `docs/` 資料夾慣例，user 打斷指出「沒有 docs 這種設計」——這是合理的質疑，因為 9 份 skill 是給任何專案用的通用流程，不該沒驗證就假設一個路徑慣例存在。

**釐清後結果**：user 確認就是要用 `docs/` 這個固定資料夾名稱，差別只在於「資料夾不存在時要不要直接建立」——答案是直接建立，不用先問使用者。所以最終規則是「MUST 寫進專案的 `docs/` 資料夾，資料夾不存在就直接建立」，不是退回更模糊的「專案慣用文件位置」講法。

### I3 — 落地範圍

9 份 SKILL.md 都加上「## 持久化」規則（各 phase Output MUST 寫成 `docs/` 下的 md，檔名依內容命名，資料夾不存在就直接建立）；`change-request` 額外兩處連動修正：
1. 步驟1「取得既有脈絡」從「只能靠使用者貼內容」改成「優先搜尋專案 `docs/` 資料夾，找不到才問使用者」——這是持久化政策帶來的連鎖改善，之前「不落地存檔」的前提消失了，change-request 沒有理由繼續假設沒有地方可以找
2. 步驟3「記錄分診結果」從「提醒使用者自行記錄」改成「MUST 寫進 `docs/change-log.md`」

三份 meta 設計文件（`DESIGN.md`/`SDLC_Agent協作版.md`/`DESIGN-RATIONALE.md`）的「Input/Output 交接方式」段落同步改寫，移除「不綁定個人工具/部門通用」的原始理由陳述，改為指向本段。

**保留**：本輪只反轉持久化政策本身，沒有重新設計「phase 之間要不要自動讀取對方寫好的 docs/ 檔案」這個更進一步的問題（例如 `requirement-scoping` 開始時要不要自動 Read `docs/product-discovery.md`）——目前做法是 Lead 對話中手動延續脈絡，尚未寫成 skill 規則，留待下次有具體需要再議。

---

## Follow-up 決策 6：Phase 5-8 從「轉交既有工具」改為「完全自包含」（第七輪討論）

觸發：用測試專案（Next.js）實際走到 Phase 5，`implementation-handoff` 當時的內容寫死「前置條件全部確認後：提醒使用者/Lead 針對每張票依 `feature` 或 `fix` skill 的 SOP 派工」——但 `feature`/`fix` 是既有專案 Java/Vue/Python 專屬 skill，該測試專案用不上。

### J1 — 第一次修正方向錯誤

Lead 第一版修正：加一個技術棧判斷分支，「本專案沒有對應既有流程 → MUST 先呼叫 `typescript-dev`/`python-dev` 取得品質規範」。user 立即指出這是同一種錯誤換了個對象——`typescript-dev` 一樣是 Lead 個人 `.claude/skills/` 才有的東西，不是團隊共用的保證存在物。這跟 Follow-up 決策5 反轉的「不綁定個人工具」精神是同一條線，只是這次犯在「該轉交去哪個工具」這個維度，不是「要不要持久化」。

### J2 — 「工具名稱放 CLAUDE.md 綁定層」提案，被進一步推翻

**Lead 第二次提案**：skill 本體只寫「依既有開發流程」通用字眼，實際工具名稱（`feature`/`fix`/多角色審查/`CI/CD 稽核工具`）搬去 `CLAUDE.md` 建一張「SDLC Phase 5-8 綁定表」，比照 global CLAUDE.md 既有的「正本 vs 綁定層」模式。User 一度確認這個方向可行（CLAUDE.md 綁定表本身沒問題），但隨後追問「skill 不該在裡面寫 CLAUDE.md 吧」——點出即使只是「指向 CLAUDE.md」這個動作本身，也是把 skill 綁定在 Claude Code 專屬的檔名慣例上，同一類問題換第三個地方出現。

### J3 — 最終決定：完全依 IAO 原文，不提任何既有 skill/agent/工具

User 明確拍板：「所有流程都是按照 `SDLC_主流程版_IAO.md` 去設計，不要再管現有的 skill agent了」——目的是「這一切都是要為團隊設計的，讓任何人拿到這組 skill 都能用」。

| 選項 | 說明 | 選中 |
|---|---|:---:|
| A. 呼叫既有專案專屬 skill（`feature`/`fix`/多角色審查/`CI/CD 稽核工具`） | 原始設計，D1/D2 的「避免製造第二套真相源」邏輯 | 推翻 |
| B. 呼叫個人 dev skill（`typescript-dev`/`python-dev`）作 fallback | Lead 第一次修正 | 推翻（J1）|
| C. 工具名稱搬進 CLAUDE.md 綁定層，skill 本體只留通用判斷 | Lead 第二次修正 | 推翻（J2）|
| D. Phase 5-8 完全自包含，直接執行 IAO 步驟 21-35，不提任何外部 skill/agent/工具名稱（✅ user 選中）| 跟 Phase 1-4 同一種設計方式 | ✅ |

**取捨**：放棄「Phase 5-8 不重複既有專案既有 review/gate 邏輯」這個 D1/D2 最初的核心考量，換取「9 份 skill 對任何團隊/任何技術棧都能直接用，不需要先確認對方有沒有裝對應工具」的可攜性。這是本文件第二次出現「為了通用性犧牲某個原本合理的設計理由」的模式（第一次是 Follow-up 決策5 的持久化反轉），兩次的方向剛好相反（一次為了 Claude Code 實際好用而綁定，一次為了團隊可攜而解綁），提醒：**通用性 vs 實用性的取捨沒有固定答案，每次都要重新問 user，不能套用上一次的結論**。

### J4 — 新發現的缺口：Lead-direct vs 派工沒有門檻

複查測試專案實際執行紀錄時發現：Lead 在 Phase 5 寫 `lib/repositories`/`lib/search` 等一大批檔案時，完全是 Lead-direct 自己寫完，沒有派任何 agent。原因是 `implementation-handoff` 原本的通用 fallback 只寫「Lead-direct 或派 `general-purpose` agent 依票實作皆可」，兩個選項並列、沒有判斷標準，等於沒有規則。

**落地**：比照既有專案既有 `CLAUDE.md`「自主執行原則」的 Lead-direct 門檻（`< 20 行 + 單檔 + 無 schema + 無新依賴`），抽出可攜版本補進 `implementation-handoff`/`qa-handoff`：單一票 ≤20行/單檔/無新依賴 → Lead-direct；超過 → MUST 派工，多張範圍獨立的票 MUST 平行派，不要序列一張張自己做。`qa-handoff` 另外補「至少一個獨立角度覆核」取代原本多角色審查的角色編制精神。

**落地範圍**：`implementation-handoff`/`qa-handoff`/`release-handoff`/`ops-feedback` 全部改寫為自包含流程（依 IAO 步驟 21-35 直接執行）；`product-discovery`/`system-design`/`dev-setup`/`change-request` 裡殘留的 `feature`/`fix`/`sa` agent/Apollo/Maven/CLAUDE.md/GitLab 引用一併清除；8 份 `references/phase-exit-criteria.md` + `system-design/references/agent-teams-workflow.md` 同步更新。驗證：對 9 個 skill 目錄下所有 `.md` 跑關鍵字 grep，確認 0 殘留命中。

**保留**：`agents/sa.md` 檔案本身沒有刪除，只是 SDLC 的 `system-design` 不再依賴它——`agents/sa.md` 在既有專案其他非 SDLC 場景（一般 PR spec 橋接）仍照舊使用，第三輪 Follow-up 決策2 的 F1 擴充決策在那個場景下仍然有效，只是不再是 SDLC 的一部分。「agent teams 團隊開發」的完整通用設計（多大該平行派幾個、怎麼組隊）user 已提出是下一階段議題，本輪只做了 Phase 5 的最小門檻版本，尚未展開。

## Follow-up 決策 7：白紙測試打臉、CLAUDE.md 兩個真正的源頭 bug、hook 提案被推翻（第九輪討論；第八輪 = Agent Teams 角色檔，見 DESIGN.md）

觸發：第七輪把 Phase 5-8 改完全自包含後，user 要求「真實測試，不是唬爛的」——派一個無對話記憶的白紙 agent 接手該測試專案。Agent 跟 Lead 自己先前的行為一模一樣：直接開始寫 API route 檔案，完全沒有呼叫 `implementation-handoff`。Lead 中斷測試後提案用 `PreToolUse` hook 攔截，被 user 推翻：「不是 hooks 問題吧，源頭就是問題吧，派工什麼派 claude.md 規則有沒有寫」，並釐清「團隊」的實際定義——公司同事，每人會把這組 skill/agent 裝進**自己電腦**的 Claude Code 或 Codex，且多數是 AI 新手；Codex 在他們的用法裡就是最基本用法，只讀 `AGENTS.md` 當扁平 system prompt，沒有 Claude 那種依 `description` frontmatter 自動配對的 Skill tool。

### K1 — hook 提案為什麼被推翻是對的

`PreToolUse` hook 要嘛寫在 `既有專案/.claude/settings.local.json`（個人 local scope，不隨 9 份 skill 一起分享），要嘛寫在 `.claude/settings.json`（project scope，但 Codex 不吃 Claude Code 的 hook 格式，對 Codex 使用者完全無效）。不管哪種都無法達成「任何人拿到這組 skill 都能用」——這是跟 Follow-up 決策6 的 J1/J2（`typescript-dev`、CLAUDE.md 綁定層被推翻）同一種錯誤的第三次變體：把解法綁在 Wayne 個人環境或 Claude Code 專屬機制上。

### K2 — 實際去查，找到兩個真正的源頭 bug（都在 `<你的專案>/CLAUDE.md`，非猜測，逐項 grep 驗證過）

1. **Step 0 二分法邏輯本身是錯的**：原文「問題本質/使用者/方案任一不確定→走 SDLC；三者都明確→跳去下方 Phase 5 表」。這種**已經走完 Phase 1-4、`docs/` 已有完整產出**的專案，此刻「三者都明確」自然為真（因為 Phase 1-4 的產出正是讓它們變明確）——Step 0 因此把它導去 Phase 5 表（`feature`/`fix`/`java-dev` 等既有專案專屬工具表），完全繞過 `implementation-handoff`，因為那張表裡沒有一列在講「這個專案是不是已經在 SDLC pipeline 半途」。這是二分法本身的設計缺陷，不是文字寫得不夠嚇人。
2. **Phase 5-8 那四列「何時」欄位逐列錯位一格**：實際比對 4 份 SKILL.md 的 `description:` frontmatter 後發現，`CLAUDE.md` 表格裡標成 `implementation-handoff` 那列寫的「開發完成，確認可進測試」，其實是 `qa-handoff` 自己的 trigger 原文；標成 `qa-handoff` 那列寫的「測試通過，確認可部署」，其實是 `release-handoff` 的 trigger 原文；`release-handoff` 那列同理錯位成 `ops-feedback` 的。只有 `ops-feedback` 那列剛好沒錯。對照 `.claude/rules/skill-trigger-matrix.md` 同一組 SDLC 列，四列全部正確對齊——證實只有 `CLAUDE.md` 這份表格在某次轉謄摘要時整段錯位，不是 skill 本身寫錯。

兩個 bug 疊加的結果：一個新 Lead（不論是我自己或白紙 agent）讀到「`implementation-handoff` ← 開發完成，確認可進測試」會合理推論「開發還沒完成，這行不適用我」，即使沒被 Step 0 先擋掉，也會被錯位的文字擋掉——**規則文字本身在教它跳過**，不是它不服從規則。

### K3 — 為什麼修 CLAUDE.md 還不夠

`<你的專案>/CLAUDE.md` 是 Wayne 個人專案檔案，不會跟著 9 份 skill 一起分享給同事；而現在能讓 Lead 在動手前檢查「有沒有 skill 適用」這件事，實際上是靠 Wayne 個人全域設定裡的 `using-superpowers` meta-skill（`~/.claude/skills/`，插件性質）在撐——這同樣不會出現在同事自己的 Claude Code（除非他們也裝了同一個插件），Codex 使用者則完全沒有這層機制，只讀 `AGENTS.md` 扁平文字。真正可攜的機制必須：(a) 不依賴 Skill tool 的自動配對，改用「檢查 `docs/` 資料夾現況→對表→直接 Read 對應 SKILL.md 檔案並照做」這種機械式、任何工具都能執行的動作（Read 是兩邊都有的基本能力）；(b) 內容本身要能整段複製貼上到任何團隊自己的 `CLAUDE.md`/`AGENTS.md`，不能只活在 Wayne 的專案裡。

### K4 — 落地

- **`<你的專案>/CLAUDE.md`**：Step 0 改三分法（先查 `docs/` 有無 SDLC 產出物 → 決定走哪條路，不再只憑「問題清不清楚」）；Phase 5-8 四列「何時」全部改成「`docs/` 現況」（例如「有 dev-setup.md，`handoff-log.md` 無 Phase 5 記錄」），可直接檢查而非憑印象。這份是 Wayne 自己的落地示範，不是團隊共用件。
- **`implementation-handoff`/`qa-handoff`/`release-handoff`** 的持久化段各加一行：MUST 用固定標頭（`## Phase 5 — Implementation`/`## Phase 6 — Testing`/`## Phase 7 — Release`）分節寫入共用的 `docs/handoff-log.md`——沒有這個，CLAUDE.md 新表格裡「檢查有沒有 Phase 5 記錄」這句話本身無從執行。
- **團隊可攜的部分**：寫進 `DESIGN.md` 第九輪，用「docs/ 現況 → 對應 SKILL.md」的同一張表，但語氣改成可直接複製進任何團隊自己 `CLAUDE.md`/`AGENTS.md` 的形式，動作寫成「打開並讀取該 SKILL.md 檔案」而非「觸發某個 skill」——這樣 Codex 使用者一樣能照做，不需要 Skill tool。發布/分裝方式（獨立 repo/整包複製/submodule）user 尚未決定，本輪只確保內容本身寫在對的地方、語氣中立，之後決定怎麼發都不用重寫內容。
