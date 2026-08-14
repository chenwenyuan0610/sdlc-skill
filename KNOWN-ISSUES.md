# 已知問題（2026-07-31 版）

這一版經過三輪獨立稽核（三個沒有背景知識的審視者分別走劇本、做對抗性破壞、做跨檔逐項比對），找出約 50 個問題。**會在生產環境造成實際損害的 6 個已經修掉**，其餘照實列在下面。

**為什麼還是發出來**：這些問題不會毀東西，但**會讓你在某些情況下卡住或判不出來**。先知道它們在哪，比撞到才發現快。

撞到任何一條 → 照規則登記進 `skills/sdlc-orchestrator/references/framework-defects.md` 的登記簿（那個檔自己就是登記簿，直接 append 一列）。

---

## 已修掉的（本版不會發生）

| 問題 | 修法 |
|---|---|
| 覆核角色宣稱唯讀，實際握有 shell | `sdlc-reviewer` 工具收成 `Read/Glob/Grep`（技術上真的寫不了東西）；`sdlc-verifier` 保留 `Bash`（`target=evidence` 要重跑指令才驗得了證據）但**明文標示它沒有工具層限制、不得在自動核准模式下派它** |
| 步驟 21「建立資料庫、資料表」沒有環境界定 | 動手前 MUST 先確認連線目標並向使用者複述；**MUST NOT 對共用 dev／staging／production 執行結構變更** |
| Phase 5／6 沒有版控紅線（原本只寫在演進模式永遠不會進的 Phase 4） | 兩個 phase 各補「NEVER 自動 commit／push／建 branch／開 MR」 |
| 寫 `docs/` 產出物沒有防覆寫，而檔名是最常見的既有文件檔名 | 四個會寫 `docs/` 的 phase 各補「同名檔已存在 MUST NOT 直接覆寫」 |
| 「綁定層優先，一律照綁定走」可以蓋掉「部署 MUST 人工觸發」這條紅線 | 明文「綁定層只能加嚴，不得放寬；綁定表指定的是按哪個按鈕，不是可以由 AI 代按」 |
| 煙霧測試退版仍可寫「狀態：完成」 | 只有綠燈才可寫完成；退版維持「進行中」並回 Phase 5 修 |

---

## 還沒修的（照字面走會卡住或判不出來）

### 流程走不通

| # | 問題 | 你會遇到什麼 | 先這樣繞 |
|---|---|---|---|
| 1 | **產出物檔名寫「例如」，但路由拿它當唯一機械判定依據** | `product-discovery` 說「例如 `docs/product-discovery.md`」，而入口判定「只看 `product-discovery.md` 這一個檔」。你命名成別的，下次定位就判「不在流程裡」 | **檔名照字面用**：`product-discovery.md`／`requirements-spec.md`，不要改 |
| 2 | **設計文件檔名三處各列一套** | `system-design` 列了 `logic-flow.md`，但入口的完成判定式裡沒有它；判定式裡的 `components.md`／`modules.md` 反而沒被 `system-design` 命名 | 產出 `architecture.md` ＋ `db-schema.md` 或 `api-spec.md`，判定式才認得 |
| 3 | **`handoff-log.md` 沒有「這次變更」的概念** | 第二次以後的變更：上一次留下的 Phase 5／6「完成」還在，新變更寫完 code 之後定位會判「Phase 6 已通過、無 Phase 7」→ **送去部署一個沒測過的變更** | 每次新變更**手動把 `handoff-log.md` 的舊分節改名**（例 `## Phase 5 — Implementation（變更 A）`），或開新檔分卷 |
| 4 | **`system-design` 的 exit-criteria 沒有演進模式** | SKILL 說演進「只要三項」，exit-criteria 卻無條件要 ER 圖／元件清單／模組劃分 | 演進模式以 **SKILL.md 的三項為準**；exit-criteria 只當創世模式的清單 |
| 5 | **「瑣碎變更直接進開發」是死巷** | `change-request` 說瑣碎變更不用分診直接開發；`implementation-handoff` 說沒有輕量 spec 就回去分診 | 瑣碎變更也走一次 `change-request`，寫一行 spec 就好 |
| 6 | **`NEEDS WORK` 有一條出不來** | 因「Verified Clean 不完整」被判 NEEDS WORK 時，補完不需要改程式碼 → 計數不歸零 → 永遠 NEEDS WORK | 補完 Verified Clean 之後視同「已修正」，計數歸零 |
| 7 | **兩個覆核角色的報告模板缺 `BLOCKED`** | 環境起不來時模板裡沒得填，會被誤記成程式碼缺陷 | 環境問題一律填 `BLOCKED`，即使模板沒列 |
| 8 | **Phase 6 可以帶著 `NEEDS WORK` 宣告完成** | exit-criteria 只要求「已標記」，沒說「有 NEEDS WORK 就不得寫完成」 | 有任何 `NEEDS WORK` 未解決 → 不要寫 `狀態：完成` |

