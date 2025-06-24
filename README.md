# PDF Contract Analyzer

**PDF Contract Analyzer** — это веб-приложение на FastAPI, которое позволяет анализировать договоры в формате PDF с помощью ChatGPT. Оно извлекает ключевую информацию, такую как предмет договора, условия и стороны.

## 🚀 Функции

- Загрузка и хранение PDF-документов
- Автоматический анализ текста с помощью OpenAI GPT
- Извлечение и отображение:
  - Предмета договора
  - Ключевых условий (до 5)
  - Сторон договора (работодатель, работник и т. д.)
- История загруженных договоров
- Удобный и адаптивный UI

## 🛠️ Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/PDF_Contract_Analyzer.git
   cd PDF_Contract_Analyzer
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте `.env` файл и добавьте свой OpenAI API ключ, а также базу данных:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/contracts_db
   ```

4. Запустите приложение:
   ```
   python run.py
   ```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## 📁 Структура проекта

- `app/` — логика FastAPI, шаблоны и обработка PDF/AI
- `static/` — стили
- `uploads/` — папка для загруженных PDF (игнорируется в гите)
- `run.py` — точка входа
- `analyzer_launcher/` — упрощенный запуск при помощи .bat
- `assets/` - скриншоты

## ⚙️ Зависимости

- Python 3.10+
- FastAPI
- SQLAlchemy
- Jinja2
- python-dotenv
- pdfplumber
- OpenAI API

## 🧠 Примечание

⚠️ Все PDF-файлы анализируются локально, но отправляются на сервера OpenAI для анализа. Не загружайте конфиденциальные данные без разрешения.

## 📄 Лицензия

MIT License. Проект создан в обучающих целях.

## 📸 Скриншоты

Главная страница:
![Главная](assets/screenshot1.png)

Результат анализа:
![Результат](assets/screenshot2.png)