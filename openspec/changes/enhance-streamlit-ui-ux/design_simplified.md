# Design Document: Streamlit UI/UX Enhancement (Simplified)

**Change ID:** `enhance-streamlit-ui-ux`  
**Date:** 2025-10-29  
**Author:** Architecture Team  
**Scope:** 2 核心功能（UI 系統、性能優化）

---

## 🏗️ Architectural Overview

```
┌─────────────────────────────────────────┐
│     Streamlit Web Application           │
├─────────────────────────────────────────┤
│  Navigation & Layout Layer              │
│  ├─ Sidebar (enhanced)                  │
│  ├─ Header (with theme toggle)          │
│  └─ Main content area                   │
├─────────────────────────────────────────┤
│  UI Components Layer                    │
│  ├─ Neumorphism Card System             │
│  ├─ Theme Provider (Light/Dark)         │
│  ├─ Toast/Notification System           │
│  └─ Loading State Management            │
├─────────────────────────────────────────┤
│  Performance Layer                      │
│  ├─ Caching & Session Management        │
│  ├─ Conditional Rendering               │
│  └─ Performance Monitoring              │
└─────────────────────────────────────────┘
```

---

## 🎨 Design System Evolution

### Current State (v1.0)
- ✅ Neumorphism 設計系統
- ✅ 6 個頁面應用
- ✅ 基礎 CSS 變數
- ❌ 沒有黑暗模式
- ❌ Toast 通知系統
- ❌ 性能監控

### Target State (v2.0)
- ✅ 增強 Neumorphism（支持明暗主題）
- ✅ 完整的主題系統
- ✅ 豐富的交互反饋系統
- ✅ 性能優化層
- ✅ 性能監控儀表板

---

## 🔀 Theme System Design

### Dual-Theme Architecture

```python
# themes/light_theme.py
LIGHT_THEME = {
    'primary_bg': '#f5f5f5',
    'element_bg': '#ffffff',
    'text_primary': '#2d2d2d',
    'accent_sage': '#8b7d6b',
    'accent_warm': '#d4a574',
    'error': '#e74c3c',
    'success': '#27ae60',
    'warning': '#f39c12',
}

# themes/dark_theme.py
DARK_THEME = {
    'primary_bg': '#1a1a1a',
    'element_bg': '#2d2d2d',
    'text_primary': '#f5f5f5',
    'accent_sage': '#a89968',
    'accent_warm': '#e8c89a',
    'error': '#ff6b6b',
    'success': '#51cf66',
    'warning': '#ffa94d',
}
```

### Theme Persistence
- 存儲位置: `st.session_state['theme']`
- 備份存儲: 瀏覽器 localStorage (使用 streamlit-extras)
- 默認值: 基於系統偏好 (prefers-color-scheme)

---

## 💬 Feedback & Interaction System

### Toast/Notification Levels
```python
class NotificationLevel(Enum):
    SUCCESS = "✅ Success"      # 綠色
    INFO = "ℹ️ Information"     # 藍色
    WARNING = "⚠️ Warning"      # 橙色
    ERROR = "❌ Error"          # 紅色

# 使用示例
show_toast(
    message="Model trained successfully!",
    level=NotificationLevel.SUCCESS,
    duration=3  # seconds
)
```

### Loading States
- 全頁 loading: Spinner + 進度文本
- 組件 loading: Skeleton 加載骨架
- 交互 loading: 按鈕禁用 + 加載指示器

---

## ⚡ Performance Optimization

### 策略

1. **Caching Layer**
   ```python
   @st.cache_data(ttl=300)  # 5 分鐘
   def load_model_metrics():
       # 不會重複執行
       return expensive_computation()
   ```

2. **Conditional Rendering**
   ```python
   if st.session_state.get('show_advanced'):
       advanced_options()  # 只在需要時渲染
   ```

3. **Data Loading Optimization**
   - 虛擬滾動 (大型表格)
   - 分頁 (數據列表)
   - 延遲加載 (圖表)

### 性能指標
| 指標 | 目標 | 當前 |
|------|------|------|
| FCP (首次內容繪製) | < 1s | 測量中 |
| LCP (最大內容繪製) | < 2.5s | 測量中 |
| TTI (互動時間) | < 3.8s | 測量中 |

---

## 🔗 Integration Points

### Session State Management
```
User Action
    ↓
st.session_state Update
    ↓
UI Re-render
    ↓
Visual Feedback (Toast/Loading)
    ↓
Data Update (if needed)
```

### Theme System Integration
```
User toggles theme
    ↓
st.session_state['theme'] = new_theme
    ↓
CSS variables updated
    ↓
streamlit reruns (automatic)
    ↓
Page displays with new theme
```

---

## 📊 Data Flow

```
┌──────────────┐
│ User Input   │
└──────┬───────┘
       │
       ↓
┌──────────────────────┐
│ Input Validation     │ ← Show error toast if invalid
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ Show Loading State   │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ Process Data         │
│ (Model/Analysis)     │
└──────┬───────────────┘
       │
       ├─→ Success ─→ Show success toast + Display result
       │
       └─→ Error   ─→ Show error toast + Display error details
```

---

## 🧪 Testing Strategy

### Unit Tests
- Theme switching logic
- Input validation
- Notification system
- Caching mechanisms

### Integration Tests
- Page navigation with theme persistence
- Loading states across all pages
- Form submission workflows
- Performance impact

### E2E Tests
- 完整使用者旅程 (選擇主題 → 執行操作 → 查看結果)
- 效能基準測試
- 快取效能驗證

### Performance Tests
- 頁面加載時間監控
- 內存使用監控
- 緩存效率測試

---

## 🚀 Migration Path

### 向後兼容性
- 現有功能保持不變
- 新組件逐步集成
- 舊 CSS 保留，新 CSS 並行

### Phase-by-Phase Rollout
1. 主題系統 (無破壞性更改)
2. 導航改進 (增強現有功能)
3. 交互反饋 (新組件)
4. 性能優化 (後台改進)

---

## 🔒 Security Considerations

- Theme 設置不涉及敏感資訊 (安全)
- 用戶輸入始終驗證 (防止 XSS)
- 本地存儲僅存主題 (無個人資訊)

---

## 📝 Future Enhancements

- 🎨 用戶自定義主題編輯器
- 🌐 多語言支持
- 📊 高級分析儀表板

---

**Status**: 設計完成 ✅
