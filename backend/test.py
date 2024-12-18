from pprint import pprint
from graph import super_graph

for s in super_graph.stream(
    {
        "messages": [
            ("user", "Research AI agents and write a brief report about them.")
        ],
    },
    {"recursion_limit": 150},
):
    pprint(s)
    pprint("---")
