import pytest
from unittest.mock import MagicMock

from src.utils import check_token


@pytest.fixture
def mock_get_api_url():
    """Mocked version of the get_api_url function."""
    return MagicMock(return_value="http://example.com")


def test_check_token_valid(mock_get_api_url, mocker):
    """
    Tests that the check_token function returns True when the token is valid.

    Args:
        mock_get_api_url: A mocked version of the get_api_url function.
        mocker: A mocker object used to patch the get_api_url function.
    """
    update = MagicMock()
    context = MagicMock()
    requests_mock = MagicMock()
    
    # Set the status code of the requests object to 200 to simulate a valid token.
    requests_mock.post.return_value.status_code = 200

    # Patch the get_api_url function with the mock object.
    mocker.patch("src.utils.get_api_url", mock_get_api_url)

    # Call the check_token function with the mock objects.
    result = check_token(update, context, requests_lib=requests_mock)

    assert result is True


def test_check_token_invalid(mock_get_api_url, mocker):
    """
    Tests that the check_token function returns False when the token is invalid.

    Args:
        mock_get_api_url: A mocked version of the get_api_url function.
        mocker: A mocker object used to patch the get_api_url function.
    """
    update = MagicMock()
    context = MagicMock()
    requests_mock = MagicMock()
    
    # Set the status code of the requests object to 401 to simulate an invalid token.
    requests_mock.post.return_value.status_code = 401

    # Patch the get_api_url function with the mock object.
    mocker.patch("src.utils.get_api_url", mock_get_api_url)

    # Call the check_token function with the mock objects.
    result = check_token(update, context, requests_lib=requests_mock)

    assert result is False
