# Railway Deployment Setup

## Переменные окружения для Railway

Добавьте следующие переменные в настройки вашего проекта Railway:

### Обязательные переменные:

```
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-change-this-in-production
CORS_ORIGINS=https://your-frontend-domain.com
FRONTEND_URL=https://your-frontend-domain.com
```

### Опциональные переменные:

```
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### База данных:

Railway автоматически предоставляет переменную `DATABASE_URL` при подключении PostgreSQL базы данных.

### Настройка базы данных:

1. В Railway Dashboard добавьте PostgreSQL сервис
2. Railway автоматически создаст переменную `DATABASE_URL`
3. Убедитесь, что ваше приложение использует эту переменную

### Проверка:

После деплоя проверьте:
- `https://your-app.up.railway.app/` - должен показать информацию об API
- `https://your-app.up.railway.app/health` - должен показать статус "healthy"
- `https://your-app.up.railway.app/docs` - документация API (только в development)

## Возможные проблемы:

1. **Application failed to respond** - обычно означает проблемы с переменными окружения или базой данных
2. **Database connection failed** - проверьте DATABASE_URL
3. **CORS errors** - проверьте CORS_ORIGINS
