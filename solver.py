import time

import gurobipy as gp
from gurobipy import GRB

import constants

"""
    Aggiunge i vincoli di precedenza fissati a priori al modello di gurobi
    
    Param: 
        m: modello gurobi
        c: lista di variabili che rappresentano i tempi di completamento dei job
        v: lista delle relazioni di precedenza fissate
        p: lista dei processing time dei job
        
"""


def set_fixed_precedence(m, c, v, p):
    i = v[0]
    j = v[1]
    m.addConstr(c[0, j] - p[j] >= c[0, i], name="Vincolo di precedenza fissato " + str(i) + str(j))


"""
    Imposta il valore del bigM pari a alla somma dei processing time dei job + il massimo processing time
    
    Param:
        p: lista dei processing time
    
    Output:
        valore del big M utilizzato
"""


def set_bigM(p):
    sum = 0
    for val in p:
        sum += val
    return sum + max(p)


"""
    Implementa la costruzione e risoluzione del modello PLI tramite le API di GUROBI
    
    Param: 
        p: lista dei processing time 
        v: lista delle precedenze fissate
        
    Output:
        valore della soluzione migliore trovata
        lowerbound migliore trovato
        gap tra soluzione migliore trovata e LB trovato
        tempo totale di esecuzione
"""


def pli_implementation(p, v):
    n = len(p)
    M = set_bigM(p)
    try:
        env = gp.Env()
        m = gp.Model("1|prec|sum(Ci)", env=env)
        # x[i,j]=1 significa che i precede j
        x = []
        for i in range(n):
            x.append([])
            for j in range(n):
                if j > i:
                    x[i].append(m.addVar(vtype=GRB.BINARY, name="x[" + str(n * i + j) + "]"))
                else:
                    x[i].append(None)
        c = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="c")

        # Funzione obiettivo: minimizzare somma tempi di completamento
        m.setObjective(c.sum(), GRB.MINIMIZE)

        for k in v:
            i = k[0]
            j = k[1]
            m.addConstr(c[0, j] - p[j] >= c[0, i], name="Vincolo di precedenza fissato " + str(i) + str(j))
        # Vincoli
        for i in range(n):
            m.addConstr(c[0, i] >= p[i], name="tempo di completamento" + str(i))
            for j in range(n):
                if i != j and x[i][j] is not None:
                    m.addConstr(c[0, j] >= c[0, i] + p[j] - (M * (1 - x[i][j])),
                                name="precedenza di i su j " + str(i) + str(j))
                    m.addConstr(c[0, i] >= c[0, j] + p[i] - (M * x[i][j]),
                                name="precedenza di j su i " + str(j) + str(i))

        m.setParam("TimeLimit", constants.COMPUTATION_TIME)

        t = time.time()
        m.optimize()
        total = time.time() - t
        return m.ObjVal, m.ObjBound, m.MIPGap, total

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
