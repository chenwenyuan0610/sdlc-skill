# SDLC 開發工作入口 — Step 0 完整判斷規則

> 本檔是「開發工作入口 Step 0 判斷表」（`claude_sdlc.md`，貼進你 `CLAUDE.md`/`AGENTS.md` 的那份）的完整版：該表是速查摘要，**語意衝突以本檔為準**。設計依據 → `DESIGN.md`。
>
> ⚠ **本檔是規則包正本，領域中立。** 不得寫入任何特定環境的工具名、repo 名、目錄慣例或工單系統——那些放你自己的 `CLAUDE.md`/`AGENTS.md` 綁定層。

## Step 0 — 先判斷現在在 SDLC 哪個階段

**先查專案 `docs/` 現況，不要只憑「問題現在清不清楚」判斷** —— Phase 1-4 產出的正是「清楚的問題/方案」，這是進 Phase 5-8 的前提，不是跳過 Phase 1-4 的理由。

**由上而下，第一個命中的那一條勝。**

**開始比對之前先看一眼 `docs/sdlc-mode.md`**——它宣告這個專案跑哪幾關。**沒有這個檔就當「全跑」**（預設值，舊專案行為完全不變）。之所以要有這個檔：**檔案缺席永遠只能解讀成「還沒做」，唯有一份正面存在的宣告才能解讀成「刻意不做」**——否則定位機制分不出「這關還沒做」和「這關決定不做」。三種模式、三個配套、以及「實作與測試永遠不能跳」的下限 → `references/tailoring.md`。

### 0. 問題本身還講不清楚 → 先收斂（優先於 `docs/` 現況）

不確定是全新構想還是既有系統的問題／bug 不知道 root cause 或詳細需求在哪／還沒決定要不要做 → 先進 `converge`，講清楚再回本表第 1-3 條定位。

`converge` **在 pipeline 之外、不計入 9 份 SDLC skill 編制**（定位比照 `debug`：只在需要時觸發，不是固定關卡）；純討論、不設 exit criteria，可唯讀調查但 **MUST NOT 改 DB／程式碼**，要使用者明確確認方向才算收斂完成。

⚠ 這是「需求模糊」的**唯一出口**——不要在 `converge` 之外另開一套問法（兩套並存＝第二真相源）。「重大架構決策／安全合規／外部 API 規格不明」不走這條，那是要使用者拍板，直接中斷問。

⚠ `docs/` 已有產出物、但**這次的新問題**還講不清楚時，仍先走 `converge`，收斂完再回表定位。

### 1. 專案 `docs/` 有 `product-discovery.md` → 已在 SDLC pipeline 裡

用 Phase 表依 `docs/` 現況判斷目前哪個 phase，不可跳過。

⚠ **判定基準只看 `product-discovery.md` 這一個檔，不看其他任何 SDLC 檔名。** 理由：`requirements-spec.md`／`design.md`／`architecture.md`／`dev-setup.md`／`handoff-log.md`／`change-log.md`／`change-specs/`／`converge-summary.md`／`feedback-log.md` **演進模式也會產生**（見下方「演進模式的例外」），拿它們當判定依據會把老專案誤判成「已在 pipeline」。而 `product-discovery.md` **只有走完 Phase 1 才會存在，演進模式從不產生它**——這是唯一能機械區分「創世 pipeline」與「演進產物」的檔案。

### 2. `docs/` 沒有 `product-discovery.md`，且這是全新構想、還沒有任何既有系統（創世模式）

問題本質／使用者／方案任一不確定 → 從 Phase 1（`product-discovery`）；三者都已明確 → 直接進開發實作。

### 3. `docs/` 沒有 `product-discovery.md`，但專案是既有運行中的系統（演進模式）

**別因為缺 `docs/` 就當成新專案退回 Phase 1。**

