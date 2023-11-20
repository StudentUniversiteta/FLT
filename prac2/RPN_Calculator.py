def calculate_rpn(rpn_expression):
    stack = []  # Стек для операндов

    for token in rpn_expression.split():
        if token.isdigit():  # Если токен является числом
            stack.append(int(token))  # Преобразуем токен в целое число и добавляем его в стек
        else:  # Если токен является оператором
            operand2 = stack.pop()  # Извлекаем два последних операнда из стека
            operand1 = stack.pop()

            if token == '+':
                result = operand1 + operand2  # Выполняем операцию сложения
            elif token == '-':
                result = operand1 - operand2  # Выполняем операцию вычитания
            elif token == '*':
                result = operand1 * operand2  # Выполняем операцию умножения
            elif token == '/':
                result = operand1 / operand2  # Выполняем операцию деления
            else:
                raise ValueError("Неподдерживаемая операция: " + token)

            stack.append(result)  # Результат операции добавляем в стек

    return stack.pop()  # Возвращаем окончательный результат


# Пример использования
rpn_expression = input("Введите выражение в обратной польской записи: ")
result = calculate_rpn(rpn_expression)
print("Результат вычислений: ", result)