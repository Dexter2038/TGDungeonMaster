from typing import Iterator
from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from together import Together
from together.types.chat_completions import ChatCompletionChunk, ChatCompletionResponse


router = Router(name=__name__)


client: Together = Together()


@router.message(F.text)
async def echo(message: Message) -> None:
    response: ChatCompletionResponse | Iterator[ChatCompletionChunk] = (
        client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=1024,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
        )
    )
    answer = response.choices[0].message.content
    print("Ответил на {}: {}".format(message.text, answer))
    await message.reply(answer)
