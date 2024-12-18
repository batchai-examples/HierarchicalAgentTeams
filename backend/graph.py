from typing import Literal

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.types import Command

from tools import make_supervisor_node
from research_team import research_graph
from paper_writing_team import paper_writing_graph

##########################################################################################
# Add Layers
# 
# In this design, we are enforcing a top-down planning policy. We've created two graphs already, 
# but we have to decide how to route work between the two.
#
# We'll create a third graph to orchestrate the previous two, and add some connectors to 
# define how this top-level state is shared between the different graphs.


llm = ChatOpenAI(model="gpt-4o")

teams_supervisor_node = make_supervisor_node(llm, ["research_team", "writing_team"])

def call_research_team(state: MessagesState) -> Command[Literal["supervisor"]]:
    response = research_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="research_team"
                )
            ]
        },
        goto="supervisor",
    )


def call_paper_writing_team(state: MessagesState) -> Command[Literal["supervisor"]]:
    response = paper_writing_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="writing_team"
                )
            ]
        },
        goto="supervisor",
    )


# Define the graph.
super_builder = StateGraph(MessagesState)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research_team", call_research_team)
super_builder.add_node("writing_team", call_paper_writing_team)

super_builder.add_edge(START, "supervisor")
super_graph = super_builder.compile()


# from IPython.display import Image

# output_path = "super_graph.png" 

# png = Image(super_graph.get_graph().draw_mermaid_png())
# png_data = png.data
# with open(output_path, "wb") as file:
#     file.write(png_data)

# print(f"Graph has been saved to {output_path}")

# for s in super_graph.stream(
#     {
#         "messages": [
#             ("user", "Research AI agents and write a brief report about them.")
#         ],
#     },
#     {"recursion_limit": 150},
# ):
#     pprint(s)
#     pprint("---")
