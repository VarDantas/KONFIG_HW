"""Модуль трансформации AST (дерева разбора) и вычисления."""
import math
from lark import Transformer


class ConfigTransformer(Transformer):
    """Преобразователь дерева разбора в словарь конфигурации."""

    def __init__(self):
        """Инициализация окружения констант."""
        super().__init__()
        self.env = {}
        self.MIN_ADD_ARGS = 2
        self.SQRT_ARGS = 1

    def start(self, items):
        """Возвращает итоговый словарь конфигурации."""
        return self.env

    def var_decl(self, items):
        """Объявление константы на этапе трансляции."""
        name = str(items[0])
        value = items[1]
        self.env[name] = value
        return name, value

    def number(self, items):
        """Преобразование числа в тип float."""
        return float(items[0])

    def var_ref(self, items):
        """Обращение к ранее объявленной константе."""
        name = str(items[0])
        if name not in self.env:
            raise ValueError(f"Неизвестная константа: {name}")
        return self.env[name]

    def array(self, items):
        """Формирование массива из значений."""
        return list(items)

    def eval_expr(self, items):
        """Вычисление префиксного выражения (например: .{+ имя 1.0}.)."""
        op = str(items[0])
        args = items[1:]

        if op == "+":
            if len(args) < self.MIN_ADD_ARGS:
                raise ValueError("Для сложения нужно минимум 2 аргумента")
            return sum(args)

        if op == "sqrt":
            if len(args) != self.SQRT_ARGS:
                raise ValueError("Функция sqrt принимает ровно 1 аргумент")
            return math.sqrt(args[0])

        raise ValueError(f"Неизвестная операция: {op}")
