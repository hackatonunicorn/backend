#!/usr/bin/env python3
"""
Скрипт запуска для Railway
"""
import os
import sys
import subprocess
from pathlib import Path

def run_migrations():
    """Запускает миграции перед стартом сервера"""
    print("🔄 Проверка и запуск миграций...")
    
    try:
        # Импортируем и запускаем миграции
        migration_script = Path(__file__).parent / "scripts" / "run_migrations.py"
        
        result = subprocess.run(
            [sys.executable, str(migration_script)],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✅ Миграции выполнены успешно!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Предупреждение: Ошибка миграций: {e}")
        print(f"Stderr: {e.stderr}")
        # Не останавливаем запуск, возможно таблицы уже существуют
        return False
    except Exception as e:
        print(f"⚠️ Предупреждение: Неожиданная ошибка миграций: {e}")
        return False

def main():
    """Запуск приложения с правильным портом"""
    # Получаем порт из переменной окружения или используем 8000 по умолчанию
    port = os.getenv("PORT", "8000")
    
    print(f"🚀 Запуск приложения на порту {port}")
    
    # Запускаем миграции перед стартом сервера
    run_migrations()
    
    # Команда запуска
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port,
        "--workers", "1"
    ]
    
    print(f"Выполняем команду: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Остановка сервера...")
        sys.exit(0)

if __name__ == "__main__":
    main()
