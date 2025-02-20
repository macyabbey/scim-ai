from dotenv import load_dotenv
from scimaitools.sql_read_schema import read_schema
from smolagents import CodeAgent, HfApiModel
from smolagents.monitoring import LogLevel

load_dotenv()

# You can choose to not pass any model_id to HfApiModel to use a default free model
# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
model = HfApiModel()
agent = CodeAgent(
  tools=[read_schema],
  model=model,
  verbosity_level=LogLevel.DEBUG,
  add_base_tools=True,
  additional_authorized_imports=["pprint"],
)
