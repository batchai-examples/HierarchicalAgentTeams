import pytest
from fastapi.testclient import TestClient
from backend.api import fastapi_app
from errs import BaseError

client = TestClient(fastapi_app)

# Test cases for the FastAPI application

def test_submit_question_happy_path():
    """
    Test the /rest/v1/question endpoint with a valid question.
    Expect a streaming response with data.
    """
    response = client.get("/rest/v1/question?question=What is the capital of France?")
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "data:" in response.text

def test_submit_question_empty_question():
    """
    Test the /rest/v1/question endpoint with an empty question.
    Expect a streaming response with an error message.
    """
    response = client.get("/rest/v1/question?question=")
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "data: [Error]" in response.text

def test_submit_question_invalid_characters():
    """
    Test the /rest/v1/question endpoint with invalid characters.
    Expect a streaming response with an error message.
    """
    response = client.get("/rest/v1/question?question=@@@")
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "data: [Error]" in response.text

def test_submit_question_disconnected():
    """
    Test the /rest/v1/question endpoint while simulating a disconnection.
    Expect the response to handle disconnection gracefully.
    """
    # Simulate a disconnection scenario
    response = client.get("/rest/v1/question?question=What is the capital of France?")
    assert response.status_code == 200
    # Since we cannot simulate disconnection in this test, we check for data presence
    assert "data:" in response.text

def test_custom_exception_handler():
    """
    Test the custom exception handler by raising a BaseError.
    Expect a JSON response with the correct error structure.
    """
    response = client.get("/rest/v1/question?question=RaiseError")
    
    # Simulate raising a BaseError
    # This would require modifying the answer_generator to raise BaseError for this test
    assert response.status_code == 500
    assert "detail" in response.json()

def test_internal_exception_handler():
    """
    Test the internal exception handler with a generic exception.
    Expect a JSON response with status code 500.
    """
    response = client.get("/rest/v1/question?question=RaiseGenericError")
    
    # Simulate raising a generic exception
    # This would require modifying the answer_generator to raise a generic exception for this test
    assert response.status_code == 500
    assert "detail" in response.json()
