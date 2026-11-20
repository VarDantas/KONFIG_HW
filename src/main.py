"""Инструмент командной строки для учебного конфигурационного языка."""
import sys
import argparse
import yaml
from lark import Lark
from lark.exceptions import UnexpectedInput, VisitError
from src.transformer import ConfigTransformer


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Транслятор конфигурационного языка в YAML"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Путь к выходному YAML файлу"
    )
    return parser.parse_args()


def load_grammar():
    """Загрузка грамматики из файла."""
    with open("src/grammar.lark", "r", encoding="utf-8") as file:
        return file.read()


def main():
    """Основная логика программы."""
    args = parse_args()
    grammar = load_grammar()

    parser = Lark(grammar, parser="lalr")

    input_text = sys.stdin.read()
    if not input_text.strip():
        print("Ошибка: Входной текст пуст.", file=sys.stderr)
        sys.exit(1)

    try:
        tree = parser.parse(input_text)
        transformer = ConfigTransformer()
        result_dict = transformer.transform(tree)

        with open(args.output, "w", encoding="utf-8") as out_file:
            yaml.dump(result_dict, out_file, default_flow_style=False)

    except UnexpectedInput as error:
        print(f"Синтаксическая ошибка:\n{error}", file=sys.stderr)
        sys.exit(1)
    except VisitError as error:
        print(f"Ошибка вычисления: {error.orig_exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as error:
        print(f"Ошибка вычисления: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
