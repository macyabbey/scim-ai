import subprocess
from pathlib import Path
from unittest import mock

from dotenv import load_dotenv
from scimaiagentsserverjava.tools.start_server import start_server

load_dotenv()

def test_tool_start_server_success() -> None:
    """Test start_server when subprocess succeeds."""
    mock_jar_path = "/path/to/mock.jar"
    
    # Create a mock Path that returns True for exists()
    mock_path = mock.Mock(spec=Path)
    mock_path.exists.return_value = True
    
    with mock.patch("pathlib.Path", return_value=mock_path):
        with mock.patch("subprocess.run") as mock_run:
            # Configure mock to simulate successful subprocess execution
            mock_process = mock.Mock()
            mock_process.returncode = 0
            mock_process.stdout = "Server started successfully"
            mock_process.stderr = None
            mock_run.return_value = mock_process
            
            result = start_server(mock_jar_path)
            
            assert result.success
            assert result.exit_code == 0
            assert result.message == "Server started successfully"
            mock_run.assert_called_once()

def test_tool_start_server_failure() -> None:
    """Test start_server when subprocess fails."""
    mock_jar_path = "/path/to/mock.jar"
    
    # Create a mock Path that returns True for exists()
    mock_path = mock.Mock(spec=Path)
    mock_path.exists.return_value = True
    
    with mock.patch("pathlib.Path", return_value=mock_path):
        with mock.patch("subprocess.run") as mock_run:
            # Configure mock to simulate failed subprocess execution
            mock_process = mock.Mock()
            mock_process.returncode = 1
            mock_process.stdout = None
            mock_process.stderr = "Server failed to start"
            mock_run.return_value = mock_process
            
            result = start_server(mock_jar_path)
            
            assert not result.success
            assert result.exit_code == 1
            assert result.error_message == "Server failed to start"
            mock_run.assert_called_once()
