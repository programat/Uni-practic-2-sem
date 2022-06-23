# Дана квадратная матрица A размерности n x n. Привести ее к нижне-треугольной форме.
# Чтение производится из файла

from fractions import Fraction as fr  #модуль для работы с рациональными числами (дробями)

def init_matrix(file):
    a=list(file.readlines())
    try:
        a = [list(map(fr, a[i].split())) for i in range(len(a))]
    except ValueError:
        print('Введены недопустимые данные! Досрочный выход!')
        exit()
    b= []
    for i in range(len(a)):
        if (a[i] != []):
            b.append(a[i])
    if b == []:
        print('Введенные данные пусты')
        exit()
    len_b = len(b[0])
    for i in range(len(b)):
        if (len(b[i]) != len_b):
            print('Введенные данные не соответствуют требованиям (длины строк матрицы отличаются и(или) введены лишние символы)')
            exit()
    if (len_b != len(b)):
        print('Введенные данные не соответствуют требованиям (матрица не квадратная)')
        exit()
    return b

def print_matrix(matrix):
    for i in range(len(matrix)):
        print(*matrix[i])

def swap_row(matrix, i):
    if(matrix[i][i] == 0):
        for j in range(len(matrix)):
            if matrix[j][i] != 0:
                matrix[j], matrix[i] = matrix[i], matrix[j]
                break
        return matrix
    else: return matrix

def det(matrix):
    for i in range(len(matrix)-1): #цикл, который отвечает за переход к строке, которую будем домножать
        if(matrix[i][i] == 0):
            matrix = swap_row(matrix, i)
            if (matrix[i][i] == 0):
                continue
        for j in range(i+1, len(matrix)): #цикл, который отвечает за строку от которой будем отнимать
            difference = (matrix[j][i] / matrix[i][i]) * (-1)
            for l in range(len(matrix)): #цикл, который отвечает за обход элементов на одной строке
                matrix[j][l] += difference*matrix[i][l]
    determinant = 1
    for i in range(len(matrix)):
        determinant *= matrix[i][i]
    # return ('%f' % determinant).rstrip('0').rstrip('.')
    # return round(float(determinant), 6)
    return determinant

try:
    #подключение файла
    print('Введите название файла c расширением для считывания:')
    name_file = input('data/')
    for i in name_file:  #если пользователь введет пробелы перед названием
        if(i == ' '): name_file = name_file.replace(' ', '', 1)
        else: break

    try:
        file_data_input = open(rf'data/{name_file}', 'r', encoding='utf-8')
        matrix = init_matrix(file_data_input)
        file_data_input.close() #отключение обработанного файла
    except FileNotFoundError:
        print('Файл не найден!')
        exit()
    answer = det(matrix)

    #подключение файла на дозапись
    print('Введите название файла c расширением для записи:')
    name_file = input('data/')
    for i in name_file:  #если пользователь введет пробелы перед названием
        if(i == ' '): name_file = name_file.replace(' ', '', 1)
        else: break
    try:
        file_data_output = open(rf'data/{name_file}', 'a', encoding='utf-8')
        file_data_output.write(f'\nОтвет = {answer}')
        file_data_output.close()
    except FileNotFoundError:
        print('Файл не найден')
        exit()
except KeyboardInterrupt:
    print('Досрочный выход!')