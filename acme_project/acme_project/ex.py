import time


# Принимает на вход функцию:
def time_of_function(func):
    # Объявляем внутреннюю функцию — её-то и вернём, когда опишем.
    def wrapper():
        start_time = time.time()
        print('Время пошло')

        # Вызываем полученную функцию и 
        # cохраняем результат её выполнения в переменную.
        result = func()

        execution_time = round(time.time() - start_time, 1)
        # Можем использовать результат выполнения полученной функции:
        print(f'Через {execution_time} сек функция вернула «{result}»')
        # Возвращаем результат выполнения полученной функции.
        return result
    # Возвращаем функцию wrapper, но не вызываем её:
    return wrapper


@time_of_function
def sleep_one_sec():
    time.sleep(1)
    return 'Результат первой функции.'

sleep_one_sec()

def sleep_two_sec():
    return 'Результат второй функции.'