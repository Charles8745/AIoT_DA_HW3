# Streamlit Cloud 部署指南

## 部署步驟

### 1. 準備 GitHub 倉庫

確保您的項目已推送到 GitHub：
```bash
git add .
git commit -m "Fix import paths for Streamlit Cloud deployment"
git push origin enhanced_ui
```

### 2. 在 Streamlit Cloud 上部署

1. 訪問 [https://share.streamlit.io/](https://share.streamlit.io/)
2. 點擊 "New app"
3. 選擇您的 GitHub 倉庫和分支
4. 在 "Main file path" 中輸入：`app/streamlit_app.py`
5. 點擊 "Deploy"

### 3. 配置環境

Streamlit Cloud 會自動：
- 檢測 `config.requirements.txt` 並安裝依賴
- 讀取 `.streamlit/config.toml` 配置
- 使用 `app/streamlit_app.py` 作為入口點

## 部署後常見問題

### ❌ ModuleNotFoundError: No module named 'plotly'

**原因**: 依賴未安裝

**解決**:
```bash
# 確保 config/requirements.txt 存在且包含所有依賴
pip install -r config/requirements.txt
```

### ❌ ImportError: cannot import name 'get_toast_manager'

**原因**: 導入路徑不正確

**解決**: 已在 `app/streamlit_app.py` 中修復：
```python
# 現在支持多種導入方式
try:
    from app.ui.notifications import get_toast_manager
except ImportError:
    from ui.notifications import get_toast_manager
```

### ❌ FileNotFoundError: datasets/...csv

**原因**: 相對路徑問題

**解決**: 使用 `Path(__file__).parent` 構建絕對路徑

## 文件結構確認

Streamlit Cloud 上的項目結構應為：

```
AIoT_DA_HW3/
├── app/
│   ├── streamlit_app.py      ← 入口點
│   ├── ui/
│   └── utils/
├── datasets/
├── notebooks/
├── config/
│   └── requirements.txt      ← 依賴文件
├── .streamlit/
│   └── config.toml          ← Streamlit 配置
└── streamlit.toml           ← 根目錄配置
```

## 重新部署

如果需要更新應用：

1. 在本地修改代碼
2. 提交到 GitHub
3. Streamlit Cloud 會自動檢測更新並重新部署

```bash
git add .
git commit -m "Update: [description of changes]"
git push origin enhanced_ui
```

## 性能優化

對於 Streamlit Cloud 的最佳性能：

- ✅ 使用 `@st.cache_data` 緩存數據
- ✅ 使用 `@st.cache_resource` 緩存資源
- ✅ 避免在每次運行時重新加載大型數據集
- ✅ 使用 TTL 基礎快取（已實現）

## 監控

- 查看應用日誌：Settings → App logs
- 檢查部署狀態：Manage app → Settings
- 監控運行時間和資源使用情況

## 支持

- 📖 [Streamlit Cloud 文檔](https://docs.streamlit.io/streamlit-cloud)
- 💬 [Streamlit 社區論壇](https://discuss.streamlit.io/)
- 🐛 [GitHub Issues](https://github.com/Charles8745/AIoT_DA_HW3/issues)
