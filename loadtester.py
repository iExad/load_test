import os
import time
import multiprocessing
import psutil

def cpu_load(duration, cpu_percentage):
    """Генерация нагрузки на процессор."""
    end_time = time.time() + duration
    while time.time() < end_time:
        # Нагрузка на CPU
        array = [0] * (10**6)  # Использование памяти
        if psutil.cpu_percent(interval=1) < cpu_percentage:
            _ = sum(array)  # Простое вычисление
        else:
            time.sleep(0.1)  # Уменьшаем загрузку

def memory_load(duration, memory_limit_mb):
    """Генерация нагрузки на память."""
    memory_usage = []
    end_time = time.time() + duration
    while time.time() < end_time:
        memory_usage.append(bytearray(10**6))  # Выделить 1 МБ
        if psutil.virtual_memory().available < memory_limit_mb * (1024 ** 2):
            memory_usage.pop(0)  # Освободить память

def disk_load(duration, disk_limit_mb):
    """Генерация нагрузки на диск."""
    end_time = time.time() + duration
    file_name = "load_test_file.dat"
    with open(file_name, 'wb') as f:
        while time.time() < end_time:
            # Запись данных на диск
            f.write(os.urandom(10**6))  # Записываем 1 МБ
            if os.path.getsize(file_name) > disk_limit_mb * (1024 ** 2):
                f.truncate(0)  # Удаляем файл когда достигли лимита

if __name__ == "__main__":
    cpu_percentage = 50  # Максимальная загрузка CPU (процент) в данный момент не работает
    memory_limit_mb = 256  # Максимальное использование памяти (МБ)
    disk_limit_mb = 100  # Максимально допустимый размер файла на диске (МБ)
    duration = 60  # Длительность теста (сек.)

    # Создаём процессы для тестирования
    cpu_process = multiprocessing.Process(target=cpu_load, args=(duration, cpu_percentage,))
    memory_process = multiprocessing.Process(target=memory_load, args=(duration, memory_limit_mb,))
    disk_process = multiprocessing.Process(target=disk_load, args=(duration, disk_limit_mb,))

    cpu_process.start()
    memory_process.start()
    disk_process.start()

    # Ожидание завершения тестов
    cpu_process.join()
    memory_process.join()
    disk_process.join()

    print("Нагрузочное тестирование завершено.")
