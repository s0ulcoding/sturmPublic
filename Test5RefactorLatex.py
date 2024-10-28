import numpy as np
from prettytable import PrettyTable
import math
import random
#from to_latex import construct_latex_str, generate_tex_file, generate_pdf_from_tex_file
import to_latex

def sokr(a):
    b = np.array(a, dtype=np.int64)  # Функция, которая делает набор чисел взаимно простыми
    gcd_ = np.gcd.reduce(b)
    return np.floor_divide(b, gcd_)
def delenie(a,b):               #Функция, находящая остаток от деления многочленов f(x) на g(x)
    quot, remainder = np.polydiv(a, b)
    return remainder
def smena(f1, a):                #Функция, считающая кол-во смен знаков в ряде Штурма в определённой точке
    c = 0
    znak = []                    #Создаём массив, в который будем добавлять 1, если мн-н положителен, и -1, если  он отрицателен
    for i in range(len(f1)):
        if np.polyval(f1[i], a) > 0:
            znak.append(1)
        elif np.polyval(f1[i], a) < 0:
            znak.append(-1)
    for i in range(1, len(znak)):     #Считаем кол-во смен знаков в этом массиве
        if znak[i-1] != znak[i]:
            c += 1
    return c
gran_set = set()
qglob = 1
def gener_3():
    global gran_set
    while True:
        cfs = np.random.randint(-5, 5, size=3)
        if cfs[0] == 0 or\
           cfs[1]*cfs[1] - 4*cfs[0]*cfs[2] <= 0:
            continue
        roots = np.roots(cfs)
        if np.all(np.equal(np.mod(roots, 1), 0)):
            continue
        poly_coeffs.append(cfs)
        gran_set |= {(np.floor(r), np.ceil(r)) for r in roots}
        break
def gener_2():
    global qglob
    check=False                             #Флаг, отслеживающий,правильно ли сгенерирован двучлен
    while check==False:
        p = random.randint(-10,10)
        q = random.choice([2,4,5])
        qglob = q
        root = p/q
        if root%1!=0:
            check = True
            gran = (math.floor(root), math.ceil(root))
            gran_set.add(gran)
            poly_coeffs.append([1,-root])
while True:
    try:                                                #Проверим, что степень многочлена, введенная пользователем, находится в нужном диапазоне
        n = int(input('Введите степень многочлена: '))
        if n <= 5 and n >= 3:
            break
        else:
            print('Степень должна быть больше 2 и меньше 6')
    except ValueError:
        print("Вводить можно только числа")
granica = 15                                              #Для многочленов ограничим его коэффиценты по модулю числом 15,для того чтобы вычисления не получились слишком громоздкими
flag = True
while len(gran_set)!=n or flag:                         #Пока стпень многочлена не совпадает с выбранной или коэффиценты слишком велики
    left_to_gener = n
    poly_coeffs = []
    gran_set = set()
    while left_to_gener >= 2:                                      #Если степень генерируемого многочлена отличается от желаемой не менее чем на 2, тогда
        gener_3()                                       #Сгенерируем трехчлен - при умножении на генерируемый он повысит его степень на 2
        left_to_gener = left_to_gener - 2
    if left_to_gener == 1:                                         #Если же степень отличается от желаемой только на 1, тогда
        gener_2()                                         #Сгенерируем двучлен - при умножении он повысит степень на 1
    ans = np.poly1d([1])
    for i in poly_coeffs:                                    #Умножим сгенерированные многочлены
        ans*=np.poly1d(i)
    ans*=qglob
    ans = np.poly1d(sokr(ans.c))
    if max(ans.c) <= granica and min(ans.c) >= -granica:    #Если коэффиценты итогового многочлена подходят ограничению по модулю, тогда остановим генерацию
        flag = False
    else:
        flag = True                                         #Иначе запустим генерацию заново
print('\n',ans)


#print({numpy_poly_to_latex(ans)})
#doc = Document('qweqwe')
#doc.append(*numpy_poly_to_latex(ans))
#with doc.create(Section('Математическое выражение')):
#    doc.append(Math(data=[numpy_poly_to_latex(ans)],escape=True))
#doc.generate_tex()

