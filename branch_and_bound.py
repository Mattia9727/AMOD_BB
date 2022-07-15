import time
from bisect import bisect, insort, insort_left
from collections import namedtuple
from operator import attrgetter
from pprint import pprint
from numpy import linalg
from gurobipy import GRB

import constants
import solver


def sort(sub_li):
    return (sorted(sub_li, reverse=True, key=lambda x: float(x[1])))


# fixed: job già fissati
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


def get_relaxed_obj_func_weight(lambda_list, constr, p):
    weight_c = []
    weight_p = 0
    for i in range(len(p)):
        w = 1
        for j in range(len(constr)):
            v = constr[j]
            if i == v[0]:
                w += lambda_list[j]
            elif i == v[1]:
                w -= lambda_list[j]
            if i == 0:
                weight_p += p[v[1]] * lambda_list[j]
        weight_c.append(w)
    return weight_c, weight_p


def is_solution_feasible(x, v):
    for constr in v:
        idx_0 = x.index(constr[0])
        idx_1 = x.index(constr[1])
        if idx_0 > idx_1:
            return 0
    return 1


# prob: il problema in analisi
# i: il job da aggiungere a prob se non vale la regola di dominanza
# v: vincoli di precedenza
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


def solve_relaxed_problem(problem, p, weight_c, weighted_p):
    xStar = problem.copy()
    xStar.extend(smith_rule(p, weight_c, problem))
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

def ammissible(v,n):
    amm_list = []
    v_copy = v.copy()
    amm_list.append(v_copy[0])
    br=0
    for constr in v_copy:
        new_ins = 1
        if constr == v_copy[0]:
            continue
        for amm in amm_list:
            if br==1:
                break
            br=0
            if constr == amm:
                break
            if (constr[0] in amm) or (constr[1] in amm):
                new_ins = 0
                found = -1
                foundi=-1
                for i in amm_list:
                    if constr==i:
                        continue
                    if constr[0] in i:
                        br = 1
                        if found != -1:
                            for j in amm_list[found]:
                                i.insert(foundi+1,j)
                                foundi+=1
                            amm_list.pop(found)
                        else:
                            i.insert(i.index(constr[0]) + 1, constr[1])
                            found = amm_list.index(i)
                            foundi=i.index(constr[1])
                    elif constr[1] in i:
                        br = 1
                        if found != -1:
                            for j in amm_list[found]:
                                i.insert(foundi,j)
                                foundi+=1
                            amm_list.pop(found)
                        else:
                            i.insert(i.index(constr[1]), constr[0])
                            found = amm_list.index(i)
                            foundi=i.index(constr[0])
            br = 0
        if new_ins == 1:
            amm_list.append(constr)

    ret_list = []
    for i in amm_list:
        for j in i:
            if j not in ret_list:
                ret_list.append(j)
    for i in range(n):
        if i not in ret_list:
            ret_list.append(i)
    return ret_list

def get_feasible_solution(v, p):
    solution = []
    for i in range(len(p)):
        solution.append(i)
    for i in range(len(v)):
        feasible = True
        for constr in v:
            before = constr[0]
            after = constr[1]
            idx_before = solution.index(before)
            idx_after = solution.index(after)
            if idx_before > idx_after:
                solution.remove(before)
                solution.insert(max(0, idx_after-1), before)
                feasible = False
        if feasible:
            break
    c_sum = 0
    c = 0
    for job in solution:
        c = c + p[job]
        c_sum += c
    return c_sum

def subgradiente(prob, p, lambda_list, v):
    k = 50
    h = 1
    z_feasible = get_feasible_solution(v, p)
    lambda_inc = [3,1,5,3,2,4,1,1]
    lambda_list = lambda_inc.copy()
    lowerbound_inc = -GRB.INFINITY
    omega = 1
    epsilon = 1/32
    # w_c, w_p = get_relaxed_obj_func_weight([0]*len(v), v, p)
    # l_lambda_prec = solve_relaxed_problem(prob, p, w_c, w_p)[2]
    # l_lambda_curr = None
    while h < k:
        w_c, w_p = get_relaxed_obj_func_weight(lambda_list, v, p)
        # if l_lambda_curr is not None:
        #     l_lambda_prec = l_lambda_curr
        c_star, l_lambda_curr = solve_relaxed_problem(prob, p, w_c, w_p)[1:]

        if lowerbound_inc < l_lambda_curr:
            print("AGGIORNO DA " + str(lowerbound_inc)+ " A "+str(l_lambda_curr))
            lowerbound_inc = l_lambda_curr
            lambda_inc = lambda_list.copy()
            h = 1
        else:
            h = h+1
       # print("LOWER BOUND " + str(l_lambda_curr))
        s = []
        is_zero = True
        for constr in v:
            subgrad = p[constr[1]] - c_star[constr[1]] + c_star[constr[0]]
            s.append(subgrad)
            if is_zero and subgrad != 0:
                is_zero = False
        if is_zero:
            break
        #norma = linalg.norm(s)
        #omega = (z_feasible - l_lambda_curr) / (norma * norma)
        for i in range(len(lambda_list)):
            lambda_list[i] = max(0,lambda_list[i] + ((omega * s[i])))
        omega = omega/2
        if omega < epsilon:
            break
    return lambda_inc

# xInc: Soluzione incumbent
# zInc: Valore della soluzione incumbent
# Q   : Coda nodi foglia attivi
# m   : Problema corrente
def bb_implementation(p, v, lambda_list):
    n = len(p)
    xInc = None
    zInc = GRB.INFINITY
    Node = namedtuple('Node', ('fixed_schedule', 'father_lb'))
    by_lb = attrgetter('father_lb')
    Q = [Node([], GRB.INFINITY)]                                                    # Lista dei prob da analizzare
    Q.sort(key=by_lb)
    weight_c, weight_p_sum = get_relaxed_obj_func_weight(lambda_list, v, p)         # Calcolo i valori per la funzione obiettivo rilassata
    # Lista dei problemi analizzati e dei LB
    LB_current = GRB.INFINITY
    # Calcolo i valori per la funzione obiettivo rilassata
    t = time.time()
    t2 = time.time()

    while Q != [] and t2 - t <= constants.COMPUTATION_TIME:
        prob = Q.pop(0)                                                             # Prende un problema da analizzare
        if prob[1] > zInc:                                                          # Se il LB del padre è maggiore di zInc, chiudo il problema
            continue
        # Risolvo il rilassamento lagrangiano del problema
        xStar, cStar, zStarRL = solve_relaxed_problem(prob[0], p, weight_c, weight_p_sum)
        LB_current = prob[1]
        # Calcolo il valore della soluzione
        zStar = 0
        c = 0
        if (is_solution_feasible(xStar, v)):                                        # Controllare se xStar è feasible per il problema originale
            for job in xStar:
                c += p[job]
                zStar += c
            if zStar < zInc:                                                        # Aggiorniamo gli incumbent
                xInc = xStar
                zInc = zStar
                if zStar == LB_current:
                    t2 = time.time()
                    return [xInc, zInc, t2 - t,0]
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
    if t2-t>=constants.COMPUTATION_TIME:
        gap = (zInc - LB_current)/LB_current
    return [xInc, zInc, t2 - t, gap]
