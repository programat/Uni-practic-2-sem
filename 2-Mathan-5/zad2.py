import matplotlib
import matplotlib.pyplot as plt
from numpy import exp, sqrt, sin, log, linspace, seterr, nanmin, \
    nanmax, inf

matplotlib.use("TkAgg")
seterr(divide='ignore', invalid='ignore')  # обработка ошибок в numpy

# массив лямбда-функций
func = [lambda x: 1 / x,
        lambda x: x / (x ** 2 - 4 * x + 3),
        lambda x: x ** 2 / (x ** 2 - 4),
        lambda x: sqrt(x ** 2 - 1),
        lambda x: (x ** 2 + 1) / sqrt(x ** 2 - 1),
        lambda x: (exp(-x ** 2) + 2),
        lambda x: (1 / (1 - exp(x))),
        lambda x: (exp(1 / x)),
        lambda x: (sin(x) / x),
        lambda x: (log(1 + x))]

hl = [0, 0, 1, None, None, 2, 0, 1, 0, None]  # горизонтальные асимптоты
vl = [[0], [1, 3], [-2, 2], [], [-1, 1], [], [0], [0], [0], []]  # вертикальные асимптоты
al = [[], [], [], [lambda x: x], [lambda x: x], [], [], [], [], []]  # наклонные асимптоты
name = [r'$y = \frac{1}{x}$', r'$y = \frac{x}{x ^ 2 - 4 \cdot x + 3}$', r'$y = \frac{x ^ 2}{x ^ 2 - 4}$',
        r'$y = \sqrt{x ^ 2 - 1}$', r'$y = \frac{x ^ 2 + 1}{\sqrt{x ^ 2 - 1}}$', r'$y = e^{-x ^ 2} + 2$',
        r'$y = \frac{1}{1 - e^x}$', r'$y = e^{\frac{1}{x}}$', r'$y = \frac{\sin(x)}{x}$', r'$y = \ln(1 + x)$']

def select_function():
    print("Список функций:")
    print("0. Завершить работу", "1. y = 1/x ", "2. y = 1 / ((x - 3) ^ 2 - 3)", "3. y = (x / (x ^ 2 - 2 * x))",
          "4. y = (x ^ 2 - 3) / (sqrt(x ^ 2 - 1))", "5. y = (exp(1 / (x + 3)))", "6. y = (sin(x) / x)",
          "7. y = (1 / (1 - exp(x)))", "8. y = (sqrt(x ^ 2 - 1))", "9. y = (exp(-x ^ 2) + 3)", "10. y = log(1 + x)", sep="\n")
    number = input("Выберите номер функции: ")
    while number not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        number = (input("Номер функции некорректный, попробуйте снова: "))
    return int(number) - 1

print("Добро пожаловать!")
number = select_function()
while number != -1:
    action = -1
    while action != 2:
        print("Выберите действие: ")
        print("1. Выбрать точку", "2. Вернуться к списку функций", sep="\n")
        action = int(input())
        while action not in [1, 2]:
            try:
                action = int(input("Номер действия некорректный, введите 1 или 2: "))
            except ValueError:
                pass
        if action == 1:
            try:
                x0 = float(input("Введите точку: "))
                if (number == 3 or number == 4) and -1 < x0 < 1:
                    print('В этой точке функция не существует')
                    continue
                if number == 9 and x0 <= -1:
                    print('В этой точке функция не существует')
                    continue
            except ValueError:
                print("Неверный ввод точки. Введите inf или число")
                continue

            if x0 == float('inf'):  # отрисовка наклонных и горизонтальных асимптот
                x = linspace(-10, 10, 101)
                if not (al[number] == []):  # отрисовка наклонных асимптот
                    for j in range(len(al[number])):
                        y = al[number][j](x)
                        plt.plot(x, y, color='#939393')
                y = func[number](x)
                if not (hl[number] is None):  # отрисовка горизонтальных асимптот
                    plt.hlines(hl[number], nanmin(x[x != -inf]), nanmax(x[x != inf]))
            else:
                if x0 in vl[number]:  # отрисовка вертикальных асимптот
                    x = linspace(-10, 10, 101)
                    y = func[number](x)
                    for i in range(len(vl[number])):
                        plt.vlines(vl[number][i], nanmin(y[y != -inf]), nanmax(y[y != inf]))
                else:  # отрисовка графика функции в окрестности точки х0
                    x = linspace(x0 - 1, x0 + 1, 101)
                    y = func[number](x)

            plt.plot(x, y, color='#b23dff')
            plt.grid()
            plt.title('График функции ' + name[number])
            plt.show()
    number = select_function()

print("До свидания!")
exit()

# x0 = float(input('x0 = '))
# u = float(input('u = '))
# x0_below, x0_above = (x0 - u, x0 + u)
#
# y = lambda x: 1 / x
# y = np.vectorize(y)
# if u != float('inf'):
#     x = np.linspace(x0_below, x0_above)
# else:
#     x = np.linspace(-1000, 1000, 500)
# x[(x < -1) & (x > 1)] = np.nan
#
# plt.plot(x, y(x))
# plt.grid()
#
# plt.show()
