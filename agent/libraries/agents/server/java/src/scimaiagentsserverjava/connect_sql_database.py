import os

from dotenv import load_dotenv
from scimaicommon.instrument import initialize_tracing
from scimaicommon.model import get_model
from smolagents import CodeAgent

from .tools import (
  add_sql_connection,
  build_server,
  start_server,
  test_server,
  save_sql_group_service,
  save_sql_user_service,
)

load_dotenv()
initialize_tracing(os.environ["SMOLAGENTS_TRACING_ENDPOINT"])

agent = CodeAgent(
  tools=[
    add_sql_connection,
    save_sql_group_service,
    save_sql_user_service,
    build_server,
    start_server,
    test_server,
  ],
  model=get_model(),
  add_base_tools=True,
  additional_authorized_imports=["pprint"],
)
