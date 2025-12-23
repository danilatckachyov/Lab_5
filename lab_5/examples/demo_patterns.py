"""Демонстрация применения паттернов проектирования."""

from src.database.connection import DatabaseConnection
from src.patterns.factory_method import (
    EmployeeFactoryRegistry,
    ManagerFactory,
    DeveloperFactory,
    SalespersonFactory
)
from src.patterns.strategy import (
    BonusCalculator,
    PerformanceBonusStrategy,
    SeniorityBonusStrategy,
    ProjectBonusStrategy
)
from src.patterns.observer import (
    NotificationSystem,
    EmployeeSubject,
    EmailNotifier
)


def demonstrate_singleton():
    """Демонстрация паттерна Singleton."""
    print("=" * 60)
    print("1. ДЕМОНСТРАЦИЯ ПАТТЕРНА SINGLETON")
    print("=" * 60)
    
    # Создаем несколько экземпляров
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    db3 = DatabaseConnection.get_instance()
    
    # Проверяем, что все ссылки указывают на один объект
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 is db3: {db1 is db3}")
    print(f"Все экземпляры одинаковые: {db1 is db2 is db3}")
    print(f"ID db1: {id(db1)}")
    print(f"ID db2: {id(db2)}")
    print(f"ID db3: {id(db3)}")
    
    # Получаем подключение
    conn1 = db1.get_connection()
    conn2 = db2.get_connection()
    print(f"\nПодключения одинаковые: {conn1 is conn2}")
    print()
    
    return db1


def demonstrate_factory_method():
    """Демонстрация паттерна Factory Method."""
    print("=" * 60)
    print("2. ДЕМОНСТРАЦИЯ ПАТТЕРНА FACTORY METHOD")
    print("=" * 60)
    
    # Использование реестра фабрик
    manager = EmployeeFactoryRegistry.create_employee(
        "manager",
        id=1,
        name="Иван Иванов",
        department="Управление",
        base_salary=100000,
        bonus=20000
    )
    print(f"Создан через реестр: {manager.get_info()}")
    
    # Использование конкретных фабрик
    manager_factory = ManagerFactory()
    developer_factory = DeveloperFactory()
    salesperson_factory = SalespersonFactory()
    
    manager2 = manager_factory.create_employee(
        id=2,
        name="Петр Петров",
        department="Управление",
        base_salary=90000,
        bonus=15000
    )
    
    developer = developer_factory.create_employee(
        id=3,
        name="Анна Сидорова",
        department="Разработка",
        base_salary=80000,
        tech_stack=["Python", "Django", "PostgreSQL"],
        seniority_level="senior"
    )
    
    salesperson = salesperson_factory.create_employee(
        id=4,
        name="Мария Козлова",
        department="Продажи",
        base_salary=60000,
        commission_rate=0.1,
        sales_volume=500000
    )
    
    print(f"\nСоздан через ManagerFactory: {manager2.get_info()}")
    print(f"Создан через DeveloperFactory: {developer.get_info()}")
    print(f"Создан через SalespersonFactory: {salesperson.get_info()}")
    print()
    
    return [manager, manager2, developer, salesperson]


def demonstrate_strategy():
    """Демонстрация паттерна Strategy."""
    print("=" * 60)
    print("3. ДЕМОНСТРАЦИЯ ПАТТЕРНА STRATEGY")
    print("=" * 60)
    
    from src.employees.manager import Manager
    
    employee = Manager(
        id=5,
        name="Тестовый Менеджер",
        department="Тест",
        base_salary=100000,
        bonus=0
    )
    
    calculator = BonusCalculator()
    
    # Стратегия на основе производительности
    calculator.set_strategy(PerformanceBonusStrategy())
    performance_bonus = calculator.calculate(employee, performance_rating=1.5)
    print(f"Бонус за производительность (рейтинг 1.5): {performance_bonus:.2f}")
    
    # Стратегия на основе стажа
    calculator.set_strategy(SeniorityBonusStrategy())
    seniority_bonus = calculator.calculate(employee, years_of_service=5)
    print(f"Бонус за стаж (5 лет): {seniority_bonus:.2f}")
    
    # Стратегия на основе проектов
    calculator.set_strategy(ProjectBonusStrategy())
    project_bonus = calculator.calculate(
        employee,
        project_count=3,
        completed_projects=2
    )
    print(f"Бонус за проекты (3 проекта, 2 завершено): {project_bonus:.2f}")
    
    # Сравнение стратегий
    print(f"\nСравнение стратегий для сотрудника с зарплатой {employee.base_salary}:")
    print(f"  Производительность: {performance_bonus:.2f}")
    print(f"  Стаж: {seniority_bonus:.2f}")
    print(f"  Проекты: {project_bonus:.2f}")
    print()
    
    return calculator


