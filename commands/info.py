import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

import const
from const import __version__, __author__
from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='info_blueprint'
)

@user.on.message_handler(FromMe(), text="Info")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n⚠🚫Обновить надо🥵 {version_rest['version']}\n" \
                      f"{version_rest['description']}\n"
    else:
        update_text = ""

    text = f"""
    🤑☺️ DМL LP ❤️ v{__version__}
    |🔴 Ключ рукаптчи: {"✅" if db.ru_captcha_key else "❌"}
    |🟠 Удаление уведомлений: {"✅" if db.delete_all_notify else "❌"}
    |🟡 Выключение уведомлений: {"✅" if db.disable_notifications else "❌"}
    |🟢 В игноре: {len(db.ignored_members)}
    |🔵 В глобальном игноре: {len(db.ignored_global_members)}
    |🟣 В муте: {len(db.muted_members)}
    |🟤 Довов: {len(db.trusted)}
    |⚫ Алиасов: {len(db.aliases)}
    |⚪ Шаблонов для удаления: {len(db.regex_deleter)}
    |🔴 Выходить из бесед: {"✅" if db.auto_exit_from_chat else "❌"}
    |🟠 Удалять диалог: {"✅" if db.auto_exit_from_chat_delete_chat else "❌"}
    |🟡 Добавлять пригласившего в ЧС: {"✅" if db.auto_exit_from_chat_add_to_black_list else "❌"}
    |🟢 Повторялка: {"✅" if db.repeater_active else "❌"}
    |🔵 Триггер на повторялку: {db.repeater_word}       
    |🟣 Сервисные префиксы: {' '.join(db.service_prefixes)}
    |🟤 Свои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    |⚫ Префиксы дежурного: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}{update_text}
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
