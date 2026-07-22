# SDLC Orchestrator — 設計摘要

> 狀態：**9 份 Skill + 3 份角色檔 + 2 份共用 references 已實作完成**（8 個 phase skill + 1 個 change-request 分診 skill；角色檔 `agents/sdlc-implementer|sdlc-reviewer|sdlc-verifier.md`；共用 `references/agent-teams.md` + `references/severity-format.md`）。細節理由與被否決方案 → `DESIGN-RATIONALE.md`（需要時再看）。
> 來源：`SDLC_主流程版_IAO.md`（8 階段 35 步驟 SDLC 流程）。
> 實際檔案：安裝時所選 `skills/` 根目錄下的 `{product-discovery,requirement-scoping,system-design,dev-setup,implementation-handoff,qa-handoff,release-handoff,ops-feedback,change-request}/SKILL.md`

## 這是什麼

把 35 步驟 SDLC 流程設計成**領域中立、可攜的** agent 協作 skill——任何團隊/專案拿走這 9 份都能直接用，不綁定任何特定工具或既有 skill（第七輪已定案，見下）。Phase 1-8 全部自包含，直接依 IAO 原文步驟執行。

**為什麼是 9 份而不是 35 份**：每個「階段」（原文 8 大階段）對應一份 skill，不是每個步驟一份——階段內的步驟是同一段緊密相連的工作流（例如步驟 11-17 同屬設計階段，最後彙整成同一份設計文件，拆開會打散同一個工作流）。第 9 份 `change-request` 是額外新增，接住步驟 9/17「初版重量級、之後變更輕量版」的雙重性質缺口。完整逐階段理由（含每個 phase 為什麼是這個顆粒度）→ `SDLC_Agent協作版.md` D2.5 段。

## 4 個決策

| # | 決策 | 一句話理由 |
|---|---|---|
| D1 範圍 | 全流程包裹（8 階段全涵蓋） | Agent 協作要涵蓋全流程，非只做前段規劃 |
| D2 架構 | ~~單一 orchestrator + phase references~~ → **已修訂：8 個獨立 phase skill，不加前綴命名** | 便於未來設計 agent teams workflow 依情況引用不同 skill；修訂細節與風險 → DESIGN-RATIONALE.md |
| D3 Gate | 獨立 Phase Exit Criteria | 不重用既有 既有的品質關卡；已解決重疊問題：改成「依路徑決定用哪套」——走完整 SDLC 流程只用 Phase Exit Criteria，沒走完整流程（小型 fix/個人專案/小工具）維持用既有 既有的品質關卡，兩者不同時套用同一件工作 |
| D4 分層 | ~~不分層，直接綁既有專案~~ → **已被第七輪修訂**：skill 本體完全領域中立，既有專案綁定只放 `<你的專案>/CLAUDE.md`「SDLC Phase 5-8 綁定」段 | 原「先求落地」；第七輪測試專案實測證明綁定要拆到 CLAUDE.md 層 |

## 生命週期:創世 vs 演進（第十一輪，2026-07-10）

**洞見**（user）：管線本質是「線性位置」模型（你在第幾階段），但真正該分的是兩種生命週期——**一次性「創世」**（蒐集需求/技術選型/整體架構，新專案做一次、舊專案永遠不做）vs **重複用「演進」**（每個功能：需求-delta → 設計-delta[DB/API/元件一組] → 實作 → 測試 → 部署，永遠迴圈）。

**戳到的真缺口**：`change-request`（演進入口）原本寫死「找不到 `docs/` 既有文件 → 當成新方向退回 `product-discovery`」。承重假設 = 專案有 genesis 期文件。**舊專案（跑很久、從沒走過這套 SDLC、`docs/` 空）要加一個需設計的新功能時，會被誤判成全新構想送去需求發想**——具體失敗場景真實存在（任何成熟 codebase 採用這套流程的第一天）。

**最小路由修法**（不拆新 skill，維持 `change-request` 只分診不做設計）：
- 分辨軸從「`docs/` 有沒有文件」改成「有沒有既有系統」。既有程式碼就算系統存在。
- `change-request` 步驟1 改三層 fallback：docs 文件 → 程式碼現況當基線 → 只有純全新構想才退 `product-discovery`。
- 「需要新設計決策」仍路由到 `system-design` 只做該面向，且它的 `docs/design.md` 產出順手替沒文件的舊專案補上基線，下次變更就有得對照。
- 四個入口同步：`change-request/SKILL.md`、`<你的專案>/CLAUDE.md` Step 0（拆創世/演進）、本檔 Entry Protocol 第一條、`測試專案的 AGENTS.md`。