- 一看就知道改哪的瑣碎變更（改 constant／補 log／既有模組內小修）→ 直接開發實作
- 需要新設計決策（新 schema／API／元件／模組）、或範圍不確定是否在既有範圍內 → `change-request`（用程式碼現況當基線分診，會轉去只做該面向的 `system-design` design-delta，或帶著輕量 spec 直接進 Phase 5）

**掃到同主題舊專案時怎麼定位它**：使用者沒指名專案時，**MUST 先掃專案根目錄找同主題既有專案**再判創世／演進——否則會重做一個已經存在的系統。但**掃到不等於要接**：

| 情況 | 定位 |
|------|------|
| 使用者要接續它 | 演進模式 → 第 3 條 |
| 使用者要開全新專案 | **創世模式 → 第 2 條**；舊專案降為**知識輸入（前車之鑑）**，只帶「它撞過什麼牆」進 Phase 1，**不當基底、不當路由依據** |

**MUST 問使用者「要接續它，還是只當參考」，NEVER 由執行者預設偏向接續。** 另：讀舊專案的程式碼只能得到「它這樣寫」，**不等於「這樣做可行」**——後者需要測試證據，引用時 MUST 標注有無。

⚠ 使用環境若已有程式碼導航索引，**先查索引再掃 repo**，不要每次全域重掃。

## 演進模式的例外（這些檔不算「進入 pipeline」）

老專案在第 3 條路徑下產生的**下列檔案一律不算「進入 pipeline」**——下次再有變更，仍然走第 3 條（`change-request` 分診）：

| 檔案 | 誰產生 |
|---|---|
| design-delta——**單一面向的 `architecture.md`／`db-schema.md`／`api-spec.md`／`components.md`／`modules.md`／`logic-flow.md`，以及彙整版 `docs/design.md`** | `system-design` 演進支線（該 skill 允許「拆成多檔」或「彙整成單一 `design.md`」，**兩種都是 design-delta**）|
| `docs/change-log.md` | `change-request` 步驟 3 |
| `docs/change-specs/<變更名>.md`（輕量 spec ＋ 測試描述）| `change-request` 步驟 3 |
| `docs/handoff-log.md`（含 `## Phase 5`／`## Phase 6`／`## Phase 7` 分節）| `implementation-handoff`／`qa-handoff`／`release-handoff` |
| `docs/converge-summary.md` | `converge`（不當場接續時）|
| `docs/feedback-log.md` | `ops-feedback` |

**上表其實就是「除了 `product-discovery.md` 以外的全部」**——所以第 1 條的判定基準才收斂成只看那一個檔。列表在此是為了說明**為什麼**；日後新增任何產出物，只要它不是 `product-discovery.md`，預設就落在本例外裡，**不需要回來補這張表**。

**理由**：老專案的 repo／骨架／版控早就存在，Phase 4 那三個 Output 對它沒有意義；**沒有人需要為了改一行 code 先回頭把九關補完**。要真的讓老專案「正式進入 pipeline 走完整流程」，是使用者明講的決定，不是靠檔案出現自動發生。

⚠ **漏判的後果有兩個方向**：往回是退到 Phase 1 重做需求發想；**往前是被 Phase 表定位成「Phase 5/6 已完成、無 Phase 7」→ 送去部署一個還沒動工的變更**。

## Phase 4 限創世模式

`dev-setup` 只在「全新專案骨架尚未建立」時走（既有專案要新增獨立子模組、骨架真的從零建時亦適用，範圍限該新模組）。演進模式下，Phase 4 唯一不能丟的產出物「**測試描述**」已移交上游承接——`change-request`「在既有範圍內」那條路寫進 `docs/change-specs/<變更名>.md`，`system-design` 演進支線寫進該次的 design-delta，兩條路都是**寫在程式碼之前**，然後直接進 `implementation-handoff`。

