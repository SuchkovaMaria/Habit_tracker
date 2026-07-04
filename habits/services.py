import requests

from config.settings import TG_URL, BOT_TOKEN


def send_tg_massege(tg_chat_id, massage):
    """Функция отправки сообщения в ТГ"""

    params = {
        'text': massage,
        'tg_chat_id': tg_chat_id,
    }

    response = requests.post(f"{TG_URL}{BOT_TOKEN}/sendMessage", json=params)
    return response.json()