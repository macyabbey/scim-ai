import os

from dotenv import load_dotenv
from scimaicommon.instrument import initialize_tracing
from scimaicommon.model import get_model
from scimaitools.sql_read_schema import read_schema
from smolagents import CodeAgent
from smolagents.monitoring import LogLevel

load_dotenv()
initialize_tracing(os.environ["SMOLAGENTS_TRACING_ENDPOINT"])

agent = CodeAgent(
  tools=[read_schema],
  model=get_model(),
  verbosity_level=LogLevel.DEBUG,
  add_base_tools=True,
  additional_authorized_imports=["pprint"],
)
