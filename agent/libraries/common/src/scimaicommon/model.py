from smolagents import LiteLLMModel

# https://github.com/huggingface/smolagents/blob/7927bcaea90d882c1c56261a6ea5c5ab88c0e766/src/smolagents/models.py#L820

# See https://docs.litellm.ai/docs/providers

def get_model(model_id: str = "gpt-4o") -> LiteLLMModel:
    return LiteLLMModel(model_id)
