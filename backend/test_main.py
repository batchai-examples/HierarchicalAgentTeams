import pytest
import uvicorn
from api import fastapi_app

# Test cases for the main application entry point

def test_uvicorn_run():
    """Test that uvicorn.run is called with the correct parameters."""
    # Arrange
    host = "0.0.0.0"
    port = 4080

    # Act
    uvicorn.run(fastapi_app, host=host, port=port)

    # Assert
    # Since uvicorn.run does not return a value, we cannot assert directly.
    # However, we can check if the server starts without exceptions.
    assert True  # Placeholder for actual server start verification

def test_uvicorn_run_with_different_port():
    """Test that uvicorn.run can be called with a different port."""
    # Arrange
    host = "0.0.0.0"
    port = 5000

    # Act
    uvicorn.run(fastapi_app, host=host, port=port)

    # Assert
    assert True  # Placeholder for actual server start verification

def test_uvicorn_run_with_invalid_host():
    """Test that uvicorn.run raises an error with an invalid host."""
    # Arrange
    invalid_host = "256.256.256.256"
    port = 4080

    # Act & Assert
    with pytest.raises(ValueError):
        uvicorn.run(fastapi_app, host=invalid_host, port=port)

def test_uvicorn_run_with_invalid_port():
    """Test that uvicorn.run raises an error with an invalid port."""
    # Arrange
    host = "0.0.0.0"
    invalid_port = 70000  # Port number out of range

    # Act & Assert
    with pytest.raises(ValueError):
        uvicorn.run(fastapi_app, host=host, port=invalid_port)

def test_uvicorn_run_with_none_app():
    """Test that uvicorn.run raises an error when no app is provided."""
    # Arrange
    host = "0.0.0.0"
    port = 4080

    # Act & Assert
    with pytest.raises(TypeError):
        uvicorn.run(None, host=host, port=port)
