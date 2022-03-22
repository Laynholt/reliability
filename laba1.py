
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import remove, path

from lib import Exponential, Gamma, Rayleigh, TruncatedNormal

TIME_STEP = 100
TIME = 2000 + TIME_STEP
PLOT_STEP = TIME_STEP


def task():
    # Менять значения тут
    # --------------------- #
    tn = TruncatedNormal(450, 120)
    g = Gamma(35, 75)
    r = Rayleigh(4 * 10 ** (-5))
    e = Exponential(1 * 10 ** (-4))
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
    count = 0
    t_mean = 0
    for i in range(0, TIME, TIME_STEP):
        tnf_list.append(tn.f(i))
        tnp_list.append(tn.p(i))
        tnl_list.append(0 if tnp_list[count] == 0 else tnf_list[count] / tnp_list[count])

        gf_list.append(g.f(i))
        gp_list.append(g.p(i))
        gl_list.append(0 if gp_list[count] == 0 else gf_list[count] / gp_list[count])

        rf_list.append(r.f(i))
        rp_list.append(r.p(i))
        rl_list.append(0 if rp_list[count] == 0 else rf_list[count] / rp_list[count])

        ef_list.append(e.f(i))
        ep_list.append(e.p(i))
        el_list.append(0 if ep_list[count] == 0 else ef_list[count] / ep_list[count])

        l_list.append(tnl_list[count] + gl_list[count] + rl_list[count] + el_list[count])
        p_list.append(tnp_list[count] * gp_list[count] * rp_list[count] * ep_list[count])
        f_list.append(l_list[count] * p_list[count])

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
    # save the excel file
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

    # plt.title('Интенсивность отказов L2')
    # ax = plt.gca()
    # df_l.plot(kind='line', x='t час.', y='L2(t)', color='blue', ax=ax)
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    # plt.show()

    plt.title('Интенсивность отказов системы')
    ax = plt.gca()
    df_l.plot(kind='line', x='t час.', y='Lc(t)', color='yellowgreen', ax=ax)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + TIME_STEP, end, PLOT_STEP))
    plt.show()
