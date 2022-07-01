import time

import gurobipy as gp
from gurobipy import GRB
import generation


def bb_implementation():
    pass


# m: gurobi model
# x: variabili di precedenza
# i,j: indici da fissare
def set_fixed_precedence(m, x, i, j):
    m.addConstr(x[i, j] == 1, name="vincolo di precedenza fissato "+str(i)+str(j)+str(1))
    m.addConstr(x[j, i] == 0, name="vincolo di precedenza fissato "+str(j)+str(i)+str(0))


# n: numero di job
# p: lista contenente i processing time dei job
# v: vincoli di precedenza
def pli_implementation(n, p, v):
    M = 1000
    try:
        # Create a new model
        m = gp.Model("scheduling")

        # x[i,j]=1 significa che i precede j
        x = m.addMVar((n, n), vtype=GRB.BINARY, name="x")
        s = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="s")
        c = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="c")

        # Funzione obiettivo: minimizzare somma tempi di completamento
        m.setObjective(c.sum(), GRB.MINIMIZE)

        # Vincoli
        for i in range(n):
            m.addConstr(c[0, i] == s[0, i] + p[i], name="tempo di completamento" + str(i))
            for j in range(i, n):
                if i != j:

                    m.addConstr(x[i, j] + x[j, i] == 1, name="x" + str(i) + str(j))
                    for k in v:
                        if k == [i, j]:
                            set_fixed_precedence(m,x,i,j)
                        elif k == [j, i]:
                            set_fixed_precedence(m,x,j,i)


                    m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (1 - x[i, j])),
                                name="precedenza di i su j " + str(i) + str(j))
                    m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (x[j, i])),
                                name="precedenza di i su j " + str(i) + str(j))

                    m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * x[i, j]),
                                name="precedenza di j su i " + str(j) + str(i))
                    m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * (1 - x[j, i])),
                                name="precedenza di j su i " + str(j) + str(i))

        # Optimize model
        consts =m.getConstrs()
        m.optimize()
        consts = m.getConstrs()
        print("Somma tempi di completamento", m.ObjVal)
        print(x.X)
        print(c.X)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')



def main():
    t = time.time()
    file = open("instances.txt","r")
    pr_time = file.readline()
    while not pr_time == None and pr_time:
        prec = file.readline()
        if pr_time[-1:] == "\n":
            pr_time = pr_time[:-1]
        pr_time_list = generation.parse_pr_time(pr_time)
        prec_list = generation.parse_prec(prec)
        pli_implementation(10, pr_time_list, prec_list)
        pr_time = file.readline()

    total = time.time() - t
    print(total)


if __name__ == "__main__":
    main()
