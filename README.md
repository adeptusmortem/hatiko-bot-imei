# Бэкенд-система для проверки IMEI устройств

Проект представляет собой бэкенд-систему для проверки IMEI устройств, интегрированную с Telegram-ботом и предоставляющую API для внешних запросов. Система позволяет проверять валидность IMEI и получать информацию о устройстве через внешний сервис [imeicheck.net](https://imeicheck.net/).

---

## Функционал

### 1. Доступ
- **Белый список пользователей для Telegram**:
  - Только пользователи из белого списка могут взаимодействовать с ботом.

- **Авторизация через API**:
  - Доступ к API осуществляется по токену авторизации.

### 2. Telegram-бот
- Пользователь отправляет боту IMEI.
- Бот проверяет IMEI на валидность и отправляет информацию о устройстве.

### 3. API
- **Запрос на получение информации**:
  - Метод: `POST /api/check-imei`
  - Параметры запроса:
    - `imei` (строка, обязательный) — IMEI устройства.
    - `token` (строка, обязательный) — токен авторизации.
  - Ответ: JSON с информацией о IMEI.

---

## Стэк
- **Язык программирования**: Python
- **Фреймворки**:
  - Flask (для API)
  - python-telegram-bot (для Telegram-бота)
- **База данных**: SQLite (для хранения белого списка пользователей)
- **Внешний сервис**: [imeicheck.net](https://imeicheck.net/)

---

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/adeptusmortem/hatiko-bot-imei.git
   cd imei-checker
