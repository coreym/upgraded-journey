from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-1.5-flash',
    name='formatter_agent',
    description="A Formatter agent that takes a set of claim fields and turns them into an EDI 837 claim.",
    instruction="You are a Formatter agent. Your purpose is to take a set of claim fields and format them into a valid EDI 837 claim.",
)
