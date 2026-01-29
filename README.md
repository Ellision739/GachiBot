# ♂ GachiBot TG ♂

Профессиональный асинхронный Telegram-бот для настоящих Dungeon Masters. Интеграция с ВК, кастомные никнеймы и встроенная система баг-репортов.

## Особенности
- **VK API Integration**: Цитаты и видео из лучших гачи-пабликов.
- **Async Data Manager**: Хранение данных в JSON с использованием `asyncio.Lock` и автоматическими бэкапами.
- **Pydantic Settings**: Строгая валидация настроек и окружения.
- **Custom Middlewares**: Приветствие новых пользователей и "тихий режим".

## Технологии
- **Python 3.10+**
- **Aiogram 3.x** (Telegram Bot API)
- **VK API** (Wrapper для ВК)
- **Pydantic Settings** (Config management)

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/your-username/gachibot-tg.git](https://github.com/your-username/gachibot-tg.git)
   cd gachibot-tg
2. **Создайте виртуальное окружение и установите зависимости:**

python -m venv venv
source venv/bin/activate  # Для Linux/macOS

или

venv\Scripts\activate
pip install -r requirements.txt     # Для Windows

3. **Настройте переменные окружения: Создайте файл .env в корне и заполните его:**

BOT_TOKEN=твой_токен_телеграм
VK_USER_TOKEN=твой_токен_вк
ADMIN_ID=твой_телеграм_id

4. **Запустите бота:**

python main.py


гачи помощь — список всех доступных команд.

⚠️ **Примечание.**
Для работы команды гачи аудио необходимо наличие папки music/ с MP3 файлами.
