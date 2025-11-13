#!/usr/bin/env python3
"""
Запускатель всех тестов для Frame Framework
"""

import unittest
import sys
import os

def run_all_tests():
    """Запускает все тесты"""
    # Добавляем текущую директорию в путь
    sys.path.append(os.path.dirname(__file__))
    
    print("🧪 Запуск тестов Frame Framework...")
    print(f"Python path: {sys.path}\n")
    
    # Находим все тестовые файлы
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('unitests', pattern='test_*.py')
    
    # Запускаем тесты
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Возвращаем код успеха/ошибки
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    print(f"\n{'✅ Все тесты прошли успешно!' if exit_code == 0 else '❌ Обнаружены ошибки в тестах'}")
    sys.exit(exit_code)