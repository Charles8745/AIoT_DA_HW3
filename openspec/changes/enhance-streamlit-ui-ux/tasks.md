# Implementation Tasks: Enhance Streamlit UI/UX

**Change ID:** `enhance-streamlit-ui-ux`  
**Version:** 1.0  
**Status:** 📋 To Do  
**Phase:** Pre-Implementation  

---

## Overview

本檔案列出實施 UI/UX 增強所需的所有任務，按優先級和依賴關係排序。

---

## 📋 Task Checklist

### Phase 1: Theme System & UI Fundamentals (Days 1-2)

**Priority:** 🔴 Critical  
**Dependencies:** None  

#### Task 1.1: Create Theme Manager Module
- [ ] 創建 `sources/themes.py`
- [ ] 實現 `ThemeManager` 類
  - [ ] `get_theme()` 方法
  - [ ] `set_theme(theme_name)` 方法
  - [ ] `get_colors()` 方法
- [ ] 定義 light 和 dark 主題配置
- [ ] 添加顏色對比度驗證
- [ ] 編寫 20+ 單元測試
- [ ] **Acceptance**: 
  - [ ] 主題切換工作正常
  - [ ] 顏色對比度符合 WCAG AA
  - [ ] 所有測試通過

**Estimated Time:** 4 hours  
**Owner:** UI Lead  

#### Task 1.2: Implement Theme Persistence
- [ ] 使用 `st.session_state` 存儲主題選擇
- [ ] 集成瀏覽器 localStorage (使用 streamlit-extras)
- [ ] 檢測系統偏好 (prefers-color-scheme)
- [ ] 實現主題加載邏輯
- [ ] 添加過渡動畫 (300ms)
- [ ] **Acceptance**:
  - [ ] 主題在刷新後保持
  - [ ] 系統偏好自動應用
  - [ ] 過渡平滑

**Estimated Time:** 3 hours  
**Depends On:** Task 1.1  

#### Task 1.3: Create Enhanced Navigation Component
- [ ] 創建 `sources/navigation.py`
- [ ] 實現 `NavigationItem` 類
- [ ] 實現 `SidebarNavigator` 類
  - [ ] `render()` 方法
  - [ ] `get_active_page()` 方法
  - [ ] 鍵盤快捷鍵支持 (Alt+1, Alt+2, etc.)
- [ ] 添加活動頁面高亮
- [ ] 編寫焦點管理邏輯
- [ ] 添加 50+ 行單元測試
- [ ] **Acceptance**:
  - [ ] 導航菜單正確渲染
  - [ ] 快捷鍵工作正常
  - [ ] 焦點管理正確
  - [ ] 所有測試通過

**Estimated Time:** 4 hours  
**Depends On:** Task 1.1  

#### Task 1.4: Create Toast Notification System
- [ ] 創建 `sources/notifications.py`
- [ ] 實現 `NotificationLevel` enum
- [ ] 實現 `Toast` 類
- [ ] 實現 `show_toast()` 函數
  - [ ] Level 參數 (success, info, warning, error)
  - [ ] 自動消失計時
  - [ ] 堆疊支持
- [ ] 添加 CSS 樣式
- [ ] 編寫 30+ 行測試
- [ ] **Acceptance**:
  - [ ] Toast 顯示在正確位置
  - [ ] 自動消失計時工作
  - [ ] 多個 toast 正確堆疊
  - [ ] 顏色清晰區分

**Estimated Time:** 3 hours  
**Depends On:** None  

#### Task 1.5: Update CSS Variables System
- [ ] 修改 `streamlit_app.py` 中的 CSS
- [ ] 將所有硬編碼顏色轉換為 CSS 變數
- [ ] 創建明暗兩套顏色變數
- [ ] 更新所有組件引用
- [ ] 測試主題切換時的顏色更新
- [ ] **Acceptance**:
  - [ ] 所有顏色使用變數
  - [ ] 沒有硬編碼顏色值
  - [ ] 主題切換立即生效
  - [ ] 沒有顏色閃爍