**為什麼不拆新 skill**：第四輪已三次因「別重造第二套邏輯」否決拆分。這個洞見的正確落點在路由層（誰接住既有專案的變更），不是再切 skill——`system-design` 早已把設計活動（架構/DB/API/元件/模組）grouped 成一份，grouping 需求已滿足。

## Phase → Skill 對應

| Phase | 步驟 | Skill 名稱 | 誰做 |
|---|---|---|---|
| 1 需求發想 | 1-5 | `product-discovery` | Lead 對話為主 |
| 2 需求分析 | 6-10 | `requirement-scoping` | Lead + user 拍板 |
| 3 設計 | 11-17 | `system-design` | Lead-direct 或派 `general-purpose` agent（依範圍判斷，見 SKILL.md）；步驟17 Lead彙整 |
| 4 開發前準備 | 18-20 | `dev-setup` | Lead-direct，版控步驟只能列清單（NEVER 自動建 branch/push） |
| 5 開發實作 | 21-24 | `implementation-handoff` | Lead-direct 或派工（依票範圍：≤20行/單檔 → Lead-direct，較大範圍 MUST 派工且平行） |
| 6 測試 | 25-28 | `qa-handoff` | 同上；獨立審查角度不可省略（測試者需獨立於實作者視角） |
| 7 部署 | 29-32 | `release-handoff` | Lead 列檢查清單，**部署動作 user 手動觸發**（安全紅線） |
| 8 維運 | 33-35 | `ops-feedback` | Lead 彙整回饋，觸發下一輪 Phase 1 |

**+ `change-request`**（第四輪新增，不對應特定步驟編號，是跨 phase 的分診 skill）：專案已有既有需求規格/設計文件、出現新變更時觸發，判斷該走「輕量開票直接進開發」/「回 system-design 做單一設計面向」/「其實是新方向回 product-discovery」三條路之一，自己不做設計。

## Input/Output 交接方式

**已反轉（第六輪，見 DESIGN-RATIONALE.md「Follow-up 決策 5」）**：skill **MUST 負責持久化**。每個 phase skill 引導該階段該問什麼、該產出什麼概念，且**必須**把實際的需求規格書 / 設計文件 / ER 圖等產出物寫成 markdown 檔案存進專案的 `docs/` 資料夾（專案尚無此資料夾就直接建立，不用先問使用者），不可只留在對話紀錄裡；檔案不存在視為該階段未完成。原本「不綁定個人工具、給部門通用」的考量已被 user 明確否決，理由與細節見 `DESIGN-RATIONALE.md`。

## 未決事項（第二輪收斂結果，全部已定案）

第二輪用 first-principles-thinking + pursue-excellence 兩個框架收斂，完整選項比較與分析過程 → `DESIGN-RATIONALE.md`「Follow-up 決策」段。

| # | 議題 | 結果 |
|---|---|---|
| E1 觸發分工 | product-discovery 用「確定性」判斷取代「規模」判斷（規模判斷有循環依賴：規模要等做完需求發想才知道） | `product-discovery`/`system-design` SKILL.md 已改 |
| E2 中途例外 | 8 份 SKILL.md 停止條件統一補一行「發現前面階段有問題→明確告知回哪個 phase」 | 8 份 SKILL.md 已改 |
| E3 Exit Criteria 補齊 | 全部比照 Phase 3 補正式 checklist（Lead 原建議「全部不補」，user 選擇更完整的方案，覆蓋 Lead 建議） | 7 份新 `references/phase-exit-criteria.md` 已建立 |
| E4 Agent teams | 現在就做最小雛形：Workflow tool 做「system-design 步驟11 多角度並行評估」，範圍限定不擴及其他 phase | `system-design/references/agent-teams-workflow.md` 已建立（**第七輪已移除，不在本包內**）|

## 第三輪：Agent 派工方式（全部已定案）

完整討論過程（含 user 的「不想要太多 agent 角色」顧慮、被推翻的方案）→ `DESIGN-RATIONALE.md`「Follow-up 決策 2」段。

