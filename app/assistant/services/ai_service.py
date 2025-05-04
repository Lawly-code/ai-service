from config import DEEPSEEK_TOKEN, TEMPERATURE, MAX_TOKENS
from assistant.models import InputDataDTO, OutputDataDTO
from assistant.repositories import BaseAssistantRepository, DeepSeekRepository
from assistant.utils.prompt import prompt


class AIService:
    def __init__(self, temperature: float = TEMPERATURE, max_tokens: int = MAX_TOKENS):
        self.repository: BaseAssistantRepository = DeepSeekRepository(
            api_key=DEEPSEEK_TOKEN
        )
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def execute_response(self, input_data: InputDataDTO) -> OutputDataDTO:
        """
        Выполняет запрос к репозиторию и возвращает ответ.

        :param input_data: Входные данные для запроса.
        :return: Ответ от репозитория.
        """
        response = await self.repository.execute_response(input_data=input_data)
        await self.repository.close()
        return response

    async def improve_text(self, user_prompt: str) -> str:
        """
        Улучшает текст, используя AI.

        :param user_prompt: Исходный текст для улучшения.
        :return: Улучшенный текст.
        """

        input_data = InputDataDTO(
            system_prompt=prompt("improve_text"),
            user_prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        response = await self.execute_response(input_data=input_data)
        return response.assistant_reply

    async def ai_chat(self, user_prompt: str) -> str:
        """
        Выполняет чат с AI.

        :param user_prompt: Вопрос или сообщение для AI.
        :return: Ответ AI на заданный вопрос.
        """

        input_data = InputDataDTO(
            system_prompt=prompt("ai_chat"),
            user_prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        response = await self.execute_response(input_data=input_data)
        return response.assistant_reply

    async def custom_template(self, user_prompt: str) -> str:
        """
        Генерирует кастомный шаблон документа.

        :param user_prompt: Входные данные для генерации шаблона.
        :return: Текст сгенерированного шаблона документа.
        """
        input_data = InputDataDTO(
            system_prompt=prompt("custom_template"),
            user_prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        response = await self.execute_response(input_data=input_data)
        return response.assistant_reply
