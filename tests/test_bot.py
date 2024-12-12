import os
import pytest
from unittest.mock import patch, MagicMock
from bot import extract_links, add_to_linkwarden, handle_message, start, send_message_with_retry, error_handler

@pytest.fixture
def mock_update():
    mock = MagicMock()
    mock.effective_chat.id = 12345
    mock.message.text = "Check out this link: https://example.com"
    return mock

@pytest.fixture
def mock_context():
    return MagicMock()

def test_extract_links():
    text = "Here are some links: https://example.com and http://test.com"
    links = extract_links(text)
    assert links == ["https://example.com", "http://test.com"]

@patch('bot.requests.Session.post')
def test_add_to_linkwarden_success(mock_post):
    mock_post.return_value.status_code = 200
    url = "https://example.com"
    result = add_to_linkwarden(url)
    assert result is True

@patch('bot.requests.Session.post')
def test_add_to_linkwarden_failure(mock_post):
    mock_post.return_value.status_code = 500
    url = "https://example.com"
    result = add_to_linkwarden(url)
    assert result is False

@patch('bot.add_to_linkwarden')
@patch('bot.send_message_with_retry')
@pytest.mark.asyncio
async def test_handle_message(mock_send_message, mock_add_to_linkwarden, mock_update, mock_context):
    mock_add_to_linkwarden.return_value = True
    await handle_message(mock_update, mock_context)
    mock_send_message.assert_called_once_with(mock_update, mock_context, "Links added to Linkwarden:\nhttps://example.com")

@patch('bot.send_message_with_retry')
@pytest.mark.asyncio
async def test_handle_message_no_links(mock_send_message, mock_update, mock_context):
    mock_update.message.text = "No links here"
    await handle_message(mock_update, mock_context)
    mock_send_message.assert_called_once_with(mock_update, mock_context, "No links found in the message.")

@patch('bot.time.sleep', return_value=None)
@patch('bot.requests.Session.post')
def test_add_to_linkwarden_retry(mock_post, mock_sleep):
    mock_post.side_effect = [requests.exceptions.Timeout, requests.exceptions.Timeout, MagicMock(status_code=200)]
    url = "https://example.com"
    result = add_to_linkwarden(url)
    assert result is True
    assert mock_post.call_count == 3

@patch('bot.logger.error')
@pytest.mark.asyncio
async def test_error_handler(mock_logger_error, mock_update, mock_context):
    mock_context.error = Exception("Test error")
    await error_handler(mock_update, mock_context)
    mock_logger_error.assert_called_with(msg="Exception while handling an update:", exc_info=mock_context.error)

@patch('bot.time.sleep', return_value=None)
@patch('bot.logger.warning')
@patch('bot.logger.error')
@pytest.mark.asyncio
async def test_send_message_with_retry(mock_logger_error, mock_logger_warning, mock_sleep, mock_update, mock_context):
    mock_context.bot.send_message.side_effect = [TimedOut, TimedOut, None]
    await send_message_with_retry(mock_update, mock_context, "Test message")
    assert mock_context.bot.send_message.call_count == 3
    mock_logger_warning.assert_called_with("Attempt 2 failed: . Retrying...")
    mock_logger_error.assert_called_with("Failed to send message after 3 attempts: .")
