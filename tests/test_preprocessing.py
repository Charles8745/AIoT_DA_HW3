"""文本預處理模組的單元測試。

測試 PreprocessingConfig、TextPreprocessor 和相關函數。

Test Coverage:
    - Configuration classes
    - Individual preprocessing functions
    - Pipeline orchestration (process method)
    - Batch processing
    - Error handling
    - Edge cases

Author:
    AIoT_DA_HW3 Team
"""

import pytest
import sys
import os

# Add sources directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sources'))

from preprocessing import (
    PreprocessingConfig,
    TextPreprocessor,
    preprocess_text,
    get_default_config,
    get_aggressive_config,
    get_conservative_config,
    ENGLISH_STOPWORDS
)


class TestPreprocessingConfig:
    """測試 PreprocessingConfig 資料類。"""
    
    def test_default_config(self):
        """測試預設配置。"""
        config = PreprocessingConfig()
        assert config.lowercase == True
        assert config.remove_urls == True
        assert config.remove_emails == True
        assert config.remove_punctuation == True
        assert config.remove_numbers == False
        assert config.remove_stopwords == False
        assert config.normalize_whitespace == True
        assert config.remove_non_ascii == True
    
    def test_custom_config(self):
        """測試自訂配置。"""
        config = PreprocessingConfig(
            lowercase=False,
            remove_urls=False,
            remove_numbers=True,
            remove_stopwords=True
        )
        assert config.lowercase == False
        assert config.remove_urls == False
        assert config.remove_numbers == True
        assert config.remove_stopwords == True
    
    def test_config_all_false(self):
        """測試全關閉配置。"""
        config = PreprocessingConfig(
            lowercase=False,
            remove_urls=False,
            remove_emails=False,
            remove_punctuation=False,
            remove_numbers=False,
            remove_stopwords=False,
            normalize_whitespace=False,
            remove_non_ascii=False
        )
        # 驗證所有選項都是 False
        assert not config.lowercase
        assert not config.remove_urls
        assert not config.remove_emails
        assert not config.remove_punctuation
        assert not config.remove_numbers
        assert not config.remove_stopwords
        assert not config.normalize_whitespace
        assert not config.remove_non_ascii


