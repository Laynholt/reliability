
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import remove, path

from lib import Exponential, Gamma, Rayleigh, TruncatedNormal

TIME_STEP = 100
TIME = 2000 + TIME_STEP
PLOT_STEP = TIME_STEP

count = 0


def calculate_fpl(f_list: list, p_list: list, l_list: list, i: int, distribution):
    f_list.append(distribution.f(i))
    p_list.append(distribution.p(i))
    l_list.append(0 if p_list[count] == 0 else f_list[count] / p_list[count])


def task():
    # Менять значения тут
    # --------------------- #
    tn = TruncatedNormal(360, 70)
    g = Gamma(30, 100)
    r = Rayleigh(4 * 10 ** (-5))
    e = Exponential(7 * 10 ** (-3))
    # --------------------- #

    print("c = ", tn.c, "; k = ", tn.k)

    m_list = []
    sigma_list = []

    tnf_list = []
    tnp_list = []

    gf_list = []
    gp_list = []

    rf_list = []
    rp_list = []

    ef_list = []
    ep_list = []

    tnl_list = []
    gl_list = []
    rl_list = []
    el_list = []

    f_list = []
    p_list = []
    l_list = []

    m_list.append(tn.m)
    sigma_list.append(tn.sigma)
    m_list.append(g.m)
    sigma_list.append(g.sigma)
    m_list.append(r.m)
    sigma_list.append(r.sigma)
    m_list.append(e.m)
    sigma_list.append(e.sigma)

    time_list = []
    t_mean = 0
    global count
    for i in range(0, TIME, TIME_STEP):
        # Вычисляем f, p, l для каждого распределения
        calculate_fpl(f_list=tnf_list, p_list=tnp_list, l_list=tnl_list, i=i, distribution=tn)
        calculate_fpl(f_list=gf_list, p_list=gp_list, l_list=gl_list, i=i, distribution=g)
        calculate_fpl(f_list=rf_list, p_list=rp_list, l_list=rl_list, i=i, distribution=r)
        calculate_fpl(f_list=ef_list, p_list=ep_list, l_list=el_list, i=i, distribution=e)

        # Вычисляем fc, pc, lc для каждого распределения
        l_list.append(tnl_list[count] + gl_list[count] + rl_list[count] + el_list[count])
        p_list.append(tnp_list[count] * gp_list[count] * rp_list[count] * ep_list[count])
        f_list.append(l_list[count] * p_list[count])

        # Средняя наработка до отказа по Формуле Симпсона
        if i != 0 and i != (TIME - TIME_STEP):
            t_mean += ((3 + (-1)**count) * tnp_list[count] * gp_list[count] * rp_list[count] * ep_list[count])

        time_list.append(i)
        count += 1
    t_mean = 100 / 3 * (1 + t_mean)
    print("Средняя наработка до отказа Tср: ", t_mean)

    # Заполняем эксель файл
    df_m_sigma = pd.DataFrame({
        'Значения / Методы распределение': ['m', 'sigma'],
        'Усеченное нормальное': [m_list[0], sigma_list[0]],
        'Гамма': [m_list[1], sigma_list[1]],
        'Рэлея': [m_list[2], sigma_list[2]],
        'Экспоненциальное': [m_list[3], sigma_list[3]]
    })
    df_p = pd.DataFrame({
        't час.': time_list,
        'P1(t)': tnp_list,
        'P2(t)': gp_list,
        'P3(t)': rp_list,
        'P4(t)': ep_list,
        'Pc(t)': p_list,
    })
    df_f = pd.DataFrame({
        't час.': time_list,
        'F1(t)': tnf_list,
        'F2(t)': gf_list,
        'F3(t)': rf_list,
        'F4(t)': ef_list,
        'Fc(t)': f_list,
    })
    df_l = pd.DataFrame({
        't час.': time_list,
        'L1(t)': tnl_list,
        'L2(t)': gl_list,
        'L3(t)': rl_list,
        'L4(t)': el_list,
        'Lc(t)': l_list,
    })

    file_path = 'output1.xlsx'
    if path.exists(file_path):
        remove(file_path)

    writer = pd.ExcelWriter(file_path)
    df_m_sigma.to_excel(writer, 'm_sigma')
    df_p.to_excel(writer, 'P')
    df_f.to_excel(writer, 'F')
    df_l.to_excel(writer, 'L')
    # Сохраняем файл
    writer.save()

    # Рисуем графики
    plt.title('Распределение времени безотказной работы')
    ax = plt.gca()
    df_p.plot(kind='line', x='t час.', y='P1(t)', color='red', ax=ax)
    df_p.plot(kind='line', x='t час.', y='P2(t)', color='blue', ax=ax)
    df_p.plot(kind='line', x='t час.', y='P3(t)', color='green', ax=ax)
    df_p.plot(kind='line', x='t час.', y='P4(t)', color='indigo', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()

    plt.title('Распределение времени безотказной работы системы')
    ax = plt.gca()
    df_p.plot(kind='line', x='t час.', y='Pc(t)', color='yellowgreen', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()

    plt.title('Плотность вероятности')
    ax = plt.gca()
    df_f.plot(kind='line', x='t час.', y='F1(t)', color='red', ax=ax)
    df_f.plot(kind='line', x='t час.', y='F2(t)', color='blue', ax=ax)
    df_f.plot(kind='line', x='t час.', y='F3(t)', color='green', ax=ax)
    df_f.plot(kind='line', x='t час.', y='F4(t)', color='indigo', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()

    # plt.title('Плотность вероятности F4')
    # ax = plt.gca()
    # df_f.plot(kind='line', x='t час.', y='F4(t)', color='indigo', ax=ax)
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    # plt.show()

    plt.title('Плотность вероятности системы')
    ax = plt.gca()
    df_f.plot(kind='line', x='t час.', y='Fc(t)', color='yellowgreen', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()

    plt.title('Интенсивность отказов')
    ax = plt.gca()
    df_l.plot(kind='line', x='t час.', y='L1(t)', color='red', ax=ax)
    df_l.plot(kind='line', x='t час.', y='L2(t)', color='blue', ax=ax)
    df_l.plot(kind='line', x='t час.', y='L3(t)', color='green', ax=ax)
    df_l.plot(kind='line', x='t час.', y='L4(t)', color='indigo', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()

    # plt.title('Интенсивность отказов L4')
    # ax = plt.gca()
    # df_l.plot(kind='line', x='t час.', y='L4(t)', color='indigo', ax=ax)
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    # plt.show()

    plt.title('Интенсивность отказов системы')
    ax = plt.gca()
    df_l.plot(kind='line', x='t час.', y='Lc(t)', color='yellowgreen', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()
