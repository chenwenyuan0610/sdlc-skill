> ⚠ **本檔是選用的進階編排腳本，不在  的主流程內**，照 SKILL.md 做事不需要讀它。它依賴使用環境是否提供多 agent 編排工具——**環境沒有這類工具就整份不適用**。

# System Design — Agent Teams 協作雛形（Workflow tool 最小雛形）

> 這是「議題 4：Agent teams 協作 workflow」的第一步雛形，範圍限定在 `system-design` 步驟 11（系統架構設計）需要多角度比較方案的情境。**不是**整套 SDLC 的 agent teams 機制，其餘 7 個 phase 目前仍是各自獨立、不互相呼叫。

## 觸發條件（雙重限制，兩者都要）
1. 步驟 11 系統架構設計有多個可行方向需要比較（例如效能優先 vs 成本優先 vs 維護性優先，設計上真的會分岔）
2. 使用者明確同意使用 Workflow tool（依 Workflow tool 本身的 opt-in 政策，需使用者說 "ultracode" 或明確要求多 agent 編排）——**不是預設路徑**，沒有明確同意就用一般的單一 agent 派工即可

## 做法：3 種視角並行產出方案，再綜合評分

```js
export const meta = {
  name: 'system-design-multi-angle',
  description: '多個視角並行評估架構方案，供 system-design skill 步驟 11 使用',
  phases: [
    { title: 'Evaluate', detail: '3 個角度各自產出架構方案' },
    { title: 'Synthesize', detail: '綜合評分，挑選或融合最佳方案' },
  ],
}

// 3 個 prompt 都要內嵌同一套紀律：不假設不清楚的地方、read-only、先確認既有系統慣例再設計、
// 輸出包含架構方案 + 取捨說明 + 明確待確認問題清單；只是各自加一個角度限定，不是叫三個不同角色
const LENSES = [
  { key: 'performance', prompt: '以效能優先角度，針對需求規格書設計系統架構（分層/服務/技術棧），並說明取捨。' },
  { key: 'cost', prompt: '以成本與資源效率優先角度，針對需求規格書設計系統架構，並說明取捨。' },
  { key: 'maintainability', prompt: '以長期維護性優先角度，針對需求規格書設計系統架構，並說明取捨。' },
]

const DESIGN_SCHEMA = {
  type: 'object',
  properties: {
    architecture: { type: 'string' },
    tradeoffs: { type: 'string' },
  },
  required: ['architecture', 'tradeoffs'],
}

phase('Evaluate')
const proposals = await parallel(LENSES.map(l => () =>
  agent(l.prompt, { label: `design:${l.key}`, schema: DESIGN_SCHEMA })
    .then(r => ({ lens: l.key, ...r }))
))

phase('Synthesize')
const synthesis = await agent(
  `比較以下 3 個架構方案（效能優先/成本優先/維護性優先），綜合評分並挑選最適合目前需求規格的方案，或說明如何融合其中優點：\n${JSON.stringify(proposals.filter(Boolean))}`,
  { label: 'synthesize' }
)

return { proposals: proposals.filter(Boolean), synthesis }
```

Lead 在觸發條件成立時，把上面腳本連同實際需求規格內容代入 `LENSES` 的 prompt，透過 Workflow tool 呼叫（`script` 參數帶入本腳本）。回傳結果由 Lead 彙整進步驟 11 的 Output（系統架構圖 + 技術選型），並跟使用者確認最終選哪個方向。

## 邊界（避免這個雛形擴張成整套機制）
- 只用在步驟 11，不擴及步驟 12-17（資料庫/API/元件/模組/開票/文件彙整仍是 Lead-direct 或單一 agent 派工）
- 不是自動觸發，每次都要重新確認使用者同意
- 這不是「8 個 phase skill 互相引用」的解法——那個問題（議題 4 的完整範圍）仍待未來有具體失敗案例時再設計
