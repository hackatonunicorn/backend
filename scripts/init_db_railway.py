#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных в Railway
"""
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine
from app.models import Base

def init_database():
    """Инициализирует базу данных"""
    print("🚀 Инициализация базы данных...")
    
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы базы данных созданы успешно!")
        
        # Проверяем подключение
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Подключение к базе данных работает!")
            
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
