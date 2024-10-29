import os
import platform
import subprocess

import numpy as np
import sympy as sp
from sympy.abc import x
from math import gcd

def get_mul_polynoms(poly_a, poly_b):
    n, m = len(poly_a)-1, len(poly_b)-1
    res = [0 for _ in range(n+m+1)]
    for k in range(n+m+1):
        for i in range(k+1):
            if i >= n+1 or k-i >= m+1:
                continue
            res[k] += poly_a[i] * poly_b[k-i]
    return res

def get_latex_poly(poly):
    s = ''
    if 100 >= 2: # для скобок нужно, чтобы кол-во ненулевых коэф-в >= 2
        s += str(sp.Poly(poly, x).as_expr())
    else:
        pass
    s = s.replace('**', '^')
    s = s.replace('*', '')
    s = s.replace(".0", "")
    return s
def get_poly_coefs_str(poly_coeffs: np.array) -> str:
    s = ''
    for polynom in poly_coeffs:
        if 100 >= 2:
            s += '('
        s += get_latex_poly(polynom)
        if 100 >= 2:
            s += ')'
    return s


def construct_latex_str(poly_coeffs_1, poly_coeffs_2, table_1, table_2, roots):
    # poly_coeffs_1 - многочлены, в произведение которых раскладывается сгенерированный
    s = '''\\documentclass{article}
\\usepackage[T2A]{fontenc}
\\usepackage{amssymb}
\\usepackage{amsmath}
\\usepackage{ragged2e}
\\usepackage[a5paper, left=10mm, right=10mm, top=15mm, bottom=20mm]{geometry}
\\usepackage{float}
\\usepackage{wrapfig}
\\usepackage[english, russian]{babel}
\\pagestyle{empty}
\\begin{document}
\\noindent'''
    # Высчитываем коэффициенты многочлена (нужно перемножить)
    res_poly = [1]
    for poly in poly_coeffs_1:
        res_poly = get_mul_polynoms(res_poly, poly)
    for i in range(len(res_poly)):
        res_poly[i] = int(res_poly[i])
    gcd_ = gcd(*res_poly)
    for i in range(len(res_poly)):
        res_poly[i] /= gcd_
    s += f'Исходный многочлен: ${get_latex_poly(res_poly).replace(".0", "")}$.\\\\'
    # Откуда то берём исходный многочлен и вставляем информацию
    s += f'Данный многочлен раскладывается в произведение многочленов следующим образом: $${get_poly_coefs_str(poly_coeffs_1)}.$$'
    s += '\nСистема Штурма для этого многочлена имеет вид:'
    for poly in poly_coeffs_2:
        s += f'$${get_latex_poly(poly).replace(".0", "")}$$ '

    n, m = len(table_1), len(table_1[0]) # n - кол-во строк, m - кол-во столбцов
    s += 'Таблица перемен знаков системы Штурма:\n'
    s += '\\begin{center}\n\\begin{tabular}'
    s += '{'
    for i in range(m):
        s += '|c'
    s += '|}\n'
    # Первая строка с информацией
    s += '\\hline $\\,$ & $f(x)$'
    for i in range(m-3):
        s += f' & $f_{i+1}(x)$'
    s += ' & Кол-во перемен знаков\\\\\n'
    # Оставшиеся строки берутся
    for i in range(n):
        s += '\\hline'
        for j in range(m):
            s += f' ${table_1[i][j]}$ &'
        s = s[:-2] + '\\\\'
    s += '\\hline\n\\end{tabular}\n\\end{center}\n'
    s += 'У данного многочлена всего 5 корня(ей).\n'

    # Вторая таблица
    n, m = len(table_2), len(table_2[0])
    s += '\\begin{center}\n\\begin{tabular}'
    s += '{'
    for i in range(m):
        s += '|c'
    s += '|}\n'
    s += '\\hline $\\,$ & $f(x)$'
    for i in range(m-3):
        s += f' & $f_{i+1}(x)$'
    s += ' & Кол-во перемен знаков\\\\\n'
    # После заполнения первой строки заполняем вторую
    for i in range(n):
        s += f'\\hline $x={table_2[i][0]}$ &'
        for j in range(1, m):
            s += f' ${table_2[i][j]}$ &'
        s = s[:-2] + '\\\\'
    s += '\\hline\n\\end{tabular}\n\\end{center}\n'
    for i in range(len(roots)):
        s += f'{i+1}-й корень лежит между ${roots[i]-1}$ и ${roots[i]}$.\\\\'
    s = s[:-2] + '\end{document}'
    return s

def generate_tex_file(s, pathname):
    f = open(pathname, 'w', encoding='UTF-8')
    f.write(s)
    f.close()

def generate_pdf_from_tex_file(pathname):
    filename, ext = os.path.splitext(pathname)
    pdf = pathname + '.pdf'
    subprocess.run(['pdflatex', '-interaction=nonstopmode', pathname])

if __name__ == '__main__':
    poly_coef = [[1, -2, -1], [-2, 0, 4], [1, 0.5]]
    poly_coef_2 = [[-2, 5, 4, -11, 0, 2],
                   [-5, 10, 6, -11, 0],
                   [-18, 27, 11, -10],
                   [-241, 241, 50],
                   [-2, 1]]
    table_1 = [[-4, '+', '-', '+', '-', '+', '-', 5],
               [4, '-', '-', '-', '-', '-', '-', 0]]
    table_2 = [[-4, '+', '-', '+', '-', '+', '-', 5],
               [-3, '+', '-', '+', '-', '+', '-', 5],
               [-2, '+', '-', '+', '-', '+', '-', 5],
               [-1, '-', '+', '+', '-', '+', '-', 4],
               [0, '+', '0', '-', '+', '+', '-', 3],
               [1, '-', '0', '+', '+', '-', '-', 2],
               [2, '+', '+', '-', '-', '-', '-', 1],
               [3, '-', '-', '-', '-', '-', '-', 0]]
    roots = [-1, 0, 1, 2]
    almost_pdf = construct_latex_str(poly_coef, poly_coef_2, table_1, table_2, roots)
    generate_tex_file(almost_pdf, 'testing.tex')
    generate_pdf_from_tex_file('testing.tex')
