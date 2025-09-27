#!/usr/bin/env python3
"""
Скрипт запуска для Railway
"""
import os
import sys
import subprocess

def main():
    """Запуск приложения с правильным портом"""
    # Получаем порт из переменной окружения или используем 8000 по умолчанию
    port = os.getenv("PORT", "8000")
    
    print(f"🚀 Запуск приложения на порту {port}")
    
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
