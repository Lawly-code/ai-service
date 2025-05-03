from assistant.models import InputDataDTO
from assistant.repositories import DeepSeekRepository
from assistant.services.ai_service import AIService
from config import DEEPSEEK_TOKEN, TEMPERATURE, MAX_TOKENS
from utils.prompt import prompt


async def ai_chat(user_prompt: str) -> str:
    service = AIService(repository=DeepSeekRepository(api_key=DEEPSEEK_TOKEN))
    input_data = InputDataDTO(
        system_prompt=prompt("ai_chat"),
        user_prompt=user_prompt,
        temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    response = await service.execute_response(input_data=input_data)
    return response.assistant_reply
