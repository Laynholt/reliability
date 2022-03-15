import pandas as pd
import matplotlib.pyplot as plt
from os import remove, path
from scipy.integrate import trapz

from lib import Exponential, Gamma, Rayleigh, TruncatedNormal, Weibula

TIME_STEP = 50
TIME = 1000 + TIME_STEP


f_list = []
p_list = []
l_list = []
count = 0


def func(fc_list: list, pc_list: list, lc_list: list, m: int):
    fc_list.append((m + 1) * f_list[count] * (1 - p_list[count]) ** m)
    pc_list.append(1 - (1 - p_list[count]) ** (m + 1))
    lc_list.append(0 if pc_list[count] == 0 else fc_list[count] / pc_list[count])


def task():
    # Менять значения тут
    # --------------------- #
    # distribution = TruncatedNormal(360, 70)
    # distribution = Gamma(30, 100)
    # distribution = Rayleigh(4 * 10 ** (-5))
    distribution = Exponential(0.007)
    # distribution = Weibula(4, 500)

    # distribution_type = 'Усеченное нормальное'      # Если усеченное нормальное
    # distribution_type = 'Гамма'                     # Если гамма
    # distribution_type = 'Рэлея'                     # Если Рэлея
    distribution_type = 'Экспоненциальное'        # Если экспоненциальное
    # distribution_type = 'Вейбула'                     # Если Вейбула
    # --------------------- #

    m = distribution.m
    sigma = distribution.sigma

    file_path = 'output2.xlsx'
    if path.exists(file_path):
        remove(file_path)

    writer = pd.ExcelWriter(file_path)

    df_m_sigma = pd.DataFrame({
        'Значения / Методы распределение': ['m', 'sigma'],
        distribution_type: [m, sigma]
    })
    df_m_sigma.to_excel(writer, 'm_sigma')

    global f_list
    global p_list
    global l_list
    global count

    fc0_list = []
    pc0_list = []
    lc0_list = []

    fc1_list = []
    pc1_list = []
    lc1_list = []

    fc2_list = []
    pc2_list = []
    lc2_list = []

    time_list = []
    for i in range(0, TIME, TIME_STEP):
        f_list.append(distribution.f(i))
        p_list.append(distribution.p(i))
        l_list.append(0 if p_list[count] == 0 else f_list[count] / p_list[count])

        func(fc_list=fc0_list, pc_list=pc0_list, lc_list=lc0_list, m=0)
        func(fc_list=fc1_list, pc_list=pc1_list, lc_list=lc1_list, m=1)
        func(fc_list=fc2_list, pc_list=pc2_list, lc_list=lc2_list, m=2)

        time_list.append(i)
        count += 1

    print('Среднее времени безотказной работы системы при m = 0: ', trapz(pc0_list) * TIME_STEP)
    print('Среднее времени безотказной работы системы при m = 1: ', trapz(pc1_list) * TIME_STEP)
    print('Среднее времени безотказной работы системы при m = 2: ', trapz(pc2_list) * TIME_STEP)

    # Заполняем эксель файл
    df_p = pd.DataFrame({
        't час.': time_list,
        'P(t)': p_list,
        'Pc(t) [m = 0]': pc0_list,
        'Pc(t) [m = 1]': pc1_list,
        'Pc(t) [m = 2]': pc2_list
    })
    df_f = pd.DataFrame({
        't час.': time_list,
        'F(t)': f_list,
        'Fc(t) [m = 0]': fc0_list,
        'Fc(t) [m = 1]': fc1_list,
        'Fc(t) [m = 2]': fc2_list
    })
    df_l = pd.DataFrame({
        't час.': time_list,
        'L(t)': l_list,
        'Lc(t) [m = 0]': lc0_list,
        'Lc(t) [m = 1]': lc1_list,
        'Lc(t) [m = 2]': lc2_list
    })

    df_p.to_excel(writer, 'P')
    df_f.to_excel(writer, 'F')
    df_l.to_excel(writer, 'L')

    # save the excel file
    writer.save()

    # Рисуем графики
    plt.title('Распределение времени безотказной работы')
    ax = plt.gca()
    df_p.plot(kind='line', x='t час.', y='P(t)', color='red', ax=ax)
    plt.show()

    plt.title('Распределение времени безотказной работы системы')
    ax = plt.gca()
    df_p.plot(kind='line', x='t час.', y='Pc(t) [m = 0]', color='blue', ax=ax)
    df_p.plot(kind='line', x='t час.', y='Pc(t) [m = 1]', color='green', ax=ax)
    df_p.plot(kind='line', x='t час.', y='Pc(t) [m = 2]', color='yellowgreen', ax=ax)
    plt.show()

    plt.title('Плотность вероятности')
    ax = plt.gca()
    df_f.plot(kind='line', x='t час.', y='F(t)', color='red', ax=ax)
    plt.show()

    plt.title('Плотность вероятности системы')
    ax = plt.gca()
    df_f.plot(kind='line', x='t час.', y='Fc(t) [m = 0]', color='blue', ax=ax)
    df_f.plot(kind='line', x='t час.', y='Fc(t) [m = 1]', color='green', ax=ax)
    df_f.plot(kind='line', x='t час.', y='Fc(t) [m = 2]', color='yellowgreen', ax=ax)
    plt.show()

    plt.title('Интенсивность отказов')
    ax = plt.gca()
    df_l.plot(kind='line', x='t час.', y='L(t)', color='red', ax=ax)
    plt.show()

    plt.title('Интенсивность отказов системы')
    ax = plt.gca()
    df_l.plot(kind='line', x='t час.', y='Lc(t) [m = 0]', color='blue', ax=ax)
    df_l.plot(kind='line', x='t час.', y='Lc(t) [m = 1]', color='green', ax=ax)
    df_l.plot(kind='line', x='t час.', y='Lc(t) [m = 2]', color='yellowgreen', ax=ax)
    plt.show()