class TestTextPreprocessor:
    """測試 TextPreprocessor 類。"""
    
    def test_initialization_default(self):
        """測試預設初始化。"""
        processor = TextPreprocessor()
        assert processor.config is not None
        assert processor.stopwords_set is not None
    
    def test_initialization_with_config(self):
        """測試帶配置的初始化。"""
        config = PreprocessingConfig(remove_stopwords=True)
        processor = TextPreprocessor(config)
        assert processor.config == config
    
    def test_initialization_invalid_config(self):
        """測試無效配置類型。"""
        with pytest.raises(TypeError):
            TextPreprocessor("invalid")
    
    def test_remove_urls(self):
        """測試 URL 移除。"""
        processor = TextPreprocessor()
        
        # 測試 HTTP URLs
        text = "Visit http://example.com for more"
        result = processor.remove_urls(text)
        assert "http://example.com" not in result
        assert "for more" in result
        
        # 測試 HTTPS URLs
        text = "Check https://secure.com now"
        result = processor.remove_urls(text)
        assert "https://secure.com" not in result
        
        # 測試 www URLs
        text = "Go to www.example.com"
        result = processor.remove_urls(text)
        assert "www.example.com" not in result
    
    def test_remove_emails(self):
        """測試電郵移除。"""
        processor = TextPreprocessor()
        
        text = "Contact me at john@example.com for help"
        result = processor.remove_emails(text)
        assert "john@example.com" not in result
        assert "for help" in result
        
        # 測試多個電郵
        text = "Email admin@test.com or support@company.net"
        result = processor.remove_emails(text)
        assert "admin@test.com" not in result
        assert "support@company.net" not in result
    
    def test_remove_punctuation(self):
        """測試標點符號移除。"""
        processor = TextPreprocessor()
        
        text = "Hello!!! How are you???"
        result = processor.remove_punctuation(text)
        assert "!!!" not in result
        assert "???" not in result
        assert "Hello" in result
        assert "How" in result
    
    def test_remove_numbers(self):
        """測試數字移除。"""
        processor = TextPreprocessor()
        
        text = "Call 555-1234 or dial 1800HELP"
        result = processor.remove_numbers(text)
        assert "555" not in result
        assert "1234" not in result
        assert "1800" not in result
        assert "Call" in result
        assert "or" in result
    
    def test_normalize_whitespace(self):
        """測試空白正規化。"""
        processor = TextPreprocessor()
        
        # 多個空格
        text = "Hello    world"
        result = processor.normalize_whitespace(text)
        assert result == "Hello world"
        
        # 換行符
        text = "Hello\nworld"
        result = processor.normalize_whitespace(text)
        assert result == "Hello world"
        
        # 首尾空格
        text = "  Hello world  "
        result = processor.normalize_whitespace(text)
        assert result == "Hello world"
    
    def test_normalize_case(self):
        """測試大小寫正規化。"""
        processor = TextPreprocessor()
        
        text = "HELLO World"
        result = processor.normalize_case(text)
        assert result == "hello world"
    
    def test_remove_non_ascii(self):
        """測試非 ASCII 移除。"""
        processor = TextPreprocessor()
        
        text = "Hello café"
        result = processor.remove_non_ascii(text)
        assert "é" not in result
        assert "Hello" in result
        assert "caf" in result
    
    def test_remove_stopwords(self):
        """測試停用詞移除。"""
        processor = TextPreprocessor()
        
        text = "the quick brown fox"
        result = processor.remove_stopwords(text)
        # 'the' 應該被移除
        assert result != text
        assert "quick" in result
        assert "brown" in result
        assert "fox" in result
    
    def test_process_basic(self):
        """測試基本的 process() 管道。"""
        processor = TextPreprocessor()
        
        text = "Visit http://spam.com!!! Contact: spam@fake.net"
        result = processor.process(text)
        
        # 驗證 URLs 和 emails 已移除
        assert "http://spam.com" not in result
        assert "spam@fake.net" not in result
        # 驗證結果是小寫
        assert result == result.lower()
    
    def test_process_aggressive(self):
        """測試積極的 process() 配置。"""
        config = get_aggressive_config()
        processor = TextPreprocessor(config)
        
        text = "The quick brown fox jumps over the lazy dog"
        result = processor.process(text)
        
        # 驗證停用詞已移除
        assert "the" not in result.split()
        assert "over" not in result.split()
        # 驗證核心詞保留
        assert "quick" in result
        assert "brown" in result
    
    def test_process_empty_string(self):
        """測試空字串。"""
        processor = TextPreprocessor()
        result = processor.process("")
        assert result == ""
    
    def test_process_none_input(self):
        """測試 None 輸入。"""
        processor = TextPreprocessor()
        with pytest.raises(ValueError):
            processor.process(None)
    
    def test_process_numeric_input(self):
        """測試數字輸入。"""
        processor = TextPreprocessor()
        # 應該接受數字並轉換為字串
        result = processor.process(12345)
        assert isinstance(result, str)
    
    def test_batch_process(self):
        """測試批量處理。"""
        processor = TextPreprocessor()
        
        texts = [
            "Visit http://example.com",
            "Email test@example.net",
            "Hello!!! World???"
        ]
        results = processor.batch_process(texts)
        
        assert len(results) == len(texts)
        assert all(isinstance(r, str) for r in results)
        # 驗證 URLs 和 emails 已移除
        assert "http://example.com" not in results[0]
        assert "test@example.net" not in results[1]
    
    def test_batch_process_empty_list(self):
        """測試空列表。"""
        processor = TextPreprocessor()
        with pytest.raises(ValueError):
            processor.batch_process([])
    
    def test_batch_process_none_input(self):
        """測試 None 輸入。"""
        processor = TextPreprocessor()
        with pytest.raises(ValueError):
            processor.batch_process(None)
    
    def test_batch_process_invalid_type(self):
        """測試無效類型。"""
        processor = TextPreprocessor()
        with pytest.raises(TypeError):
            processor.batch_process("not a list")


