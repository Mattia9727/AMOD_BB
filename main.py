import time

import gurobipy as gp
from gurobipy import GRB
import generation
import resolver

# prob: sottoproblema
# processing_time: tempi di processamento dei job
# gurobi model
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
        print(constr)
        print(x)
        if(x[constr[0] * n + constr[1]].X == 0):
            return 0
    return 1

def get_results(model,n):
    x = []
    for i in range(n*n):
        x.append(model.getVarByName("x["+ str(i) +"]"))
    return x, model.ObjVal

def dominance_rule(prob,i,v):
    job_in_constr = -1
    for prec in v:
        if i == prec[1]:
            job_in_constr = prec[0]
    if prob == []:
        if job_in_constr != -1:
            return 1
        else:
            return 0
    else:
        for j in prob:
            if job_in_constr != -1:
                if j == job_in_constr:
                    return 0
            else:
                return 0
    return 1

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
        model, x, s = resolver.pli_implementation(n,p,v,1,mu_list)
        newModel = set_additional_constr(prob, p, model, s)
        try:
            resModel, time= resolver.solve_model(newModel)
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


def main():
    t = time.time()
    file = open("instances.txt","r")
    pr_time = file.readline()
    pr_time_list = generation.parse_pr_time(pr_time)
    prec = file.readline()
    prec_list = generation.parse_prec(prec)
    mu = generation.mu_gen(2 * len(prec_list))
    # while pr_time:
    #     prec = file.readline()
    #     pr_time_list = generation.parse_pr_time(pr_time)
    #     prec_list = generation.parse_prec(prec)
    #     mu = generation.mu_gen(2*len(prec_list))
    #     resolver.pli_implementation(10, pr_time_list, prec_list, 0)
    #     resolver.pli_implementation(10, pr_time_list, prec_list, 1, mu)
    #     pr_time = file.readline()

#CALCOLO TEMPO PLI

    # t = time.time()
    m, total_pli = resolver.solve_model(resolver.pli_implementation(len(pr_time_list), pr_time_list, prec_list, 0)[0])[1]
    # total_pli = resolver.solve_model(resolver.pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)[0])[1]
    # total = time.time() - t


#CALCOLO TEMPO BB

    xz, total = bb_implementation(len(pr_time_list), pr_time_list, prec_list, mu)
    print("\n\n\n")
    print("CALCOLO CON PLI")
    print(total_pli)
    print(m.ObjVal)
    print("CALCOLO CON BB")
    print(total)
    print(xz[1])
    print("\n\n\n")

if __name__ == "__main__":
    main()
