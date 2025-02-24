from pathlib import Path

from dotenv import load_dotenv
from scimaiagentsserverjava.tools.build_server import build_server
from scimaiagentsserverjava.tools.start_server import start_server

load_dotenv()


def test_tool_start_server() -> None:
    result = build_server()
    assert result.success
    assert Path(result.jar_abs_path).exists()
    result = start_server(result.jar_abs_path)
    assert result.success
    # assert result.error_message is None
    # assert result.message is not None
    assert result.exit_code == 0
