# Лабораторные работы по дисциплине "Надежность автоматизированных систем обработки информации и управления"
Проект состоит из двух файлов для двух лабораторных работ соответственно и позволяет получить конечные данные и результирующие графики по исходным данным.

# Параметры запуска
В зависимости от необходимого задания раскомментировать нужный модуль в файле main.py:
```
# from laba1 import task
from laba2 import task

if __name__ == "__main__":
    task()
```

Менять параметры можно в файлах laba1.py и laba2.py в помеченных комментариями зонах.
```
 # Менять значения тут
    # --------------------- #
    tn = TruncatedNormal(400, 92)
    g = Gamma(8, 77)
    r = Rayleigh(1 * 10 ** (-5))
    e = Exponential(6 * 10 ** (-3))
    # --------------------- #
```

# Запуск проекта
```
python main.py
```
В результате работы проекта будет создан exel файл с результатами вычислений и выведены графики этих результатов. 

# Лабораторная работа 1
Нерезервированная система состоит из 4 элементов, имеющих различные законы распределения времени работы до отказа.
Необходимо определить показатели надежности каждого элемента и всей системы:
•	Вероятность безотказной работы системы;
•	Плотность распределения времени до отказа системы;
•	Интенсивность отказов системы;
•	Среднее время безотказной работы системы.

Пример результатов работы для исходных данных:
- Усеченное нормальное: (400, 92)
- Гамма: (8, 77)
- Рэлея: (1* 10^-5)
- Экспоненциальное: (6 * 10^-3)

Результаты:
c =  1.0000068747252044 ; k =  3.133648451746235e-05
Средняя наработка до отказа Tср:  97.5417938661333

Графики
![image](https://user-images.githubusercontent.com/41357381/175787481-8de0043e-ac66-408a-a0b8-355d0bc6dd60.png)
![image](https://user-images.githubusercontent.com/41357381/175787505-b910b9d5-8c9f-489e-943c-0bf04b15557c.png)
![image](https://user-images.githubusercontent.com/41357381/175787513-a36e68bf-3b07-4510-aa24-2c178fba113a.png)
![image](https://user-images.githubusercontent.com/41357381/175787525-f86bb0c7-a835-40a7-8ed9-7cf45f3b60b4.png)
![image](https://user-images.githubusercontent.com/41357381/175787540-917342b3-4e9c-4380-aa30-43276fe63ecd.png)
![image](https://user-images.githubusercontent.com/41357381/175787546-49ba1430-e028-47be-bdc2-67c4466a55f2.png)

Табличные значения
![image](https://user-images.githubusercontent.com/41357381/175787591-63cac83f-df97-4148-b4c2-2a13aa6ddca3.png)
![image](https://user-images.githubusercontent.com/41357381/175787558-d5cdb6a4-4b03-4b36-bec2-d6ec27f15903.png)
![image](https://user-images.githubusercontent.com/41357381/175787563-c6be5ffb-6b7f-4de0-8c61-aee97f2201fc.png)
![image](https://user-images.githubusercontent.com/41357381/175787574-81c27d50-42b1-4997-99ab-e7805d7a2347.png)

# Лабораторная работа 2
Определить все показатели надежности системы. Результаты представить в виде таблиц и графиков. 
Принять m=0, 1, 2; временной интервал принять равным t=1000 час, h=50час; экспоненциальное распределение Exp(0,007).

Пример результатов работы для исходных данных:
Усеченное нормальное: (400, 180)

Результаты:
Среднее времени безотказной работы системы при m = 0:  406.17734695259946
Среднее времени безотказной работы системы при m = 1:  504.14351958819054
Среднее времени безотказной работы системы при m = 2:  554.2657548730579

Графики
![image](https://user-images.githubusercontent.com/41357381/175787745-7f36faeb-e865-4b62-9e49-08a5c018c73f.png)
![image](https://user-images.githubusercontent.com/41357381/175787758-3b4736dd-f3d3-4b94-8214-0cac34ded828.png)
![image](https://user-images.githubusercontent.com/41357381/175787770-75a4ddd7-932b-43c0-98e7-fff60f5d84dc.png)

Табличные значения

![image](https://user-images.githubusercontent.com/41357381/175787787-f0e8286a-f9ae-4ff7-af08-f4a1433395a8.png)

![image](https://user-images.githubusercontent.com/41357381/175787794-a7d69e19-4b2a-4432-a6c5-5ee604371c80.png)

![image](https://user-images.githubusercontent.com/41357381/175787802-72b48af7-db6d-4026-8290-00550ea83d00.png)

