try:
    name_file1 = input("Введите название файла с расширением, в котором хранятся циклы: ")
    # разбиваем данные на массив
    f = open(f'data/{name_file1}', 'r')
    data = f.read()  # считали сразу весь файл
    cycles = data.split('\n\n')  # циклы отделены друг от друга пустой строкой
    for i in range(len(cycles)):
        cycles[i] = cycles[i].split('\n')
        for j in range(len(cycles[i])):
            cycles[i][j] = cycles[i][j].split()
            cycles[i][j] = list(map(int, cycles[i][j]))
    n = len(cycles) - 1  # количество циклов ФМЦ без произвольного

    # создаем двоичную маску
    for i in range(2 ** n):
        mask = bin(i)[2:]  # берем двоичное число без префикса
        mask = '0' * (n - len(mask)) + mask  # приводим к общему виду
        mask = list(map(int, list(mask)))  # создаем из mask массив, где каждый элемент - число
        gotcha = []
        for j in range(n):  # перебираем значения маски
            if mask[j] == 1:
                for u, v in cycles[j]:
                    u, v = min(u, v), max(u, v)
                    edge = [u, v]

                    # реализация процесса суммирования
                    if edge in gotcha:
                        gotcha.remove(edge)
                    else:
                        gotcha.append(edge)
        k = 0

        # выстраиваем ребра произвольного цикла по возрастанию их номеров
        while k < len(cycles[-1]):
            u, v = cycles[-1][k]
            u, v = min(u, v), max(u, v)
            cycles[-1][k] = [u, v]
            k += 1

        # если
        flag1 = False
        if len(gotcha) != len(cycles[-1]):
            flag1 = True
            continue  # если длина не совпадает, то дальше по циклу не идем и переходим на след итерацию

        for u1, v1 in gotcha:
            flag2 = True  # то есть есть ребро, которое есть в gotcha, но нет в cycles[-1]
            for u2, v2 in cycles[-1]:
                if u1 == u2 and v1 == v2:
                    flag2 = False  # а, походу нет
                    break
            if flag2:
                flag1 = True
        if not flag1:  # если в конечном счете flag1 == False, то мы нашли представление произвольного цикла в виде суммы циклов из ФМЦ
            break

    name_file2 = input("Введите название файла с расширением, в который необходимо записать ответ: ")
    with open(f'data/{name_file2}', 'w') as graph:
        if flag1:
            graph.write('Решение отсутствует')
        else:
            graph.write('Произвольный цикл состоит из циклов:\n')
            for i in range(n):
                if mask[i] == 1:
                    graph.write(f'Цикл С{str(i + 1)}, состоящий из рёбер: \n')
                    for u, v in cycles[i]:
                        graph.write(f'{str(u)} {str(v)}\n')
        print("Успешно!")

# исключение для ошибок прерывания выполнения программы и неправильного обращения к файлу
except (FileNotFoundError, IsADirectoryError):
    print("Файл с входными данными не найден")
except (IsADirectoryError, TypeError):
    print("Введены неверные данные")

input("Для продолжения нажмите любую клавишу...")
