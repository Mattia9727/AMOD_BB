import time

import gurobipy as gp
from gurobipy import GRB

import branch_and_bound
import generator
import solver



def main():
    t = time.time()
    file = open("instances.txt","r")
    # pr_time_list = generator.parse_pr_time(file.readline())
    # prec_list = generator.parse_prec(file.readline())

    # mu = generator.mu_gen(2 * len(prec_list))
    mu = []
    # for i in range(len(prec_list)):
    #     mu.append(1)
    # while pr_time:
    #     prec = file.readline()
    #     pr_time_list = generator.parse_pr_time(pr_time)
    #     prec_list = generator.parse_prec(prec)
    #     mu = generator.mu_gen(2*len(prec_list))
    #     solver.pli_implementation(10, pr_time_list, prec_list, 0)
    #     solver.pli_implementation(10, pr_time_list, prec_list, 1, mu)
    #     pr_time = file.readline()

#CALCOLO TEMPO PLI

    # t = time.time()
    m, total_pli = resolver.solve_model(resolver.pli_implementation(len(pr_time_list), pr_time_list, prec_list, 0)[0])[1]
    # total_pli = resolver.solve_model(resolver.pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)[0])[1]
    # total = time.time() - t


#CALCOLO TEMPO BB


    # print("\n\n\n")
    #
    # print("CALCOLO CON PLI")
    # print(total_pli)
    # print(m.ObjVal)
    #
    # print("CALCOLO CON BB")
    # print(total)
    # print(xz[1])
    # print("\n\n\n")



if __name__ == "__main__":
    main()
    #solver.pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)
    #pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 1, [1,1,-1,-1,2,4])