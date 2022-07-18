import time
from bisect import insort
from collections import namedtuple
from operator import attrgetter

from gurobipy import GRB

import constants


def sort(sub_li):
    return sorted(sub_li, reverse=True, key=lambda x: float(x[1]))


"""
    Questa funzione implementa la regola di Smith
    
    Param: 
        p: lista di processing time job
        fixed: job già fissati
        w: lista dei pesi delle variabili della funzione obiettivo
    
    Output: 
        Scheduling ottimo  del rilassamento   
"""


def smith_rule(p, w, fixed):
    if len(p) == len(w):
        density_list = []
        schedule_list = []
        for i in range(len(p)):
            if not fixed.count(i):
                density_list.append([i, w[i] / p[i]])
        density_list = sort(density_list)
        for i in range(len(density_list)):
            schedule_list.append(density_list[i][0])
        return schedule_list
    else:
        return "Error: different lengths"


"""
    Questa funzione calcola i pesi delle variabili della funzione obiettivo e il termine costante
    relativo alla somma dei processing time pesati con i lambda

    Param: 
        lambda_list: lista dei moltiplicatori lagrangiani
        constr: lista delle precedenze fissate
        p: lista dei processing time

    Output: 
        lista dei pesi delle variabili
        somma pesata dei processing time
"""


def get_relaxed_obj_func_weight(lambda_list, constr, p):
    weight_c = []
    weighted_p = 0
    for i in range(len(p)):
        w = 1
        for j in range(len(constr)):
            v = constr[j]
            if i == v[0]:
                w += lambda_list[j]
            elif i == v[1]:
                w -= lambda_list[j]
            if i == 0:
                weighted_p += p[v[1]] * lambda_list[j]
        weight_c.append(w)
    return weight_c, weighted_p


"""
    Controlla se un certo schedule è ammissibile per le precedenze fissate oppure no
    
    Param:
        x: schedule da verificare
        v: insieme delle precedenze
    Output:
        1 se lo schedule è ammissibile
        0 altrimenti
"""


def is_solution_feasible(x, v):
    for constr in v:
        idx_0 = x.index(constr[0])
        idx_1 = x.index(constr[1])
        if idx_0 > idx_1:
            return 0
    return 1


""" 
    Controlla se, aggiungendo un job a un sottoschedule, esso rimane ammissibile oppure no
    
    Param: 
        prob: il problema in analisi
        i: il job da aggiungere
        v: lista dei vincoli
    
    Output: 
        1 se il sottoschedule è ammissibile
        0 altrimenti
"""


def is_new_problem_feasible(prob, i, v):
    job_in_constr = []
    for prec in v:
        if i == prec[1]:
            job_in_constr.append(prec[0])

    if not job_in_constr:
        return 0
    else:
        for j in prob:
            if j in job_in_constr:
                job_in_constr.remove(j)
        if job_in_constr:
            return 1
        return 0


""" 
    Risolve il sottoproblema utilizzando la regola di Smith

    Param: 
        prob: il problema in analisi
        p: lista dei processing time
        weight_c: lista dei pesi delle variabili
        weighted_p: somma pesata dei processing time

    Output: 
        scheduling ottimo,
        lista dei tempi di completamento relativi allo scheduling ottimo,
        valore della soluzione ottima del problema rilassato
"""


def solve_relaxed_problem(prob, p, weight_c, weighted_p):
    xStar = prob.copy()
    xStar.extend(smith_rule(p, weight_c, prob))
    # Calcolo il valore corrispondente alla soluzione trovata
    zStar = 0
    c = 0
    cStar = []
    for job in xStar:
        c += p[job]
        cStar.append(c)
        zStar += (c * weight_c[job])
    zStar += weighted_p
    return xStar, cStar, zStar


