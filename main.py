from pprint import pprint
import branch_and_bound
import generator
import solver


def main():
    # Header del file csv contenente i risultati
    header = ["#Job", "#Precedenze", "Risultato PLI", "Bound PLI", "Gap PLI", "Risultato BB", "Gap BB", "Tempo PLI",
              "Tempo BB"]
    choice = input("Se si vogliono usare i processing time e le precedenze del file ""instances.txt"", premere ""i"" e poi invio. \n"
                   "Se si vogliono inserire qui i processing time e le precedenze, premere ""k"" e poi invio.\n"
                   "Se si vuole uscire, premere ""q"" e poi invio.\n"
                   "Scelta: ")
    if choice == "q" or choice =="Q":
        exit(0)
    if choice == "i" or choice == "I":
        # File contenente le istanze da eseguire
        txt_files = ["instances.txt"]
        # File su cui vengono scritti i risultati
        csv_files = ["results.csv"]

        for n in range(len(txt_files)):
            txt_file = txt_files[n]
            csv_file = csv_files[n]
            lambda_list = []
            with open(csv_file, 'w', encoding='UTF8') as f:
                f.close()

            import csv
            with open(csv_file, 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)

            with open(txt_file, "r", encoding='UTF8') as instances:
                pr_time = instances.readline()
                while pr_time:
                    prec = instances.readline()
                    pr_time_list = generator.parse_pr_time(pr_time)
                    prec_list = generator.parse_prec(prec)
                    # Risolvo con pli
                    objVal, objBound, gap_pli, total_pli = solver.pli_implementation(pr_time_list, prec_list)
                    for i in range(len(prec_list)):
                        lambda_list.append(.5)
                    #Risolvo con branch & bound
                    x, z, total_bb, gap_bb = branch_and_bound.bb_implementation(pr_time_list, prec_list, lambda_list)
                    pr_time = instances.readline()
                    # Riga di dati da scrivere del csv
                    data = [len(pr_time_list), len(prec_list), objVal, objBound, gap_pli, z, gap_bb, total_pli, total_bb]

                    with open(csv_file, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
    elif choice == "k" or choice == "K":
        p_str = input("Inserire lista di processing time separati da ""_"" (es: 5_9_2_1 identifica 4 job): ")
        prec_str = input("Inserire lista di precedenze separate da ""_"" (es: 3,5_4,3_2,0 identifica 3 precedenze): ")
        pr_time_list = generator.parse_pr_time(p_str)
        prec_list = generator.parse_prec(prec_str)
        objVal, objBound, gap_pli, total_pli = solver.pli_implementation(pr_time_list, prec_list)
        lambda_list = []
        for i in range(len(prec_list)):
            lambda_list.append(.5)
        # Risolvo con branch & bound
        x, z, total_bb, gap_bb = branch_and_bound.bb_implementation(pr_time_list, prec_list, lambda_list)
        # Riga di dati da scrivere del csv
        data = [len(pr_time_list), len(prec_list), objVal, objBound, gap_pli, z, gap_bb, total_pli, total_bb]

        dictionary = dict(zip(header, data))
        pprint(dictionary)



if __name__ == "__main__":
    main()
