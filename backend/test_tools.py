import pytest
from backend.tools import scrape_webpages, create_outline, read_document, write_document, edit_document

# Test cases for the tools in backend/tools.py

# Test case for scrape_webpages function
def test_scrape_webpages():
    """Test the scrape_webpages function with a valid URL."""
    # Step 1: Define a valid URL for testing
    urls = ["https://example.com"]
    # Step 2: Call the function
    result = scrape_webpages(urls)
    # Step 3: Assert that the result is not empty and contains expected format
    assert result != ""
    assert '<Document name="' in result

# Test case for create_outline function
def test_create_outline():
    """Test the create_outline function with valid input."""
    # Step 1: Define points and file name
    points = ["Introduction", "Methodology", "Conclusion"]
    file_name = "test_outline.txt"
    # Step 2: Call the function
    result = create_outline(points, file_name)
    # Step 3: Assert that the result is as expected
    assert result == f"Outline saved to {file_name}"

# Test case for read_document function
def test_read_document():
    """Test the read_document function with a valid file."""
    # Step 1: Write a test document
    write_document("This is a test document.", "test_document.txt")
    # Step 2: Call the function to read the document
    result = read_document("test_document.txt")
    # Step 3: Assert that the content is as expected
    assert result == "This is a test document.\n"

# Test case for write_document function
def test_write_document():
    """Test the write_document function with valid content."""
    # Step 1: Define content and file name
    content = "This is a new document."
    file_name = "new_document.txt"
    # Step 2: Call the function
    result = write_document(content, file_name)
    # Step 3: Assert that the result is as expected
    assert result == f"Document saved to {file_name}"

# Test case for edit_document function
def test_edit_document():
    """Test the edit_document function with valid inputs."""
    # Step 1: Write a test document
    write_document("Line 1\nLine 2\nLine 3", "edit_document.txt")
    # Step 2: Define inserts
    inserts = {2: "Inserted Line"}
    # Step 3: Call the function
    result = edit_document("edit_document.txt", inserts)
    # Step 4: Assert that the result is as expected
    assert result == f"Document edited and saved to edit_document.txt"
    # Step 5: Read the document to verify content
    edited_content = read_document("edit_document.txt")
    assert edited_content == "Line 1\nInserted Line\nLine 2\nLine 3\n"

# Test case for edit_document with out of range line number
def test_edit_document_out_of_range():
    """Test the edit_document function with an out of range line number."""
    # Step 1: Write a test document
    write_document("Line 1\nLine 2\nLine 3", "edit_document_out_of_range.txt")
    # Step 2: Define inserts with an out of range line number
    inserts = {5: "Inserted Line"}
    # Step 3: Call the function
    result = edit_document("edit_document_out_of_range.txt", inserts)
    # Step 4: Assert that the result indicates an error
    assert result == "Error: Line number 5 is out of range."
