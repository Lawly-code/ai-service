import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

import random
from typing import AsyncGenerator

import time
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from protos.ai_service.client import AIAssistantClient

from grpc_server.server import AIAssistantServicer

time.sleep(2)


@pytest.fixture(scope="function")
async def ai_grpc_client() -> AsyncGenerator[AIAssistantClient, None]:
    client = AIAssistantClient(host="test_grpc_service", port=50051)
    yield client
    await client.close()


@pytest.fixture(scope="session")
def random_text():
    """Генерирует случайный текст для моков"""
    texts = [
        "Это тестовый ответ от AI ассистента.",
        "Вот улучшенная версия вашего текста.",
        "В ответ на ваш запрос, вот сгенерированный шаблон документа.",
        "AI ассистент готов помочь вам с этим вопросом.",
        "Документ успешно сгенерирован согласно вашим требованиям.",
    ]
    return random.choice(texts)


@pytest.fixture(scope="session")
def mock_ai_service():
    """Создает замоканный AIService"""
    with patch('assistant.services.ai_service.AIService') as mock_service:
        service_instance = mock_service.return_value

        # Настраиваем моки методов, которые возвращают случайный текст
        async def mock_improve_text(text):
            return f"Улучшено: {text}"

        async def mock_ai_chat(text):
            return f"Ответ на: {text}"

        async def mock_custom_template(text):
            return f"Шаблон по запросу: {text}"

        service_instance.improve_text = AsyncMock(side_effect=mock_improve_text)
        service_instance.ai_chat = AsyncMock(side_effect=mock_ai_chat)
        service_instance.custom_template = AsyncMock(side_effect=mock_custom_template)

        yield service_instance


@pytest.fixture(scope="session")
def mock_context():
    """Создает замоканный gRPC контекст"""
    context = MagicMock()
    context.set_code = MagicMock()
    context.set_details = MagicMock()
    return context


@pytest.fixture(scope="session")
def servicer(mock_ai_service):
    """Создает экземпляр AIAssistantServicer с замоканным AIService"""
    with patch('assistant.services.ai_service.AIService', return_value=mock_ai_service):
        return AIAssistantServicer()