"""
    Applica il metodo del subgradiente per calcolare i moltiplicatori lagrangiani ottimi.
    Lo pseudocodice dell'algoritmo è stato preso dalle slides del prof. Sassano 
    http://www.diag.uniroma1.it//~sassano/Slides/OCO2_2016/OCO2_RilassamentoLagrangiano_e_Subgradiente.pdf
    
    Param: 
        prob: problema per cui calcolare i migliori moltiplicatori
        p: lista dei processing time dei job
        v: lista delle precedenze fissate
    
    Output:
        lista dei moltiplicatori lagrangiani ottimi per il problema dato
            
"""


def subgradiente(prob, p, v):
    lambda_inc = [0] * len(v)
    lambda_list = lambda_inc.copy()
    lowerbound_inc = -GRB.INFINITY
    omega = 1
    epsilon = 1 / 32
    while omega < epsilon:
        w_c, w_p = get_relaxed_obj_func_weight(lambda_list, v, p)
        c_star, l_lambda_curr = solve_relaxed_problem(prob, p, w_c, w_p)[1:]
        if lowerbound_inc < l_lambda_curr:
            lowerbound_inc = l_lambda_curr
            lambda_inc = lambda_list.copy()
        s = []
        for constr in v:
            subgrad = p[constr[1]] - c_star[constr[1]] + c_star[constr[0]]
            s.append(subgrad)
        for i in range(len(lambda_list)):
            lambda_list[i] = max(0, lambda_list[i] + (omega * s[i]))
        omega = omega / 2
    return lambda_inc


""" 
    Implementazione dell'algoritmo di Branch & Bound relativo al problema 1|prec|ΣCi

    Param: 
        p: lista dei processing time
        v: lista delle precedenze tra job
        lambda_list: lista dei lambda

    Output: 
        xInc: soluzione migliore trovata
        zInc: valore della soluzione migliore trovata
        t2-t: tempo di esecuzione dell'algoritmo
        gap: gap tra soluzione migliore trovata e LB trovato
"""


def bb_implementation(p, v, lambda_list):
    n = len(p)
    xInc = None
    zInc = GRB.INFINITY
    # [] corrisponde alla root
    Node = namedtuple('Node', ('fixed_schedule', 'father_lb'))
    by_lb = attrgetter('father_lb')
    Q = [Node([], GRB.INFINITY)]  # Lista dei prob da analizzare
    Q.sort(key=by_lb)
    weight_c, weight_p_sum = get_relaxed_obj_func_weight(lambda_list, v,
                                                         p)  # Calcolo i valori per la funzione obiettivo rilassata
    # Lista dei problemi analizzati e dei LB
    LB_current = GRB.INFINITY
    # Calcolo i valori per la funzione obiettivo rilassata
    t = time.time()
    t2 = time.time()

    while Q != [] and t2 - t <= constants.COMPUTATION_TIME:
        prob = Q.pop(0)  # Prende un problema da analizzare
        if prob[1] > zInc:  # Se il LB del padre è maggiore di zInc, chiudo il problema
            continue
        # Risolvo il rilassamento lagrangiano del problema
        xStar, cStar, zStarRL = solve_relaxed_problem(prob[0], p, weight_c, weight_p_sum)
        LB_current = prob[1]
        # Calcolo il valore della soluzione
        zStar = 0
        c = 0
        if (is_solution_feasible(xStar, v)):  # Controllare se xStar è feasible per il problema originale
            for job in xStar:
                c += p[job]
                zStar += c
            if zStar < zInc:  # Aggiorniamo gli incumbent
                xInc = xStar
                zInc = zStar
                if zStar == LB_current:
                    t2 = time.time()
                    return [xInc, zInc, t2 - t, 0]
        # Decomporre in sottoproblemi
        for i in range(n):
            no_add = 0
            for j in prob[0]:
                if i == j:
                    no_add = 1
                    break
            if no_add == 0:
                if not is_new_problem_feasible(prob[0], i, v):
                    # Branching
                    addProb = prob[0].copy()
                    addProb.append(i)
                    new_node = Node(addProb, zStarRL)
                    insort(Q, new_node, key=by_lb)
        t2 = time.time()
    gap = 0
    if t2 - t >= constants.COMPUTATION_TIME:
        gap = (zInc - LB_current) / zInc
    return [xInc, zInc, t2 - t, gap]