class TestConvenienceFunctions:
    """測試便利函數。"""
    
    def test_preprocess_text_default(self):
        """測試預設配置的便利函數。"""
        text = "Visit http://EXAMPLE.COM!!!"
        result = preprocess_text(text)
        assert isinstance(result, str)
        assert "http://example.com" not in result
    
    def test_preprocess_text_with_config(self):
        """測試帶配置的便利函數。"""
        text = "The quick brown fox"
        config = get_aggressive_config()
        result = preprocess_text(text, config)
        # 停用詞應該被移除
        assert "quick" in result
        assert "brown" in result
    
    def test_get_default_config(self):
        """測試獲取預設配置。"""
        config = get_default_config()
        assert isinstance(config, PreprocessingConfig)
        assert config.remove_stopwords == False
    
    def test_get_aggressive_config(self):
        """測試獲取積極配置。"""
        config = get_aggressive_config()
        assert isinstance(config, PreprocessingConfig)
        assert config.remove_stopwords == True
        assert config.remove_numbers == True
    
    def test_get_conservative_config(self):
        """測試獲取保守配置。"""
        config = get_conservative_config()
        assert isinstance(config, PreprocessingConfig)
        assert config.remove_stopwords == False
        assert config.remove_punctuation == False


class TestEdgeCases:
    """測試邊界情況。"""
    
    def test_very_long_text(self):
        """測試非常長的文本。"""
        processor = TextPreprocessor()
        long_text = "word " * 10000  # 10,000 個詞
        result = processor.process(long_text)
        assert isinstance(result, str)
    
    def test_special_characters(self):
        """測試特殊字符。"""
        processor = TextPreprocessor()
        text = "Price: $$$, Email: test@ex.com, URL: http://test.com"
        result = processor.process(text)
        assert "$$$" not in result
        assert "test@ex.com" not in result
        assert "http://test.com" not in result
    
    def test_mixed_case_urls(self):
        """測試混合大小寫的 URLs。"""
        processor = TextPreprocessor()
        text = "Visit HTTP://EXAMPLE.COM or HTTPS://SECURE.COM"
        result = processor.remove_urls(text)
        assert "HTTP://EXAMPLE.COM" not in result
        assert "HTTPS://SECURE.COM" not in result
    
    def test_unicode_text(self):
        """測試 Unicode 文本。"""
        processor = TextPreprocessor()
        text = "Hello 世界 café"
        result = processor.process(text)
        assert isinstance(result, str)
    
    def test_repeated_punctuation(self):
        """測試重複的標點符號。"""
        processor = TextPreprocessor()
        text = "Really!!!!! Amazing?????? Yes!!!"
        result = processor.remove_punctuation(text)
        assert "!" not in result
        assert "?" not in result
        assert "Really" in result


class TestIntegration:
    """整合測試。"""
    
    def test_full_spam_pipeline(self):
        """測試完整的垃圾短信管道。"""
        config = get_aggressive_config()
        processor = TextPreprocessor(config)
        
        spam_text = "CLICK HERE!!! Visit http://money.com or email winner@fake.net for FREE $$$ CALL NOW 1-800-SPAM"
        result = processor.process(spam_text)
        
        # 驗證清理效果
        assert "http://money.com" not in result
        assert "winner@fake.net" not in result
        assert "$$$" not in result
        assert "1800" not in result
        # 驗證核心詞保留
        assert "click" in result
        assert "free" in result
    
    def test_config_combinations(self):
        """測試不同的配置組合。"""
        configs = [
            get_default_config(),
            get_aggressive_config(),
            get_conservative_config()
        ]
        
        text = "Visit HTTP://EXAMPLE.COM and email test@ex.com!!!"
        
        for config in configs:
            processor = TextPreprocessor(config)
            result = processor.process(text)
            assert isinstance(result, str)
            assert len(result) >= 0
    
    def test_reproducibility(self):
        """測試結果的可重複性。"""
        processor = TextPreprocessor()
        text = "Test string with http://url.com and email@test.net"
        
        result1 = processor.process(text)
        result2 = processor.process(text)
        
        assert result1 == result2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
