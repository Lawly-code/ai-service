from assistant.models import InputDataDTO, OutputDataDTO
from assistant.repositories import BaseAssistantRepository


class AIService:
    def __init__(self, repository: BaseAssistantRepository):
        self.repository = repository

    async def execute_response(self, input_data: InputDataDTO) -> OutputDataDTO:
        """
        Выполняет запрос к репозиторию и возвращает ответ.
        :param input_data: Входные данные для запроса.
        :return: Ответ от репозитория.
        """
        response = await self.repository.execute_response(input_data=input_data)
        await self.repository.close()
        return response
