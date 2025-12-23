"""Фабрика для создания сотрудников (обратная совместимость)."""

from src.patterns.factory_method import EmployeeFactoryRegistry


class EmployeeFactory:
    """
    Фабрика для создания объектов сотрудников.
    
    Обертка над EmployeeFactoryRegistry для обратной совместимости.
    Использует паттерн Factory Method через EmployeeFactoryRegistry.
    """
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs):
        """
        Создать сотрудника указанного типа.
        
        Args:
            emp_type: Тип сотрудника ("manager", "developer", "salesperson", "employee")
            **kwargs: Параметры для создания сотрудника
        
        Returns:
            Объект сотрудника соответствующего типа
        
        Raises:
            ValueError: Если указан неверный тип сотрудника
        """
        return EmployeeFactoryRegistry.create_employee(emp_type, **kwargs)





