def infix_to_rpn(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}  # Определение приоритета операций
    stack = []  # Стек (для операторов)
    rpn = []  # Обратная польская запись
    number = ''  # Строка для сохранения чисел

    for char in expression:
        if char.isalnum():  # Если символ является буквой или цифрой
            number += char  # Добавляем его к текущему числу
        else:
            if number:  # Если строка числа не пуста, добавляем число в обратную польскую запись
                rpn.append(number)
                number = ''  # Сбрасываем строку числа

            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[
                    -1] != '(':  # Пока стек не пуст и последний символ в стеке не является открывающей скобкой
                    rpn.append(stack.pop())  # Удаляем символ из стека и добавляем его в обратную польскую запись
                stack.pop()  # Удаляем открывающую скобку из стека
            elif char in precedence:
                while stack and stack[-1] != '(' and precedence[char] <= precedence[stack[-1]]:
                    # Пока стек не пуст, последний символ в стека не является открывающей скобкой и приоритет текущего оператора
                    # меньше или равен приоритету последнего символа в стеке
                    rpn.append(stack.pop())
                stack.append(char)

    if number:
        rpn.append(number)

    while stack:  # Пока стек не пуст
        rpn.append(stack.pop())

    return ' '.join(rpn)  # Возвращаем обратную польскую запись


# Пример использования
infix_expression = input("Введите алгебраическое выражение: ")
rpn_expression = infix_to_rpn(infix_expression)
print("Обратная польская запись: ", rpn_expression)