| # | 議題 | 結果 |
|---|---|---|
| F1 SA agent scope 落差 | 既有 `sa.md` 是單一 PR spec 用途，跟 system-design 步驟11-15 要的架構/DB/API/元件/模組設計產出不貼合。**不新建角色檔**（user 明確不想要為了 SDLC 多開一組「員工」），改成擴充既有 `sa.md` 加一個 system-design mode，同一角色雙用途 | `agents/sa.md` 已改（148行，eval過） |
| F2 Phase1-2 派工邊界模糊 | product-discovery/requirement-scoping 的「可選派 agent」明確定義成 `general-purpose` + 唯讀（Read/Glob/Grep/WebSearch，不給 Edit/Write） | 兩份 SKILL.md 已改 |

## 第四輪：一次性 vs 重複用 + Change Request Skill（全部已定案）

完整討論過程（含 35 步驟逐步分類、pattern-match 發現、被否決的兩個方案）→ `DESIGN-RATIONALE.md`「Follow-up 決策 3」段。

| # | 議題 | 結果 |
|---|---|---|
| G1 一次性 vs 重複用 | 35 步驟重新對照分類：Phase 1（1-5）+ 步驟11/15/18 純一次性；步驟12-14/16 + Phase 5-8 純重複用；**步驟9（需求規格書）跟17（設計文件）是雙重性質**——初版重量級、之後每次變更是輕量版，這是問題核心 | 分類記錄於 DESIGN-RATIONALE.md，未改動既有 8 個 skill 的結構 |
| G2 雙重性質怎麼接 | 新建 `change-request` skill 專門接住「專案進行中的新變更」。核心定位選了「純路由/分診」（否決「自己做輕量設計」——pattern-match 發現那會重蹈 既有的品質關卡/sa.md 角色/回頭規則三次都出現過的「重複造第二套邏輯」錯誤）| `change-request/SKILL.md` 已建立（43行，eval過） |

## 初步驗證測試（第一輪：user 給提示詞，Lead 客觀判斷觸發結果）

**測試1**：「全新專案，建立專案資料夾。需求是開發一套（跟本業無關的）網站...」

- 客觀判斷結果：觸發 `product-discovery`（使用者情境未講清楚，符合 TRIGGER 條件），`dev-setup` 正確地**沒有**被字面關鍵字「建立專案資料夾」誤導提前觸發（因為它的 TRIGGER 明確要求「設計文件已確認」）
- 發現一個追問點：9 份 skill 的 TRIGGER 條件都沒有限定「必須跟既有專案/既有業務領域 有關」，任何全新專案構想都會觸發
- **user 確認：這是預期行為，不是漏洞**——這套流程設計目的就是「公司任何要開發的項目都要走這個流程」，不限定 既有業務領域，之前只是沒把這件事明講進文件

## 全面複查（第四輪後，新增 change-request 引發的跨檔案一致性檢查）

實際跑指令核對（非印象），找到並修正 2 處真實缺口：
1. `system-design/SKILL.md` 觸發條件原寫「不適用：小範圍功能改動」，但 `change-request` 會把「只需要單一設計面向」（本質上是小範圍）導去 `system-design`，兩份文件互相矛盾 → 已改：區分「完全不涉及新設計決策」（不適用）vs「只涉及單一設計面向」（適用，只派 `sa` agent 做那一面向）
2. `ops-feedback` 步驟35/下一步仍停留在「小修正→fix；新需求→product-discovery」舊的兩分法，沒接進新增的 `change-request` 中間路徑 → 已改：三分法（小修正→fix／既有規格內變更→change-request／全新方向→product-discovery）

## 第五輪：外部路由文件缺口與驗證

**發現**：`CLAUDE.md`「開發工作入口」表與 `.claude/rules/skill-trigger-matrix.md`（自稱唯一路由依據）從 9 份 skill 建立以來都沒提到它們，Lead 會直接套用舊表「新功能 → `feature`」跳過整個 pipeline——這跟「全面複查」查的 9 份 skill 彼此矛盾是不同層次的缺口（外部路由 vs 內部一致性）。完整討論過程 → `DESIGN-RATIONALE.md`「Follow-up 決策 4」段。

