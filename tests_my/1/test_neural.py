import frame.frame_core as frame_core
import math
import random

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Создаем Frame для хранения параметров сети
        self.ctx = frame_core.Frame(name='neural_network', safemode=False)
        
        # Инициализируем веса случайными значениями
        with self.ctx:
            # Веса от входного к скрытому слою
            self.ctx.Var('W1', [[random.uniform(-1, 1) for _ in range(input_size)] 
                               for _ in range(hidden_size)])
            self.ctx.Var('b1', [0.0] * hidden_size)
            
            # Веса от скрытого к выходному слою
            self.ctx.Var('W2', [[random.uniform(-1, 1) for _ in range(hidden_size)] 
                               for _ in range(output_size)])
            self.ctx.Var('b2', [0.0] * output_size)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, inputs):
        """Прямое распространение"""
        with self.ctx:
            W1 = self.ctx.Get('W1')
            b1 = self.ctx.Get('b1')
            W2 = self.ctx.Get('W2')
            b2 = self.ctx.Get('b2')
            
            # Скрытый слой
            hidden_inputs = [sum(w * i for w, i in zip(weights, inputs)) + bias 
                           for weights, bias in zip(W1, b1)]
            hidden_outputs = [self.sigmoid(x) for x in hidden_inputs]
            
            # Выходной слой
            final_inputs = [sum(w * h for w, h in zip(weights, hidden_outputs)) + bias 
                          for weights, bias in zip(W2, b2)]
            final_outputs = [self.sigmoid(x) for x in final_inputs]
            
            return hidden_outputs, final_outputs

    def train(self, training_inputs, training_outputs):
        """Обучение на одном примере"""
        with self.ctx:
            # Прямое распространение
            hidden_outputs, final_outputs = self.forward(training_inputs)
            
            W1 = self.ctx.Get('W1')
            W2 = self.ctx.Get('W2')
            
            # Ошибка выходного слоя
            output_errors = [target - output for target, output in zip(training_outputs, final_outputs)]
            
            # Градиенты выходного слоя
            output_gradients = [error * self.sigmoid_derivative(output) 
                              for error, output in zip(output_errors, final_outputs)]
            
            # Ошибка скрытого слоя
            hidden_errors = [sum(W2[j][i] * output_gradients[j] for j in range(self.output_size))
                           for i in range(self.hidden_size)]
            
            # Градиенты скрытого слоя
            hidden_gradients = [error * self.sigmoid_derivative(hidden_output) 
                              for error, hidden_output in zip(hidden_errors, hidden_outputs)]
            
            # Обновление весов выходного слоя
            new_W2 = []
            for i in range(self.output_size):
                new_weights = []
                for j in range(self.hidden_size):
                    new_weights.append(W2[i][j] + self.learning_rate * output_gradients[i] * hidden_outputs[j])
                new_W2.append(new_weights)
            
            new_b2 = [b + self.learning_rate * g for b, g in zip(self.ctx.Get('b2'), output_gradients)]
            
            # Обновление весов скрытого слоя
            new_W1 = []
            for i in range(self.hidden_size):
                new_weights = []
                for j in range(self.input_size):
                    new_weights.append(W1[i][j] + self.learning_rate * hidden_gradients[i] * training_inputs[j])
                new_W1.append(new_weights)
            
            new_b1 = [b + self.learning_rate * g for b, g in zip(self.ctx.Get('b1'), hidden_gradients)]
            
            # Сохраняем обновленные веса
            self.ctx.Var('W1', new_W1)
            self.ctx.Var('b1', new_b1)
            self.ctx.Var('W2', new_W2)
            self.ctx.Var('b2', new_b2)

    def predict(self, inputs):
        """Предсказание"""
        _, outputs = self.forward(inputs)
        return outputs

    def save(self, filename):
        """Сохранение модели"""
        self.ctx.save(filename, format='pickle')

    def load(self, filename):
        """Загрузка модели"""
        self.ctx.load(filename, format='pickle')

# Пример использования
if __name__ == "__main__":
    # Создаем нейросеть для решения XOR
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)
    
    # Данные для обучения (XOR)
    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]
    
    # Обучение
    print("Обучение сети...")
    for epoch in range(10000):
        for inputs, targets in training_data:
            nn.train(inputs, targets)
        
        if epoch % 1000 == 0:
            error = 0
            for inputs, targets in training_data:
                prediction = nn.predict(inputs)
                error += (targets[0] - prediction[0]) ** 2
            print(f"Эпоха {epoch}, Ошибка: {error/4:.4f}")
    
    # Тестирование
    print("\nТестирование:")
    for inputs, targets in training_data:
        prediction = nn.predict(inputs)
        print(f"Вход: {inputs}, Ожидалось: {targets[0]}, Получено: {prediction[0]:.4f}")
    
    # Сохранение модели
    nn.save("neural_network_model.pkl")
    print("\nМодель сохранена в 'neural_network_model.pkl'")
    
    # Загрузка модели (пример)
    # new_nn = SimpleNeuralNetwork(2, 4, 1)
    # new_nn.load("neural_network_model.pkl")