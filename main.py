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

    data = []
    header = ["#Job", "#Precedenze", "Lista mu", "Risultato PLI", "Risultato BB", "Tempo PLI", "Tempo BB"]
    pTimes = [49, 37, 32, 2, 21, 9, 49, 12, 20, 4, 11, 5, 36, 78, 4, 55, 34, 19, 98, 76, 33]
    mu = []
    a,b = [12,35,47,21,16,46,20,4,11,23,4,11], [[8,7],[6,1],[1,4]]
    t = time.time()
    objVal, objBound, gap, total_pli = solver.pli_implementation(a,b)
    total_pli = time.time() - t
    t = time.time()
    xz = branch_and_bound.bb_implementation(a,b, [0,0,1])
    total = time.time() - t
                # for i in range (5,16):
                #     print("SIAMO AL JOB: "+str(i ))
                #     pr_time_list= []
                #     prec_list = []
                #     for j in range(i):
                #         pr_time_list.append(pTimes[j])
                #         if j!=0 and j<round(float(i/2)):
                #             prec_list.append([j-1,j])
                #             mu.append(1)
                #
                #     while (len(prec_list)!= 0):
                #         m, total_pli = solver.solve_model(solver.pli_implementation(len(pr_time_list), pr_time_list, prec_list, 0)[0])
                #         xz, total_bb = branch_and_bound.bb_implementation(len(pr_time_list), pr_time_list, prec_list, mu)
                #
                #         data.append([str(len(pr_time_list)), str(len(prec_list)), str(mu), total_pli, total_bb])
                #
                #         prec_list.pop(len(prec_list) - 1)
                #         mu.pop(len(mu) - 1)
                #
                # import csv
                #
                # with open('results.csv', 'w', encoding='UTF8') as f:
                #     writer = csv.writer(f)
                #     # write the header
                #     writer.writerow(header)
                #
                #     # write the data
                #     writer.writerows(data)

    # total_pli = solver.solve_model(solver.pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)[0])[1]
    # total = time.time() - t


#CALCOLO TEMPO BB


    print("\n\n\n")
    #
    print("CALCOLO CON PLI")
    print(total_pli)
    print(objVal)
    print(objBound)
    print(gap)
    print("\n")
    #
    print("CALCOLO CON BB")
    print(total)
    print(xz)






if __name__ == "__main__":
    main()
