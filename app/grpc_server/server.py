import grpc
import logging
from typing import Optional

from assistant.services.ai_service import AIService
from config import TEMPERATURE, MAX_TOKENS
from protos.ai_service import ai_service_pb2 as ai_pb2
from protos.ai_service import ai_service_pb2_grpc as ai_pb2_grpc


class AIAssistantServicer(ai_pb2_grpc.AIAssistantServicer):
    """
    Реализация GRPC сервиса для работы с AI Assistant (асинхронная версия)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def ImproveText(self, request, context):
        """
        Улучшает текст, используя AI
        """
        try:
            user_prompt = request.user_prompt
            temperature = (
                request.temperature if request.HasField("temperature") else TEMPERATURE
            )
            max_tokens = (
                request.max_tokens if request.HasField("max_tokens") else MAX_TOKENS
            )
            ai_service = AIService(temperature, max_tokens)

            self.logger.info("GRPC запрос ImproveText получен")

            # Вызываем метод AI сервиса
            result = await ai_service.improve_text(user_prompt)

            # Создаем метаданные ответа
            import time

            metadata = ai_pb2.ResponseMetadata(
                timestamp=int(time.time()), model="DeepSeek", tokens_used=0
            )

            # Формируем ответ
            return ai_pb2.TextResponse(assistant_reply=result, metadata=metadata)
        except Exception as e:
            self.logger.error(
                f"Ошибка при обработке GRPC запроса ImproveText: {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Внутренняя ошибка сервера: {str(e)}")
            return ai_pb2.TextResponse()

    async def AIChat(self, request, context):
        """
        Выполняет чат с AI
        """
        try:
            user_prompt = request.user_prompt
            temperature = (
                request.temperature if request.HasField("temperature") else TEMPERATURE
            )
            max_tokens = (
                request.max_tokens if request.HasField("max_tokens") else MAX_TOKENS
            )
            ai_service = AIService(temperature, max_tokens)

            self.logger.info("GRPC запрос AIChat получен")

            # Вызываем метод AI сервиса
            result = await ai_service.ai_chat(user_prompt)

            # Создаем метаданные ответа
            import time

            metadata = ai_pb2.ResponseMetadata(
                timestamp=int(time.time()), model="DeepSeek", tokens_used=0
            )

            # Формируем ответ
            return ai_pb2.TextResponse(assistant_reply=result, metadata=metadata)
        except Exception as e:
            self.logger.error(f"Ошибка при обработке GRPC запроса AIChat: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Внутренняя ошибка сервера: {str(e)}")
            return ai_pb2.TextResponse()

    async def CustomTemplate(self, request, context):
        """
        Генерирует кастомный шаблон документа
        """
        try:
            user_prompt = request.user_prompt
            temperature = (
                request.temperature if request.HasField("temperature") else TEMPERATURE
            )
            max_tokens = (
                request.max_tokens if request.HasField("max_tokens") else MAX_TOKENS
            )
            ai_service = AIService(temperature, max_tokens)

            self.logger.info("GRPC запрос CustomTemplate получен")

            # Вызываем метод AI сервиса
            result = await ai_service.custom_template(user_prompt)

            # Создаем метаданные ответа
            import time

            metadata = ai_pb2.ResponseMetadata(
                timestamp=int(time.time()), model="DeepSeek", tokens_used=0
            )

            # Формируем ответ
            return ai_pb2.TextResponse(assistant_reply=result, metadata=metadata)
        except Exception as e:
            self.logger.error(
                f"Ошибка при обработке GRPC запроса CustomTemplate: {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Внутренняя ошибка сервера: {str(e)}")
            return ai_pb2.TextResponse()


class AsyncGRPCServer:
    """
    Класс-обертка для запуска асинхронного GRPC сервера
    """

    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """
        Запуск асинхронного GRPC сервера
        """
        # Создаем экземпляр асинхронного сервера
        self.server = grpc.aio.server()

        # Создаем сервисер и добавляем его на сервер
        servicer = AIAssistantServicer()
        ai_pb2_grpc.add_AIAssistantServicer_to_server(servicer, self.server)

        # Добавляем порт для прослушивания
        listen_addr = f'[::]:{self.port}'
        self.server.add_insecure_port(listen_addr)

        # Запускаем сервер
        await self.server.start()
        self.logger.info(
            f"Асинхронный GRPC сервер AI Assistant запущен на порту {self.port}"
        )

        return self

    async def stop(self, grace: Optional[float] = None):
        """
        Остановка GRPC сервера

        Args:
            grace: период ожидания в секундах перед принудительной остановкой
        """
        if self.server:
            await self.server.stop(grace)
            self.logger.info("GRPC сервер AI Assistant остановлен")

    async def wait_for_termination(self):
        """
        Ожидание завершения работы сервера
        """
        if self.server:
            await self.server.wait_for_termination()