**Estimated Time:** 3 hours  
**Depends On:** Task 1.1, 1.2  

---

### Phase 2: Navigation & Interactive Feedback (Days 2-3)

**Priority:** 🟡 High  
**Dependencies:** Phase 1 完成  

#### Task 2.1: Integrate Theme Toggle to UI
- [ ] 在 `page_overview()` 中添加主題切換按鈕
- [ ] 連接到 `ThemeManager`
- [ ] 添加按鈕圖標 (☀️/🌙)
- [ ] 測試所有頁面的主題切換
- [ ] **Acceptance**:
  - [ ] 按鈕在頁頭可見
  - [ ] 點擊切換主題
  - [ ] 所有頁面更新

**Estimated Time:** 2 hours  
**Depends On:** Task 1.1, 1.5  

#### Task 2.2: Integrate Toast System to Pages
- [ ] 更新 `page_live_inference()` 添加成功/錯誤 toast
- [ ] 更新 `page_metrics_explorer()` 添加加載 toast
- [ ] 在所有表單提交後添加 toast
- [ ] 測試 toast 在各個頁面的顯示
- [ ] **Acceptance**:
  - [ ] Toast 在關鍵操作後出現
  - [ ] 消息清晰有幫助
  - [ ] 不影響用戶交互

**Estimated Time:** 3 hours  
**Depends On:** Task 1.4  

#### Task 2.3: Implement Keyboard Navigation
- [ ] 在 `streamlit_app.py` 添加鍵盤事件監聽
- [ ] 實現 Alt+N 快捷鍵切換頁面
- [ ] 實現 Tab 鍵導航
- [ ] 實現 Escape 鍵關閉模態
- [ ] 添加鍵盤幫助菜單 (Alt+H)
- [ ] 測試所有快捷鍵
- [ ] **Acceptance**:
  - [ ] 快捷鍵工作正常
  - [ ] 焦點管理正確
  - [ ] 幫助菜單顯示所有快捷鍵

**Estimated Time:** 4 hours  
**Depends On:** Task 1.3  

#### Task 2.4: Create Form Validation Component
- [ ] 創建 `sources/form_components.py`
- [ ] 實現 `ValidatedInput` 類
- [ ] 實現 `ValidatedSlider` 類
- [ ] 實現實時驗證邏輯
- [ ] 添加錯誤提示和成功指示
- [ ] 編寫 40+ 行測試
- [ ] **Acceptance**:
  - [ ] 實時驗證工作正常
  - [ ] 錯誤提示清晰
  - [ ] 成功狀態標記
  - [ ] 所有驗證規則有效

**Estimated Time:** 3 hours  
**Depends On:** None  

#### Task 2.5: Integrate Form Validation to Pages
- [ ] 更新 `page_live_inference()` 使用 `ValidatedInput`
- [ ] 更新 `page_metrics_explorer()` 表單驗證
- [ ] 在所有輸入字段添加幫助文本
- [ ] 測試表單驗證在各頁面
- [ ] **Acceptance**:
  - [ ] 表單驗證工作正常
  - [ ] 錯誤防止提交
  - [ ] 幫助文本有用

**Estimated Time:** 2.5 hours  
**Depends On:** Task 2.4  

---

### Phase 3: Responsive Design (Days 3-4)

**Priority:** 🟡 High  
**Dependencies:** Phase 1 完成  

#### Task 3.1: Create Responsive Layout Helpers
- [ ] 創建 `sources/responsive_styles.py`
- [ ] 定義斷點常數
  - [ ] MOBILE (0-639px)
  - [ ] TABLET (640-1023px)
  - [ ] DESKTOP (1024px+)
- [ ] 實現 `ResponsiveGrid` 類
- [ ] 實現 `get_column_count()` 函數
- [ ] 編寫 30+ 行測試
- [ ] **Acceptance**:
  - [ ] 斷點正確
  - [ ] 列數計算準確
  - [ ] 所有測試通過