**修法**：`CLAUDE.md` 補 Step 0 確定性判斷 + SDLC Phase 1-8/`change-request` 路由表（原表格降級為條件式的 Phase 5 子表）；`skill-trigger-matrix.md` 新增「SDLC Pipeline Skills」表 + Skill Priority Rules 第 6 條。

**修復後冷測試驗證**：派一個無對話記憶的 fresh agent，用 user 原始提示詞（含「開始開發」這個比第一輪 smoke test 更強的行動指令詞）實測 → 正確觸發 `product-discovery`，正確排除 `feature`/`dev-setup`/`requirement-scoping`/`system-design`。**誠實保留**：agent 引用依據主要是各 skill 既有 TRIGGER 文字 + CLAUDE.md 既有「需求模糊→中斷問 user」原則，非逐字引用新增文字，屬強力佐證非可完全切割因果的證明；且用 subagent 模擬，非真正重開 session。細節 → `DESIGN-RATIONALE.md`「Follow-up 決策 4」H2 段。

## 第七輪：Phase 5-8 從「轉交既有工具」改為「完全自包含」（推翻 D1/D2 的既有工具假設）

**觸發**：用測試專案實際走 Phase 5 時，發現 `implementation-handoff` 寫死「轉交 `feature`/`fix` skill」——但 該測試專案是 Next.js 專案，`feature`/`fix` 是既有專案 Java/Vue 專屬工具，根本用不上。修第一版時 Lead 一度改成「本專案沒有既有流程 → 呼叫 `typescript-dev`」，被 user 指出這**换了個對象犯同一種錯**——`typescript-dev` 一樣是綁在 Lead 個人 `.claude/skills/` 的東西，其他同事拿到這 9 份 skill 時不一定有。user 明確拍板：**「所有流程都按照 SDLC_主流程版_IAO.md 去設計，不要再管現有的 skill/agent」**——這是給團隊用的通用流程，任何人拿到都要能用。

**決定**：`implementation-handoff`/`qa-handoff`/`release-handoff`/`ops-feedback` 從「檢查前置條件 + 轉交既有工具」整個改成跟 Phase 1-4 一樣**自包含**——直接依 IAO 步驟 21-35 的 Input/Action/Output 執行，不轉交任何外部 skill/agent/工具名稱：
- `implementation-handoff`：步驟21-24（DB建置/後端API/前端元件/頁面組裝）自己直接做，不轉交 `feature`/`fix`
- `qa-handoff`：步驟25-28（單元/整合/驗收/回歸測試）自己直接執行測試，不轉交多角色審查 review
- `release-handoff`：步驟29-32（部署前檢查/staging/production/煙霧測試）自己列檢查清單執行，只有「部署動作本身」仍要求人工手動觸發（這是安全紅線，不是既有工具問題）
- `ops-feedback`：拿掉 Elasticsearch/`fix` skill 等具體工具提及，改generic 描述

**新增的判斷標準（原本沒有,是這輪補上的缺口）**：發現 Lead 自己在測試專案全部 Lead-direct 完成 `lib/repositories`/`lib/search` 等大量檔案，完全沒有派工——因為原本的通用 fallback 只寫「Lead-direct 或派 general-purpose agent 皆可」，沒有給判斷門檻。這次補上**具體、可攜的 Lead-direct vs 派工門檻**：單一票 ≤20行/單檔/無新依賴 → Lead-direct；超過 → MUST 派工，多張獨立票 MUST 平行派，不要序列一張張自己做。`qa-handoff` 同理補上「至少一個獨立角度覆核」的門檻，取代原本的多角色審查角色編制。

**波及範圍**：不只 Phase 5-8，`product-discovery`/`system-design`/`dev-setup`/`change-request` 裡殘留的 `feature`/`fix`/`sa` agent/Apollo/Maven/CLAUDE.md/GitLab 等具體引用也一併清除（`system-design` 原本重度依賴 `agents/sa.md` 雙 mode 設計，這次改成通用的 Lead-direct/派工判斷，`agents/sa.md` 擴充決策——第三輪 F1——在 SDLC skill 範圍內視為已被取代，`agents/sa.md` 本身留給既有專案其他非 SDLC 場景繼續用）。8 份 `references/phase-exit-criteria.md` + `agent-teams-workflow.md` 同步清除。

