import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from smolagents import tool

script_path = Path(__file__).parent
server_cwd = script_path / ".." / ".." / ".." / ".." / "server"
server_abs_cwd = server_cwd.resolve()

class StartResult(BaseModel):
    """Represents the result of an attempt to start a server.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to strict mode.
        success (bool): Indicates whether the server start attempt was successful.
        error_message (str | None): Contains the error message if the server start attempt failed, otherwise None.

    """

    model_config = ConfigDict(strict=True)
    success: bool
    error_message: str | None

@tool
def start_server(jar_abs_path: str) -> StartResult:
    """Start the scim server and return a build result.

    To fix failed builds, an update or write operation may need to be changed.

    Returns a BuildResult.
    """
    result = subprocess.run(
        ["java", "-jar", jar_abs_path],
        cwd=server_abs_cwd,
        capture_output=True,
        text=True, check=False,
    )

    exit_code = result.returncode
    stdout = result.stdout
    stderr = result.stderr

    return StartResult(
        success=exit_code == 0,
        error_message=stderr,
    )
    # You can now use exit_code, stdout, and stderr as needed
