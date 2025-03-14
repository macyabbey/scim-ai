from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from dotenv import load_dotenv
from scimaiagentsserverjava.tools.build_server import build_server

load_dotenv()
@pytest.mark.parametrize("return_code", [1, 2])
@patch("scimaiagentsserverjava.tools.build_server.subprocess.run")
def test_tool_build_server_failure(mock_run, return_code) -> None:
    """Tests the build_server function when the subprocess call fails.
    
    Verifies that the build_server function correctly processes failed subprocess 
    results and returns appropriate error information.
    
    Args:
        mock_run: Mocked subprocess.run function
        return_code: Parametrized non-zero return code to test with
    """
    # Setup mock return value with failure
    mock_process = MagicMock()
    mock_process.returncode = return_code
    mock_process.stdout = "Some output"
    mock_process.stderr = "Build failed with error"
    mock_run.return_value = mock_process
    
    # Run function and assertions
    result = build_server()
    
    # Verify subprocess was called
    mock_run.assert_called_once()
    
    # Verify failure results
    assert not result.success
    assert result.message is not None
    assert "failed" in result.error_message.lower() and "error" in result.error_message.lower()
    assert result.exit_code == return_code

@pytest.mark.parametrize("jar_path", ["/tmp/mock_server.jar", "/usr/local/mock_server.jar"])
@patch("scimaiagentsserverjava.tools.build_server.subprocess.run")
def test_tool_build_server(mock_run, jar_path, monkeypatch) -> None:
    """Tests the build_server function with mocked subprocess call.
    
    Verifies that the build_server function correctly processes subprocess results
    and returns the expected values.
    
    Args:
        mock_run: Mocked subprocess.run function
        jar_path: Parametrized path to test with
        monkeypatch: Pytest fixture to modify environment
    """
    # Setup mock return value
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Build successful"
    mock_process.stderr = None
    mock_run.return_value = mock_process
    
    # Mock the jar path output
    monkeypatch.setattr(Path, "exists", lambda self: True)
    
    # Run function and assertions
    result = build_server()
    
    # Verify subprocess was called
    mock_run.assert_called_once()
    
    # Verify results
    assert result.success
    assert Path(result.jar_abs_path).exists()
    assert result.message is not None
    assert result.exit_code == 0
