# Specification: Streamlit UI System

**Capability:** `streamlit-ui-system`  
**Version:** 1.0  
**Status:** 📋 Proposed  
**Change ID:** `enhance-streamlit-ui-ux`  

---

## Overview

本規範定義 Streamlit 應用的統一 UI 系統，包括導航結構、主題管理、設計系統組件和交互反饋機制。

---

## ADDED Requirements

### Requirement 1: Theme Management System
**Description:** 提供統一的主題管理系統，支持淺色和黑暗模式切換。

**Details:**
- 定義明暗兩套完整的顏色方案
- 提供主題切換函數和 UI 控件
- 持久化用戶主題選擇 (session_state + localStorage)
- 自動適應系統主題偏好

**Implementation:**
- 新建 `sources/themes.py` 模組
  - `ThemeManager` 類
  - `get_theme()` 函數
  - `apply_theme()` 函數
- 更新 `streamlit_app.py`
  - 集成主題切換控件

**Acceptance Criteria:**
- [ ] 主題在頁面重新加載後保持
- [ ] 系統偏好自動檢測有效
- [ ] 顏色對比度符合 WCAG 標準
- [ ] 過渡效果平滑 (300ms)

#### Scenario: 用戶從淺色切換到黑暗模式
```
Given: 用戶在淺色模式下查看應用
When: 用戶點擊頁頭的主題切換按鈕
Then: 
  - 應用立即切換到黑暗模式
  - 所有顏色自動更新
  - 用戶選擇保存到 session_state
  - 頁面重新加載後仍是黑暗模式
```

#### Scenario: 新用戶打開應用
```
Given: 新用戶首次打開應用，無之前的主題選擇
When: 應用加載
Then:
  - 檢查瀏覽器 prefers-color-scheme
  - 自動應用匹配的主題 (light 或 dark)
  - 保存為默認選擇
```

---

### Requirement 2: Enhanced Navigation Component
**Description:** 改進側邊欄導航，支持響應式設計、視覺反饋和鍵盤導航。

**Details:**
- 側邊欄在桌面上保持展開，移動設備上摺疊
- 活動頁面高亮標記
- 支持鍵盤快捷鍵 (Alt+1, Alt+2 等)
- 導航項目有懸停和焦點狀態

**Implementation:**
- 新建 `sources/navigation.py` 模組
  - `NavigationItem` 類
  - `SidebarNavigator` 類
- 創建導航菜單 HTML/CSS
- 集成鍵盤事件處理

**Acceptance Criteria:**
- [ ] 導航在 3 個設備尺寸下都可用
- [ ] 活動項目清晰標記
- [ ] 鍵盤快捷鍵正常工作
- [ ] 焦點管理正確
- [ ] 流量統計顯示導航改進 20%

#### Scenario: 用戶通過鍵盤在頁面間導航
```
Given: 用戶使用鍵盤瀏覽應用
When: 用戶按 Alt+3 快捷鍵
Then:
  - 導航到 "Model Comparison" 頁面
  - 焦點自動移到頁面主內容區
  - 頁面加載且不閃爍
```

#### Scenario: 用戶在手機上訪問應用
```
Given: 用戶在手機 (320px 寬) 上打開應用
When: 應用加載
Then:
  - 側邊欄隱藏，顯示漢堡菜單
  - 點擊漢堡菜單後側邊欄作為抽屜出現
  - 側邊欄寬度適合手機屏幕
  - 可以通過返回按鈕或點擊外部關閉
```

---

### Requirement 3: Toast/Notification System
**Description:** 提供非阻塞式通知系統，用於顯示操作結果、錯誤和警告。

**Details:**
- 4 個通知級別 (success, info, warning, error)
- 位置: 右上角固定
- 自動消失 (3-5 秒可配置)
- 支持堆疊顯示多個通知

**Implementation:**
- 新建 `sources/notifications.py` 模組
  - `NotificationLevel` enum
  - `Toast` 類
  - `show_toast()` 函數
- 更新 streamlit_app.py
  - 在關鍵操作後調用 `show_toast()`

**Acceptance Criteria:**
- [ ] 通知在指定位置出現
- [ ] 自動消失計時器工作
- [ ] 多個通知能正確堆疊
- [ ] 顏色和圖標清晰區分級別
- [ ] 關閉按鈕可用

