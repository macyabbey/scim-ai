from pathlib import Path

from dotenv import load_dotenv
from scimaiagentsserverjava.tools.build_server import build_server

load_dotenv()

def test_tool_build_server() -> None:
    result = build_server()
    assert result.success
    assert Path(result.jar_abs_path).exists()
    assert result.error_message is None
    assert result.message is not None
    assert result.exit_code == 0
