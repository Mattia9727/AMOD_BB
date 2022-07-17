import csv
import time

import gurobipy as gp
from gurobipy import GRB

import branch_and_bound
import generator
import solver


def main():
    # t = time.time()
    header = ["#Job", "#Precedenze", "Lista mu", "Risultato PLI", "Bound PLI", "Gap PLI", "Risultato BB", "Gap BB", "Tempo PLI", "Tempo BB"]
    pTimes = [49, 37, 32, 2, 21, 9, 49, 12, 20, 4, 11, 5, 36, 78, 4, 55, 34, 19, 98, 76, 33]

    a, b = [12, 35, 47, 21, 16, 46, 20, 4, 11, 23, 4, 11], [[8, 7], [6, 1], [1, 4]]
    prova = "7,8_13,6_10,5_7,18_1,5_12,14_4,6_16,12_9,6_10,19"
    provaP = generator.parse_prec(prova)
    # t = time.time()
    # objVal, objBound, gap, total_pli = solver.pli_implementation(a,b)
    # total_pli = time.time() - t
    # t = time.time()
    # xz = branch_and_bound.bb_implementation(a,b, [1,1,1])



    # print("\n\n\n")
    #
    # print("CALCOLO CON PLI")
    # print(total_pli)
    # print(objVal)
    # print(objBound)
    # print(gap)
    # print("\n")
    #
    # print("CALCOLO CON BB")
    # print(xz)



    # total = time.time() - t

    # print("SIAMO AL JOB: "+str(i))
    pr_time_list = []
    prec_list = []

    # txt_files = ["instances_8_2_0.txt","instances_8_2_1.txt",
    #             "instances_8_4_0.txt","instances_8_4_1.txt",
    #             "instances_9_2_1.txt","instances_6_2_1.txt",
    #             "instances_7_2_1.txt"]
    txt_files = ["instances_20_19_0.txt"]
    csv_files = ["instances_20_19_0.csv"]
    # csv_files = ["instances_8_2_0.csv","instances_8_2_1.csv",
    #             "instances_8_4_0.csv","instances_8_4_1.csv",
    #             "instances_9_2_1.csv","instances_6_2_1.csv",
    #             "instances_7_2_1.csv"]

    # txt_files = ["instances_20_5_0.txt","instances_20_5_1.txt",
    #             "instances_20_10_0.txt","instances_20_10_1.txt",
    #             "instances_21_10_1.txt","instances_22_10_1.txt",
    #             "instances_23_10_1.txt"]
    #
    # csv_files = ["instances_20_5_0.csv","instances_20_5_1.csv",
    #             "instances_20_10_0.csv","instances_20_10_1.csv",
    #             "instances_21_10_1.csv","instances_22_10_1.csv",
    #             "instances_23_10_1.csv"]

    for n in range(len(txt_files)):
        txt_file = txt_files[n]
        csv_file = csv_files[n]
        lambda_list = []
        with open("results\\"+csv_file, 'w', encoding='UTF8') as f:
            f.close()

        import csv
        with open("results\\"+csv_file, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)

        #with open(txt_file, "r", encoding='UTF8') as instances:
        with open("instances\\"+txt_file, "r", encoding='UTF8') as instances:
            pr_time = instances.readline()
            first = 1
            while pr_time:
                prec = instances.readline()
                pr_time_list = generator.parse_pr_time(pr_time)
                prec_list = generator.parse_prec(prec)
                # mu = generator.mu_gen(len(prec_list))
                objVal, objBound, gap_pli, total_pli = solver.pli_implementation(pr_time_list, prec_list)
                # if first==1:
                #     first = 0
                for i in range(len(prec_list)):
                    lambda_list.append(.5)
                x,z,total_bb, gap_bb = branch_and_bound.bb_implementation(pr_time_list, prec_list, lambda_list)
                pr_time = instances.readline()

                data = [len(pr_time_list), len(prec_list), str(lambda_list), objVal, objBound, gap_pli, z, gap_bb, total_pli, total_bb]

                with open("results\\"+csv_file, 'a', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    # write the data
                    writer.writerow(data)

    # total_pli = solver.solve_model(solver.pli_implementation(10, [12,35,47,21,16,46,20,4,11,23], [[8,7],[6,1],[1,4]], 0)[0])[1]
    # total = time.time() - t


#CALCOLO TEMPO BB

if __name__ == "__main__":
    main()
