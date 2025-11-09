"""
LLM Provider Abstraction Layer
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
import anthropic
import openai
from app.core.config import settings
import structlog

logger = structlog.get_logger()


class LLMProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """Generate text completion"""
        pass


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate(
        self,
        messages: List[Message],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str = "claude-3-5-sonnet-20241022",
        **kwargs,
    ) -> str:
        try:
            # Convert messages to Anthropic format
            formatted_messages = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]

            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=formatted_messages,
                **kwargs,
            )

            return response.content[0].text
        except Exception as e:
            logger.error("Anthropic API error", error=str(e))
            raise


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider"""

    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def generate(
        self,
        messages: List[Message],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: str = "gpt-4-turbo-preview",
        **kwargs,
    ) -> str:
        try:
            # Convert messages to OpenAI format
            formatted_messages = [
                {"role": msg.role, "content": msg.content} for msg in messages
            ]

            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=formatted_messages,
                **kwargs,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error("OpenAI API error", error=str(e))
            raise


class LLMService:
    """Main LLM service with provider abstraction"""

    def __init__(
        self,
        provider: LLMProvider = LLMProvider(settings.DEFAULT_LLM_PROVIDER),
    ):
        self.provider_type = provider
        self.provider = self._initialize_provider(provider)

    def _initialize_provider(self, provider: LLMProvider) -> BaseLLMProvider:
        """Initialize the selected LLM provider"""
        if provider == LLMProvider.ANTHROPIC:
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key not configured")
            return AnthropicProvider(settings.ANTHROPIC_API_KEY)
        elif provider == LLMProvider.OPENAI:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider(settings.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    async def generate(
        self,
        messages: List[Message],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """Generate text using the configured provider"""
        return await self.provider.generate(messages, max_tokens, temperature, **kwargs)

    def switch_provider(self, provider: LLMProvider):
        """Switch to a different LLM provider"""
        self.provider_type = provider
        self.provider = self._initialize_provider(provider)
        logger.info("Switched LLM provider", provider=provider.value)