⚠ **跳過 Phase 3-4 不包含跳過測試**：開發完成一律 MUST 接 `qa-handoff`（Phase 6）。既有專案的改動落在別人寫的、還在跑的程式碼上，回歸測試的價值比新專案更高。

## Phase 3 設計完成的判定

**此判定只適用創世模式**——演進模式下只補單一設計面向是正常的（`change-request` 明確指定「只需要做哪一個設計面向」），不因為只有一份檔就判 Phase 3 未完成。

三者任一成立即算完成：

1. 有 `docs/design.md`
2. 有 `architecture.md`，且 `db-schema.md`／`api-spec.md`／`components.md`／`modules.md` 至少再有一份
3. 有 `architecture.md`，且檔內明確寫出本專案不涉及資料庫／不提供對外介面

只有單獨一份 `architecture.md` 又沒有第 3 點的聲明 → 不算完成（可能是專案原有的無關文件）。

## 階段完成狀態的判定

`docs/handoff-log.md` 的每個 `## Phase N` 分節，第一行 MUST 是 `狀態：進行中` 或 `狀態：完成`。**標頭存在不等於做完** —— 只看標頭會把做到一半的階段誤判成已結束而跳過。

**判斷順序：先掃有沒有任何分節是「進行中」，有的話那就是目前階段**（Phase 6 測試失敗要退回 Phase 5 也走這條路）；都沒有才往下按產出物比對。⚠ 少了這一步，Phase 6 做到一半時「已有 `## Phase 6` 記錄」與「無 Phase 6 **通過**記錄」會同時成立，**整張 Phase 表沒有任何一列命中**。

## 跨包變更（變更橫跨 ≥2 個 repo 時）

需求級的單一真相記錄放「發起變更的主 repo」的 `docs/change-log.md`（與 `change-request` skill 實際寫入的檔案一致），內含：規格 delta ＋ 涉及的 repo 清單 ＋ 各 repo 狀態表。各 repo 各自走完整 pipeline、完成後回寫狀態。順序原則 = **API 供應方先行**（先做提供介面的那一端，再做消費端）。

使用環境若指定了別的存放位置，以綁定層為準。

## Phase 5-8 的工具綁定（依你的環境自行定義）

這 9 份 skill 是**領域中立**的通用流程，不假設任何特定技術棧或工具。Phase 5-8（開發/測試/部署/維運）在各團隊往往已有既有工具與規範，因此：

- **你的環境若已有既有流程**（既有的開發規範 skill、審查編制、部署稽核流程、監控系統）→ 在你自己的 `CLAUDE.md`/`AGENTS.md` 寫一張「Phase → 對應工具」的綁定表，skill 會優先照綁定走
- **沒有綁定** → skill 內建的通用 fallback 接手（品質門禁、獨立審查精神、部署前檢查清單、監控盤點），不會卡住

⚠ **綁定層為別條路線定義的派工 Tier 表，不自動套用到 SDLC**——那類表往往綁著該路線自己的審查編制，套過來會派出 SDLC 明文禁派的角色。SDLC 的 Tier 與完工覆核以 `references/agent-teams.md` 為準，除非綁定層明文指定「SDLC 用哪張表」。

**設計原則（勿破壞）**：skill 檔案本身**不寫死任何工具名稱**，只講「依既有流程/若無則走通用 fallback」；「這個 phase 轉交去哪個工具」的實際綁定只放在你自己的 `CLAUDE.md`/`AGENTS.md`。未來簡化這些 skill 時 **NEVER 把特定環境的工具名硬編進 skill 本體**（會破壞可攜性，讓這包無法給下一個團隊用）。

**治理保證必須寫在規則文字裡，不得依賴本機自動化**：hook／lint／腳本**不隨規則包發送**，所以任何「不能再犯」的保證若只實作成腳本檢查，對拿到規則包的人等於不存在。

各 skill 完整的 TRIGGER / DO NOT TRIGGER 條件見其 `SKILL.md` 的 frontmatter description。
