#!/usr/bin/env python3
"""
Скрипт для прямого создания таблиц без миграций
Используется как fallback, если Alembic не работает
"""
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models import User, OAuthAccount

def create_tables_direct():
    """Создает таблицы напрямую через SQLAlchemy"""
    print("🔄 Создание таблиц напрямую...")
    
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы успешно!")
        
        # Проверяем, что таблицы действительно созданы
        with engine.connect() as connection:
            # Проверяем таблицу users
            result = connection.execute("SELECT COUNT(*) FROM users")
            users_count = result.fetchone()[0]
            print(f"✅ Таблица 'users' создана (записей: {users_count})")
            
            # Проверяем таблицу oauth_accounts
            result = connection.execute("SELECT COUNT(*) FROM oauth_accounts")
            oauth_count = result.fetchone()[0]
            print(f"✅ Таблица 'oauth_accounts' создана (записей: {oauth_count})")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
        return False

if __name__ == "__main__":
    success = create_tables_direct()
    sys.exit(0 if success else 1)
