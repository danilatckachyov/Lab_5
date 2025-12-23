"""Модуль с реализацией паттернов проектирования."""

from src.database.connection import DatabaseConnection
from src.patterns.factory_method import (
    EmployeeFactory,
    ManagerFactory,
    DeveloperFactory,
    SalespersonFactory,
    EmployeeFactoryRegistry
)
from src.patterns.strategy import (
    BonusStrategy,
    PerformanceBonusStrategy,
    SeniorityBonusStrategy,
    ProjectBonusStrategy,
    BonusCalculator
)
from src.patterns.observer import (
    Observer,
    Subject,
    NotificationSystem,
    EmployeeSubject,
    EmailNotifier
)

__all__ = [
    'DatabaseConnection',
    'EmployeeFactory',
    'ManagerFactory',
    'DeveloperFactory',
    'SalespersonFactory',
    'EmployeeFactoryRegistry',
    'BonusStrategy',
    'PerformanceBonusStrategy',
    'SeniorityBonusStrategy',
    'ProjectBonusStrategy',
    'BonusCalculator',
    'Observer',
    'Subject',
    'NotificationSystem',
    'EmployeeSubject',
    'EmailNotifier'
]

