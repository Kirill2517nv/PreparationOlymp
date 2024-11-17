import subprocess
import os
from termcolor import colored
import colorama

# Инициализируем colorama для корректного отображения цветов в Windows
colorama.init(autoreset=True)


# Функция для чтения и проверки ответа
def read_and_check_answer(n, k, line, input_data):
    lines = input_data.strip().split("\n")
    m = int(lines[0].strip())

    if m == -1:
        return -1

    if m < 2:
        raise ValueError(f"Length of the sequence must be at least 2, but {m} found")

    inds = list(map(int, lines[1].strip().split()))
    if len(inds) != m:
        raise ValueError("Number of indices doesn't match m")

    have_break = False
    for i in range(1, m):
        if not (line[inds[i - 1] - 1][1] <= line[inds[i] - 1][0]):
            raise ValueError(
                f"{i + 1}-th game starts before the end of {i}-th: "
                f"{line[inds[i - 1] - 1][1]} >= {line[inds[i] - 1][0]}"
            )
        have_break |= line[inds[i - 1] - 1][1] + k <= line[inds[i] - 1][0]

    if not have_break:
        raise ValueError("No long enough break found")

    return m


# Функция для тестирования одного файла
def run_test(input_file: str, expected_output_file: str):
    input_file = os.path.normpath(input_file)
    expected_output_file = os.path.normpath(expected_output_file)

    # Чтение входных данных
    with open(input_file, 'r') as f_in:
        n = int(f_in.readline().strip())
        k = int(f_in.readline().strip())
        line = [tuple(map(int, f_in.readline().strip().split())) for _ in range(n)]

    # Чтение ожидаемого результата
    with open(expected_output_file, 'r') as f_out:
        expected_output = f_out.read().strip()

    # Запуск task5.py и получение вывода
    result = subprocess.run(
        ['python', 'task5.py'],  # Команда для запуска вашего скрипта
        input=f"{n}\n {k}\n" + "\n".join(f"{a} {b}" for a, b in line),
        text=True,
        capture_output=True
    )

    # Получаем результат программы
    program_output = result.stdout.strip()

    # Чтение и проверка ответа
    try:
        j_ans = read_and_check_answer(n, k, line, expected_output)
        p_ans = read_and_check_answer(n, k, line, program_output)
    except ValueError as e:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored(f"Error: {e}", "yellow"))
        return False

    # Сравниваем результаты
    if j_ans == -1:
        if p_ans != -1:
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored("Participant found the sequence, but jury didn't", "yellow"))
            return False
        else:
            print(colored(f"Test {input_file} passed.", "green"))
            return True
    else:
        if p_ans == -1:
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored("Participant didn't find the sequence, but jury did", "yellow"))
            return False
        elif p_ans < j_ans:
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored(f"Participant's answer is worse than jury's, {p_ans} < {j_ans}", "yellow"))
            return False
        elif p_ans > j_ans:
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored(f"Participant's answer is better than jury's, {p_ans} > {j_ans}", "yellow"))
            return False
        else:
            print(colored(f"Test {input_file} passed.", "green"))
            return True


# Функция для запуска всех тестов
def run_all_tests():
    test_dir = './tests'
    test_cases = [f[:-2] for f in os.listdir(test_dir) if f.endswith('.a')]

    total_tests = len(test_cases)
    passed_tests = 0

    for test_case in test_cases:
        input_file = os.path.join(test_dir, test_case)
        expected_output_file = os.path.join(test_dir, test_case + '.a')

        if run_test(input_file, expected_output_file):
            passed_tests += 1

    print("\n" + "-" * 40)
    print(f"Total tests: {total_tests}")
    print(colored(f"Passed tests: {passed_tests}", "green"))
    print(colored(f"Failed tests: {total_tests - passed_tests}", "red"))
    if passed_tests == total_tests:
        print(colored("All tests passed!", "green", attrs=["bold"]))
    else:
        print(colored("Some tests failed.", "red", attrs=["bold"]))


if __name__ == "__main__":
    run_all_tests()
