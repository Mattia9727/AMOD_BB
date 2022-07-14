import csv
import time

import gurobipy as gp
from gurobipy import GRB

import branch_and_bound
import generator
import solver


def main():
    # t = time.time()
    header = ["#Job", "#Precedenze", "Lista mu", "Risultato PLI", "Risultato BB", "Tempo PLI", "Tempo BB"]
    pTimes = [49, 37, 32, 2, 21, 9, 49, 12, 20, 4, 11, 5, 36, 78, 4, 55, 34, 19, 98, 76, 33]
    mu = []
    a, b = [12, 35, 47, 21, 16, 46, 20, 4, 11, 23, 4, 11], [[8, 7], [6, 1], [1, 4]]
    prova = "7,8_13,6_10,5_7,18_1,5_12,14_4,6_16,12_9,6_10,19"
    provaP = generator.parse_prec(prova)
    print(ammissible(provaP,20))
    return
    # t = time.time()
    # objVal, objBound, gap, total_pli = solver.pli_implementation(a,b)
    # total_pli = time.time() - t
    # t = time.time()
    # xz = branch_and_bound.bb_implementation(a,b, [0,0,1])
    # total = time.time() - t

    # print("SIAMO AL JOB: "+str(i))
    pr_time_list= []
    prec_list = []

    txt_file = "instances_20_10_1.txt"
    csv_file = "instances_20_10_1.csv"

    with open(csv_file, 'w', encoding='UTF8') as f:
        f.close()

    import csv
    with open(csv_file, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)

    with open(txt_file, "r", encoding='UTF8') as instances:
        pr_time_list = generator.parse_pr_time(instances.readline())
        prec_list = generator.parse_prec(instances.readline())
        pr_time = instances.readline()
        for i in range(len(prec_list)):
            mu.append(1)
        while pr_time:
            prec = instances.readline()
            pr_time_list = generator.parse_pr_time(pr_time)
            prec_list = generator.parse_prec(prec)
            # mu = generator.mu_gen(len(prec_list))
            objVal, objBound, gap, total_pli = solver.pli_implementation(pr_time_list, prec_list)
            x,z,total_bb = branch_and_bound.bb_implementation(pr_time_list, prec_list, mu)
            pr_time = instances.readline()

            data = [len(pr_time_list), len(prec_list), str(mu), objVal, objBound, gap, z, total_pli, total_bb]

            with open(csv_file, 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the data
                writer.writerow(data)

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
