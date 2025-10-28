# 📋 變更提案總結：Enhanced Text Preprocessing Pipeline

## 提案 ID
`add-enhanced-text-preprocessing`

## 位置
`openspec/changes/add-enhanced-text-preprocessing/`

## 📁 檔案結構

```
openspec/changes/add-enhanced-text-preprocessing/
├── proposal.md                    # 提案概述、動機、範圍
├── design.md                      # 技術架構和設計決策
├── tasks.md                       # 實施檢查清單 (9 個階段)
└── specs/
    └── text-preprocessing/
        └── spec.md               # 詳細規範和使用案例
```

## 🎯 提案摘要

**目標**: 擴充和標準化文本預處理功能，為垃圾短信和網釣檢測提供一致的、可重用的預處理管道。

**當前問題**:
- 只有基本的 `get_lemmas()` 和 `get_tokens()` 函數
- 預處理分散在各個 notebook 中
- 缺乏 URL/email 移除、停用詞移除等功能
- 難以跨模型復現預處理

**解決方案**:
✅ 新增 `sources/preprocessing.py` 模組
✅ 配置驅動的 `TextPreprocessor` 類
✅ 8 個核心預處理功能
✅ 向後兼容 (不破壞現有代碼)
✅ 完整的測試和文檔

## 🔑 主要功能

### 預處理功能 (8 個)
1. **URL 移除** - 移除 http/https 連結
2. **Email 移除** - 移除電郵地址
3. **大小寫正規化** - 轉換為小寫
4. **標點符號移除** - 清理特殊字符
5. **停用詞移除** - 移除常見英文詞彙
6. **數字處理** - 移除或保留數字
7. **空白正規化** - 清理多餘空格
8. **非 ASCII 移除** - 可選的字符過濾

### 核心設計
- **配置系統**: `PreprocessingConfig` 資料類允許靈活的預處理管道
- **處理順序**: URL/Email → 大小寫 → 標點 → 數字 → 空白 → 停用詞
- **批量處理**: 支援一次處理多條消息
- **向後相容**: 保留現有 `get_lemmas()` 和 `get_tokens()`

## 📊 實施規劃

### 9 個實施階段
| 階段 | 任務 | 預計時間 |
|------|------|--------|
| 1️⃣ 模組設置 | 建立基礎結構 | 15 分鐘 |
| 2️⃣ 基本函數 | URL/Email/標點/大小寫移除 | 30 分鐘 |
| 3️⃣ 停用詞處理 | NLTK 集成 | 20 分鐘 |
| 4️⃣ 管道 & 批量 | 編排完整流程 | 25 分鐘 |
| 5️⃣ 向後兼容 | 更新 defs.py，橋接函數 | 20 分鐘 |
| 6️⃣ 單元測試 | > 85% 覆蓋率 | 45 分鐘 |
| 7️⃣ Notebook 整合 (可選) | 示例和演示 | 30 分鐘 |
| 8️⃣ 文檔 | 使用示例和指南 | 30 分鐘 |
| 9️⃣ 驗證 | 最終測試和整合 | 20 分鐘 |

**總時間**: 2.5-3 小時 ⏱️

## 💾 受影響的檔案

### 新檔案
- ✨ `sources/preprocessing.py` (新模組，~300-400 行代碼)

### 修改的檔案
- 📝 `sources/defs.py` (新增導入和橋接函數)

### 測試檔案
- 🧪 `tests/test_preprocessing.py` (新增)

## ✅ 成功標準

- ✅ 所有預處理函數在 SMS 垃圾和網釣資料集上測試通過
- ✅ 輸出文本一致 (無多餘空白)
- ✅ 保持向後相容性
- ✅ 支援靈活的配置組合
- ✅ 性能 < 5ms/條消息
- ✅ > 85% 單元測試覆蓋率
- ✅ 完整的代碼文檔和示例

## 📖 使用示例

### 基礎用法
```python
from sources.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor()
text = "Visit https://example.com NOW!!! Contact: spam@fake.net"
cleaned = preprocessor.process(text)
# Output: "visit now contact"
```

### 自訂配置
```python
from sources.preprocessing import PreprocessingConfig, TextPreprocessor

config = PreprocessingConfig(
    remove_urls=True,
    remove_emails=True,
    remove_stopwords=True,
    remove_numbers=True
)
preprocessor = TextPreprocessor(config)
```

### 批量處理
```python
import pandas as pd

df = pd.read_csv('datasets/sms_spam_no_header.csv')
preprocessor = TextPreprocessor()
df['cleaned'] = df['text'].apply(preprocessor.process)
```

## 🚀 下一步

### 1. 審查提案 (你的動作)
請審查以下檔案:
- `proposal.md` - 驗證目標和範圍
- `design.md` - 檢查技術架構
- `tasks.md` - 確認實施計劃

### 2. 批准實施 (你的動作)
告訴我: 「開始實施預處理功能」或「批准提案」

### 3. 我會執行實施
- 逐個完成 9 個階段的任務
- 定期更新進度
- 完成後更新 `tasks.md` 中的檢查清單

## 📝 提案狀態

- 📋 **狀態**: 準備批准
- 👤 **建立者**: GitHub Copilot
- 📅 **建立日期**: 2025-10-22
- 📊 **範圍**: 中等 (新模組)
- ⚡ **破壞性變更**: 無 (完全向後相容)
- 🎯 **優先級**: 中等 (改進代碼品質和重用)

---

**💡 提示**: 所有詳細資訊都在相應的 `.md` 檔案中。根據需要查看特定的設計決策或任務。
