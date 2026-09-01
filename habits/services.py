import requests

from config.settings import BOT_TOKEN, TG_URL


def send_tg_massege(tg_chat_id, massage):
    """Функция отправки сообщения в ТГ"""

    params = {
        "text": massage,
        "chat_id": tg_chat_id,
    }

    response = requests.post(f"{TG_URL}{BOT_TOKEN}/sendMessage", json=params)
    # print(response.text) для проверки через shell
    return response.json()
