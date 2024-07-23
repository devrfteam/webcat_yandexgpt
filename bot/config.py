API_TOKEN = ''
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YANDEX_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer <TOKEN>"
}

instr = """
На основании текста определи категорию контента только из предложенних ниже. Выведи в ответе только категорию.

...Список категорий...
"""
