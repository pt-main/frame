import inspect
import functools

def code_snapshot(construct):
    """
    Декоратор, который получает код конструкции и заменяет её на функцию,
    выводящую код и кидающую ошибку при вызове.
    """
    def wrapper(*args, **kwargs):
        # Получаем исходный код конструкции
        try:
            source_code = inspect.getsource(construct)
            print(f"Код конструкции '{construct.__name__}':")
            print("=" * 50)
            print(source_code)
            print("=" * 50)
        except (OSError, TypeError) as e:
            print(f"Не удалось получить исходный код: {e}")
        
        # Создаем функцию, которая кидает ошибку при вызове
        @functools.wraps(construct)
        def error_function(*args, **kwargs):
            raise RuntimeError(f"Конструкция '{construct.__name__}' не может быть вызвана. Используется только для демонстрации кода.")
        
        return error_function
    
    return wrapper

# Пример использования:

@code_snapshot
class MyClass:
    def __init__(self, x):
        self.x = x
    
    def method(self):
        return f"Value: {self.x}"
    
    def another_method(self, y):
        return self.x + y

@code_snapshot
def my_function(x, y=10):
    """Простая функция для демонстрации"""
    result = x + y
    return result * 2

# Более сложная версия с дополнительными параметрами:

def code_snapshot_advanced(show_code=True, custom_message=None):
    def decorator(construct):
        def wrapper(*args, **kwargs):
            if show_code:
                try:
                    source_code = inspect.getsource(construct)
                    print(source_code)
                except (OSError, TypeError) as e:
                    print(f"Cant get source code: {e}")
            @functools.wraps(construct)
            def error_function(*args, **kwargs):
                message = custom_message or f"Construction '{construct.__name__}' is not callable. Function imported to frame."
                raise RuntimeError(message)
            return error_function
        return wrapper
    return decorator




def import_construction(custom_message=None):
    def decorator(construct):
        def wrapper(*args, **kwargs):
            try:
                source_code = inspect.getsource(construct)
                print(source_code)
            except (OSError, TypeError) as e:
                print(f"Cant get source code: {e}")
            return func
        return wrapper
    return decorator



# Пример использования улучшенной версии:

@import_construction()
class AdvancedClass:
    def __init__(self, name):
        self.name = name
    
    @property
    def display_name(self):
        return f"Name: {self.name.upper()}"
    
    @classmethod
    def from_dict(cls, data):
        return cls(data.get('name', 'default'))

# Тестирование:

if __name__ == "__main__":
    print("=== Демонстрация работы декоратора ===\n")
    
    # При попытке использовать класс - получим код и ошибку
    try:
        obj = MyClass(5)  # Выведет код класса
        obj.method()      # Вызовет ошибку
    except Exception as e:
        print(f"Ошибка: {e}\n")
    
    # При попытке использовать функцию
    try:
        func = my_function  # Выведет код функции
        result = func(3, 4)  # Вызовет ошибку
    except RuntimeError as e:
        print(f"Ошибка: {e}\n")
    
    # Демонстрация улучшенной версии
    try:
        advanced_obj = AdvancedClass("test")
    except RuntimeError as e:
        print(f"Ошибка улучшенной версии: {e}")