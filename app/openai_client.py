import os
import openai
from dotenv import load_dotenv
import json
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def analyze_contract(text: str) -> dict:
    """
    Отправить текст договора в OpenAI и получить гарантированно валидный JSON:
      - предмет: краткое описание
      - условия: словарь ключевых условий
      - стороны: список объектов {role, name}
    """
    system = {
        "role": "system",
        "content": (
            "Ты — помощник для разбора договоров. "
            "В ответе должен быть **только** JSON-объект. "
            "Используй двойные кавычки для всех строк. "
            "Не добавляй никаких комментариев или текста вне фигурных скобок."
        )
    }
    user = {
        "role": "user",
        "content": (
            "Проанализируй следующий текст договора и верни строго JSON с тремя ключами:\n"
            "  • 'предмет': краткое, емкое описание предмета договора;\n"
            "  • 'условия': основные ключевые условия договора в формате словаря (ключ — название условия, значение — краткое описание);\n"
            "  • 'стороны': массив объектов с ключами 'role' (роль) и 'name' (имя стороны), без лишних деталей.\n"
            "Пожалуйста, не добавляй никаких лишних данных или комментариев.\n\n" + text
        )
    }

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system, user],
        temperature=0
    )
    content = response.choices[0].message.content.strip()
    match = re.search(r"(\{.*\})", content, flags=re.DOTALL)
    json_str = match.group(1) if match else content

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("❌ JSON parsing error:", e)
        print("❌ Raw content:", content)
        raise ValueError(content)
