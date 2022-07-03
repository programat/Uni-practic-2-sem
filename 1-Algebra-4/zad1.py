# Дана квадратная матрица A размерности n x n. Привести ее к нижне-треугольной форме.
# Чтение производится из файла

from fractions import Fraction as fr  #модуль для работы с рациональными числами (дробями)

def init_matrix(file):
    a = list(file.readlines())  # считали все строки файла до его конца, а - массив
    try:
        a = [list(map(fr, a[i].split())) for i in range(len(a))]  # разбили все значения по пробелу и инициализрвоали их как тип fraction
    except ValueError:
        print('Введены недопустимые данные! Досрочный выход!')
        exit()
    b = []
    for i in range(len(a)):
        if (a[i] != []):  # если a[i] - не пустое значение - заполняем массив b
            b.append(a[i])
    a.clear()  # очистка массива
    if b == []:
        print('Введенные данные пусты')
        exit()
    len_b = len(b[0])

    # в результате мы заполнили массив значениями, осталось проверить, квадратная ли получилась матрица
    for i in range(len(b)):
        if (len(b[i]) != len_b):  # длина каждой строки (каждого подмассива) должна быть равна длине первой (первого)
            print('Введенные данные не соответствуют требованиям (длины строк матрицы отличаются и(или) введены лишние символы)')
            exit()
    if (len_b != len(b)):
        print('Введенные данные не соответствуют требованиям (матрица не квадратная)')
        exit()
    return b  # при соблюдении всех условиях - возвращаем готовую матрицу в нужном виде

# функция вывода матрицы, которая в рамках решаемой задачи не нужна
# def print_matrix(matrix):
#     for i in range(len(matrix)):
#         print(*matrix[i])

def swap_row(matrix, i):  # функция перемены строк местами
    if(matrix[i][i] == 0):
        for j in range(len(matrix)):
            if matrix[j][i] != 0:
                matrix[j], matrix[i] = matrix[i], matrix[j]
                break
        return matrix
    else: return matrix

def det(matrix):
    for i in range(len(matrix)-1):  # цикл, который отвечает за переход к строке, которую будем домножать
        if(matrix[i][i] == 0):  # будем идти по главной диагонали, так как ниже нее элементы должны быть равны нулю
            matrix = swap_row(matrix, i)  # если элемент опорной строки равен 0, то меняем строки местами
            if (matrix[i][i] == 0):
                continue  # если после перемены местами строки все равно равны 0, то просто переходи на след итерацию

        # на этом шаге первый элемент выбранной строки не равен 0
        for j in range(i+1, len(matrix)):  # цикл, который отвечает за строку от которой будем отнимать
            difference = (matrix[j][i] / matrix[i][i]) * (-1)  # цикл, который отвечает за вычисление разницы между первой строкой
            for l in range(len(matrix)):  # цикл, который отвечает за обход элементов на одной строке
                matrix[j][l] += difference*matrix[i][l]  # отнимаем разницу от каждого элемента строки
    determinant = 1
    for i in range(len(matrix)): # просто перемножаем элементы на главной диагонали
        determinant *= matrix[i][i]
    # return ('%f' % determinant).rstrip('0').rstrip('.')
    # return round(float(determinant), 6)
    return determinant

try:
    # подключение файла
    print('Введите название файла c расширением для считывания:')
    name_file = input('data/')
    for i in name_file:  # если пользователь введет пробелы перед названием
        if(i == ' '): name_file = name_file.replace(' ', '', 1)
        else: break

    try:
        file_data_input = open(rf'data/{name_file}', 'r', encoding='utf-8')
        matrix = init_matrix(file_data_input)
        file_data_input.close() # отключение обработанного файла
    except FileNotFoundError:
        print('Файл не найден!')
        exit()
    answer = det(matrix)  # получение определителя матрицы в виде рационального числа

    # подключение файла на дозапись
    print('Введите название файла c расширением для записи:')
    name_file = input('data/')
    for i in name_file:  # если пользователь введет пробелы перед названием
        if(i == ' '): name_file = name_file.replace(' ', '', 1)
        else: break
    try:
        file_data_output = open(rf'data/{name_file}', 'a', encoding='utf-8')
        file_data_output.write(f'\nОтвет = {answer}')
        file_data_output.close()
        print('Успешно!')
    except FileNotFoundError:
        print('Файл не найден!')
        exit()

except (IsADirectoryError, KeyboardInterrupt):  # исключение для ошибок прерывания выполнения программы и неправильного обращения к файлу
    print('\nДосрочный выход!')