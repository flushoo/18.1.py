import asyncio
import aiohttp
import multiprocessing
import threading
import time
import random


def process_data(data_chunk):
    """Обработка данных: здесь выполняется сортировка."""
    return sorted(data_chunk)


def write_to_file(filename, data):
    """Функция записи данных в файл."""
    with open(filename, 'a') as f:
        for item in data:
            f.write(f"{item}\n")


def periodic_writer(filename, queue):
    """Фоновая запись данных из очереди в файл."""
    while True:
        if not queue.empty():
            data = queue.get()
            write_to_file(filename, data)
        time.sleep(1)  # Запись выполняется раз в секунду


async def fetch_data(session, url):
    """Асинхронная загрузка данных из API."""
    async with session.get(url) as response:
        return await response.json()


async def main():
    # URL для теста (замените на реальный API)
    url = "https://jsonplaceholder.typicode.com/posts"

    # Создаем сессию aiohttp
    async with aiohttp.ClientSession() as session:
        print("Загрузка данных...")
        data = await fetch_data(session, url)  # Загружаем данные

    print("Данные загружены. Обработка...")

    # Разделяем данные на части для multiprocessing
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(data) // num_processes
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Очередь для передачи данных между потоками
    result_queue = multiprocessing.Queue()

    # Создаем и запускаем процессы
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=lambda q, c: q.put(process_data(c)), args=(result_queue, chunk))
        processes.append(process)
        process.start()

    # Ожидание завершения процессов
    for process in processes:
        process.join()

    print("Обработка завершена. Сбор результатов...")

    # Сбор результатов из очереди
    processed_data = []
    while not result_queue.empty():
        processed_data.extend(result_queue.get())

    print("Сортировка данных завершена. Инициализация записи в файл...")

    # Запись данных в файл через поток
    filename = "results.txt"
    writer_thread = threading.Thread(target=periodic_writer, args=(filename, result_queue), daemon=True)
    writer_thread.start()

    # Добавляем обработанные данные в очередь для записи
    for chunk in chunks:
        result_queue.put(chunk)

    # Ожидание записи данных
    time.sleep(3)  # Даем время на запись данных
    print(f"Данные записаны в файл: {filename}")


if __name__ == "__main__":
    asyncio.run(main())