# 🤝 貢獻指南

感謝您對本項目的興趣！本文檔將指導您如何為 AIoT Data Analysis & Visualization Suite 做出貢獻。

---

## 📋 目錄

- [行為準則](#行為準則)
- [開始貢獻](#開始貢獻)
- [開發流程](#開發流程)
- [提交指南](#提交指南)
- [代碼風格](#代碼風格)
- [測試指南](#測試指南)
- [文檔](#文檔)

---

## 🚀 開始貢獻

### 前置要求

- Python 3.8+
- Git
- 對機器學習和數據可視化有基本理解

### 設置開發環境

1. **Fork 倉庫**
   ```bash
   # 點擊 GitHub 上的 "Fork" 按鈕
   ```

2. **克隆您的 Fork**
   ```bash
   git clone https://github.com/your-username/AIoT_DA_HW3.git
   cd AIoT_DA_HW3
   ```

3. **添加上游遠端**
   ```bash
   git remote add upstream https://github.com/original-owner/AIoT_DA_HW3.git
   ```

4. **建立虛擬環境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # 或
   .\.venv\Scripts\activate  # Windows
   ```

5. **安裝開發依賴**
   ```bash
   pip install -r requirements.txt
   pip install black flake8 pytest pytest-cov
   ```

---

## 💻 開發流程

### 1. 建立特性分支

```bash
git checkout -b feature/your-feature-name
```

**分支命名約定:**
- `feature/` - 新功能
- `fix/` - bug 修復
- `docs/` - 文檔改進
- `refactor/` - 代碼重構
- `test/` - 測試改進

### 2. 進行更改

編輯檔案並確保遵循代碼風格指南（見下方）。

### 3. 測試您的更改

```bash
# 運行所有測試
pytest tests/ -v

# 運行特定測試
pytest tests/test_visualization_suite.py -v

# 生成覆蓋率報告
pytest tests/ --cov=sources --cov-report=html
```

### 4. 提交更改

```bash
git add .
git commit -m "簡短且清晰的提交信息"
```

### 5. 推送到您的 Fork

```bash
git push origin feature/your-feature-name
```

### 6. 開啟 Pull Request

在 GitHub 上開啟 PR，並填寫 PR 模板。

---

## 📝 提交指南

### 提交信息格式

遵循 Conventional Commits 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型 (Type):**
- `feat:` - 新功能
- `fix:` - bug 修復
- `docs:` - 文檔
- `style:` - 代碼風格 (不改變功能)
- `refactor:` - 代碼重構
- `test:` - 添加或改進測試
- `chore:` - 構建、依賴或工具更新

**示例:**

```
feat(visualization): add 3D scatter plot function

Add support for 3D scatter plots with interactive rotation
and zoom capabilities. Includes comprehensive docstring
and unit tests.

Closes #123
```

### PR 模板

```markdown
## 描述
簡述您的更改內容。

## 相關 Issue
修復 #123

## 更改類型
- [ ] 新功能
- [ ] bug 修復
- [ ] 文檔改進
- [ ] 代碼重構

## 測試
- [ ] 添加了單元測試
- [ ] 所有現有測試通過
- [ ] 測試覆蓋率 > 90%

## 檢查清單
- [ ] 遵循代碼風格指南
- [ ] 自我評審了代碼
- [ ] 添加了註釋
- [ ] 更新了相關文檔
- [ ] 沒有引入新的警告
```

---

## 🎨 代碼風格

### Python 代碼風格

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)：

```bash
# 使用 black 格式化
black sources/ tests/

# 使用 flake8 檢查
flake8 sources/ tests/ --max-line-length=100
```

### 命名約定

- **模組**: `lowercase_with_underscores`
- **類別**: `CamelCase`
- **函數/方法**: `lowercase_with_underscores`
- **常數**: `UPPERCASE_WITH_UNDERSCORES`
- **私有**: 以 `_` 開頭

### 註釋和文檔字符串

使用 Google 風格的 docstring：

```python
def plot_training_curves(history: dict, metric: str = 'loss', figsize: tuple = (12, 5)):
    """Plot training and validation curves.
    
    Args:
        history (dict): Training history with keys like 'loss', 'val_loss', etc.
        metric (str): Metric to plot ('loss' or 'accuracy'). Defaults to 'loss'.
        figsize (tuple): Figure size as (width, height). Defaults to (12, 5).
    
    Returns:
        tuple: (fig, axes) matplotlib figure and axes objects.
    
    Example:
        >>> history = {'loss': [0.5, 0.4, 0.3], 'val_loss': [0.55, 0.45, 0.35]}
        >>> fig, axes = plot_training_curves(history)
        >>> plt.show()
    
    Raises:
        ValueError: If metric is not 'loss' or 'accuracy'.
        KeyError: If required keys missing from history dict.
    """
```

### 行長

最多 100 個字符（黑色格式化標準）。

---

## 🧪 測試指南

### 編寫測試

使用 pytest 編寫測試：

```python
import pytest
from sources.visualization import plot_training_curves

class TestVisualization:
    """Test visualization functions."""
    
    def test_plot_training_curves_basic(self):
        """Test basic functionality of plot_training_curves."""
        history = {
            'loss': [0.5, 0.4, 0.3],
            'val_loss': [0.55, 0.45, 0.35],
            'accuracy': [0.7, 0.75, 0.8],
            'val_accuracy': [0.68, 0.73, 0.78]
        }
        
        fig, axes = plot_training_curves(history)
        
        assert fig is not None
        assert axes is not None
        assert len(axes) == 2
    
    def test_plot_training_curves_invalid_metric(self):
        """Test that invalid metric raises ValueError."""
        history = {'loss': [0.5, 0.4]}
        
        with pytest.raises(ValueError):
            plot_training_curves(history, metric='invalid')
```

### 測試覆蓋

- 確保新代碼的覆蓋率 > 90%
- 測試邊界情況和錯誤條件
- 使用 fixtures 避免重複代碼

### 運行測試

```bash
# 所有測試
pytest tests/ -v

# 特定文件
pytest tests/test_visualization_suite.py -v

# 特定函數
pytest tests/test_visualization_suite.py::TestVisualization::test_plot_training_curves_basic -v

# 帶覆蓋率
pytest tests/ --cov=sources --cov-report=term-missing
```

---

## 📚 文檔

### 添加文檔

- 在源代碼中使用清晰的 docstring
- 在 `docs/` 目錄中添加詳細文檔
- 更新 README.md（如果相關）
- 為新功能提供範例

### 文檔格式

使用 Markdown 並遵循以下結構：

```markdown
# 功能標題

簡短描述。

## 功能

- 功能 1
- 功能 2

## 使用方式

### 基本範例
代碼塊...

### 高級用法
代碼塊...

## 參數

| 參數 | 類型 | 描述 |
|------|------|------|
| param1 | str | 描述 |
```

---

## 🔄 同步上游

保持您的 fork 與上游同步：

```bash
# 獲取上游更改
git fetch upstream

# 切換到 main
git checkout main

# 合併上游更改
git merge upstream/main

# 推送到您的 fork
git push origin main
```

---

## ⚠️ 常見問題

### 我的 PR 被拒絕了怎麼辦？

- 閱讀反饋
- 進行必要的更改
- 重新推送（PR 會自動更新）

### 如何解決合併衝突？

```bash
# 重新 base 您的分支
git rebase upstream/main

# 手動解決衝突
# ... 編輯衝突檔案 ...

# 繼續 rebase
git rebase --continue

# 強制推送
git push -f origin feature/your-feature-name
```

### 許可

通過提交 PR，您同意在 MIT 許可下發布您的代碼。

---

## 📞 需要幫助？

- 查看 [文檔](./docs)
- 查看現有 Issue 和 PR
- 開啟新 Issue 詢問問題

---

感謝您的貢獻！🙏
