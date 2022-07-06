import time
from pprint import pprint

import gurobipy as gp
from gurobipy import GRB
import generator

# m: gurobi model
# x: variabili di precedenza
# i,j: indici da fissare
def set_fixed_precedence(m, c, v, p):
    i = v[0]
    j = v[1]
    m.addConstr(c[0, j] - p[j] >= c[0, i], name="Vincolo di precedenza fissato "+str(i)+str(j))

def get_relaxed_obj_func(c, x, v, mu_list):
    vars = []
    mu_sum = 0
    for i in range(len(v)):
        constr = v[i]
        if constr[0] < constr[1]:
            vars.append(x[constr[0]][constr[1]])   # x=1
            mu_sum += mu_list[i]
        else:
            vars.append(x[constr[1]][constr[0]])   # x=0
    relax_vars = gp.LinExpr(mu_list, vars)

    return c.sum() + (relax_vars - mu_sum)

def set_bigM(p):
    sum = 0
    for val in p:
        sum += val
    return 10 * sum


# n: numero di job
# p: lista contenente i processing time dei job
# v: vincoli di precedenza
def pli_implementation(n, p, v, relax, mu_list=None):
    M = set_bigM(p)
    try:
        # Create a new model
        # with gp.Env() as env, gp.Model("scheduling",env=env) as m:
        env = gp.Env()
        m = gp.Model("scheduling",env=env)
        # x[i,j]=1 significa che i precede j
        x=[]
        for i in range(n):
            x.append([])
            for j in range(n):
                if j>i:
                    x[i].append(m.addVar(vtype=GRB.BINARY, name="x["+str(n*i+j)+"]"))
                else:
                    x[i].append(None)
        s = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="s")
        c = m.addMVar((1, n), lb=0, vtype=GRB.CONTINUOUS, name="c")

        # Funzione obiettivo: minimizzare somma tempi di completamento
        if relax == 0:
            m.setObjective(c.sum(), GRB.MINIMIZE)
        else:
            m.setObjective(get_relaxed_obj_func(c, x, v, mu_list), GRB.MINIMIZE)
        for k in v:
            if relax == 0:
                set_fixed_precedence(m, c, k, p)
        # Vincoli
        for i in range(n):
            m.addConstr(c[0, i] == s[0, i] + p[i], name="tempo di completamento" + str(i))
            for j in range(n):

                if i != j and x[i][j] is not None:
                    m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (1-x[i][j])), name="precedenza di i su j " + str(i) + str(j))
                    m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * x[i][j]),   name="precedenza di j su i " + str(j) + str(i))
        return m,x,s

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')

def solve_model(m):
    # Optimize model
    try:
        t = time.time()
        m.optimize()
        total = time.time() - t
        return m, total

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        raise Exception