if n != 4:
    if n == 3:
        print('Этот многочлен был сгенерирован из трёхчлена с коэффицентами', *poly_coeffs[0],'и двучлена (x-(',poly_coeffs[1][1],'))')
    else:
        print('Этот многочлен был сгенерирован из трёхчленов с коэффицентами', *poly_coeffs[0],',',*poly_coeffs[1], 'и двучлена (x-(',poly_coeffs[2][1],'))')
else:
    print('Этот многочлен был сгенерирован из трёхчленов с коэффицентами', *poly_coeffs[0], 'и', *poly_coeffs[1])
ask_question = str(input('Вы хотите вывести решение методом Штурма для этого многочлена? (Да/Нет)\n'))
if ask_question != 'Нет':                                   #Если ответ пользовотеля не "Нет"
    coeff_ishod = ans.c
    max_coeff = -100000
    for i in range(1, len(coeff_ishod)):
        if coeff_ishod[i] > max_coeff:
            max_coeff = coeff_ishod[i]                      #Выбираем максимальный из коэффицентов
    poly = ans
    poly*=qglob
    poly = np.poly1d(sokr(poly.c))
    sturm_sequence = []
    sturm_sequence.append(poly)                                              #Генерация ряда Штурма шаг 1 (1-й элемент - сам многочлен)
    sturm_sequence.append(np.poly1d(sokr(np.poly1d(np.polyder(poly)).c)))    #Генереация ряда Шутма шаг 2 (2-й элемент - производная изначального мн-на)
    for i in range(1, len(coeff_ishod) - 2):
        sturm_sequence.append(-(np.poly1d(sokr(delenie(sturm_sequence[i - 1], sturm_sequence[i]).c)))) #Генерация ряда Штурма шаг 3 (для следующих элементов - остаток от деления
    if -((np.polydiv(sturm_sequence[-2], sturm_sequence[-1])[1])[0]) > 0:                    # (n-2)-ого элемента на (n-1)-ый, взятый с противоположным знаком
        sturm_sequence.append(np.poly1d([1]))
    elif -((np.polydiv(sturm_sequence[-2], sturm_sequence[-1])[1])[0]) < 0:
        sturm_sequence.append(np.poly1d([-1]))
    print('Система Штурма для этого многочлена имеет вид:')
    for i in sturm_sequence:
        print(i)                                                          #Вывод ряда Штурма
    verh_granica = math.ceil(abs(1 + (max_coeff / abs(coeff_ishod[0]))))  #Находим границы корней по формуле 1 + (A/|a0|)
    nij_granica = -verh_granica                                           #где A - максимальный среди коэффициентов, a0 - первый элемент
    kolvo_elem = verh_granica - nij_granica
    allsturm_sequence2 = smena(sturm_sequence, nij_granica) - smena(sturm_sequence, verh_granica)
    print('\n')
    table = PrettyTable()                                                 #Создание первой таблицы
    table.add_column(' ', [nij_granica, verh_granica])    #Создание первого столбца
    data_for_pdf_1table = [[nij_granica],[verh_granica]]
    for i in range(len(sturm_sequence)):
        nij_znak = '0'
        verh_znak = '0'
        if np.polyval(sturm_sequence[i], nij_granica) > 0:
            nij_znak = '+'
            data_for_pdf_1table[0].append("+")
        elif np.polyval(sturm_sequence[i], nij_granica) < 0:
            nij_znak = '-'
            data_for_pdf_1table[0].append("-")
        if np.polyval(sturm_sequence[i], verh_granica) > 0:
            verh_znak = '+'
            data_for_pdf_1table[1].append("+")
        elif np.polyval(sturm_sequence[i], verh_granica) < 0:
            verh_znak = '-'
            data_for_pdf_1table[1].append("-")          #Нахождение и запомнинание знака каждого мн-на из ряда Штурма на каждой и границ
        if i == 0:
            table.add_column('f(x)', [nij_znak, verh_znak])
        else:
            table.add_column('f%d(x)' % i, [nij_znak, verh_znak])
    table.add_column('Кол-во перемен знаков', [smena(sturm_sequence, nij_granica), smena(sturm_sequence, verh_granica)]) #Создание послднего стобца
    data_for_pdf_1table[0].append(smena(sturm_sequence, nij_granica))
    data_for_pdf_1table[1].append(smena(sturm_sequence, verh_granica))
    print(table)                                                                    #Вывод первой таблицы
    print('У данного многочлена всего', smena(sturm_sequence, nij_granica) - smena(sturm_sequence, verh_granica), 'корня(ей)') #Вывод кол-ва корней, исходя из первой табл

    table.clear()                      #Создание второй таблицы
    kolvo_ryadov_2tabl = 0
    podh_tochki = []                 #Массив, в который будут входить индексы всех точек в нужных границах
    data_for_pdf_2table = data_for_pdf_2table_stroki = []
    table.field_names = ['']
    for i in range(nij_granica, verh_granica + 1):
        if (smena(sturm_sequence, i - 1) != 0):
            #counter = 0
            table.add_row(['x=%d' % i])
            kolvo_ryadov_2tabl += 1
            podh_tochki.append(i)
            #data_for_pdf_2table[counter].append(i)
            #counter = counter + 1
            if (smena(sturm_sequence, i)) == 0:
                last_podh_tochka = i - 1     #Выбираем точку, после которой нет корней
    postoyanniy_ryad = []            #Постоянный ряд - массив, в котором хранится кол-во перемен знаков для каждой точки
    otveti = []
    for i in range(len(sturm_sequence)):
        temp_ryad = []               #Временный ряд - массив, в котором хранятся знаки для каждого мн-на в каждй точке
        for j in podh_tochki:
            znak = '0'
            if np.polyval(sturm_sequence[i], j) > 0:
                znak = '+'
            elif np.polyval(sturm_sequence[i], j) < 0:
                znak = '-'
            temp_ryad.append(znak)
        data_for_pdf_2table_temp = []
        for i2 in range(len(temp_ryad)):
            data_for_pdf_2table_temp.append(temp_ryad[i2])
        data_for_pdf_2table_stroki.append(data_for_pdf_2table_temp)
        if i == 0:
            table.add_column('f(x)', [x.split().pop() for x in temp_ryad])
        else:
            table.add_column('f%d(x)' % i, [x.split().pop() for x in temp_ryad])
    for i in range(kolvo_ryadov_2tabl):
        postoyanniy_ryad.append(str(smena(sturm_sequence, podh_tochki[i])))
    for i in range(1, kolvo_ryadov_2tabl):
        if smena(sturm_sequence, podh_tochki[i]) != smena(sturm_sequence, podh_tochki[i - 1]):
            otveti.append(podh_tochki[i])         #Добавляем в массив точки, в которых меняется кол-во корней (значит один из корней перед ней)
    table.add_column('Кол-во перемен знаков', [x.split().pop() for x in postoyanniy_ryad])
    print(table)                                   #Вывод второй таблицы
    for i in range(len(otveti)):
        print('%d-й корень лежит между' % (i + 1), otveti[i] - 1, 'и', otveti[i])         #Вывод промежутков с корнями
#str(input())
ask_question2 = str(input('Вы хотите сохранить решение в tex/pdf файл? (Да/Нет)\n'))
if ask_question2 != 'Нет':
    data_for_pdf_2table = [[0] * (len(data_for_pdf_2table_stroki)+ 2) for _ in range((len(data_for_pdf_2table_stroki[0])))]
    for j in range(len(data_for_pdf_2table_stroki[1])):
        data_for_pdf_2table[j][0] = podh_tochki[j]
        data_for_pdf_2table[j][-1] = postoyanniy_ryad[j]
        for i in range(len(data_for_pdf_2table_stroki)):
            data_for_pdf_2table[j][i+1] = data_for_pdf_2table_stroki[i][j]

    almost_pdf = to_latex.construct_latex_str(poly_coeffs, sturm_sequence, data_for_pdf_1table, data_for_pdf_2table, otveti)
    to_latex.generate_tex_file(almost_pdf, 'testing.tex')
    to_latex.generate_pdf_from_tex_file('testing.tex')