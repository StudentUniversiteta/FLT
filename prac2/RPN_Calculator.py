def calculate_rpn(rpn_expression):
    stack = []

    for token in rpn_expression.split():
        if token.isdigit():
            stack.append(int(token))  # в стек добавляется токен в виде целого числа
        else:
            operand2 = stack.pop()  # Извлекаем два последних операнда из стека
            operand1 = stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            else:
                raise ValueError("Неподдерживаемая операция: " + token)
            stack.append(result)
    return stack.pop()

rpn_expression = input("Введите выражение в обратной польской записи: ")
result = calculate_rpn(rpn_expression)
print("Результат вычислений: ", result)