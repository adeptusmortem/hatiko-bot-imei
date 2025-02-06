import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import requests
import json

# Чтение токенов из JSON-файла
with open("tokens.json", "r", encoding="utf-8") as file:
    tokens = json.load(file)

apiToken = tokens["apiToken"]
tgToken = tokens["tgToken"]

# apiToken = "UmnSsbgjiH45Neho0B7gyHNlu6T0yiLgFkq0fzWV86688237"

# Создание БД с белым списком пользователей
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
conn.commit()
conn.close()

# Функция для проверки IMEI через imeicheck.net
def check_imei(imei):
    url = "https://api.imeicheck.net/v1/checks"
    payload = json.dumps({
        "deviceId": imei,
        "serviceId": 12
    })
    headers = {
        'Authorization': 'Bearer ' + apiToken,
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.text

# Функция для проверки пользователя в белом списке
def is_user_allowed(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне IMEI для проверки.")

#### Функция для отладки, добавления пользователя в БД по его же запросу

# Добавить пользователя в белый списко
def add_user_to_whitelist(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

    # Обработчик команды /whitelist_me
async def whitelist_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Добавляем пользователя в белый список
    add_user_to_whitelist(user_id)
    await update.message.reply_text(f"Пользователь {user_id} добавлен в белый список.")

####

# Обработчик текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return

    imei = update.message.text
    if len(imei) != 15 or not imei.isdigit():
        await update.message.reply_text("Некорректный IMEI. IMEI должен состоять из 15 цифр.")
        return

    result = check_imei(imei)
    await update.message.reply_text(f"Результат проверки: {result}")

# Запуск бота
def main():
    # Запуск бота
    application = Application.builder().token(tgToken).build()

    # Обработка команд 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("whitelist_me", whitelist_me))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()