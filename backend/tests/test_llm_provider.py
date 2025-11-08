"""
Tests for LLM Provider
"""
import pytest
from app.services.llm_provider import LLMService, LLMProvider, Message


@pytest.mark.skip(reason="Requires API keys")
@pytest.mark.asyncio
async def test_anthropic_provider():
    """Test Anthropic provider"""
    service = LLMService(provider=LLMProvider.ANTHROPIC)
    messages = [Message(role="user", content="Hello, respond with 'Hi' only.")]

    response = await service.generate(messages, max_tokens=10, temperature=0)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.skip(reason="Requires API keys")
@pytest.mark.asyncio
async def test_openai_provider():
    """Test OpenAI provider"""
    service = LLMService(provider=LLMProvider.OPENAI)
    messages = [Message(role="user", content="Hello, respond with 'Hi' only.")]

    response = await service.generate(messages, max_tokens=10, temperature=0)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_switch_provider():
    """Test switching between providers"""
    service = LLMService(provider=LLMProvider.ANTHROPIC)
    assert service.provider_type == LLMProvider.ANTHROPIC

    # Note: This would fail without proper API keys
    # service.switch_provider(LLMProvider.OPENAI)
    # assert service.provider_type == LLMProvider.OPENAI
