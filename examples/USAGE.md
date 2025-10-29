# Usage Examples

## 線上 Demo

直接訪問: https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/

### 頁面功能介紹

#### 📊 Overview
- 快速查看所有模型性能
- 對比準確率、F1 分數等指標

#### 📈 Metrics Explorer
- 深入分析特定模型
- 查看訓練 vs 測試性能

#### ⚖️ Model Comparison
- 並排對比模型
- 雷達圖視覺化

#### 🎮 Live Playground
**操作步驟**:
1. 輸入郵件文本
2. 選擇分類模型
3. 查看預測結果和信心度

**測試樣本**:
```
Ham 範例: "Hi, are you free this weekend?"
Spam 範例: "Click here to win FREE iPhone now!!!"
```

#### 🎯 Features
- 查看高頻詞彙
- 調整 Top N 參數 (5-30)

#### 📋 Data Overview
- 瀏覽完整數據集
- 查看標籤分布

---

## 本地使用

### 運行應用
```bash
cd AIoT_DA_HW3
streamlit run app/streamlit_app.py
```

### 自定義配置
編輯 `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#2d2d2d"
backgroundColor = "#f5f5f5"
secondaryBackgroundColor = "#ebebeb"

[server]
port = 8501
headless = true
```

---

## 開發者指南

### 項目結構
```
app/
├── streamlit_app.py     # 主應用入口
├── ui/                  # UI 組件
│   ├── notifications.py # Toast 系統
│   ├── form_components.py
│   └── performance_monitor.py
└── utils/               # 工具函數
    ├── defs.py         # 文本處理
    ├── caching.py      # 快取管理
    └── data_pagination.py
```

### 新增功能
1. 在 `app/utils/` 中編寫工具函數
2. 在 `app/ui/` 中編寫 UI 組件
3. 在 `streamlit_app.py` 中集成

### 運行測試
```bash
pytest tests/
```
