from abc import ABC, abstractmethod
import aiohttp

from assistant.models import InputDataDTO, OutputDataDTO


class BaseAssistantRepository(ABC):
    """
    База для репозиториев ассистента.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        url: str,
        session: aiohttp.ClientSession | None = None,
        proxy: str | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.url = url
        self.proxy = proxy
        self.session = session

    @abstractmethod
    async def execute_response(self, input_data: InputDataDTO) -> OutputDataDTO:
        pass

    async def close(self):
        """
        Закрывает сессию.
        """
        if self.session:
            await self.session.close()
            self.session = None
