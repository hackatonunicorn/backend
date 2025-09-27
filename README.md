# Unicorn Authentication API

FastAPI бэкенд для аутентификации платформы Unicorn для фандрайзинга.

## 🚀 Быстрый деплой на Railway

### Шаг 1: Подготовка

1. Убедитесь, что ваш код загружен в GitHub репозиторий
2. Перейдите на [Railway.app](https://railway.app) и войдите через GitHub

### Шаг 2: Создание проекта

1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий `unicorn-backend`
4. Railway автоматически определит, что это Python проект

### Шаг 3: Настройка базы данных

1. В вашем проекте нажмите "+" для добавления сервиса
2. Выберите "Database" → "PostgreSQL"
3. Railway создаст PostgreSQL базу данных
4. Скопируйте переменную `DATABASE_URL` из настроек базы данных

### Шаг 4: Настройка переменных окружения

В настройках вашего сервиса добавьте следующие переменные:

```env
# Обязательные
DATABASE_URL=postgresql://... (автоматически создается Railway)
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random

# Опциональные (можно оставить пустыми для начала)
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-domain.com,https://your-frontend-domain.vercel.app

# OAuth (добавить позже)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=

# Email (добавить позже)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=noreply@unicorn.com

# Redis (Railway может создать автоматически)
REDIS_URL=redis://... (если нужен)
```

### Шаг 5: Деплой

1. Railway автоматически начнет деплой после добавления переменных
2. Дождитесь завершения сборки (обычно 2-3 минуты)
3. Получите URL вашего API (что-то вроде `https://unicorn-backend-production-xxxx.up.railway.app`)

### Шаг 6: Проверка

Откройте в браузере:
- `https://your-api-url.railway.app/` - главная страница
- `https://your-api-url.railway.app/docs` - документация API
- `https://your-api-url.railway.app/health` - проверка здоровья

## 📋 API Эндпоинты

### Аутентификация

- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/auth/google` - OAuth Google
- `POST /api/v1/auth/linkedin` - OAuth LinkedIn
- `GET /api/v1/auth/me` - Получить профиль пользователя

### Пример запроса регистрации:

```bash
curl -X POST "https://your-api-url.railway.app/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "company_name": "Acme Inc",
    "password": "SecurePass123",
    "agree_terms": true
  }'
```

### Пример запроса входа:

```bash
curl -X POST "https://your-api-url.railway.app/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123",
    "remember_me": false
  }'
```

## 🔧 Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `env.example`

3. Запустите локально:
```bash
uvicorn app.main:app --reload
```

## 📝 Структура проекта

```
app/
├── __init__.py
├── main.py              # Главный файл приложения
├── config.py            # Конфигурация
├── database.py          # Настройки БД
├── models.py            # Модели SQLAlchemy
├── schemas.py           # Pydantic схемы
├── auth.py              # JWT аутентификация
├── oauth.py             # OAuth интеграция
├── crud.py              # CRUD операции
├── dependencies.py      # Зависимости FastAPI
├── exceptions.py        # Обработка ошибок
└── routers/
    ├── __init__.py
    └── auth.py          # Роуты аутентификации

alembic/                 # Миграции БД
scripts/                 # Скрипты
requirements.txt         # Зависимости Python
railway.json             # Конфигурация Railway
```

## 🛡️ Безопасность

- JWT токены с истечением через 15 минут (access) и 7 дней (refresh)
- Rate limiting: 5 запросов в минуту на IP
- Валидация паролей (минимум 8 символов, заглавные, строчные, цифры)
- Хеширование паролей с bcrypt
- CORS настройки для фронтенда

## 📊 Мониторинг

Railway предоставляет:
- Логи в реальном времени
- Метрики производительности
- Мониторинг базы данных
- Автоматические бэкапы

## 💰 Стоимость

Railway предоставляет:
- **Бесплатный план**: $5 кредитов в месяц (достаточно для тестирования)
- **Pro план**: $20/месяц за неограниченное использование

Для небольшого проекта бесплатного плана будет достаточно!
