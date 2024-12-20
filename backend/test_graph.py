import pytest
from unittest.mock import patch, AsyncMock
from backend.graph import call_research_team, call_paper_writing_team, super_graph
from langchain_core.messages import HumanMessage

# Test cases for the graph functions

@pytest.mark.asyncio
async def test_call_research_team_happy_path():
    """
    Test the call_research_team function with a valid state.
    It should return a Command with updated messages and goto 'supervisor'.
    """
    # Arrange
    state = {
        "messages": [
            HumanMessage(content="Research AI agents and write a brief report about them.", name="user")
        ]
    }
    
    with patch('backend.research_graph.invoke', return_value={"messages": [HumanMessage(content="Research report generated.", name="research_team")]}) as mock_invoke:
        # Act
        command = await call_research_team(state)

        # Assert
        assert command.goto == "supervisor"
        assert command.update["messages"][0].content == "Research report generated."
        mock_invoke.assert_called_once()

@pytest.mark.asyncio
async def test_call_paper_writing_team_happy_path():
    """
    Test the call_paper_writing_team function with a valid state.
    It should return a Command with updated messages and goto 'supervisor'.
    """
    # Arrange
    state = {
        "messages": [
            HumanMessage(content="Write a paper about AI advancements.", name="user")
        ]
    }
    
    with patch('backend.paper_writing_graph.invoke', return_value={"messages": [HumanMessage(content="Paper draft created.", name="writing_team")]}) as mock_invoke:
        # Act
        command = await call_paper_writing_team(state)

        # Assert
        assert command.goto == "supervisor"
        assert command.update["messages"][0].content == "Paper draft created."
        mock_invoke.assert_called_once()

@pytest.mark.asyncio
async def test_call_research_team_no_messages():
    """
    Test the call_research_team function with an empty messages state.
    It should raise an IndexError since there are no messages to process.
    """
    # Arrange
    state = {
        "messages": []
    }
    
    with pytest.raises(IndexError):
        await call_research_team(state)

@pytest.mark.asyncio
async def test_call_paper_writing_team_no_messages():
    """
    Test the call_paper_writing_team function with an empty messages state.
    It should raise an IndexError since there are no messages to process.
    """
    # Arrange
    state = {
        "messages": []
    }
    
    with pytest.raises(IndexError):
        await call_paper_writing_team(state)

@pytest.mark.asyncio
async def test_super_graph_stream():
    """
    Test the super_graph's async stream method with valid input.
    It should yield messages containing AIMessageChunk.
    """
    # Arrange
    input_data = {
        "messages": [
            ("user", "Research AI agents and write a brief report about them.")
        ]
    }
    
    async def mock_astream(*args, **kwargs):
        yield [{"checkpoint_ns": "search:1"}, {"content": "AI agents researched.", "checkpoint_ns": "search:1"}]

    with patch.object(super_graph, 'astream', new_callable=AsyncMock, side_effect=mock_astream):
        # Act
        async for messages in super_graph.astream(input_data, {"recursion_limit": 150}, stream_mode="messages"):
            # Assert
            assert len(messages) > 0
            assert "content" in messages[1]

@pytest.mark.asyncio
async def test_super_graph_stream_no_messages():
    """
    Test the super_graph's async stream method with no messages.
    It should handle the case gracefully without yielding any messages.
    """
    # Arrange
    input_data = {
        "messages": []
    }
    
    async def mock_astream(*args, **kwargs):
        yield []

    with patch.object(super_graph, 'astream', new_callable=AsyncMock, side_effect=mock_astream):
        # Act
        async for messages in super_graph.astream(input_data, {"recursion_limit": 150}, stream_mode="messages"):
            # Assert
            assert len(messages) == 0
