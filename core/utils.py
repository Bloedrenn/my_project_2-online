import os
import asyncio
from openai import AsyncOpenAI

API_KEY = os.getenv("VSE_GPT_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.vsegpt.ru/v1",
)

prompt = """
Привет! Вы помогаете мне с валидацией пользовательских отзывов о барбершопе.
Ваша задача проверить отзыв на:
1. Наличие нецензурной лексики
2. Оскорбительный характер
3. Наличие рекламных ссылок или явной рекламы товаров/услуг
В целом на адекватность отзыва.
Если отзыв проходит проверку, вернуть JSON объект формата
{"id": 1, "status": "true"}
Если отзыв не проходит проверку, вернуть JSON объект формата
{"id": 1, "status": "false"}
"""

async def validate_review(review_text: str, review_id: int) -> str:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"ID отзыва: {review_id}\nТекст отзыва: {review_text}"}
    ]
    
    response = await client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        response_format={"type": "text"},
        temperature=0.5
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    async def test():
        test_review = "Спасибо за стрижку но лучше зайдите к нам в наше заведение через дорогу. Называется Лысый Арбуз!"
        result = await validate_review(test_review, 1)
        print(result)
    
    asyncio.run(test())
