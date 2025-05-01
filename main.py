import asyncio
import aiohttp
import re

from enum import Enum
from pydantic import BaseModel


class ResponseAIStatus(str, Enum):
    SUCCESS = "success"
    PROCESSING = "processing"
    ERROR = "error"


class ResponseAI(BaseModel):
    status: ResponseAIStatus
    thread_id: str | None
    response_text: str | None = None
    error_message: str | None = None




class DeepSeekAssistant:
    def __init__(self, api_key: str, model: str = "deepseek-chat", proxy: str | None = None,
                 system_prompt: str | None = None):
        """
        Асинхронный клиент для DeepSeek API через aiohttp
        """
        self.api_key = api_key
        self.model = model
        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.proxy = proxy
        self.system_prompt = system_prompt
        self.session: aiohttp.ClientSession | None = None

    async def _create_session(self):
        """Создание aiohttp-сессии"""
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=60)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    def _remove_sources(self, text: str) -> str:
        """Удаляет метки типа [*] из текста"""
        cleaned_text = re.sub(r'\[.*?\]', '', text)
        cleaned_text = re.sub(r'【.*?†.*?】', '', cleaned_text)
        return cleaned_text

    async def communicate(self, request: str) -> ResponseAI:
        """Отправка сообщения и получение ответа"""
        try:
            if not self.session:
                await self._create_session()

            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": request})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7
            }

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
                    assistant_reply = self._remove_sources(
                        data['choices'][0]['message']['content']
                    )
                    return ResponseAI(status=ResponseAIStatus.SUCCESS, thread_id=None, response_text=assistant_reply)
                else:
                    text = await response.text()
                    return ResponseAI(status=ResponseAIStatus.ERROR, thread_id=None, error_message=text)

        except Exception as e:
            return ResponseAI(status=ResponseAIStatus.ERROR, thread_id=None, error_message=str(e))

    async def close(self):
        """Закрытие сессии"""
        if self.session:
            await self.session.close()


async def main():
    assistant = DeepSeekAssistant(
        api_key="токен",
        proxy=None,
        system_prompt="Ты — юридический эксперт по законодательству РФ. Твоя задача — переформулировать описанную мной ситуацию в юридически грамотный текст от первого лица, как если бы я готовил официальное обращение в государственный орган, суд или иную инстанцию.  Используй только четкие формулировки, официально-деловой стиль. Не забудь указать обстоятельства, дату, места и участников. Определи какие нормы права нарушены, опираясь на кодексы РФ (их тоже надо упомянуть в ответе)."
    )

    response = await assistant.communicate(
        "Я купил товар в суши Ива организация такой по доставке роллов в Воронеже пришёл домой поел роллы и обнаружил что на них нету маркировки которые должна быть в соответствии с техническим регламентом таможенного Союза хочу вернуть деньги но администратор суши и Ангелина отказывает возврате и говорит жалуетесь куда хотите")
    print(response)

    await assistant.close()


if __name__ == "__main__":
    asyncio.run(main())
