import matplotlib
import matplotlib.pyplot as plt
from numpy import exp, sqrt, sin, log, linspace, seterr, nanmin, \
    nanmax, inf

matplotlib.use("TkAgg")
seterr(divide='ignore', invalid='ignore')  # обработка ошибок в numpy

# массив лямбда-функций
func = [lambda x: 1 / x,
        lambda x: 1 / ((x - 3) ^ 2 - 3),
        lambda x: (x / (x ^ 2 - 2 * x)),
        lambda x: (x ^ 2 - 3) / (sqrt(x ^ 2 - 1)),
        lambda x: (exp(1 / (x + 3))),
        lambda x: (sin(x) / x),
        lambda x: (1 / (1 - exp(x))),
        lambda x: (sqrt(x ^ 2 - 1)),
        lambda x: (exp(-x ^ 2) + 3),
        lambda x: log(1 + x)]

hl = [0, 0, 0, None, 1, None, 0, None, 3, None]  # горизонтальные асимптоты
vl = [[0], [-3, 3], [2], [-3], [], [0], [0], [], [], []]  # вертикальные асимптоты
al = [[], [], [], [lambda x: -x, lambda x: x], [], [], [], [lambda x: -x, lambda x: x], [], []]  # наклонные асимптоты

def select_function():
    print("Список функций:")
    print("0. Завершить работу", "1. y = 1/x ", "2. y = 1 / ((x - 3) ^ 2 - 3)", "3. y = (x / (x ^ 2 - 2 * x))",
          "4. y = (x ^ 2 - 3) / (sqrt(x ^ 2 - 1))", "5. y = (exp(1 / (x + 3)))", "6. y = (sin(x) / x)",
          "7. y = (1 / (1 - exp(x)))", "8. y = (sqrt(x ^ 2 - 1))", "9. y = (exp(-x ^ 2) + 3)", "10. y = log(1 + x)", sep="\n")
    number = int(input("Выберите номер функции: "))
    while number not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        number = int(input("Номер функции некорректный, попробуйте снова: "))
    return number - 1



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