**驗證**：`grep -rniE "feature\`|fix\`|多角色審查|CI/CD 稽核工具|CLAUDE\.md|Elasticsearch|Apollo|既有專案|Maven|sa agent|前端專案|既有的品質關卡|GitLab|CI/CD 專案 |後端主專案"` 對 9 個 skill 目錄下所有 `.md` 檔案跑過，確認 0 命中。

## 第八輪：Agent Teams 正式架構（3 份角色檔 + 領域中立嚴重度格式）

**觸發**：user 指出「agent 不是應該放 agent 資料夾裡面嗎」——第七輪的 `agent-teams.md` 只是分級表，沒有真正的角色定義檔。參考 `另一個既有專案` 做法但不照抄：`另一個既有專案` 角色檔的技術棧 checklist 學不來（通用版不知道使用者技術棧），但**立場**（如 verifier「預設有問題直到證明清白」）與技術棧無關，可以搬。

**落地**：3 份角色檔進安裝時獨立選定的角色根目錄（`sdlc-implementer`＝先探索專案慣例再實作＋品質門禁 0 issues；`sdlc-reviewer`＝建設性審查；`sdlc-verifier`＝對抗性驗證，target=security|evidence 切換）。Claude Code 放在 `.claude/agents/` 時可註冊成 agent 型別；Codex 標準位置或自訂位置則作為 embed 給 generic agent 的角色定義。實際路徑由 Entry Protocol 的 `<agents-root>` 提供，不假設與 skills 同層。配套把 severity 精神改寫成技術棧無關版 → `references/severity-format.md`。**適用範圍**：Tier 分級只對 Phase 3/5/6 有意義（工作單元可拆可平行）；Phase 1/2/4 是序列人機對話，天生不適用，非遺漏。

## 第九輪：白紙測試打臉 + CLAUDE.md 兩個源頭 bug + 團隊可攜的 Entry Protocol

**觸發**：第七輪修完後用白紙 agent 真實測試測試專案，發現它跟 Lead 自己一樣直接跳過 `implementation-handoff` 開始寫 code。Lead 提案用 `PreToolUse` hook 補救，被 user 推翻——hook 綁在 Wayne 個人 `settings.local.json`/Claude Code 專屬機制上，同事裝在自己電腦的 Claude Code 或 Codex 都吃不到，是跟第七輪 J1/J2 同一種「解法綁在個人環境」錯誤的第三次變體。完整討論過程（K1-K4）→ `DESIGN-RATIONALE.md`「Follow-up 決策 7」。

**實際找到的源頭**（非猜測，逐項 grep 驗證）：`<你的專案>/CLAUDE.md` 有兩個真正的 bug，不是 hook 能解的：
1. Step 0「問題清楚→跳過 SDLC」二分法本身邏輯有洞——已經走完 Phase 1-4 的專案，此刻問題自然清楚，卻因此被導去跳過 Phase 5-8
2. Phase 5-8 那四列「何時」文字逐列錯位一格，標成 `implementation-handoff` 的那列實際寫的是 `qa-handoff` 自己的 trigger 原文（`skill-trigger-matrix.md` 同一組列沒有這個錯位，只有 `CLAUDE.md` 這份表格轉謄時錯位）

**落地**：
- `<你的專案>/CLAUDE.md` Step 0 改三分法 + Phase 5-8 四列改成「`docs/` 現況」可檢查的寫法（Wayne 自己的落地示範，非團隊共用件）
- `implementation-handoff`/`qa-handoff`/`release-handoff` 持久化段各加一行：共用的 `docs/handoff-log.md` MUST 用固定標頭（`## Phase 5/6/7 — ...`）分節，讓「有沒有這個 phase 的記錄」變成可檢查而非憑印象
- **團隊可攜的 Entry Protocol**（下方區塊）——不依賴 Skill tool 自動配對，因為同事的 Codex 用法只讀 `AGENTS.md` 扁平文字，沒有 Claude 那種 description frontmatter 自動觸發；改用「檢查 `docs/` 現況 → 對表 → 直接 Read 對應 SKILL.md 並照做」這種兩邊工具都能執行的機械動作

### Entry Protocol（可直接複製進任何團隊自己的 `CLAUDE.md` 或 `AGENTS.md`）

