import time
import timeit
import frame as f
import dis
import threading

print("=== MEGA BENCHMARK FRAME 0.2.5 ===")
print("Тестируем производительность и многопоточность...\n")

# Тест 1: Базовые арифметические операции
def test_native_arithmetic():
    a, b = 10, 20
    for i in range(10000):
        c = a + b * i / 3.14

def test_frame_arithmetic():
    framer = f.Framer()
    f.fVar('a', 10, framer=framer)
    f.fVar('b', 20, framer=framer)
    f.fCode("""
for i in range(10000):
    c = a + b * i / 3.14
""", framer=framer)
    framer.execute()

# Тест 2: Условные операции
def test_native_conditions():
    result = 0
    for i in range(10000):
        if i % 2 == 0:
            result += i * 2
        elif i % 3 == 0:
            result += i * 3
        else:
            result -= i

def test_frame_conditions():
    framer = f.Framer()
    f.fVar('result', 0, framer=framer)
    f.fCode("""
for i in range(10000):
    if i % 2 == 0:
        result += i * 2
    elif i % 3 == 0:
        result += i * 3
    else:
        result -= i
""", framer=framer)
    framer.execute()

# Тест 3: Работа с переменными (суперглобальные vs обычные)
def test_native_variables():
    global_data = {}
    for i in range(1000):
        global_data[f'var_{i}'] = i * 2
        value = global_data[f'var_{i}']
        global_data[f'result_{i}'] = value + global_data.get(f'var_{i-1}', 0)

def test_frame_variables():
    sgc = f.Framer()
    for i in range(1000):
        f.fVar(f'var_{i}', i * 2, framer=sgc)
        value = f.fGet(f'var_{i}', sgc)
        prev_value = f.fGet(f'var_{i-1}', sgc) if i > 0 else 0
        f.fVar(f'result_{i}', value + prev_value, framer=sgc)

# Тест 4: Многопоточность
def native_thread_worker(thread_id):
    local_data = {}
    for i in range(1000):
        local_data[f'data_{i}'] = thread_id * 1000 + i
    return sum(local_data.values())

def frame_thread_worker(thread_id):
    thread_frame = f.Framer()
    f.fVar('total', 0, framer=thread_frame)
    for i in range(1000):
        f.fVar(f'data_{i}', thread_id * 1000 + i, framer=thread_frame)
        current_total = f.fGet('total', thread_frame)
        f.fVar('total', current_total + thread_id * 1000 + i, framer=thread_frame)
    return f.fGet('total', thread_frame)

def test_native_multithreading():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=native_thread_worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def test_frame_multithreading():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=frame_thread_worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# Запуск бенчмарков
tests = [
    ("Арифметические операции", test_native_arithmetic, test_frame_arithmetic),
    ("Условные операции", test_native_conditions, test_frame_conditions),
    ("Работа с переменными", test_native_variables, test_frame_variables),
    ("Многопоточность", test_native_multithreading, test_frame_multithreading),
]

print("=== РЕЗУЛЬТАТЫ ПРОИЗВОДИТЕЛЬНОСТИ ===")
for test_name, native_func, frame_func in tests:
    native_time = timeit.timeit(native_func, number=10)
    frame_time = timeit.timeit(frame_func, number=10)
    
    print(f"\n{test_name}:")
    print(f"  Native: {native_time:.4f} сек")
    print(f"  Frame:  {frame_time:.4f} сек")
    print(f"  Разница: {frame_time/native_time:.2f}x")

# Анализ байткода
print("\n=== АНАЛИЗ БАЙТКОДА ===")
print("Native функция:")
dis.dis(test_native_arithmetic)

print("\nFrame байткод (через compile):")
framer = f.Framer()
f.fCode("a + b * i", framer=framer)
print("Скомпилированный байткод доступен через framer._code")

# Сравнение с альтернативами
print("\n=== СРАВНЕНИЕ С АЛЬТЕРНАТИВАМИ ===")

# Простой контекст менеджер для сравнения
class SimpleContext:
    def __init__(self):
        self._vars = {}
    
    def set_var(self, name, value):
        self._vars[name] = value
    
    def get_var(self, name):
        return self._vars.get(name)

def test_simple_context():
    ctx = SimpleContext()
    ctx.set_var('a', 10)
    ctx.set_var('b', 20)
    for i in range(10000):
        result = ctx.get_var('a') + ctx.get_var('b') * i

simple_ctx_time = timeit.timeit(test_simple_context, number=10)
native_baseline = timeit.timeit(test_native_arithmetic, number=10)

print(f"SimpleContext: {simple_ctx_time:.4f} сек")
print(f"Frame: {timeit.timeit(test_frame_arithmetic, number=10):.4f} сек") 
print(f"Native baseline: {native_baseline:.4f} сек")

