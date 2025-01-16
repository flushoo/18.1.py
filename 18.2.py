import multiprocessing
import random


def generate_random_numbers(count):
    """Генерация списка случайных чисел."""
    return [random.randint(1, 100) for _ in range(count)]


def compute_sum_of_squares(numbers, queue):
    """Функция для вычисления суммы квадратов чисел и передачи результата в очередь."""
    result = sum(x ** 2 for x in numbers)
    queue.put(result)


def main():
    num_elements = 10_000_000  # Количество чисел
    num_processes = multiprocessing.cpu_count()  # Количество процессов
    chunk_size = num_elements // num_processes  # Размер каждой части

    # Генерация списка случайных чисел
    random_numbers = generate_random_numbers(num_elements)

    # Разделение списка на части
    chunks = [random_numbers[i:i + chunk_size] for i in range(0, num_elements, chunk_size)]

    # Очередь для передачи результатов
    queue = multiprocessing.Queue()

    # Создание процессов
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=compute_sum_of_squares, args=(chunk, queue))
        processes.append(process)
        process.start()

    # Ожидание завершения всех процессов
    for process in processes:
        process.join()

    # Сбор результатов из очереди
    total_sum_of_squares = 0
    while not queue.empty():
        total_sum_of_squares += queue.get()

    print(f"Общая сумма квадратов: {total_sum_of_squares}")


if __name__ == "__main__":
    main()