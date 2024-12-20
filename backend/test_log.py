import logging
import pytest
from backend.log import get_logger, init_loggers, LogConfig, app_logger

class TestLogging:

    @pytest.fixture(autouse=True)
    def setup_logging(self):
        """Setup logging for tests."""
        # Initialize logging with a default configuration
        log_config = LogConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        init_loggers(log_config)

    def test_get_logger_auto_level(self):
        """Test get_logger with 'auto' level."""
        # Test that the logger is created with the effective level of app_logger
        logger = get_logger("test_auto")
        assert logger.level == app_logger.getEffectiveLevel()

    def test_get_logger_specific_level(self):
        """Test get_logger with a specific logging level."""
        # Test that the logger is created with a specific level
        logger = get_logger("test_specific", logging.WARNING)
        assert logger.level == logging.WARNING

    def test_init_loggers_valid_config(self):
        """Test init_loggers with a valid LogConfig."""
        # Test that init_loggers sets the app_logger level and adds a handler
        log_config = LogConfig(level="INFO", format="%(message)s")
        logger = init_loggers(log_config)
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1  # Check if a handler is added

    def test_init_loggers_invalid_level(self):
        """Test init_loggers with an invalid logging level."""
        # Test that init_loggers raises an error with an invalid level
        log_config = LogConfig(level="INVALID_LEVEL", format="%(message)s")
        with pytest.raises(ValueError):
            init_loggers(log_config)

    def test_get_logger_invalid_name(self):
        """Test get_logger with an invalid name."""
        # Test that get_logger raises an error with an invalid name
        with pytest.raises(TypeError):
            get_logger(None)

    def test_logger_formatting(self, caplog):
        """Test logger output formatting."""
        # Test that the logger outputs messages in the expected format
        logger = get_logger("test_formatting")
        logger.info("Test message")
        assert "Test message" in caplog.text
        assert "test_formatting" in caplog.text  # Check if the logger name is included
