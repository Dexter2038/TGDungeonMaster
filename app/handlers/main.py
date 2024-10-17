from os import environ
from typing import Iterator
from aiogram import Bot, Router
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.enums.parse_mode import ParseMode
from together import Together
from together.types.chat_completions import ChatCompletionChunk, ChatCompletionResponse


router = Router(name=__name__)
# model_name = "app/models/RuGPT3"

load_dotenv()

client = Together(api_key=environ['TOGETHER_API_KEY'])

@router.message(lambda x: x.text)
async def echo(message: Message, bot: Bot):
    response: ChatCompletionResponse | Iterator[ChatCompletionChunk] = client.chat.completions.create(
    model="meta-llama/Llama-Vision-Free",
    messages=[{
        "role": "user",
        "content": message.text
    }],
    max_tokens=1024,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>","<|eom_id|>"]
)
    answer = response.choices[0].message.content
    print("Ответил на {}: {}".format(message.text, answer))
    await message.reply(answer)