### 判不出來（兩個人會給不同答案）

- **「瑣碎小改」的界線**：入口舉例是「改 constant／補 log」，`change-request` 卻把 API 異動全歸為需要新設計決策。→ 卡住時照 `change-request` 的停止條件「傾向保守」。
- **`converge` 的「已答」要多深**：規則說「這是全表最低的門檻」，但沒給可判定的下限。
- **UAT 文件「已由非撰寫者跑過一次」**：單人環境沒寫明能不能用 agent 代替。

### 內部矛盾（不影響執行，但讀到會困惑）

- 工單狀態機：`ticket-spec` 說「AI 只能寫 `proposed`」，但同檔狀態表把 `in-progress` 交給「認領的人」、`ops-feedback` 也叫 Lead 寫 `in-progress`。→ 實務上照 `ops-feedback` 走，`accepted` 這一格目前沒有任何 phase 會設。
- 工單編號兩套：創世自編 `ISSUE-nn`、演進自編 `CR-nn`，而 `CR-nn` 不在 `ticket-spec` 的四種編號裡。
- N/A 豁免有四種說法：正本是三條件（`severity-format.md`），但 `qa-handoff`／`system-design` 的 exit-criteria 只寫兩條件，`dev-setup` 的 exit-criteria 用了「自動通過」（而 `severity-format` 明令禁止自動 pass）。→ **一律以 `severity-format.md` 的三條件為準**。
- `severity-format` 自己：Minor 標「不擋放行」，但「多個 Minor」又判 `NEEDS WORK`。
- `DESIGN.md` 開頭的數字自相矛盾（11 份 Skill vs 括號裡 9 個、5 份 references vs 括號列 2 份），且它的檔案清單漏了 `converge` 與 `debug`。**以 `install.py` 實際安裝的為準。**
- `DISTRIBUTION.md` 已標作廢但仍在包內，它的打包指令會漏檔。**不要照它打包，用 `install.py`。**
- 安裝說明對「會問你幾件事」三個答案（README 說三件、INSTALL 說兩件、實際四步）。
- `debug` 與其他 10 份 skill 結構不同（英文 description、沒有觸發條件段、沒有框架缺陷登記出口），且它是一條完整旁路——走它修 bug 不會經過測試與覆核關卡。**線上 bug 修完，建議自己補走一次 `qa-handoff`。**

### 隨包附上但你用不到的

`sdlc-orchestrator/` 底下的 `DESIGN-RATIONALE.md`／`SDLC_Agent協作版.md`／`SDLC_Agent_優化設計.md` 是開發這套規則時的討論紀錄，裡面提到的工具、repo、代號是**開發者自己環境的**，你沒有那些東西。當歷史讀就好，**不要照裡面的做法執行**——特別是 `SDLC_Agent_優化設計.md` 把 GitLab issue 寫成既定的工單機制，那不是規則，規則是「依你的環境綁定層指定」。

`system-design/references/agent-teams-workflow.md` 依賴一個多 agent 編排工具，你的環境沒有就整份不適用，也沒有任何 SKILL.md 會叫到它。

---

## 回報

撞到上面沒列到的問題 → append 一列到 `skills/sdlc-orchestrator/references/framework-defects.md`，**證據欄填「哪個檔的哪一行卡住你、當下的具體情況」**。空白的證據欄不受理——那條規則存在的理由是防止憑印象發明問題。
