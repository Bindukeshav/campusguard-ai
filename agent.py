from logging import config
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()   # ← ADD THIS LINE


class AgentState(TypedDict):
    finding: dict
    severity: str
    report: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)


def assess_severity(state: AgentState) -> AgentState:
    finding = state["finding"]

    if finding["type"] == "bag" and finding["status"] == "suspicious":
        state["severity"] = "high"
    elif finding["type"] == "person" and finding["status"] == "possible_fall":
        state["severity"] = "high"
    else:
        state["severity"] = "low"

    return state

def write_report(state: AgentState) -> AgentState:
    finding = state["finding"]
    severity = state["severity"]

    prompt = f"""You are a security analyst. Write a short 2-sentence incident report for this finding:
Type: {finding['type']}
Status: {finding['status']}
Severity: {severity}
"""

    response = llm.invoke(prompt)
    state["report"] = response.content
    return state

graph = StateGraph(AgentState)
graph.add_node("assess", assess_severity)
graph.add_node("report", write_report)
graph.set_entry_point("assess")
graph.add_edge("assess", "report")
graph.add_edge("report", END)

agent = graph.compile()

def investigate(finding):
    result = agent.invoke({"finding": finding, "severity": "", "report": ""})
    return result

if __name__ == "__main__":
    test_finding = {"type": "bag", "status": "suspicious"}
    result = investigate(test_finding)
    print(result)