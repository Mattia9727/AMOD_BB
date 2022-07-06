# prob: sottoproblema
# processing_time: tempi di processamento dei job
# gurobi model
from gurobipy import GRB

import solver

def sort(sub_li):
    return (sorted(sub_li, key=lambda x: x[1]))

def smith_rule(p,w):
    if len(p)==len(w):
        density_list = []
        schedule_list = []
        for i in range(len(p)):
            density_list.append([i,w[i]/p[i]])
        density_list = sort(density_list)
        for i in range(len(p)):
            schedule_list.append(density_list[i][0])
        return schedule_list
    else:
        return "Error: different lengths"

def set_additional_constr(prob, processing_time, model, s_var):
    if prob == []:
        return model
    else:
        current_starting = 0

        for i in prob:
            model.addConstr(s_var[0,i] == current_starting, name="set starting time"+ str(i)+" ="+ str(current_starting))
            current_starting += processing_time[i]

    return model

def is_feasible(x,v,n):
    for constr in v:

        if constr[0]<constr[1]:
            if(x[constr[0]][constr[1]].X == 0):
                return 0
        else:
            if (x[constr[1]][constr[0]].X == 1):
                return 0
    return 1

def get_results(model,n):
    x = []
    for i in range(n):
        x.append([])
        for j in range(n):
            x[i].append(model.getVarByName("x["+str(n*i+j)+"]"))
    return x, model.ObjVal

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

# xInc: Soluzione incumbent
# zInc: Valore della soluzione incumbent
# Q   : Coda nodi foglia attivi
# m   : Problema corrente
def bb_implementation(n, p, v, mu_list):
    xInc = None
    zInc = GRB.INFINITY
    # [] corrisponde alla root
    Q = [[]]
    totalTime = 0
    while Q != []:
        # Prende un problema da analizzare
        prob = Q.pop(0)
        # Risolvo il problema
        model, x, s = solver.pli_implementation(n,p,v,1,mu_list)
        newModel = set_additional_constr(prob, p, model, s)
        try:
            resModel, time= solver.solve_model(newModel)
            totalTime+=time
            xStar, zStar = get_results(resModel,n)
        except Exception:
            print("EXCEPTION")
            continue
        #Bounding
        if(zStar < zInc):
            # Controllare se xStar è feasible per il problema originale
            if(is_feasible(xStar,v,n)):
                # Aggiorniamo gli incumbent
                xInc = xStar
                zInc = zStar
            else:
                #Decomporre in sottoproblemi
                for i in range(n):
                    no_add = 0
                    for j in prob:
                        if i==j:
                            no_add = 1
                            break
                    if no_add == 0:
                        if not dominance_rule(prob,i,v):
                            addProb = prob.copy()
                            addProb.append(i)
                            Q.append(addProb)
    #print("RISULTATO BB: " + str(zInc))
    return [xInc, zInc], totalTime
