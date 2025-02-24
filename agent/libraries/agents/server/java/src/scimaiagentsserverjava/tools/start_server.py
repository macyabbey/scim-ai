import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from smolagents import tool

script_path = Path(__file__).parent
server_cwd = script_path / ".." / ".." / ".." / ".." / ".." / ".." / ".." / ".." / "server"
server_abs_cwd = server_cwd.resolve()

class StartResult(BaseModel):
    """Represents the result of an attempt to start a server.

    Attributes:
        model_config (ConfigDict): Configuration for the model, set to strict mode.
        success (bool): Indicates whether the server start attempt was successful.
        error_message (str | None): Contains the error message if the server start attempt failed, otherwise None.
        message (str | None): Contains the message from the server start attempt
        exit_code (int): The exit code of the server start attempt.

    """

    model_config = ConfigDict(strict=True)
    success: bool
    error_message: str | None
    message: str | None
    exit_code: int

@tool
def start_server(jar_abs_path: str) -> StartResult:
    """Start the scim server and return a build result.

    To fix failed builds, an update or write operation may need to be changed.

    Args:
        jar_abs_path: The absolute path to the JAR file to start.

    Returns a BuildResult.

    """
    result = subprocess.run(
        ["bash", "start.sh"],
        cwd=server_abs_cwd,
        capture_output=True,
        text=True, check=False,
    )

    exit_code = result.returncode
    stdout = result.stdout
    stderr = result.stderr

    return StartResult(
        success=exit_code == 0,
        error_message=stderr if stderr else None,
        message=stdout if stdout else None,
        exit_code=exit_code,
    )
    # You can now use exit_code, stdout, and stderr as needed