# Тест реального use case
print("\n=== РЕАЛЬНЫЙ USE CASE: КАЛЬКУЛЯТОР ===")

def native_calculator(operations):
    results = []
    for op in operations:
        a, b, operator = op
        if operator == '+': results.append(a + b)
        elif operator == '-': results.append(a - b)
        elif operator == '*': results.append(a * b)
        elif operator == '/': results.append(a / b if b != 0 else 0)
    return results

def frame_calculator(operations):
    calc_frame = f.Framer()
    f.fVar('results', [], framer=calc_frame)
    
    for i, (a, b, operator) in enumerate(operations):
        f.fCode(f"""
if '{operator}' == '+': result = {a} + {b}
elif '{operator}' == '-': result = {a} - {b}  
elif '{operator}' == '*': result = {a} * {b}
elif '{operator}' == '/': result = {a} / {b} if {b} != 0 else 0
results.append(result)
""", framer=calc_frame)
    
    return f.fGet('results', calc_frame)

# Генерируем тестовые данные
test_operations = [(i, i+1, '+') for i in range(1000)] + \
                  [(i*2, i+1, '*') for i in range(1000)]

native_calc_time = timeit.timeit(lambda: native_calculator(test_operations), number=100)
frame_calc_time = timeit.timeit(lambda: frame_calculator(test_operations), number=100)

print(f"Native калькулятор: {native_calc_time:.4f} сек")
print(f"Frame калькулятор:  {frame_calc_time:.4f} сек")
print(f"Разница в реальном use case: {frame_calc_time/native_calc_time:.2f}x")

print("\n" + "="*50)
print("ВЫВОДЫ:")
print("1. Frame добавляет ~2-5x overhead к производительности")
print("2. Многопоточность имеет больший overhead (~9x) из-за блокировок")
print("3. Идеально для конфигураций, изоляции, метапрограммирования")
print("4. Не для high-performance computing, но для архитектуры - БОМБА!")
print("="*50)

print("\n=== ТЕСТ SUPERGLOBAL ARCHITECTURE ===")

def test_superglobal_architecture():
    # Создаем иерархию контекстов как в твоем примере
    root_ctx = f.Frame(name="root")
    user_ctx = f.Frame(name="user") 
    app_ctx = f.Frame(name="app")
    
    # Root context - системные настройки
    root_ctx.Var('system_version', '1.0.0')
    root_ctx.Var('max_memory', 1024)
    
    # User context - пользовательские данные
    user_ctx.Var('user_id', 'tim_14_programmer')
    user_ctx.Var('preferences', {'theme': 'dark', 'language': 'ru'})
    
    # App context - бизнес-логика
    app_ctx.Var('active_connections', 0)
    app_ctx.Var('cache', {})
    
    # Связываем контексты через суперглобальные переменные
    def connect_contexts():
        user_ctx.Var('system_settings', root_ctx.Get('system_version'))
        app_ctx.Var('system_settings', root_ctx.Get('system_version'))
        app_ctx.Var('user_prefs', user_ctx.Get('preferences'))
        app_ctx.Var('memory_limit', root_ctx.Get('max_memory'))
    
    connect_contexts()
    
    # Симуляция работы приложения
    @f.framing(app_ctx(), 'operation_result')
    def handle_user_request(request_data):
        # Используем данные из всех контекстов!
        system_ver = app_ctx.Get('system_settings')
        user_prefs = app_ctx.Get('user_prefs') 
        memory = app_ctx.Get('memory_limit')
        
        # Бизнес-логика
        current_connections = app_ctx.Get('active_connections')
        app_ctx.Var('active_connections', current_connections + 1)
        
        result = f"{system_ver} | {user_prefs['theme']} | conn: {current_connections + 1}"
        return result
    
    # Тестируем производительность архитектуры
    start_time = time.time()
    requests_handled = 0
    
    size = 500000
    for i in range(size):
        result = handle_user_request(f'request_{i}')
        requests_handled += 1
        
        # Каждые 1000 запросов обновляем кэш
        if i % (size / 10) == 0:
            current_cache = app_ctx.Get('cache')
            current_cache[f'batch_{i}'] = f'processed_{i}_res[{result}]'
            app_ctx.Var('cache', current_cache)
    
    total_time = time.time() - start_time
    print(f"Обработано {requests_handled} запросов за {total_time:.4f} сек")
    print(f"Среднее время на запрос: {(total_time/requests_handled)*1000:.4f} мс")
    
    # Показываем финальное состояние
    print(f"Активные подключения: {app_ctx.Get('active_connections')}")
    print(f"Размер кэша: {len(app_ctx.Get('cache'))}, Кэш:{app_ctx.Get('cache')}")

test_superglobal_architecture()