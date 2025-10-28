# 🚀 快速參考卡 - 預處理擴充提案

## 📌 一句話總結
擴充預處理功能，從基本的 tokenization/lemmatization 添加 8 個新的文本清理函數。

## 🎯 提案 ID
```
add-enhanced-text-preprocessing
```

## 📍 位置
```
openspec/changes/add-enhanced-text-preprocessing/
```

## 📊 快速統計
| 項目 | 數值 |
|------|------|
| 新檔案 | 1 個 |
| 修改檔案 | 1 個 |
| 新函數 | 8 個 |
| 預估時間 | 2.5-3 小時 |
| 風險等級 | 🟢 低 |
| 向後相容 | ✅ 是 |

## ✨ 新增 8 個函數

```python
1. remove_urls()          # 移除 URLs
2. remove_emails()        # 移除 Email
3. normalize_case()       # 轉小寫
4. remove_punctuation()   # 移除標點
5. remove_numbers()       # 移除數字
6. normalize_whitespace() # 清理空白
7. remove_non_ascii()     # 移除非 ASCII
8. remove_stopwords()     # 移除停用詞
```

## 🧪 核心類別

```python
class TextPreprocessor:
    def __init__(config: PreprocessingConfig)
    def process(text: str) -> str
    def batch_process(texts: List[str]) -> List[str]
    
class PreprocessingConfig:
    lowercase: bool = True
    remove_urls: bool = True
    remove_emails: bool = True
    remove_punctuation: bool = True
    remove_numbers: bool = False
    remove_stopwords: bool = False
    normalize_whitespace: bool = True
    remove_non_ascii: bool = True
```

## 💡 使用範例

### 基礎用法
```python
from sources.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor()
cleaned = preprocessor.process("Visit http://spam.com!!!")
# "visit spam com"
```

### 自訂配置
```python
from sources.preprocessing import PreprocessingConfig, TextPreprocessor

config = PreprocessingConfig(remove_stopwords=True)
preprocessor = TextPreprocessor(config)
```

### 批量處理
```python
texts = df['message'].tolist()
cleaned = preprocessor.batch_process(texts)
```

## 📚 文件地圖

| 檔案 | 用途 | 閱讀時間 |
|------|------|--------|
| `README.md` | 快速概述 | 5 分鐘 |
| `proposal.md` | 為什麼 | 5 分鐘 |
| `design.md` | 怎麼做 | 7 分鐘 |
| `tasks.md` | 實施步驟 | 5 分鐘 |
| `spec.md` | 詳細規範 | 10 分鐘 |
| `REVIEW_CHECKLIST.md` | 品質檢查 | 10 分鐘 |
| `READING_GUIDE.md` | 完整指南 | 15 分鐘 |

**快速查看**: 只需 5 分鐘，直接看 `README.md`

## ✅ 成功標準

- ✅ 所有函數在 SMS 垃圾/網釣資料集測試通過
- ✅ 無破壞性變更 (向後相容)
- ✅ > 85% 單元測試覆蓋率
- ✅ < 5ms 性能/條消息
- ✅ 完整文檔和使用示例

## 🎯 實施階段 (9 個)

1. **模組設置** (15 分鐘) - 建立檔案和類別
2. **基本函數** (30 分鐘) - URL/Email/標點移除等
3. **停用詞** (20 分鐘) - NLTK 集成
4. **管道** (25 分鐘) - 完整流程編排
5. **向後相容** (20 分鐘) - defs.py 整合
6. **單元測試** (45 分鐘) - 完整測試覆蓋
7. **Notebook** (30 分鐘) - 示例和演示
8. **文檔** (30 分鐘) - 使用指南
9. **驗證** (20 分鐘) - 最終檢查

**總計**: 3.5 小時

## 🚦 當前狀態

```
📋 建立       ✅ 完成
📝 文檔       ✅ 完成
🔍 審查       ⏳ 等待
✨ 批准       ⏳ 等待
⚙️ 實施       ⏳ 待命
🧪 測試       ⏳ 待命
📦 部署       ⏳ 待命
📁 歸檔       ⏳ 待命
```

## 💬 下一步

### 如果同意:
```
告訴我: "開始實施預處理功能"
或: "批准提案"
```

### 如果需要修改:
```
告訴我: "我想修改 X 部分"
或: "我有以下建議..."
```

### 如果需要更多資訊:
```
告訴我: "解釋 Y 的設計"
或: "我需要了解 Z 的細節"
```

## 📞 常見問題

**Q: 這會破壞現有代碼嗎?**  
A: 否。完全向後相容。

**Q: 需要安裝新套件嗎?**  
A: 否。僅使用現有依賴。

**Q: 需要多久?**  
A: 2.5-3 小時，分 9 個階段。

**Q: 何時開始?**  
A: 批准後立即開始。

## 🎁 主要價值

| 好處 | 影響 |
|------|------|
| 代碼重用 | -35-40% 重複代碼 |
| 一致性 | 所有模型相同邏輯 |
| 可配置 | 任務特定預處理 |
| 可維護 | 集中管理 |
| 相容 | 無破壞 |
| 可測試 | 模組化設計 |

## 🔗 相關資源

- **OpenSpec 文檔**: `/openspec/AGENTS.md`
- **專案上下文**: `/openspec/project.md`
- **其他提案**: `/openspec/changes/` 
- **主頁**: `PROPOSAL_SUMMARY.md`

## 🏆 準備狀態

🟢 **準備批准和實施**

所有文檔完成，品質檢查通過，無阻塞因素。

---

**需要完整詳情?** 查看 `README.md` 或 `READING_GUIDE.md`
