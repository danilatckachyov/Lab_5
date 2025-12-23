"""Паттерн Strategy для расчета бонусов сотрудников."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.abstract_employee import AbstractEmployee


class BonusStrategy(ABC):
    """
    Абстрактная стратегия для расчета бонусов.
    
    Реализует паттерн Strategy - определяет семейство алгоритмов,
    инкапсулирует каждый из них и делает их взаимозаменяемыми.
    """
    
    @abstractmethod
    def calculate_bonus(self, employee: 'AbstractEmployee', **kwargs) -> float:
        """
        Рассчитать бонус для сотрудника.
        
        Args:
            employee: Объект сотрудника
            **kwargs: Дополнительные параметры для расчета
        
        Returns:
            Размер бонуса
        """
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе производительности.
    
    Бонус = базовая зарплата * коэффициент производительности
    """
    
    def calculate_bonus(self, employee: 'AbstractEmployee', 
                        performance_rating: float = 1.0, **kwargs) -> float:
        """
        Рассчитать бонус на основе производительности.
        
        Args:
            employee: Объект сотрудника
            performance_rating: Рейтинг производительности (0.0 - 2.0)
            **kwargs: Дополнительные параметры
        
        Returns:
            Размер бонуса
        """
        if not 0.0 <= performance_rating <= 2.0:
            raise ValueError("Рейтинг производительности должен быть от 0.0 до 2.0")
        
        base_salary = employee.base_salary
        # Бонус = 10% от базовой зарплаты * рейтинг
        return base_salary * 0.1 * performance_rating


class SeniorityBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе стажа работы.
    
    Бонус увеличивается с увеличением стажа.
    """
    
    def calculate_bonus(self, employee: 'AbstractEmployee', 
                        years_of_service: int = 0, **kwargs) -> float:
        """
        Рассчитать бонус на основе стажа.
        
        Args:
            employee: Объект сотрудника
            years_of_service: Количество лет работы в компании
            **kwargs: Дополнительные параметры
        
        Returns:
            Размер бонуса
        """
        if years_of_service < 0:
            raise ValueError("Стаж не может быть отрицательным")
        
        base_salary = employee.base_salary
        # Бонус = 5% от базовой зарплаты за каждый год работы (максимум 50%)
        bonus_percentage = min(years_of_service * 0.05, 0.5)
        return base_salary * bonus_percentage


class ProjectBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе участия в проектах.
    
    Бонус зависит от количества проектов и их статуса.
    """
    
    def calculate_bonus(self, employee: 'AbstractEmployee', 
                       project_count: int = 0, 
                       completed_projects: int = 0, **kwargs) -> float:
        """
        Рассчитать бонус на основе проектной деятельности.
        
        Args:
            employee: Объект сотрудника
            project_count: Общее количество проектов
            completed_projects: Количество завершенных проектов
            **kwargs: Дополнительные параметры
        
        Returns:
            Размер бонуса
        """
        if project_count < 0 or completed_projects < 0:
            raise ValueError("Количество проектов не может быть отрицательным")
        if completed_projects > project_count:
            raise ValueError("Завершенных проектов не может быть больше общего количества")
        
        base_salary = employee.base_salary
        
        # Бонус за участие в проектах: 3% за каждый проект
        participation_bonus = base_salary * 0.03 * project_count
        
        # Дополнительный бонус за завершенные проекты: 5% за каждый
        completion_bonus = base_salary * 0.05 * completed_projects
        
        return participation_bonus + completion_bonus


class BonusCalculator:
    """
    Контекст для использования стратегий расчета бонусов.
    
    Позволяет динамически менять стратегию расчета бонусов.
    """
    
    def __init__(self, strategy: BonusStrategy = None):
        """
        Инициализация калькулятора бонусов.
        
        Args:
            strategy: Стратегия расчета бонусов (опционально)
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: BonusStrategy) -> None:
        """
        Установить стратегию расчета бонусов.
        
        Args:
            strategy: Новая стратегия расчета
        """
        self._strategy = strategy
    
    def calculate(self, employee: 'AbstractEmployee', **kwargs) -> float:
        """
        Рассчитать бонус для сотрудника используя текущую стратегию.
        
        Args:
            employee: Объект сотрудника
            **kwargs: Параметры для стратегии
        
        Returns:
            Размер бонуса
        
        Raises:
            ValueError: Если стратегия не установлена
        """
        if self._strategy is None:
            raise ValueError("Стратегия расчета бонусов не установлена")
        
        return self._strategy.calculate_bonus(employee, **kwargs)

