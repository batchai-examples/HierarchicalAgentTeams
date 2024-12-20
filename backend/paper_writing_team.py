from typing import Literal
import asyncio
from langchain_core.messages import HumanMessage, AIMessageChunk
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.types import Command

from tools import write_document, edit_document, read_document, create_outline, python_repl_tool, make_supervisor_node

##############################################################################
# Document Writing Team

# Create the document writing team below using a similar approach. 
# This time, we will give each agent access to different file-writing tools.
#
# Note that we are giving file-system access to our agent here, which is not safe in all cases.


llm = ChatOpenAI(model="gpt-4o")

doc_writer_agent = create_react_agent(
    llm,
    tools=[write_document, edit_document, read_document],
    state_modifier=(
        "You can read, write and edit documents based on note-taker's outlines. "
        "Don't ask follow-up questions."
    ),
)


def doc_writing_node(state: MessagesState) -> Command[Literal["doc_writing_team_supervisor"]]:
    result = doc_writer_agent.invoke(state)

    last_response = result["messages"][-1].content
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_response, name="doc_writer")
            ]
        },
        # We want our workers to ALWAYS "report back" to the doc_writing_team_supervisor when done
        goto="doc_writing_team_supervisor",
    )


note_taking_agent = create_react_agent(
    llm,
    tools=[read_document],
    state_modifier=(
        "You can read documents and create outlines. You can read documents and create outlines for the document writer. "
        "Don't ask follow-up questions."
    ),
)


def note_taking_node(state: MessagesState, config: RunnableConfig) -> Command[Literal["doc_writing_team_supervisor"]]:
    result = note_taking_agent.invoke(state, config)

    last_response = result["messages"][-1].content
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_response, name="note_taker")
            ]
        },
        # We want our workers to ALWAYS "report back" to the doc_writing_team_supervisor when done
        goto="doc_writing_team_supervisor",
    )


chart_generating_agent = create_react_agent(
    llm, tools=[read_document, python_repl_tool]
)


def chart_generating_node(state: MessagesState) -> Command[Literal["doc_writing_team_supervisor"]]:
    result = chart_generating_agent.invoke(state)

    last_response = result["messages"][-1].content
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=last_response, name="chart_generator"
                )
            ]
        },
        # We want our workers to ALWAYS "report back" to the doc_writing_team_supervisor when done
        goto="doc_writing_team_supervisor",
    )


doc_writing_supervisor_node = make_supervisor_node(
    llm, ["note_taker"]
)

# With the objects themselves created, we can form the graph.

# Create the graph here
paper_writing_builder = StateGraph(MessagesState)
paper_writing_builder.add_node("doc_writing_team_supervisor", doc_writing_supervisor_node)
#paper_writing_builder.add_node("doc_writer", doc_writing_node)
paper_writing_builder.add_node("note_taker", note_taking_node)
#paper_writing_builder.add_node("chart_generator", chart_generating_node)

paper_writing_builder.add_edge(START, "doc_writing_team_supervisor")
paper_writing_graph = paper_writing_builder.compile()

# from IPython.display import Image

# output_path = "paper_writing_graph.png" 

# png = Image(paper_writing_graph.get_graph().draw_mermaid_png())
# png_data = png.data
# with open(output_path, "wb") as file:
#     file.write(png_data)

# print(f"Graph has been saved to {output_path}")

async def test_paper_writing_team():
    async for messages in paper_writing_graph.astream(
        {
            "messages": [
                (
                    "user",
                    "Write an outline for poem about cats",
                )
            ]
        },
        {"recursion_limit": 100},
        stream_mode="messages"
    ):
        checkpoint_ns:str = messages[1]["checkpoint_ns"]
        if checkpoint_ns.startswith("note_taker:"):
            for msg in messages:
                if isinstance(msg, AIMessageChunk):
                    content = msg.content
                    if content:
                        print(content, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(test_paper_writing_team())
    print()
