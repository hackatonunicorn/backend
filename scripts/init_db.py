#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
Запускать один раз после деплоя
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import engine
from app.models import Base
from app.config import settings

def init_database():
    """Создать все таблицы в базе данных"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_database()
