import pytest
from protos.ai_service.client import AIAssistantClient

from protos.ai_service.dto import AIRequestDTO, AIResponseDTO

from assistant.services.ai_service import AIService


@pytest.mark.asyncio
async def test_improve_text_client(
    ai_grpc_client: AIAssistantClient, mock_ai_service: AIService
):
    """Тестирует метод improve_text клиента AIAssistantClient"""
    # Подготовка
    request_data = AIRequestDTO(
        user_prompt="Этот текст нуждается в улучшении.",
        temperature=0.7,
        max_tokens=1000,
    )

    # Выполнение
    response = await ai_grpc_client.improve_text(request_data)

    # Проверка
    assert response is not None
    assert isinstance(response, AIResponseDTO)


@pytest.mark.asyncio
async def test_ai_chat_client(
    ai_grpc_client: AIAssistantClient, mock_ai_service: AIService
):
    """Тестирует метод ai_chat клиента AIAssistantClient"""
    # Подготовка
    request_data = AIRequestDTO(
        user_prompt="Что такое искусственный интеллект?", max_tokens=2000
    )

    # Выполнение
    response = await ai_grpc_client.ai_chat(request_data)

    # Проверка
    assert response is not None
    assert isinstance(response, AIResponseDTO)


@pytest.mark.asyncio
async def test_custom_template_client(
    ai_grpc_client: AIAssistantClient, mock_ai_service: AIService
):
    """Тестирует метод custom_template клиента AIAssistantClient"""
    # Подготовка
    request_data = AIRequestDTO(
        user_prompt="Договор купли-продажи", temperature=0.5, max_tokens=3000
    )

    # Выполнение
    response = await ai_grpc_client.custom_template(request_data)

    # Проверка
    assert response is not None
    assert isinstance(response, AIResponseDTO)


@pytest.mark.asyncio
async def test_improve_text_without_optional_params(
    ai_grpc_client: AIAssistantClient, mock_ai_service: AIService
):
    """Тестирует метод improve_text без опциональных параметров"""
    # Подготовка
    request_data = AIRequestDTO(
        user_prompt="Текст для улучшения без опциональных параметров"
    )

    # Выполнение
    response = await ai_grpc_client.improve_text(request_data)

    # Проверка
    assert response is not None
    assert isinstance(response, AIResponseDTO)
