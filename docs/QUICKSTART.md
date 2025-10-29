# 快速開始指南 (Quick Start)

## 🌐 線上 Demo（推薦）

**無需安裝，直接訪問**:
```
https://aiotdahw3-gapdh7jzxg5kyj9x7xate4.streamlit.app/
```

---

## 💻 本地運行

### 1. 克隆專案
```bash
git clone https://github.com/Charles8745/AIoT_DA_HW3.git
cd AIoT_DA_HW3
```

### 2. 建立虛擬環境
```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 安裝依賴
```bash
pip install -r requirements.txt
```

### 4. 運行應用
```bash
cd sources
streamlit run streamlit_app.py
```

### 5. 打開瀏覽器
```
http://localhost:8501
```

---

## 🎮 主要功能

| 頁面 | 功能 |
|------|------|
| **📊 Overview** | 所有模型的性能概覽 |
| **📈 Metrics Explorer** | 深入分析特定模型 |
| **⚖️ Model Comparison** | 模型性能對比（雷達圖） |
| **🎮 Live Playground** | 實時郵件分類推理 |
| **🎯 Features** | 高頻詞彙分析 |
| **📋 Data Overview** | 數據集統計 |

---

## 📝 常見問題

**Q: 為什麼應用無法啟動？**  
A: 確保所有依賴已安裝。運行 `pip install -r requirements.txt`

**Q: 如何更改端口？**  
A: `streamlit run streamlit_app.py --server.port 8502`

**Q: 如何關閉應用？**  
A: 按 `Ctrl+C` (macOS/Linux) 或 `Ctrl+C` (Windows)

---

## 📚 詳細文檔

查看完整 README.md 獲取更詳細的說明和選項。

---

**祝您使用愉快！** 🎉
