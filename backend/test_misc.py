import pytest
from datetime import datetime
from backend.misc import (
    parse_datetime,
    format_datetime,
    guess_mime_type,
    detect_encoding,
    read_file_text,
    write_file_text,
    transfer_file,
    transfer_stream,
    parse_data_url,
    get_str_header,
    get_int_header,
    get_bool_header,
    get_client_ip,
    get_client_port,
    get_client_proto,
    get_client_proxy_chain,
    basename,
    normalize_path
)
from errs import BadRequest

# Test cases for the functions in backend/misc.py

class TestMiscFunctions:

    # Test parse_datetime with valid datetime string
    def test_parse_datetime_valid_string(self):
        """Test parse_datetime with a valid datetime string."""
        result = parse_datetime("2023-10-01 12:00:00")
        assert result == datetime(2023, 10, 1, 12, 0)

    # Test parse_datetime with valid float timestamp
    def test_parse_datetime_valid_float(self):
        """Test parse_datetime with a valid float timestamp."""
        result = parse_datetime(1633072800.0)
        assert result == datetime(2021, 10, 1, 0, 0)

    # Test parse_datetime with valid int timestamp
    def test_parse_datetime_valid_int(self):
        """Test parse_datetime with a valid int timestamp."""
        result = parse_datetime(1633072800)
        assert result == datetime(2021, 10, 1, 0, 0)

    # Test parse_datetime with None
    def test_parse_datetime_none(self):
        """Test parse_datetime with None."""
        result = parse_datetime(None)
        assert result is None

    # Test parse_datetime with invalid string
    def test_parse_datetime_invalid_string(self):
        """Test parse_datetime with an invalid datetime string."""
        with pytest.raises(BadRequest):
            parse_datetime("invalid datetime")

    # Test format_datetime with valid datetime
    def test_format_datetime_valid(self):
        """Test format_datetime with a valid datetime object."""
        dt = datetime(2023, 10, 1, 12, 0)
        result = format_datetime(dt)
        assert result == "2023-10-01 12:00:00"

    # Test format_datetime with None
    def test_format_datetime_none(self):
        """Test format_datetime with None."""
        result = format_datetime(None)
        assert result is None

    # Test guess_mime_type with known file extension
    def test_guess_mime_type_known(self):
        """Test guess_mime_type with a known file extension."""
        result = guess_mime_type("example.txt")
        assert result == "text/plain"

    # Test guess_mime_type with unknown file extension
    def test_guess_mime_type_unknown(self):
        """Test guess_mime_type with an unknown file extension."""
        result = guess_mime_type("example.xyz")
        assert result == "application/octet-stream"

    # Test detect_encoding with valid bytes
    def test_detect_encoding_valid(self):
        """Test detect_encoding with valid byte content."""
        result = detect_encoding(b'This is a test.')
        assert result == 'utf-8'

    # Test parse_data_url with valid data URL
    def test_parse_data_url_valid(self):
        """Test parse_data_url with a valid data URL."""
        result = parse_data_url("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
        assert result == ("text/plain", "base64", b"Hello, World!")

    # Test parse_data_url with invalid data URL
    def test_parse_data_url_invalid(self):
        """Test parse_data_url with an invalid data URL."""
        with pytest.raises(ValueError):
            parse_data_url("invalid_data_url")

    # Test get_str_header with existing header
    def test_get_str_header_existing(self):
        """Test get_str_header with an existing header."""
        class MockRequest:
            headers = {"X-Custom-Header": "value"}

        req = MockRequest()
        result = get_str_header(req, "X-Custom-Header", "default")
        assert result == "value"

    # Test get_str_header with non-existing header
    def test_get_str_header_non_existing(self):
        """Test get_str_header with a non-existing header."""
        class MockRequest:
            headers = {}

        req = MockRequest()
        result = get_str_header(req, "X-Custom-Header", "default")
        assert result == "default"

    # Test get_int_header with existing header
    def test_get_int_header_existing(self):
        """Test get_int_header with an existing header."""
        class MockRequest:
            headers = {"X-Custom-Int": "10"}

        req = MockRequest()
        result = get_int_header(req, "X-Custom-Int", 0)
        assert result == 10

    # Test get_int_header with non-existing header
    def test_get_int_header_non_existing(self):
        """Test get_int_header with a non-existing header."""
        class MockRequest:
            headers = {}

        req = MockRequest()
        result = get_int_header(req, "X-Custom-Int", 5)
        assert result == 5

    # Test get_bool_header with existing header
    def test_get_bool_header_existing_true(self):
        """Test get_bool_header with an existing header set to 'true'."""
        class MockRequest:
            headers = {"X-Custom-Bool": "true"}

        req = MockRequest()
        result = get_bool_header(req, "X-Custom-Bool", False)
        assert result is True

    # Test get_bool_header with non-existing header
    def test_get_bool_header_non_existing(self):
        """Test get_bool_header with a non-existing header."""
        class MockRequest:
            headers = {}

        req = MockRequest()
        result = get_bool_header(req, "X-Custom-Bool", True)
        assert result is True

    # Test basename with valid path
    def test_basename_valid(self):
        """Test basename with a valid path."""
        result = basename("/path/to/file.txt")
        assert result == "to/file.txt"

    # Test normalize_path with valid path
    def test_normalize_path_valid(self):
        """Test normalize_path with a valid path."""
        result = normalize_path("/path/to/../file.txt")
        assert result == "path/to/file.txt"

    # Test normalize_path with empty path
    def test_normalize_path_empty(self):
        """Test normalize_path with an empty path."""
        result = normalize_path("")
        assert result == ""
