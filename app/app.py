from vertexai.preview import reasoning_engines

def create_agent():
    return reasoning_engines.LangchainAgent(
        model="gemini-2.0-flash",
    )
