# Design Document: Streamlit UI/UX Enhancement

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
│  Page Layer (6 pages)                   │
│  ├─ Overview (Dashboard)                │
│  ├─ Metrics Explorer                    │
│  ├─ Model Comparison                    │
│  ├─ Live Inference                      │
│  ├─ Feature Importance                  │
│  └─ Data Overview                       │
├─────────────────────────────────────────┤
│  Business Logic Layer                   │
│  ├─ Model Evaluators                    │
│  ├─ Data Preprocessing                  │
│  └─ Inference Engine                    │
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

## 📱 Responsive Design Strategy

### Breakpoints
```css
/* Mobile First Approach */
@media (min-width: 640px)  { /* tablet */ }
@media (min-width: 1024px) { /* desktop */ }
@media (min-width: 1280px) { /* large desktop */ }

/* Touch-friendly sizing */
@media (hover: none) { /* touch devices */ }
```

### Layout Adaptations

| Device | Sidebar | Columns | Font Size |
|--------|---------|---------|-----------|
| Mobile | 隱藏/抽屜 | 1 | 14px |
| Tablet | 摺疊 | 2 | 14px |
| Desktop | 展開 | 3-4 | 16px |

### Touch Interaction
- 按鈕最小尺寸: 48x48px
- 間距: 16px (touch-friendly)
- 滑塊: 增大觸控區域

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

## ♿ Accessibility (WCAG 2.1 AA)

### 核心原則

1. **Perceivable** (可感知)
   - 顏色對比度 ≥ 4.5:1 (文本)
   - 所有圖片有 alt 標籤
   - 不依賴顏色傳遞資訊

2. **Operable** (可操作)
   - 鍵盤可導航 (Tab/Shift+Tab)
   - 焦點指示器明顯
   - 跳過導航鏈接

3. **Understandable** (可理解)
   - 簡化語言
   - 清晰標籤
   - 錯誤提示和糾正建議

4. **Robust** (健壯)
   - 語義化 HTML
   - ARIA 標籤
   - 屏幕讀者兼容

### 實施清單
- [ ] 顏色對比度測試 (WAVE)
- [ ] 鍵盤導航測試
- [ ] 屏幕讀者測試 (NVDA/JAWS)
- [ ] 焦點管理檢查
- [ ] ARIA 標籤驗證

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

### Integration Tests
- Page navigation with theme persistence
- Loading states across all pages
- Form submission workflows

### E2E Tests
- 完整使用者旅程 (登錄 → 模型選擇 → 推理 → 結果查看)
- 響應式設計測試 (多個設備尺寸)
- 無障礙測試 (鍵盤導航、屏幕讀者)

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
2. 導航改進 (可選欄/菜單)
3. 交互反饋 (新組件)
4. 響應式設計 (CSS 更新)
5. 無障礙功能 (ARIA + 語義)

---

## 🔒 Security Considerations

- Theme 設置不涉及敏感資訊 (安全)
- 用戶輸入始終驗證 (防止 XSS)
- 本地存儲僅存主題 (無個人資訊)

---

## 📝 Future Enhancements

- 🎨 用戶自定義主題編輯器
- 🌐 多語言支持
- 📊 高對比度模式
- 🎬 頁面轉換動畫
- 📈 高級分析儀表板

---

**Status**: 設計審核中 ⏳