def demonstrate_observer():
    """Демонстрация паттерна Observer."""
    print("=" * 60)
    print("4. ДЕМОНСТРАЦИЯ ПАТТЕРНА OBSERVER")
    print("=" * 60)
    
    from src.employees.manager import Manager
    
    # Создаем сотрудника
    employee = Manager(
        id=6,
        name="Наблюдаемый Менеджер",
        department="Отдел А",
        base_salary=95000,
        bonus=10000
    )
    
    # Создаем субъект для сотрудника
    employee_subject = EmployeeSubject(employee)
    
    # Создаем наблюдателей
    notification_system = NotificationSystem()
    email_notifier = EmailNotifier("hr@company.com")
    
    # Подписываем наблюдателей
    employee_subject.attach(notification_system)
    employee_subject.attach(email_notifier)
    
    print("Наблюдатели подписаны на изменения сотрудника")
    print()
    
    # Имитируем изменения
    old_salary = employee.calculate_salary()
    employee.bonus = 15000
    new_salary = employee.calculate_salary()
    employee_subject.notify_salary_change(old_salary, new_salary)
    
    # Изменение отдела
    old_dept = employee.department
    employee.department = "Отдел Б"
    employee_subject.notify_department_change(old_dept, employee.department)
    
    # Изменение статуса
    employee_subject.notify_status_change("Активен")
    
    # Отписываем одного наблюдателя
    employee_subject.detach(email_notifier)
    print("Email-уведомитель отписан")
    print()
    
    # Еще одно изменение (только notification_system получит уведомление)
    employee_subject.notify_salary_change(new_salary, new_salary + 5000)
    
    # Статистика уведомлений
    print(f"Всего уведомлений в системе: {len(notification_system.get_notifications())}")
    print(f"Отправлено email: {len(email_notifier.get_sent_emails())}")
    print()
    
    return employee_subject, notification_system


def demonstrate_integration():
    """Демонстрация совместного использования паттернов."""
    print("=" * 60)
    print("5. ИНТЕГРАЦИЯ ПАТТЕРНОВ")
    print("=" * 60)
    
    # Создаем сотрудника через Factory Method
    developer = EmployeeFactoryRegistry.create_employee(
        "developer",
        id=7,
        name="Интеграционный Разработчик",
        department="Разработка",
        base_salary=85000,
        tech_stack=["Python", "FastAPI"],
        seniority_level="middle"
    )
    
    # Подключаем Observer
    employee_subject = EmployeeSubject(developer)
    notification_system = NotificationSystem()
    employee_subject.attach(notification_system)
    
    # Используем Strategy для расчета бонуса
    calculator = BonusCalculator(PerformanceBonusStrategy())
    bonus = calculator.calculate(developer, performance_rating=1.8)
    
    print(f"Сотрудник создан: {developer.name}")
    print(f"Бонус рассчитан (Strategy): {bonus:.2f}")
    
    # Уведомляем об изменении
    old_salary = developer.calculate_salary()
    # В реальности здесь было бы изменение зарплаты
    employee_subject.notify_salary_change(old_salary, old_salary + bonus)
    
    print(f"Уведомления отправлены (Observer)")
    print(f"Всего уведомлений: {len(notification_system.get_notifications())}")
    print()


def main():
    """Главная функция для запуска всех демонстраций."""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНОВ ПРОЕКТИРОВАНИЯ")
    print("=" * 60 + "\n")
    
    # 1. Singleton
    db = demonstrate_singleton()
    
    # 2. Factory Method
    employees = demonstrate_factory_method()
    
    # 3. Strategy
    calculator = demonstrate_strategy()
    
    # 4. Observer
    employee_subject, notification_system = demonstrate_observer()
    
    # 5. Интеграция
    demonstrate_integration()
    
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)
    
    # Закрываем подключение к БД
    db.close_connection()
    print("\nПодключение к базе данных закрыто.")


if __name__ == "__main__":
    main()

