from pydantic import BaseModel

from assistant.models.enum import ResponseAIStatus


class InputDataDTO(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float
    max_tokens: int

    def to_messages(self) -> list[dict]:
        """Преобразует текст в формат сообщений"""
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt}
        ]


class OutputDataDTO(BaseModel):
    assistant_reply: str | None = None
    status: ResponseAIStatus
    thread_id: str | None = None
    error_message: str | None = None
