from vertexai.preview import reasoning_engines

def create_agent():
    return reasoning_engines.LangchainAgent(
        model="gemini-1.0-pro-001",
        tools=[get_exchange_rate],
    )
