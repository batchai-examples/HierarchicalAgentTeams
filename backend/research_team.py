from typing import Literal

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.types import Command

from tools import tavily_tool, scrape_webpages, make_supervisor_node

#######################################################################################################################
# Define Agent Teams
# Now we can get to define our hierarchical teams. "Choose your player!"

# Research Team
# The research team will have a search agent and a web scraping "research_agent" as the two worker nodes. 
# Let's create those, as well as the team supervisor.

llm = ChatOpenAI(model="gpt-4o")

search_agent = create_react_agent(llm, tools=[tavily_tool])


def search_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = search_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="search")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


web_scraper_agent = create_react_agent(llm, tools=[scrape_webpages])


def web_scraper_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = web_scraper_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="web_scraper")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


research_supervisor_node = make_supervisor_node(llm, ["search", "web_scraper"])

# Now that we've created the necessary components, defining their interactions is easy. 
# Add the nodes to the team graph, and define the edges, which determine the transition criteria.

research_builder = StateGraph(MessagesState)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("search", search_node)
research_builder.add_node("web_scraper", web_scraper_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()

###############################################################################
# from IPython.display import Image

# output_path = "research_graph.png" 

# png = Image(research_graph.get_graph().draw_mermaid_png())
# png_data = png.data
# with open(output_path, "wb") as file:
#     file.write(png_data)

# print(f"Graph has been saved to {output_path}")

###############################################################################
# We can give this team work directly. Try it out below.

# for s in research_graph.stream(
#     {"messages": [("user", "when is Taylor Swift's next tour?")]},
#     {"recursion_limit": 100},
# ):
#     pprint(s)
#     pprint("---")


