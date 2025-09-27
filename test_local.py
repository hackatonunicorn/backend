#!/usr/bin/env python3
"""
Скрипт для тестирования локального запуска приложения
"""
import os
import sys
import subprocess
from pathlib import Path

def test_local():
    """Тестирует локальный запуск приложения"""
    print("🚀 Тестирование локального запуска...")
    
    # Проверяем, что мы в правильной директории
    if not Path("app/main.py").exists():
        print("❌ Файл app/main.py не найден. Запустите скрипт из корня проекта.")
        return False
    
    # Устанавливаем переменные окружения для тестирования
    env = os.environ.copy()
    env.update({
        "ENVIRONMENT": "development",
        "DATABASE_URL": "sqlite:///./test.db",
        "SECRET_KEY": "test-secret-key",
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:8000",
    })
    
    try:
        # Запускаем uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ]
        
        print(f"Выполняем команду: {' '.join(cmd)}")
        print("🌐 Приложение будет доступно по адресу: http://localhost:8000")
        print("📚 Документация: http://localhost:8000/docs")
        print("❤️ Health check: http://localhost:8000/health")
        print("\nНажмите Ctrl+C для остановки...")
        
        subprocess.run(cmd, env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Остановка сервера...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_local()
    sys.exit(0 if success else 1)