#### Scenario: 用戶提交表單成功
```
Given: 用戶填寫表單並點擊提交
When: 服務器返回成功響應
Then:
  - 綠色 success toast 出現在右上角
  - 顯示消息 "✅ Model trained successfully!"
  - 3 秒後自動消失
  - 用戶能夠關閉 toast
```

#### Scenario: 用戶操作導致錯誤
```
Given: 用戶執行導致錯誤的操作
When: 錯誤發生
Then:
  - 紅色 error toast 出現
  - 顯示錯誤信息和可能的解決方案
  - 5 秒後自動消失 (比成功更長)
  - 用戶可以手動關閉
```

---

### Requirement 4: Enhanced Form Validation & Feedback
**Description:** 提供實時表單驗證和清晰的反饋提示。

**Details:**
- 實時驗證 (邊輸入邊檢查)
- 清晰的錯誤提示 (紅色邊框 + 錯誤文本)
- 成功驗證視覺指示 (綠色對勾)
- 幫助文本和提示

**Implementation:**
- 創建 `sources/form_components.py`
  - `ValidatedInput` 類
  - `ValidatedSlider` 類
  - Validation 規則集合
- 更新表單頁面集成

**Acceptance Criteria:**
- [ ] 實時驗證不超過 100ms 延遲
- [ ] 錯誤提示清晰且有幫助
- [ ] 成功狀態明顯標記
- [ ] 所有表單字段都有標籤和幫助文本

#### Scenario: 用戶輸入無效的模型參數
```
Given: 用戶在推理頁面調整參數
When: 用戶輸入無效值 (例如負數)
Then:
  - 輸入字段邊框變紅
  - 顯示錯誤提示 "Value must be positive"
  - 提交按鈕禁用
  - 用戶修正後，錯誤消失，按鈕啟用
```

---

## MODIFIED Requirements

### Requirement 5: Update Neumorphism Design System
**Description:** 擴展現有的 Neumorphism 設計系統，支持主題切換。

**Details:**
- 將硬編碼顏色改為 CSS 變數
- 創建明暗兩套色彩方案
- 保留動畫和陰影設計

**Scope:**
- 修改 `streamlit_app.py` 中的 `NEUMORPHISM_CSS`
- 新增 CSS 變數定義
- 更新所有顏色引用

**Acceptance Criteria:**
- [ ] 所有顏色使用 CSS 變數
- [ ] 主題切換時顏色立即更新
- [ ] 過渡效果流暢

#### Scenario: 應用加載時應用主題
```
Given: 應用初始化
When: 頁面加載
Then:
  - CSS 變數根據當前主題設置
  - 所有組件使用正確的顏色
  - 沒有顏色閃爍
```

---

## REMOVED Requirements

無需移除的需求。

---

## Related Capabilities

- **streamlit-responsive-design**: 導航在所有設備上都應可用
- **streamlit-accessibility**: 所有組件應支持鍵盤導航
- **streamlit-performance**: 主題切換應在 300ms 內完成

---

## Testing & Validation

### Manual Testing
- [ ] 淺色/黑暗模式切換
- [ ] 各頁面導航正常
- [ ] Toast 通知正確顯示
- [ ] 表單驗證工作

### Automated Testing
```python
def test_theme_manager():
    """Test theme switching."""
    tm = ThemeManager()
    assert tm.get_theme() == 'light'
    tm.set_theme('dark')
    assert tm.get_theme() == 'dark'

def test_toast_notification():
    """Test toast display."""
    show_toast("Test message", NotificationLevel.SUCCESS)
    # 驗證 toast 在 DOM 中
```

### Browser Testing
- Chrome, Firefox, Safari, Edge
- 確保 CSS 變數支持
- 檢查 localStorage 功能

---

## Implementation Timeline

| Task | Duration | Dependencies |
|------|----------|--------------|
| 主題系統實現 | 1 day | None |
| 導航組件改進 | 1 day | 主題系統 |
| Toast 系統 | 0.5 day | None |
| 表單驗證 | 1 day | None |
| 集成測試 | 1 day | All |
| **Total** | **4.5 days** | |

---

**Status**: Pending Approval ⏳
