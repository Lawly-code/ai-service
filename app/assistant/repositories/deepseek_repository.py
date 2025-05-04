import aiohttp

from assistant.models import InputDataDTO, OutputDataDTO
from assistant.models.enum import ResponseAIStatus
from assistant.repositories import BaseAssistantRepository


class DeepSeekRepository(BaseAssistantRepository):
    """
    Репозиторий для DeepSeek API.
    """

    def __init__(
        self, api_key: str, model: str = "deepseek-chat", proxy: str | None = None
    ):
        super().__init__(
            api_key=api_key,
            model=model,
            url="https://api.deepseek.com/v1/chat/completions",
            proxy=proxy,
        )

    async def _create_session(self):
        """Создание aiohttp-сессии"""
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=60)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    async def execute_response(self, input_data: InputDataDTO) -> OutputDataDTO:
        try:
            if not self.session:
                await self._create_session()

            payload = {
                "model": self.model,
                "messages": input_data.to_messages(),
                "temperature": input_data.temperature,
            }
            if input_data.max_tokens is not None:
                payload["max_tokens"] = input_data.max_tokens

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            request_kwargs = {
                "headers": headers,
                "json": payload,
            }
            if self.proxy:
                request_kwargs["proxy"] = self.proxy

            async with self.session.post(self.url, **request_kwargs) as response:
                if response.status == 200:
                    data = await response.json()
                    assistant_reply = data['choices'][0]['message']['content']
                    return OutputDataDTO(
                        assistant_reply=assistant_reply,
                        status=ResponseAIStatus.SUCCESS,
                        thread_id=None,
                        response_text=assistant_reply,
                    )
                else:
                    text = await response.text()
                    return OutputDataDTO(
                        status=ResponseAIStatus.ERROR,
                        thread_id=None,
                        error_message=text,
                    )

        except Exception as e:
            return OutputDataDTO(
                status=ResponseAIStatus.ERROR, thread_id=None, error_message=str(e)
            )
