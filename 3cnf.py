import pysat
from pysat import solvers
import os

# Функция, вычисляющая хроматическое число графа
# Выводит самое хроматическое число k и модель
def find_chrom_k(matrix, n):
    flag = False
    k = 0
    while (flag == False):
        k += 1
        solver = solvers.Glucose3()
        clauses = transform(matrix, n, k)
        for clause in clauses:
            solver.add_clause(clause)
        flag = solver.solve()
        model = solver.get_model()
    return k, model

def transform(matrix, n, k):
    # Нам нужно создать для каждой вершины графа k переменных:
    # x11 .. x1k
    #    ...
    # xn1 .. xnk
    
    # функция, которая вычисляет номер перменной, отвечаюдей за v вершину и ее цвет j
    def get_index(v, j):
        return v * k + j + 1
    
    # Далее описываются 3 условия для создания КНФ, решающее раскраску графа
    clauses = []
    
    # Хотя бы одна из k переменных, отвечающих за вершину должна быть 1
    # x_11 or ... or x_1k = 1
    # ...
    # x_n1 or ... or x_nk = 1
    
    for tmp in range(n):
        temp_list = []
        for i in range(k):
            temp_list.append(get_index(tmp, i))
        clauses.append(temp_list)
        
    # Соседение ребра(те, что соеденены ребрем) должны иметь разные цвета:
    # not x_ik v not x_jk, (u, v) in E
    for v in range(n):
        for u in range(v, n):
            if matrix[v][u]:
                for i in range(k):
                    clause = [-get_index(v, i), -get_index(u, i)]
                    clauses.append(clause)
    
    # При этом они должнны быть попарно различными:
    # поэтому добавляем попарное орицание
    # not x_i1 or not x_ij
    # ...
    # not x_i(k-1) or not x_ik
    for v in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                clause = [-get_index(v, c1), -get_index(v, c2)]
                clauses.append(clause)

    return clauses 
    
# функция, создающая таблицу смежности из данных входного файла
def create_data_graph(file):
    data_graph = []
    n, m = 0, 0
    flag = True
    for line in file:
        if flag:
            n, m = map(int, line.strip('\n').split())
            flag = False
            for i in range(n):
                data_graph.append(list())
                for j in range(n):
                    data_graph[i].append(0)
        else:
            f, s = map(int, line.strip('\n').split())
            f -= 1
            s -= 1
            data_graph[f][s] = 1
            data_graph[s][f] = 1

    return data_graph, n, m

# Основная часть программы

# перебираем все входные файлы
for i in range(1, 31):
    if 1 <= i <= 9:
        filename = "0" + str(i) + ".in"
    else:
        filename = str(i) + ".in"
    file = open(filename, 'r')
    
    # Создаем таблицу смежности
    matrix, n, m = create_data_graph(file)
    
    # Далее ищем хроматическое число графа
    model = list()
    k, model = find_chrom_k(matrix, n)
    
    # Создаем файл файл для ответа и помещаем в него сам ответ
    ans = open(filename[:-3] + ".ans", 'w')
    ans.write(str(k) + '\n')
    temp_string = str()

    for v in range(n):
        for c in range(k):
            if model[v*k + c] > 0:
                temp_string = temp_string + str(c + 1) + " " 
    temp_string = temp_string[:-1]
    ans.write(temp_string)
    
    file.close()
    ans.close()
