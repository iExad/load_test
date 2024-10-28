FROM python:3.9-slim
RUN pip install psutil
COPY load_test.py /app/load_test.py
WORKDIR /app
CMD ["python", "load_test.py"]
root@prometheusgrafana:~# cat load_test.py
import os
import time
import random
import multiprocessing
import psutil

def cpu_load(duration):
    """Генерация нагрузки на процессор."""
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = sum([i ** 2 for i in range(10000)])  # Пример нагрузки на CPU

def memory_load(duration, memory_limit_mb):
    """Генерация нагрузки на память."""
    memory_usage = []
    end_time = time.time() + duration
    while time.time() < end_time:
        memory_usage.append(bytearray(10**6))  # Использование 1 МБ
        if psutil.virtual_memory().available < memory_limit_mb * (1024 ** 2):
            memory_usage.pop(0)  # Освобождение памяти

def disk_load(duration, disk_limit_mb):
    """Генерация нагрузки на диск."""
    end_time = time.time() + duration
    file_name = "load_test_file.dat"
    with open(file_name, 'wb') as f:
        while time.time() < end_time:
            f.write(os.urandom(10**6))  # Запись 1 МБ
            if os.path.getsize(file_name) > disk_limit_mb * (1024 ** 2):
                f.truncate(0)  # Очистка файла при превышении лимита

def main():
    cpu_duration = 10  # Длительность нагрузки на CPU (сек)
    memory_limit_mb = 512  # Максимальное использование памяти (МБ)
    disk_limit_mb = 100  # Максимально допустимый размер файла на диске (МБ)

    while True:
        delay = random.randint(5, 15)  # Случайный интервал задержки (от 5 до 15 секунд)
        time.sleep(delay)  # Ожидание случайного периода времени

        # Запуск нагрузки в отдельном процессе
        processes = []

        # Запуск нагрузки на CPU в процессе
        cpu_process = multiprocessing.Process(target=cpu_load, args=(cpu_duration,))
        cpu_process.start()
        processes.append(cpu_process)

        # Запуск нагрузки на память
        memory_process = multiprocessing.Process(target=memory_load, args=(cpu_duration, memory_limit_mb))
        memory_process.start()
        processes.append(memory_process)

        # Запуск нагрузки на диск
        disk_process = multiprocessing.Process(target=disk_load, args=(cpu_duration, disk_limit_mb))
        disk_process.start()
        processes.append(disk_process)

        # Ожидание завершения всех процессов
        for p in processes:
            p.join()

if __name__ == "__main__":
    main()
