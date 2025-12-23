"""Паттерн Singleton для управления подключением к базе данных."""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    Класс для управления единственным подключением к базе данных SQLite.
    
    Реализует паттерн Singleton - гарантирует единственный экземпляр
    подключения в рамках приложения.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """
        Создание или возврат единственного экземпляра.
        
        Returns:
            Единственный экземпляр DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Инициализация подключения (выполняется только один раз)."""
        if self._connection is None:
            self._db_path = "employee_management.db"
    
    def get_connection(self, db_path: Optional[str] = None) -> sqlite3.Connection:
        """
        Получить подключение к базе данных.
        
        Args:
            db_path: Путь к файлу базы данных (опционально)
        
        Returns:
            Объект подключения к SQLite
        """
        if db_path:
            self._db_path = db_path
        
        if self._connection is None:
            self._connection = sqlite3.connect(
                self._db_path,
                check_same_thread=False
            )
            self._connection.row_factory = sqlite3.Row
            # Создаем таблицы при первом подключении
            self._create_tables()
        
        return self._connection
    
    def close_connection(self) -> None:
        """Закрыть подключение к базе данных."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def _create_tables(self) -> None:
        """Создать необходимые таблицы в базе данных."""
        cursor = self._connection.cursor()
        
        # Таблица сотрудников
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                base_salary REAL NOT NULL,
                employee_type TEXT NOT NULL,
                data_json TEXT
            )
        """)
        
        # Таблица отделов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                name TEXT PRIMARY KEY,
                data_json TEXT
            )
        """)
        
        self._connection.commit()
    
    @classmethod
    def get_instance(cls) -> 'DatabaseConnection':
        """
        Получить единственный экземпляр класса (альтернативный способ).
        
        Returns:
            Единственный экземпляр DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __str__(self) -> str:
        """Строковое представление."""
        status = "подключено" if self._connection is not None else "не подключено"
        return f"DatabaseConnection (статус: {status})"

