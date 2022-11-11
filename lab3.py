stuffdict = {'в': (3, 25),
             'п': (2, 15),
             'б': (2, 15),
             'а': (2, 20),
             'и': (1, 5),
             'н': (1, 15),
             'т': (3, 20),
             'о': (1, 25),
             'ф': (1, 15),
             'д': (1, 10),
             'к': (2, 20),
             'р': (2, 20)
             }

start_value = 15
result_value = 0


def get_area_and_value(stuffdict):
    area = [stuffdict[item][0] for item in stuffdict]
    value = [stuffdict[item][1] for item in stuffdict]
    summ = sum(value)
    return area, value, summ


def get_memtable(stuffdict, A=8):
    area, value, summ = get_area_and_value(stuffdict)
    n = len(value)
    V = [[0 for a in range(A + 1)] for i in range(n + 1)]
    for i in range(n + 1):
        for a in range(A + 1):
            if i == 0 or a == 0:
                V[i][a] = -summ
            elif area[i - 1] <= a:
                after = value[i - 1] + V[i - 1][a - area[i - 1]]
                V[i][a] = max(after, V[i - 1][a])
            # если площадь предмета больше площади столбца,
            # забираем значение ячейки из предыдущей строки
            else:
                V[i][a] = V[i - 1][a]

    return V, area, value


def get_selected_items_list(stuffdict, A):
    V, area, value = get_memtable(stuffdict)
    n = len(value)
    res = V[n][A]  # начинаем с последнего элемента таблицы
    a = A  # начальная площадь - максимальная
    items_list = []  # список занимаемых ячеек и ценностей

    for i in range(n, 0, -1):  # идём в обратном порядке
        if a <= 0:  # условие прерывания - собрали "рюкзак"
            break
        if res == V[i - 1][a]:  # ничего не делаем, двигаемся дальше
            continue
        else:
            # "забираем" предмет
            items_list.append((area[i - 1], value[i - 1]))
            res -= value[i - 1]  # отнимаем значение ценности от общей
            a -= area[i - 1]  # отнимаем площадь от общей

    selected_stuff = []
    mas = []
    # находим ключи исходного словаря - названия предметов
    for search in items_list:
        for key, value in stuffdict.items():
            if value == search and (key not in selected_stuff):
                selected_stuff.append(key)
                v = value[0]
                mas.extend([[key]] * v)
                break
    not_selected_stuff = []
    sum_not_selected = 0
    for key, value in stuffdict.items():
        for key2 in selected_stuff:
            if key2 != key:
                not_selected_stuff.append(key)
                sum_not_selected += value[1]
                break

    return selected_stuff, sum_not_selected, mas


stuff, sum_not_sel, mas = get_selected_items_list(stuffdict, 8)
V, area, value, = get_memtable(stuffdict)
summ1 = sum_not_sel - abs(V[-1][-1])  # сумма взятых предметов
result_value = summ1 - abs(V[-1][-1]) + start_value
print(mas[0:4])
print(mas[4:])
print('Итоговые очки выживания:', result_value)
