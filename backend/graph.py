from typing import Literal
import asyncio

from langchain_core.messages import HumanMessage, AIMessageChunk
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
    last_message = state["messages"][-1]
    response = research_graph.invoke({"messages": last_message})
    
    last_response = response["messages"][-1].content
    messages = [
                HumanMessage(
                    content=last_response, name="research_team"
                )
            ]

    return Command(
        update={
            "messages": messages
        },
        goto="supervisor",
    )


def call_paper_writing_team(state: MessagesState) -> Command[Literal["supervisor"]]:
    last_message = state["messages"][-1]
    response = paper_writing_graph.invoke({"messages": last_message})

    last_response = response["messages"][-1].content
    messages = [
                HumanMessage(
                    content=last_response, name="writing_team"
                )
            ]

    return Command(
        update={
            "messages": messages
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

async def test_graph():
    async for messages in super_graph.astream(
        {
            "messages": [
                ("user", "Research AI agents and write a brief report about them.")
            ],
        },
        {"recursion_limit": 150},
        stream_mode="messages"
    ):
        #print(messages)
        #print('------------------------')

        checkpoint_ns:str = messages[1]["checkpoint_ns"]
        is_cared_checkpoints = checkpoint_ns.startswith("search:") or checkpoint_ns.startswith("note_taker:")
        if True or is_cared_checkpoints:
            for msg in messages:
                if isinstance(msg, AIMessageChunk):
                    content = msg.content
                    if content:
                        print(content, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(test_graph())
    print()
