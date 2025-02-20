import os
import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from smolagents import tool

script_path = Path(__file__).parent
server_cwd = script_path / ".." / ".." / ".." / ".." / "server"
server_abs_cwd = server_cwd.resolve()

class BuildResult(BaseModel):
    """BuildResult represents the result of a build process.

    Attributes:
        success (bool): Indicates whether the build was successful.
        jar_abs_path (str): The absolute path to the generated JAR file.
        error_message (str | None): The error message if the build failed, otherwise None.

    """

    model_config = ConfigDict(strict=True)
    success: bool
    jar_abs_path: str
    error_message: str | None

@tool
def build_server() -> BuildResult:
    """Build the scim server and return a build result.

    To fix failed builds, an update or write operation may need to be changed.

    Returns a BuildResult.
    """
    result = subprocess.run(
        ["mvn", "package"],
        cwd=server_abs_cwd,
        capture_output=True,
        text=True, check=False,
    )

    exit_code = result.returncode
    stdout = result.stdout
    stderr = result.stderr

    return BuildResult(
        success=exit_code == 0,
        error_message=stderr,
        jar_abs_path=os.path.join(server_abs_cwd, "target", "scim-ai-server.jar"),
    )
    # You can now use exit_code, stdout, and stderr as needed