```
開始任何實作/測試/部署/維運工作前，先檢查你要動的那個程式專案有沒有 docs/ 資料夾。

規則由上而下逐條檢查，第一條命中就採用，不再往下看。
本次安裝的 skill 根目錄是：{{SKILLS_ROOT}}
本次安裝的角色檔根目錄是：{{AGENTS_ROOT}}
下面的 `<skill-root>` 都代表這個完整路徑；不要自行改猜 `.claude/skills` 或 `.agents/skills`。
下面的 `<agents-root>` 都代表角色檔的完整路徑；它可以與 `<skill-root>` 來自不同工具或自訂目錄。

- docs/handoff-log.md 裡有任何一節標著「進行中」或沒有寫「狀態：完成」→ 那一節就是目前的階段，
  打開並讀取 <skill-root>/<該階段對應的 skill>/SKILL.md 續作（不要因為標頭已存在就當成做完了）
- 沒有 docs/ 或 docs/ 裡沒有任何 SDLC 產出物，先分辨這是「全新構想」還是「既有系統」：
  - 全新構想、還沒有任何既有程式碼/系統 → 若問題/使用者/方案任一不確定，從
    <skill-root>/product-discovery/SKILL.md 開始；三者都已明確而想直接動手也可以，
    但那等於自願跳過需求與設計階段、不會留下 docs/ 產出物，下次接手會被判定回第一階段
  - 已經有在跑的既有程式碼（老專案採用這套流程，只是還沒補 docs/）→ 不要當成新專案。
    瑣碎小改直接動手；需要新設計決策或範圍不確定 → 打開並讀取
    <skill-root>/change-request/SKILL.md，照做（它會用程式碼現況當基線分診）
- 有 docs/product-discovery.md，沒有 docs/requirements-spec.md
  → 打開並讀取 <skill-root>/requirement-scoping/SKILL.md，照做
- 有 docs/requirements-spec.md，設計文件還沒齊 → 打開並讀取
  <skill-root>/system-design/SKILL.md，照做
  （設計算完成的條件：有 docs/design.md；或 architecture.md 加上 db-schema.md／api-spec.md／
    components.md／modules.md 其中任一份；或 architecture.md 裡明確寫了本專案不涉及
    資料庫／對外介面。單獨一份 architecture.md 又沒有這類聲明，不算完成）
- 有設計文件，沒有 docs/dev-setup.md → 打開並讀取 <skill-root>/dev-setup/SKILL.md，照做
- 有 docs/dev-setup.md，docs/handoff-log.md 沒有「## Phase 5」完成記錄
  → 打開並讀取 <skill-root>/implementation-handoff/SKILL.md，照做
- docs/handoff-log.md 有「## Phase 5」完成記錄，沒有「## Phase 6」記錄
  → 打開並讀取 <skill-root>/qa-handoff/SKILL.md，照做
- docs/handoff-log.md 有「## Phase 6」通過記錄，沒有「## Phase 7」記錄
  → 打開並讀取 <skill-root>/release-handoff/SKILL.md，照做
- 已上線 / 有 docs/feedback-log.md，且沒有任何進行中的階段
  → 打開並讀取 <skill-root>/ops-feedback/SKILL.md，照做
- （跨階段）專案已有 docs/ 需求規格或設計文件，現在出現新的變更需求、不確定是否在既有範圍內
  → 打開並讀取 <skill-root>/change-request/SKILL.md，照做

docs/ 已經有任何 SDLC 產出物，就代表這個專案已經在流程裡，不可以跳過中間的階段。
完成任一階段後，回到本規則重新判斷下一步，不要憑對話印象直接續做。
不確定現在在哪個階段時，先看 docs/ 裡實際有哪些檔案，不要憑印象判斷。
```

**分發方式已決定（2026-07-10 user 拍板）：整包目錄複製**——同事把這包（9 份 skill 目錄 + 3 份 `agents/sdlc-*.md` + `sdlc-orchestrator/references/` 兩份共用檔）複製進安裝時分別選定的 skill 與角色根目錄；可用 Claude Code 或 Codex 標準位置，也可自訂精確目錄。Entry Protocol 會同時記錄兩個實際路徑，再寫進同一 scope 對應的 `CLAUDE.md` 或 `AGENTS.md`。完整安裝步驟 → `INSTALL.md`。

## 第十二輪：第一次真實全流程運轉（2026-07-10）

專案資料夾清空、user 本人當需求方真跑整套流程，第一棒（需求發想）當場暴露問題，立了三條規矩（完整記錄 → `SDLC_Agent協作版.md` 第十二輪段）：

