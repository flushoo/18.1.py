import threading
import random


class Counter:
    """Класс для управления общим счётчиком с использованием блокировки."""
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self, amount):
        """Увеличивает счётчик на заданное число с использованием блокировки."""
        with self.lock:
            self.value += amount


def worker(counter, increments):
    """Функция потока, которая увеличивает счётчик."""
    for _ in range(increments):
        random_increment = random.randint(1, 10)
        counter.increment(random_increment)


def main():
    total_threads = 5        # Количество потоков
    increments_per_thread = 100  # Количество увеличений на поток

    counter = Counter()  # Общий счётчик

    # Создание и запуск потоков
    threads = []
    for _ in range(total_threads):
        thread = threading.Thread(target=worker, args=(counter, increments_per_thread))
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    print(f"Итоговое значение счётчика: {counter.value}")


if __name__ == "__main__":
    main()