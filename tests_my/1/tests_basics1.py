import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from frame import Frame, fVar, fGet, fExec, fOp, FramerError, exec_and_return, MathPlugin

class TestFrameCore(unittest.TestCase):
    
    def test_basic_frame_creation(self):
        """Тест создания базового фрейма"""
        with Frame() as f:
            self.assertIsNotNone(f)
            self.assertTrue(hasattr(f, 'framer'))
    
    def test_fvar_operations(self):
        """Тест операций с переменными"""
        with Frame() as f:
            # Создание переменных
            x = fVar('x', 10, framer=f())
            y = fVar('y', 20, framer=f())
            
            # Получение значений
            self.assertEqual(fGet('x', f()), 10)
            self.assertEqual(fGet('y', f()), 20)
    
    def test_arithmetic_operations(self):
        """Тест арифметических операций"""
        with Frame(safemode=False) as f:
            fVar('a', 15, framer=f())
            fVar('b', 25, framer=f())
            fVar('result', 'a + b', with_eval=True, framer=f())
            
            result = exec_and_return(f.compile(), 'result', locals(), globals())
            self.assertEqual(result, 40)
    
    def test_condition_blocks(self):
        """Тест условных блоков"""
        with Frame(safemode=False) as f:
            fVar('x', 10, framer=f())
            fVar('y', 20, framer=f())
            
            fOp.match('x > y', 'result = "x bigger"', 'result = "y bigger"', framer=f())
            fVar('result', 'result', with_eval=True, framer=f())
            
            self.assertEqual(exec_and_return(f.compile(), 'result', locals(), globals()), "y bigger")
    
    def test_frame_serialization(self):
        """Тест сериализации фрейма"""
        import tempfile
        import json
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            # Сохраняем фрейм
            with Frame(safemode=False) as frame:
                frame.Var('test_data', 42)
                frame.save(filename, format='json')
            
            # Загружаем фрейм
            with Frame().load(filename, format='json') as loaded_frame:
                self.assertEqual(loaded_frame.Get('test_data'), 42)
                
        finally:
            os.unlink(filename)
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        with Frame() as f:
            # Попытка использовать несуществующую переменную
            fVar('invalid', 'undefined_fvar', with_eval=True, framer=f())

class TestMathPlugin(unittest.TestCase):
    
    def test_plugin_initialization(self):
        """Тест инициализации плагина"""
        frame = Frame(safemode=False)
        plugin = MathPlugin(frame)
        
        self.assertEqual(plugin.work(), 'mathplugin <v0.1.1>')
        self.assertFalse(plugin._state['included'])
    
    def test_plugin_inclusion(self):
        """Тест включения плагина"""
        frame = Frame(safemode=False)
        plugin = MathPlugin(frame)
        plugin.include()
        
        self.assertTrue(plugin._state['included'])
        # Проверяем, что зависимости добавлены в код
        code = frame.compile()
        self.assertIn('import math, cmath', code)
    
    def test_math_operations(self):
        """Тест математических операций"""
        frame = Frame(safemode=False)
        plugin = MathPlugin(frame).include()
        
        # Тест параболы
        plugin.parabola(5, 'result')
        self.assertEqual(exec_and_return(frame.compile(), 'result', locals(), globals()), 25)
        
        # Тест квадратного корня
        plugin.sqrt(16, 'sqrt_result')
        self.assertEqual(exec_and_return(frame.compile(), 'sqrt_result', locals(), globals()), 4.0)
    
    def test_complex_math(self):
        """Тест сложных математических функций"""
        frame = Frame(safemode=False)
        plugin = MathPlugin(frame).include()
        
        # Тест дискриминанта
        plugin.discriminant(1, -3, 2, 'disc_result')
        result = exec_and_return(frame.compile(), 'disc_result', locals(), globals())
        self.assertEqual(result[2], 1)  # Дискриминант должен быть 1
    
    def test_sigmoid_function(self):
        """Тест функции сигмоиды"""
        frame = Frame(safemode=False)
        plugin = MathPlugin(frame).include()
        
        plugin.sigmoid(0, 'sigmoid_result')
        result = exec_and_return(frame.compile(), 'sigmoid_result', locals(), globals())
        self.assertAlmostEqual(result, 0.5, places=5)



if __name__ == '__main__':
    unittest.main()