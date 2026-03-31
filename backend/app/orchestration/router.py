from .agents import diagnosis_agent, voice_agent, advisory_agent, assistant_agent

def route_request(request_type: str, payload: dict):
    # Dummy router skeleton
    if request_type == "diagnose":
        return diagnosis_agent.handle(payload)
    elif request_type == "voice":
        return voice_agent.handle(payload)
    elif request_type == "assistant":
        return assistant_agent.handle(payload)
    else:
        return advisory_agent.handle(payload)