**Estimated Time:** 2.5 hours  
**Depends On:** None  

#### Task 3.2: Optimize CSS for Mobile
- [ ] 為所有組件添加媒體查詢
  - [ ] 在 640px 處調整
  - [ ] 在 1024px 處調整
- [ ] 優化 padding/margin for mobile
- [ ] 調整字體大小
- [ ] 優化按鈕尺寸 (48x48px minimum)
- [ ] **Acceptance**:
  - [ ] 沒有硬編碼 px (使用相對單位)
  - [ ] 所有元素在 3 個斷點可用
  - [ ] 沒有水平溢出

**Estimated Time:** 3 hours  
**Depends On:** Task 3.1  

#### Task 3.3: Create Mobile Navigation Drawer
- [ ] 創建 `sources/mobile_drawer.py`
- [ ] 實現 `MobileDrawer` 類
- [ ] 在手機上隱藏側邊欄，顯示漢堡菜單
- [ ] 實現抽屜滑出/滑入動畫 (300ms)
- [ ] 添加手勢支持 (向左滑關閉)
- [ ] 測試在多個屏幕寬度
- [ ] **Acceptance**:
  - [ ] 漢堡菜單在 < 768px 出現
  - [ ] 抽屜平滑動畫
  - [ ] 手勢關閉工作
  - [ ] 焦點管理正確

**Estimated Time:** 3.5 hours  
**Depends On:** Task 3.1  

#### Task 3.4: Optimize Images & Charts for Responsive
- [ ] 使用 Plotly 響應式設置更新圖表
- [ ] 設置圖表容器寬度 100%
- [ ] 調整圖表高度計算
- [ ] 測試圖表在小屏幕上的顯示
- [ ] **Acceptance**:
  - [ ] 圖表在所有尺寸可見
  - [ ] 交互功能在移動設備上可用
  - [ ] 沒有溢出

**Estimated Time:** 2 hours  
**Depends On:** Task 3.1  

#### Task 3.5: Device Responsiveness Testing
- [ ] 在 10+ 設備上測試 (iOS/Android/Web)
  - [ ] iPhone SE (375px)
  - [ ] iPhone 12 (390px)
  - [ ] Pixel 6 (412px)
  - [ ] iPad (768px)
  - [ ] iPad Pro (1024px)
  - [ ] Desktop (1920px)
- [ ] 檢查無水平滾動
- [ ] 驗證所有功能可用
- [ ] 記錄任何問題
- [ ] **Acceptance**:
  - [ ] 所有設備上都可用
  - [ ] 沒有佈局問題
  - [ ] 性能良好

**Estimated Time:** 4 hours  
**Depends On:** Task 3.1-3.4  

---

### Phase 4: Accessibility (Days 4-6)

**Priority:** 🟡 High  
**Dependencies:** Phase 1 完成  

#### Task 4.1: Color Contrast Audit
- [ ] 使用 WebAIM Contrast Checker 檢查所有顏色對
- [ ] 使用 WAVE 掃描所有頁面
- [ ] 使用 Lighthouse 檢查無障礙得分
- [ ] 記錄所有對比度問題
- [ ] **Acceptance**:
  - [ ] 所有顏色對比度 ≥ 4.5:1
  - [ ] WAVE 無錯誤
  - [ ] Lighthouse 得分 ≥ 90

**Estimated Time:** 2.5 hours  
**Depends On:** None  

#### Task 4.2: Implement Semantic HTML & ARIA
- [ ] 創建 `sources/accessibility_helpers.py`
- [ ] 實現 ARIA label 生成函數
- [ ] 為所有 input 添加 <label>
- [ ] 為所有按鈕添加 aria-label
- [ ] 添加 aria-describedby 到表單字段
- [ ] 使用 aria-live regions 通知動態內容
- [ ] 編寫 50+ 行測試
- [ ] **Acceptance**:
  - [ ] 屏幕讀者讀出所有內容
  - [ ] 沒有缺失的 label
  - [ ] ARIA roles 正確
  - [ ] axe DevTools 無錯誤

