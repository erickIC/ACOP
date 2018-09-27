import os
from typing import List
import numpy as np

import matplotlib.pyplot as plt


def read_data_file(arquivo):
    osnrRipple = []
    osnr = []
    f = open(arquivo, 'r+')
    for line in f:
        str = line.split('\t')
        osnrRipple.append(str[0].replace(',', '.'))
        osnr.append(str[1].replace(',', '.'))
    f.close()
    return osnrRipple, osnr


def generate_pareto_file(directory):
    pareto = []
    caminhos = [os.path.join(directory, nome) for nome in os.listdir(directory)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    par = [arq for arq in arquivos if arq.lower().endswith("_par.txt")]
    for file in par:
        f = open(file, 'r+')
        for line in f:
            solution_string = line.replace(',', '.').split('\t')  # type: List[str]
            solution = [float(solution_string[0]), float(solution_string[1])]
            pareto = update_pareto(solution, pareto)
        f.close()

    f = open(directory + '_pareto.txt', 'w')
    for i in range(len(pareto)):
        f.write(str(pareto[i][0]))
        f.write('\t')
        f.write(str(pareto[i][1]))
        f.write('\n')
    f.close()


def update_pareto(candidate_solution, pareto):
    for i in range(len(pareto)):
        # A solution inside the pareto dominates the candidate solution
        if compare_by_dominance(pareto[i], candidate_solution) == 1 \
                or candidate_solution == pareto[i]:
            return pareto

    temp_pareto = []
    for i in range(len(pareto)):
        # A solution inside the pareto is dominated by the candidate solution
        # Remove the dominated solution
        if compare_by_dominance(candidate_solution, pareto[i]) != 1:
            temp_pareto.append(pareto[i])

    temp_pareto.append(candidate_solution)
    return temp_pareto


def compare_by_dominance(solution1, solution2):
    lost_in_all_dimensions = True
    win_in_all_dimensions = True
    for i in range(len(solution1)):
        if i == 1:  # OSNR
            solution1[i] *= -1
            solution2[i] *= -1

        if solution1[i] > solution2[i]: win_in_all_dimensions = False
        if solution1[i] < solution2[i]: lost_in_all_dimensions = False

        if i == 1:  # OSNR
            solution1[i] *= -1
            solution2[i] *= -1

        if not win_in_all_dimensions and not lost_in_all_dimensions: return 0  # incomparable

    if win_in_all_dimensions and lost_in_all_dimensions: return -1  # equal
    if win_in_all_dimensions: return 1  # sl1 dominates sl2
    if lost_in_all_dimensions: return -1  # sl1 is dominated by sl2

    return 0


def read_data(pasta):
    osnrRipple = []
    osnr = []
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    par = [arq for arq in arquivos if arq.lower().endswith("_par.txt")]
    for file in par:
        f = open(file, 'r+')
        for line in f:
            str = line.split('\t')
            if not (file.lower().endswith("pareto_par.txt")):
                osnrRipple.append(str[0].replace(',', '.'))
                osnr.append(str[1].replace(',', '.'))
        f.close()
    return osnrRipple, osnr;

generate_pareto_file('fb_e2_2a')
generate_pareto_file('fb_e2_3a')
generate_pareto_file('fb_e2_4a')
