import os

from dotenv import load_dotenv
from scimaicommon.instrument import initialize_tracing
from scimaicommon.model import get_model
from smolagents import CodeAgent

from .tools import (
  build_server,
  start_server,
  test_server,
  update_application_config,
  update_pom,
  write_connected_group_service,
  write_connected_user_service,
)

load_dotenv()
initialize_tracing(os.environ["SMOLAGENTS_TRACING_ENDPOINT"])

agent = CodeAgent(
  tools=[
    update_application_config,
    update_pom,
    write_connected_group_service,
    write_connected_user_service,
    build_server,
    start_server,
    test_server,
  ],
  model=get_model(),
  add_base_tools=True,
  additional_authorized_imports=["pprint"],
)
