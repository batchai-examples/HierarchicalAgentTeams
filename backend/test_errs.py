import pytest
from backend.errs import Internal, BadRequest, Unauthorized, Forbidden, NotFound, Conflict, ErrorCode

# Test cases for the error classes in backend.errs

def test_internal_error():
    """Test the Internal error class with default code."""
    error = Internal("Internal server error")
    assert error.status_code == 500
    assert error.detail == "Internal server error"
    assert error.code == ErrorCode.NONE

def test_internal_error_with_code():
    """Test the Internal error class with a specific error code."""
    error = Internal("Internal server error", ErrorCode.INVALID_PROPERTY)
    assert error.status_code == 500
    assert error.detail == "Internal server error"
    assert error.code == ErrorCode.INVALID_PROPERTY

def test_bad_request_error():
    """Test the BadRequest error class with default code."""
    error = BadRequest("Bad request")
    assert error.status_code == 400
    assert error.detail == "Bad request"
    assert error.code == ErrorCode.NONE

def test_bad_request_error_with_code():
    """Test the BadRequest error class with a specific error code."""
    error = BadRequest("Bad request", ErrorCode.INVALID_ENUM)
    assert error.status_code == 400
    assert error.detail == "Bad request"
    assert error.code == ErrorCode.INVALID_ENUM

def test_unauthorized_error():
    """Test the Unauthorized error class with default code."""
    error = Unauthorized("Unauthorized access")
    assert error.status_code == 401
    assert error.detail == "Unauthorized access"
    assert error.code == ErrorCode.NONE

def test_unauthorized_error_with_code():
    """Test the Unauthorized error class with a specific error code."""
    error = Unauthorized("Unauthorized access", ErrorCode.INVALID_PROPERTY)
    assert error.status_code == 401
    assert error.detail == "Unauthorized access"
    assert error.code == ErrorCode.INVALID_PROPERTY

def test_forbidden_error():
    """Test the Forbidden error class with default code."""
    error = Forbidden("Access forbidden")
    assert error.status_code == 403
    assert error.detail == "Access forbidden"
    assert error.code == ErrorCode.NONE

def test_forbidden_error_with_code():
    """Test the Forbidden error class with a specific error code."""
    error = Forbidden("Access forbidden", ErrorCode.INVALID_ENUM)
    assert error.status_code == 403
    assert error.detail == "Access forbidden"
    assert error.code == ErrorCode.INVALID_ENUM

def test_not_found_error():
    """Test the NotFound error class with default code."""
    error = NotFound("Resource not found")
    assert error.status_code == 404
    assert error.detail == "Resource not found"
    assert error.code == ErrorCode.NONE

def test_conflict_error():
    """Test the Conflict error class with default code."""
    error = Conflict("Conflict occurred")
    assert error.status_code == 409
    assert error.detail == "Conflict occurred"
    assert error.code == ErrorCode.NONE