**Estimated Time:** 4 hours  
**Depends On:** None  

#### Task 4.3: Implement Keyboard Navigation Enhancements
- [ ] 添加 `tabindex` 屬性
- [ ] 實現合邏輯的 Tab 順序
- [ ] 添加 `:focus` 和 `:focus-visible` 樣式
- [ ] 確保焦點指示器清晰 (≥ 3px, ≥ 3:1 對比度)
- [ ] 實現 modal 焦點陷阱
- [ ] 測試鍵盤導航
- [ ] **Acceptance**:
  - [ ] Tab 遍歷所有元素
  - [ ] 焦點順序合邏輯
  - [ ] 焦點指示器清晰
  - [ ] Modal 焦點陷阱工作

**Estimated Time:** 3.5 hours  
**Depends On:** None  

#### Task 4.4: Implement Focus Management
- [ ] 創建 `FocusManager` 類
- [ ] 打開 modal 時移動焦點
- [ ] 關閉 modal 時恢復焦點
- [ ] 實現焦點恢復邏輯
- [ ] 測試所有焦點場景
- [ ] **Acceptance**:
  - [ ] 焦點在正確的位置
  - [ ] 焦點能正確恢復
  - [ ] 無焦點陷阱 (除非必需)

**Estimated Time:** 2.5 hours  
**Depends On:** Task 4.3  

#### Task 4.5: Optimize Text Sizing & Readability
- [ ] 使用 rem 單位替代 px
- [ ] 設置字體大小
  - [ ] 正常文本: 14px
  - [ ] 大型文本: 18px
  - [ ] 按鈕: 16px
- [ ] 設置行高 ≥ 1.5
- [ ] 設置字母間距 ≥ 0.12em
- [ ] 測試 200% 瀏覽器縮放
- [ ] **Acceptance**:
  - [ ] 字體大小一致
  - [ ] 200% 縮放時沒有溢出
  - [ ] 行高和字母間距適當

**Estimated Time:** 2 hours  
**Depends On:** None  

#### Task 4.6: Accessibility Testing & Validation
- [ ] 使用屏幕讀者測試 (NVDA/JAWS/VoiceOver)
- [ ] 鍵盤導航完整測試
- [ ] 瀏覽器縮放測試 (100%-200%)
- [ ] 高對比度模式測試
- [ ] 自動化工具驗證 (axe, WAVE, Lighthouse)
- [ ] 記錄所有問題
- [ ] **Acceptance**:
  - [ ] 屏幕讀者可用性驗證
  - [ ] 所有鍵盤快捷鍵工作
  - [ ] 縮放不導致問題
  - [ ] 所有自動化測試通過

**Estimated Time:** 5 hours  
**Depends On:** Task 4.1-4.5  

---

### Phase 5: Performance Optimization (Days 5-7)

**Priority:** 🟠 Medium  
**Dependencies:** Phase 1-2 完成  

#### Task 5.1: Implement Caching Layer
- [ ] 創建 `sources/caching.py`
- [ ] 實現 `CacheManager` 類
- [ ] 在 `load_model_metrics()` 等函數上應用 `@st.cache_data`
  - [ ] TTL 設置為 5 分鐘
- [ ] 在關鍵函數上應用 session cache
- [ ] 實現緩存失效機制
- [ ] 添加緩存統計
- [ ] **Acceptance**:
  - [ ] 重複操作快 100 倍
  - [ ] TTL 後自動失效
  - [ ] 用戶可清除緩存
  - [ ] 內存使用 < 500MB

**Estimated Time:** 3 hours  
**Depends On:** None  

