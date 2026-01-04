"""Visualize the PushGuardian LangGraph workflow."""

from pushguardian.graph import build_graph

# Build the graph
graph = build_graph()

# Generate Mermaid diagram
try:
    mermaid_diagram = graph.get_graph().draw_mermaid()
    print("=" * 60)
    print("PushGuardian LangGraph Workflow (Mermaid)")
    print("=" * 60)
    print(mermaid_diagram)
    print("=" * 60)
    print("\n✅ Copy the above Mermaid code to https://mermaid.live to visualize!")

    # Save to file
    with open("graph_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_diagram)
    print("📄 Saved to graph_diagram.mmd")

except Exception as e:
    print(f"Error: {e}")
    print("\nAlternative: Print graph structure...")
    try:
        print(graph.get_graph())
    except Exception as e2:
        print(f"Error: {e2}")
