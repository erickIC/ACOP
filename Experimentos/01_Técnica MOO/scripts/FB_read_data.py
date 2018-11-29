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
        osnrRipple.append(float(str[0].replace(',', '.')))
        osnr.append(float(str[1].replace(',', '.')))
    f.close()
    return osnrRipple, osnr

def read_data_file_metric(arquivo):
    return_set = []
    f = open(arquivo, 'r+')
    for line in f:
        str = line.split('\t')
        temp_set = []
        temp_set.append(float(str[0].replace(',', '.')))
        temp_set.append(float(str[1].replace(',', '.')))
        return_set.append(temp_set)
    f.close()
    return return_set


def generate_pareto_file(directory):
    pareto = []
    caminhos = [os.path.join(directory, nome) for nome in os.listdir(directory)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    par = [arq for arq in arquivos if arq.lower().endswith("_par.txt")]
    amps = [arq for arq in arquivos if arq.lower().endswith("_amp.txt")]
    for filePar, fileAmps in zip(par,amps):
        fPar = open(filePar, 'r+')
        fAmps = open(fileAmps, 'r+')
        for linePar, lineAmp in zip(fPar, fAmps):
            solution_string = linePar.replace(',', '.').split('\t')  # type: List[str]
            solution = [float(solution_string[0]), float(solution_string[1])]
            solution.append(lineAmp)
            pareto = update_pareto(solution, pareto)
        fPar.close()
        fAmps.close()

    fPar = open(directory + '_pareto.txt', 'w')
    fAmps = open(directory + '_pareto_amps.txt', 'w')
    for i in range(len(pareto)):
        fPar.write(str(pareto[i][0]))
        fPar.write('\t')
        fPar.write(str(pareto[i][1]))
        fPar.write('\n')
        fAmps.write(pareto[i][2])
    fPar.close()
    fAmps.close()


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
    objectives = 2
    lost_in_all_dimensions = True
    win_in_all_dimensions = True
    for i in range(objectives):
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

#generate_pareto_file('fb_e1_2a')
#generate_pareto_file('fb_e1_3a')
#generate_pareto_file('fb_e1_4a')
