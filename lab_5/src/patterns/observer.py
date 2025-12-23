"""Паттерн Observer для системы уведомлений."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.abstract_employee import AbstractEmployee


class Observer(ABC):
    """
    Абстрактный наблюдатель.
    
    Определяет интерфейс для объектов, которые должны быть уведомлены
    об изменениях в субъекте.
    """
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Получить уведомление об изменении.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        pass


class Subject(ABC):
    """
    Абстрактный субъект.
    
    Определяет интерфейс для объектов, за которыми наблюдают.
    """
    
    def __init__(self):
        """Инициализация субъекта."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Подписать наблюдателя на уведомления.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """
        Отписать наблюдателя от уведомлений.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Уведомить всех наблюдателей об изменении.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        for observer in self._observers:
            observer.update(event_type, data)


class NotificationSystem(Observer):
    """
    Система уведомлений.
    
    Конкретная реализация наблюдателя для отправки уведомлений
    об изменениях в системе.
    """
    
    def __init__(self):
        """Инициализация системы уведомлений."""
        self._notifications: List[Dict[str, Any]] = []
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Обработать уведомление об изменении.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        notification = {
            "event_type": event_type,
            "data": data,
            "timestamp": self._get_timestamp()
        }
        self._notifications.append(notification)
        self._print_notification(notification)
    
    def _get_timestamp(self) -> str:
        """Получить текущую временную метку."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _print_notification(self, notification: Dict[str, Any]) -> None:
        """
        Вывести уведомление в консоль.
        
        Args:
            notification: Данные уведомления
        """
        event_type = notification["event_type"]
        data = notification["data"]
        timestamp = notification["timestamp"]
        
        print(f"[{timestamp}] Уведомление: {event_type}")
        if "employee_id" in data:
            print(f"  Сотрудник ID: {data['employee_id']}")
        if "employee_name" in data:
            print(f"  Имя: {data['employee_name']}")
        if "old_value" in data and "new_value" in data:
            print(f"  Изменение: {data['old_value']} -> {data['new_value']}")
        if "message" in data:
            print(f"  Сообщение: {data['message']}")
        print()
    
    def get_notifications(self) -> List[Dict[str, Any]]:
        """
        Получить все уведомления.
        
        Returns:
            Список всех уведомлений
        """
        return self._notifications.copy()
    
    def clear_notifications(self) -> None:
        """Очистить все уведомления."""
        self._notifications.clear()
    
    def get_notifications_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """
        Получить уведомления определенного типа.
        
        Args:
            event_type: Тип события
        
        Returns:
            Список уведомлений указанного типа
        """
        return [n for n in self._notifications if n["event_type"] == event_type]


class EmployeeSubject(Subject):
    """
    Субъект для сотрудников.
    
    Расширяет базовый класс Subject для работы с сотрудниками,
    уведомляя наблюдателей об изменениях зарплаты и других параметров.
    """
    
    def __init__(self, employee: 'AbstractEmployee'):
        """
        Инициализация субъекта сотрудника.
        
        Args:
            employee: Объект сотрудника
        """
        super().__init__()
        self._employee = employee
    
    def notify_salary_change(self, old_salary: float, new_salary: float) -> None:
        """
        Уведомить об изменении зарплаты.
        
        Args:
            old_salary: Старая зарплата
            new_salary: Новая зарплата
        """
        self.notify("salary_changed", {
            "employee_id": self._employee.id,
            "employee_name": self._employee.name,
            "old_value": old_salary,
            "new_value": new_salary,
            "message": f"Зарплата сотрудника {self._employee.name} изменена"
        })
    
    def notify_department_change(self, old_department: str, new_department: str) -> None:
        """
        Уведомить об изменении отдела.
        
        Args:
            old_department: Старый отдел
            new_department: Новый отдел
        """
        self.notify("department_changed", {
            "employee_id": self._employee.id,
            "employee_name": self._employee.name,
            "old_value": old_department,
            "new_value": new_department,
            "message": f"Сотрудник {self._employee.name} переведен в отдел {new_department}"
        })
    
    def notify_status_change(self, status: str) -> None:
        """
        Уведомить об изменении статуса.
        
        Args:
            status: Новый статус
        """
        self.notify("status_changed", {
            "employee_id": self._employee.id,
            "employee_name": self._employee.name,
            "new_value": status,
            "message": f"Статус сотрудника {self._employee.name} изменен на {status}"
        })


class EmailNotifier(Observer):
    """
    Наблюдатель для отправки email-уведомлений.
    
    Пример конкретной реализации наблюдателя.
    """
    
    def __init__(self, email: str):
        """
        Инициализация email-уведомителя.
        
        Args:
            email: Email адрес для отправки
        """
        self._email = email
        self._sent_emails: List[Dict[str, Any]] = []
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Отправить email-уведомление.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        # В реальном приложении здесь была бы отправка email
        email_data = {
            "to": self._email,
            "subject": f"Уведомление: {event_type}",
            "body": f"Событие: {event_type}\nДанные: {data}",
            "event_type": event_type
        }
        self._sent_emails.append(email_data)
        print(f"[Email] Отправлено на {self._email}: {event_type}")
    
    def get_sent_emails(self) -> List[Dict[str, Any]]:
        """
        Получить список отправленных email.
        
        Returns:
            Список отправленных email
        """
        return self._sent_emails.copy()

