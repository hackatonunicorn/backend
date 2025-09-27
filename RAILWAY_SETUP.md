# Railway Deployment Setup

## 🚨 КРИТИЧНО: Настройка переменных окружения

### Шаг 1: Добавьте PostgreSQL базу данных
1. В Railway Dashboard нажмите "+ New"
2. Выберите "Database" → "PostgreSQL"
3. Railway автоматически создаст переменную `DATABASE_URL`

### Шаг 2: Обязательные переменные окружения

Добавьте следующие переменные в настройки вашего backend сервиса:

```
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-change-this-in-production
CORS_ORIGINS=https://your-frontend-domain.com
FRONTEND_URL=https://your-frontend-domain.com
```

### Шаг 3: Проверьте, что DATABASE_URL автоматически добавлен
Railway должен автоматически добавить переменную `DATABASE_URL` после подключения PostgreSQL.

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

## 🔍 Диагностика проблем:

### Health Check не проходит:
1. **Проверьте логи деплоя** в Railway Dashboard
2. **Убедитесь, что PostgreSQL подключен** и DATABASE_URL настроен
3. **Проверьте переменные окружения** - все обязательные переменные должны быть установлены

### Проверка статуса:
```bash
# Проверьте health check
curl https://backend-production-b447.up.railway.app/health

# Должен вернуть:
{
  "status": "healthy",
  "service": "unicorn-auth-api", 
  "database": "connected",
  "environment": "production"
}
```

### Возможные проблемы:

1. **Application failed to respond** - проверьте переменные окружения и DATABASE_URL
2. **Database connection failed** - убедитесь, что PostgreSQL сервис запущен и подключен
3. **Health check timeout** - обычно означает, что приложение не запускается из-за ошибок в коде
4. **CORS errors** - проверьте CORS_ORIGINS

### После исправления:
1. Настройте переменные окружения
2. Перезапустите деплой (Redeploy)
3. Проверьте логи в Railway Dashboard