1. **提問必須選項化（Phase 1-4 + 分診確認一體適用）**：`product-discovery`/`requirement-scoping`/`system-design`/`dev-setup` 各加獨立「## 提問規則」段，`change-request`/`ops-feedback` 的路由確認同規則——每題附 2-4 個具體選項（最建議的放第一個標「建議」），使用者勾選或回編號即可，自由補充永遠允許；一次一批 ≤5 題。禁止純開放式問題轟炸。
2. **跑流程不需要派工**：正常用法 = 使用者自己開對話（平價模型即可），skill 觸發 → 做完該階段 → 關掉；下次開新對話接下一階段。多 AI 派工只出現在 Phase 5/6 票量大時（由該階段依 `references/agent-teams.md` 分級表派）。
3. **FAQ：「35 步驟綁 9 份，會不會把本可獨立的步驟綁死？」**——綁在一起的步驟本來就是同一份產出物的連續形成過程；真需要單獨跑的已有專門入口（`change-request` 分診後轉 `system-design` 只做單一面向），不預先拆。

## 下一步

1. ✅ 9 份 SKILL.md + 8 份 phase-exit-criteria.md + 1 份 agent-teams-workflow.md，全部完全領域中立，eval check 全過
2. ✅ 第五輪：`CLAUDE.md` + `skill-trigger-matrix.md` 外部路由缺口已修復並經冷測試驗證
3. ✅ 第六輪：Output 持久化政策反轉（不負責持久化 → MUST 持久化到專案 `docs/`）
4. ✅ 第七輪：Phase 5-8 從「轉交既有既有專案工具」改為「完全自包含、純 IAO 原文執行」，並補上通用的 Lead-direct/派工判斷門檻（見上）
5. ✅ Agent teams 派工分級（`references/agent-teams.md`）：4 個 Tier（Lead-direct/單一agent/平行多agent/高風險三角度審查）+ 平行派工原則 + retry 而非重派；`implementation-handoff`/`qa-handoff`/`system-design` 已指向此檔
6. ✅ 第八輪：Agent Teams 正式架構——3 份 `sdlc-*` 角色檔 + `references/severity-format.md`（見上）
7. ✅ 第九輪：白紙測試發現 `CLAUDE.md` Step 0 二分法 + Phase 5-8 表格錯位兩個源頭 bug；`handoff-log.md` 固定標頭；團隊可攜 Entry Protocol（見上）
8. ✅ 分發方式：整包目錄複製（2026-07-10 user 拍板，安裝步驟 → `INSTALL.md`）
9. ✅ 白紙重測（2026-07-10）：Claude 與 Codex 兩條路徑都 PASS——fresh agent 照 Entry Protocol 查 `docs/` 正確判定 Phase 4（有設計文件、缺 dev-setup.md）並進 `dev-setup`，未跳去寫程式；Claude 路徑並實際產出 `docs/dev-setup.md`。測試專案現況：Phase 4 已補檔，下一步 Phase 5
10. ✅ 第十一輪：創世/演進兩種生命週期——分辨軸改「有沒有既有系統」、`change-request` 三層 fallback、`CLAUDE.md` Step 0 三分法、跨包變更 SOP（見上「生命週期」段）
11. ✅ 第十二輪：真實全流程運轉立三規矩——提問選項化（6 份 skill 落地）、跑流程免派工、35→9 FAQ（見上）
12. ✅ 第十三輪（2026-07-10）：發佈前三軍交叉稽核（內部一致性/文件同步/發佈包 parity）——設計本體 0 重大問題，12 處 meta 文件收尾修復，pack 重打；冷啟動安裝實測進行中（完整記錄 → `SDLC_Agent協作版.md` 第十三輪段，內部檔）
13. ✅ 派工模型策略 + dev skill 引用（2026-07-10 user 指示）：`agent-teams.md` 新增「模型選擇」（sonnet 預設、單票 ≥2 高複雜信號才 opus、Tier/模型兩軸獨立）與「派工 prompt 附帶技術棧 dev skill」兩節；`sdlc-implementer.md` Step 1 新增第 4 項（讀取 dev skill 規範，prompt 附路徑優先、自查 `.claude/skills/` 為輔）；`INSTALL.md` 補「Phase 5/6 派工說明（權限與模型）」——同事卡權限提示不是流程壞掉
