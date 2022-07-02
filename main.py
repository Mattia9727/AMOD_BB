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
    m.addConstr(x[i, j] == 1, name="vincolo di precedenza fissato " + str(i) + str(j) + str(1))
    m.addConstr(x[j, i] == 0, name="vincolo di precedenza fissato " + str(j) + str(i) + str(0))


def get_relaxed_obj_func(c, x, v, mu_list):
    vars = []
    for constr in v:
        vars.append(x[constr[0], constr[1]])
        vars.append(x[constr[1], constr[0]])
    relax_vars = gp.LinExpr(mu_list, vars)
    mu_sum = 0
    for i in range(0,len(mu_list),2):
        mu_sum += mu_list[i]
    return c.sum() - (relax_vars - mu_sum)

def set_bigM(p):
    sum = 0
    for val in p:
        sum += val
    return 10 * sum


# n: numero di job
# p: lista contenente i processing time dei job
# v: vincoli di precedenza
def pli_implementation(n, p, v, relax, mu_list=[]):
    M = set_bigM(p)
    try:
        # Create a new model
        m = gp.Model("scheduling")

        # x[i,j]=1 significa che i precede j
        x = m.addMVar((n, n), vtype=GRB.BINARY, name="x")
        s = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="s")
        c = m.addMVar((1, n), lb=0, vtype=GRB.INTEGER, name="c")

        # Funzione obiettivo: minimizzare somma tempi di completamento
        if relax == 0:
            m.setObjective(c.sum(), GRB.MINIMIZE)
        else:
            m.setObjective(get_relaxed_obj_func(c, x, v, mu_list), GRB.MINIMIZE)

        for k in v:
            if relax == 0:
                set_fixed_precedence(m, x, k[0], k[1])

        # Vincoli
        for i in range(n):
            m.addConstr(c[0, i] == s[0, i] + p[i], name="tempo di completamento" + str(i))
            for j in range(i, n):
                if i != j:
                    m.addConstr(x[i, j] + x[j, i] == 1, name="verso precedenza " + str(i) + " -> " + str(j))

                    m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (x[j, i])), name="precedenza di i su j " + str(i) + str(j))
                    m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * x[i, j]),   name="precedenza di j su i " + str(j) + str(i))

                    # m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (1 - x[i, j])),
                    #             name="precedenza di i su j " + str(i) + str(j))
                    # m.addConstr(s[0, j] >= s[0, i] + p[i] - (M * (x[j, i])),
                    #             name="precedenza di i su j " + str(i) + str(j))
                    #
                    # m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * x[i, j]),
                    #             name="precedenza di j su i " + str(j) + str(i))
                    # m.addConstr(s[0, i] >= s[0, j] + p[j] - (M * (1 - x[j, i])),
                    #             name="precedenza di j su i " + str(j) + str(i))

        # Optimize model
        m.optimize()
        print("Somma tempi di completamento: ", m.ObjVal)
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
    while pr_time:
        prec = file.readline()
        pr_time_list = generation.parse_pr_time(pr_time)
        prec_list = generation.parse_prec(prec)
        mu = generation.mu_gen(2*len(prec_list))
        pli_implementation(10, pr_time_list, prec_list, 0)
        pli_implementation(10, pr_time_list, prec_list, 1, mu)
        pr_time = file.readline()
    #pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)
    #pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 1, [1,1,-1,-1,2,4])
    total = time.time() - t
    print(total)


if __name__ == "__main__":
    main()
