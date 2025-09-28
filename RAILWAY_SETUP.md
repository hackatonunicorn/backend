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
CORS_ORIGINS=https://your-frontend-domain.com,https://localhost:3000,http://localhost:3000
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
4. **Проверьте создание таблиц** - убедитесь, что таблицы `users` и `oauth_accounts` созданы в PostgreSQL

### Проблемы с базой данных:

#### Таблицы не созданы (500 ошибка при авторизации):
1. **Автоматическое решение**: Приложение теперь автоматически создает таблицы при запуске
2. **Ручное решение**: Если автоматическое создание не сработало:
   ```bash
   # Подключитесь к PostgreSQL через Railway Dashboard
   # Или выполните SQL команды:
   ```
   ```sql
   -- Проверьте существующие таблицы
   \dt
   
   -- Если таблиц нет, создайте их вручную или перезапустите деплой
   ```

#### Проверка статуса таблиц:
```bash
curl https://your-app.up.railway.app/health
```
Ответ должен содержать:
```json
{
  "status": "healthy",
  "service": "unicorn-auth-api",
  "database": "connected",
  "tables_created": true
}
```

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

1. **"Invalid value for '--port': '$PORT' is not a valid integer"** - ✅ ИСПРАВЛЕНО: Создан скрипт start.py для правильной обработки PORT
2. **Application failed to respond** - проверьте переменные окружения и DATABASE_URL
3. **Database connection failed** - убедитесь, что PostgreSQL сервис запущен и подключен
4. **Health check timeout** - обычно означает, что приложение не запускается из-за ошибок в коде
5. **CORS errors** - проверьте CORS_ORIGINS

### После исправления:
1. Настройте переменные окружения
2. Перезапустите деплой (Redeploy)
3. Проверьте логи в Railway Dashboard
