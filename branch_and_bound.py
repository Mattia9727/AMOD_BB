from gurobipy import GRB
import solver

def sort(sub_li):
    return (sorted(sub_li, reverse = True, key=lambda x: float(x[1])))

# fixed: job già fissati
def smith_rule(p,w,fixed):
    if len(p)==len(w):
        density_list = []
        schedule_list = []
        for i in range(len(p)):
            if not fixed.count(i):
                density_list.append([i,w[i]/p[i]])
        density_list = sort(density_list)
        for i in range(len(density_list)):
            schedule_list.append(density_list[i][0])
        return schedule_list
    else:
        return "Error: different lengths"

def is_feasible(x,v):
    for constr in v:
        idx_0 = x.index(constr[0])
        idx_1 = x.index(constr[1])
        if idx_0 > idx_1:
            return 0
    return 1

# prob: il problema in analisi
# i: il job da aggiungere a prob se non vale la regola di dominanza
# v: vincoli di precedenza
def dominance_rule(prob,i,v):
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
    xStar.extend(smith_rule(p,weight_c,problem))
    # Calcolo il valore corrispondente alla soluzione trovata
    zStar = 0
    c = 0
    for job in xStar:
        c += p[job]
        zStar += (c* weight_c[job])
    zStar += weighted_p
    return xStar, zStar

# xInc: Soluzione incumbent
# zInc: Valore della soluzione incumbent
# Q   : Coda nodi foglia attivi
# m   : Problema corrente
def bb_implementation(n, p, v, lambda_list):
    xInc = None
    zInc = GRB.INFINITY
    # [] corrisponde alla root
    # Lista dei prob da analizzare
    Q = [[[], GRB.INFINITY]]
    # Lista dei problemi analizzati e dei LB
    LB_root = GRB.INFINITY
    #Calcolo i valori per la funzione obiettivo rilassata
    weight_c, weight_p_sum = solver.get_relaxed_obj_func_weight(lambda_list, v, p)
    count=0
    while Q != []:
        # Prende un problema da analizzare
        prob = Q.pop(0)
        if prob[1] > zInc:
            continue
        count +=1
        # Risolvo il problema
        xStar, zStarRL = solve_relaxed_problem(prob[0], p, weight_c, weight_p_sum)
        if(prob[0] == []):
            LB_root = zStarRL
        # Aggiungere a Q-res
        # if zStarRL != LB_root:
        #     Q_res.append([prob[0], zStarRL])
        # Calcolo il valore della soluzione
        zStar = 0
        c = 0
        for job in xStar:
            c += p[job]
            zStar += c
        #Bounding
        if zStar < zInc:
            # Controllare se xStar è feasible per il problema originale
            if(is_feasible(xStar,v)):
                # Aggiorniamo gli incumbent
                xInc = xStar
                zInc = zStar
                if zStar == LB_root:
                    return [xInc, zInc]
    #Decomporre in sottoproblemi
        for i in range(n):
            no_add = 0
            for j in prob[0]:
                if i==j:
                    no_add = 1
                    break
            if no_add == 0:
                if not dominance_rule(prob[0],i,v):
                    addProb = []
                    addProb.append(prob[0].copy())
                    addProb[0].append(i)
                    addProb.append(zStarRL)
                    Q.append(addProb)
    #print("RISULTATO BB: " + str(zInc))
    print(count)
    return [xInc, zInc]
