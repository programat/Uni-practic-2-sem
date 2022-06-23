import os

name_file1 = input("Введите название файла, в котором хранятся циклы (без .txt): ")
if os.path.exists(f'data/{name_file1}.txt'):
    f = open(f'data/{name_file1}.txt', 'r')
    data = f.read()
    cycles = data.split('\n\n')
    for i in range(len(cycles)):
        cycles[i] = cycles[i].split('\n')
        for j in range(len(cycles[i])):
            cycles[i][j] = cycles[i][j].split()
            cycles[i][j] = list(map(int, cycles[i][j]))
    n = len(cycles) - 1
    for i in range(2 ** n):
        mask = bin(i)[2:]
        mask = '0' * (n - len(mask)) + mask
        mask = list(map(int, list(mask)))
        temp = []
        for j in range(n):
            if mask[j] == 1:
                for u, v in cycles[j]:
                    u, v = min(u, v), max(u, v)
                    edge = [u, v]

                    if edge in temp:
                        temp.remove(edge)
                    else:
                        temp.append(edge)

        k = 0
        while k < len(cycles[-1]):
            u, v = cycles[-1][k]
            u, v = min(u, v), max(u, v)
            cycles[-1][k] = [u, v]
            k += 1

        flag = False
        if len(temp) != len(cycles[-1]):
            flag = True
            continue

        for u1, v1 in temp:
            flag2 = True
            for u2, v2 in cycles[-1]:
                if u1 == u2 and v1 == v2:
                    flag2 = False
                    break
            if flag2:
                flag = True
        if not flag:
            break

    name_file2 = input("Введите название файла, в который необходимо записать ответ (без .txt): ")
    with open(f'data/{name_file2}.txt', 'w') as graph:
        if flag:
            graph.write('Решение отсутствует')
        else:
            graph.write('Произвольный цикл состоит из циклов:\n')
            for i in range(n):
                if mask[i] == 1:
                    graph.write('Цикл С' + str(i + 1) + ', состоящий из рёбер: \n')
                    for u, v in cycles[i]:
                        graph.write(str(u) + ' ' + str(v) + '\n')
        print("Успешно!")
else:
    print("Файл с входными данными не найден")

input("Для продолжения нажмите любую клавишу...")
