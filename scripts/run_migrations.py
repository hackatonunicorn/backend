#!/usr/bin/env python3
"""
Скрипт для запуска миграций Alembic
"""
import os
import sys
import subprocess
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_migrations():
    """Запускает миграции Alembic с fallback на прямое создание таблиц"""
    print("🔄 Запуск миграций базы данных...")
    
    try:
        # Переходим в директорию с alembic
        os.chdir(Path(__file__).parent.parent)
        
        # Проверяем, есть ли миграции для применения
        result = subprocess.run(
            ["alembic", "current"],
            capture_output=True,
            text=True,
            check=False
        )
        
        print(f"Текущая версия миграций: {result.stdout.strip()}")
        
        # Запускаем миграции
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Миграции выполнены успешно!")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Ошибка выполнения миграций Alembic: {e}")
        print(f"Stderr: {e.stderr}")
        
        # Fallback: пытаемся создать таблицы напрямую
        print("🔄 Пробуем создать таблицы напрямую...")
        try:
            from app.database import engine, Base
            Base.metadata.create_all(bind=engine)
            print("✅ Таблицы созданы напрямую!")
            return True
        except Exception as direct_error:
            print(f"❌ Ошибка прямого создания таблиц: {direct_error}")
            return False
            
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        
        # Fallback: пытаемся создать таблицы напрямую
        print("🔄 Пробуем создать таблицы напрямую...")
        try:
            from app.database import engine, Base
            Base.metadata.create_all(bind=engine)
            print("✅ Таблицы созданы напрямую!")
            return True
        except Exception as direct_error:
            print(f"❌ Ошибка прямого создания таблиц: {direct_error}")
            return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
