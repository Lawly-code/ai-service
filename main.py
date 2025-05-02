import asyncio

from assistant.models import InputDataDTO
from assistant.repositories import DeepSeekRepository
from assistant.services.ai_service import AIService


async def main():
    service = AIService(repository=DeepSeekRepository(api_key="токен"))
    input_data = InputDataDTO(
        system_prompt="Ты — юридический эксперт по законодательству РФ. Переформулируй ситуацию в юридически грамотный текст от первого лица, ссылаясь на кодексы РФ максимально подробно, но не указывай ФИО и другую информацию, которую я не указывал даже в обезличенной форме. Не оставляй поля для вставки моих данных. Не нужно указывать никакой лишней информации перед ответом и после. Просто преобразуй мой текст, без твоих пояснений.",
        user_prompt="Я купил товар в суши Ива организация такой по доставке роллов в Воронеже пришёл домой поел роллы и обнаружил что на них нету маркировки которые должна быть в соответствии с техническим регламентом таможенного Союза хочу вернуть деньги но администратор суши и Ангелина отказывает возврате и говорит жалуетесь куда хотите",
        temperature=0.7, max_tokens=1000)
    response = await service.execute_response(input_data=input_data)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