#### Task 5.2: Implement Lazy Loading & Conditional Rendering
- [ ] 使用 `st.tabs()` 實現標籤頁延遲加載
- [ ] 修改 `page_metrics_explorer()` 使用 tabs
- [ ] 修改 `page_feature_importance()` 使用 tabs
- [ ] 在大圖表上實現"加載更多"
- [ ] 測試標籤頁加載
- [ ] **Acceptance**:
  - [ ] 不在視圖中的標籤頁不渲染
  - [ ] 初始加載時間 < 1.5s
  - [ ] 沒有不必要的 API 調用

**Estimated Time:** 3.5 hours  
**Depends On:** None  

#### Task 5.3: Implement Pagination
- [ ] 創建 `sources/data_pagination.py`
- [ ] 實現 `Paginator` 類
- [ ] 在 `page_data_overview()` 實現分頁
- [ ] 每頁顯示 20-50 行
- [ ] 實現搜索/過濾與分頁的交互
- [ ] **Acceptance**:
  - [ ] 大型表格不凍結 UI
  - [ ] 分頁控件清晰
  - [ ] 搜索快速 (< 200ms)

**Estimated Time:** 3 hours  
**Depends On:** None  

#### Task 5.4: Implement Performance Monitoring
- [ ] 創建 `sources/performance_monitor.py`
- [ ] 實現 `PerformanceMonitor` 類
- [ ] 添加 `@timeit` decorator
- [ ] 在關鍵函數上應用監控
- [ ] 在管理頁面顯示指標
- [ ] 添加日志記錄
- [ ] **Acceptance**:
  - [ ] 所有頁面加載時間 < 2s
  - [ ] 函數執行時間被記錄
  - [ ] 性能儀表板可用

**Estimated Time:** 3 hours  
**Depends On:** None  

#### Task 5.5: CSS & JavaScript Optimization
- [ ] 使用 PurgeCSS 清理未使用的 CSS
- [ ] 最小化 CSS 文件大小
- [ ] 內聯關鍵 CSS
- [ ] 優化 JavaScript 代碼
- [ ] 使用 gzip 壓縮
- [ ] **Acceptance**:
  - [ ] CSS 文件 < 50KB
  - [ ] FCP < 1.5s
  - [ ] FP < 1s

**Estimated Time:** 2.5 hours  
**Depends On:** None  

#### Task 5.6: Performance Testing & Optimization
- [ ] 使用 Lighthouse 測試所有頁面
- [ ] 使用 WebPageTest 測試加載性能
- [ ] 使用 Chrome DevTools Profiler
- [ ] 記錄基準指標
- [ ] 比較優化前後
- [ ] **Acceptance**:
  - [ ] 所有性能目標達到
  - [ ] LCP < 2.5s
  - [ ] TTI < 3.8s
  - [ ] CLS < 0.1

**Estimated Time:** 4 hours  
**Depends On:** Task 5.1-5.5  

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 28 |
| **Total Estimated Hours** | 85 |
| **Total Estimated Days** | 11-12 days (realistic) |
| **Critical Tasks** | 5 |
| **High Priority Tasks** | 12 |
| **Medium Priority Tasks** | 11 |

---

## Phase Dependencies

```
Phase 1: Theme & Navigation
    ↓
Phase 2: Interactive Feedback
    ↓
Phase 3: Responsive Design (Parallel with Phase 2)
    ↓
Phase 4: Accessibility (Parallel with Phase 3)
    ↓
Phase 5: Performance (Parallel with Phase 4)
    ↓
Testing & Integration
    ↓
Deployment
```

---

## Progress Tracking

**Status**: 📋 Ready for Implementation Approval

Once approved, tasks will be marked as follows:
- ✅ Completed
- 🔄 In Progress
- ⏳ Pending
- ❌ Blocked

---

## Notes

- 所有時間估計包括編碼、測試和文檔
- 依賴關係可能導致串行化
- 建議並行執行無依賴的任務
- 每日站會檢查進度
- 如有 blocking 問題立即升級

**Status**: Pending Approval ⏳
