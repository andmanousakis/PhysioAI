import pytest
from typer.testing import CliRunner
from unittest.mock import patch

from message.main import app

runner = CliRunner()

@pytest.fixture
def mock_features():
    return [{
        "session_group": "test-group",
        "pain": 3,
        "fatigue": 2,
        "skipped_exercises": 1,
    }]

@pytest.fixture
def mock_response():
    return "Great job today, Alex! Keep up the consistency."

@patch("message.main.get_features")
@patch("message.main.get_user_prompt")
@patch("message.main.get_system_prompt")
@patch("message.main.chat_model.get_completion")
def test_get_message_success(
    mock_get_completion,
    mock_get_system_prompt,
    mock_get_user_prompt,
    mock_get_features,
    mock_features,
    mock_response
):
    mock_get_features.return_value = mock_features
    mock_get_user_prompt.return_value = "user prompt"
    mock_get_system_prompt.return_value = "system prompt"
    mock_get_completion.return_value = mock_response

    result = runner.invoke(app, ["get-message", "test-group"], catch_exceptions=False)

    assert result.exit_code == 0
    assert mock_response in result.stdout


@patch("message.main.get_features")
def test_get_message_no_features(mock_get_features):
    mock_get_features.return_value = []

    result = runner.invoke(app, ["get-message", "invalid-group"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "No features found for the given session_group." in result.stdout
