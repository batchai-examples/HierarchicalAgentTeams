import unittest
from unittest.mock import patch, AsyncMock
from backend.research_team import search_node, web_scraper_node, test_research_team
from langchain_core.messages import MessagesState
from langgraph.types import Command

class TestResearchTeam(unittest.TestCase):

    def setUp(self):
        # Set up a mock MessagesState for testing
        self.state = MessagesState(messages=[{"role": "user", "content": "when is Taylor Swift's next tour?"}])

    @patch('backend.research_team.search_agent.invoke', new_callable=AsyncMock)
    def test_search_node_happy_path(self, mock_invoke):
        """
        Test the search_node function with a happy path scenario.
        """
        # Mocking the response from the search agent
        mock_invoke.return_value = {
            "messages": [{"content": "Taylor Swift's next tour is in 2024."}]
        }

        result = search_node(self.state)

        # Check if the command is returned correctly
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "research_team_supervisor")
        self.assertEqual(result.update["messages"][0].content, "Taylor Swift's next tour is in 2024.")

    @patch('backend.research_team.web_scraper_agent.invoke', new_callable=AsyncMock)
    def test_web_scraper_node_happy_path(self, mock_invoke):
        """
        Test the web_scraper_node function with a happy path scenario.
        """
        # Mocking the response from the web scraper agent
        mock_invoke.return_value = {
            "messages": [{"content": "I found information about Taylor Swift's tour."}]
        }
        
        config = {}  # Mock config
        result = web_scraper_node(self.state, config)

        # Check if the command is returned correctly
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "research_team_supervisor")
        self.assertEqual(result.update["messages"][0].content, "I found information about Taylor Swift's tour.")

    @patch('backend.research_team.search_agent.invoke', new_callable=AsyncMock)
    def test_search_node_empty_response(self, mock_invoke):
        """
        Test the search_node function when the response is empty.
        """
        # Mocking an empty response from the search agent
        mock_invoke.return_value = {
            "messages": [{"content": ""}]
        }

        result = search_node(self.state)

        # Check if the command is returned correctly
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "research_team_supervisor")
        self.assertEqual(result.update["messages"][0].content, "")

    @patch('backend.research_team.web_scraper_agent.invoke', new_callable=AsyncMock)
    def test_web_scraper_node_empty_response(self, mock_invoke):
        """
        Test the web_scraper_node function when the response is empty.
        """
        # Mocking an empty response from the web scraper agent
        mock_invoke.return_value = {
            "messages": [{"content": ""}]
        }
        
        config = {}  # Mock config
        result = web_scraper_node(self.state, config)

        # Check if the command is returned correctly
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "research_team_supervisor")
        self.assertEqual(result.update["messages"][0].content, "")

    @patch('backend.research_team.search_agent.invoke', new_callable=AsyncMock)
    def test_search_node_invalid_response_structure(self, mock_invoke):
        """
        Test the search_node function with an invalid response structure.
        """
        # Mocking an invalid response structure from the search agent
        mock_invoke.return_value = {
            "messages": [{"wrong_key": "This should fail."}]
        }

        with self.assertRaises(KeyError):
            search_node(self.state)

    @patch('backend.research_team.web_scraper_agent.invoke', new_callable=AsyncMock)
    def test_web_scraper_node_invalid_response_structure(self, mock_invoke):
        """
        Test the web_scraper_node function with an invalid response structure.
        """
        # Mocking an invalid response structure from the web scraper agent
        mock_invoke.return_value = {
            "messages": [{"wrong_key": "This should fail."}]
        }
        
        config = {}  # Mock config
        with self.assertRaises(KeyError):
            web_scraper_node(self.state, config)

if __name__ == '__main__':
    unittest.main()
