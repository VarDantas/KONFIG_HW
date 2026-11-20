"""Интеграционные тесты для инструмента трансляции конфигураций."""
import subprocess
import yaml
import pytest


EXIT_SUCCESS = 0
EXIT_ERROR = 1


def run_tool(input_text, output_path):
    """Запускает инструмент командной строки с заданным вводом."""
    process = subprocess.run(
        ["python3", "-m", "src.main", "-o", str(output_path)],
        input=input_text,
        text=True,
        capture_output=True,
        check=False
    )
    return process


def test_game_physics(tmp_path):
    """Тест 1: Конфигурация физики игры (предметная область - игры)."""
    output_file = tmp_path / "out.yaml"
    input_text = (
        "var gravity = -9.8\n"
        "var mass = 5.0\n"
        "var force = .{+ gravity mass}.\n"
        "var speed = .{sqrt 16.0}.\n"
        "var hitbox = '(1.0 2.0 3.0)\n"
    )
    process = run_tool(input_text, output_file)
    
    assert process.returncode == EXIT_SUCCESS
    with open(output_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    
    assert data["gravity"] == -9.8
    assert data["mass"] == 5.0
    assert data["force"] == pytest.approx(-4.8)
    assert data["speed"] == 4.0
    assert data["hitbox"] == [1.0, 2.0, 3.0]


def test_ui_layout(tmp_path):
    """Тест 2: Параметры интерфейса (предметная область - UI)."""
    output_file = tmp_path / "out.yaml"
    input_text = (
        "var width = 1920.0\n"
        "var height = 1080.0\n"
        "var max_width = .{+ width 100.0}.\n"
        "var margins = '(10.0 20.0 10.0 20.0)\n"
    )
    process = run_tool(input_text, output_file)
    
    assert process.returncode == EXIT_SUCCESS
    with open(output_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    
    assert data["width"] == 1920.0
    assert data["height"] == 1080.0
    assert data["max_width"] == 2020.0
    assert data["margins"] == [10.0, 20.0, 10.0, 20.0]


def test_syntax_error(tmp_path):
    """Тест 3: Проверка выдачи сообщения при синтаксической ошибке."""
    output_file = tmp_path / "out.yaml"
    input_text = "var x = .{+ 1.0 2.0"
    
    process = run_tool(input_text, output_file)
    
    assert process.returncode == EXIT_ERROR
    assert "Синтаксическая ошибка" in process.stderr


def test_unknown_constant_error(tmp_path):
    """Тест 4: Проверка ошибки при обращении к неизвестной константе."""
    output_file = tmp_path / "out.yaml"
    input_text = "var x = .{+ y 1.0}.\n"
    
    process = run_tool(input_text, output_file)
    
    assert process.returncode == EXIT_ERROR
    assert "Ошибка вычисления" in process.stderr
