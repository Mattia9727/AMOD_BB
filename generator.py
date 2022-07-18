import random
from os import path

import graph_implementation

""" 
    Algoritmo per generare pseudorandomicamente istanze di job e precedenze con diversi criteri
    Viene creato un file "instances.txt" in cui vengono scritte i processing time separati da un "_", e nella riga
    successiva le precedenze "x,y" separati da "_"
    Se il file esiste già, viene sovrascritto.

    Param: 
        N: numero istanze da generare
        n: numero di job per istanza
        k: numero di precedenze per istanza
        var: 1 se processing time con alta variabilità, 0 con processing time con bassa
        hold_on: 1 se si vuole che le nuove istanze generate vengono aggiunte al file già esistente senza sovrascriverlo
"""


def generation(N, n, k, var=0, hold_on=0):
    # Il numero massimo di precedenze è n*(n-1)/2
    if k > (n * (n - 1) / 2):
        print("Ci sono cicli.")
        return
    # #Chiudo il file in cui salvo le istanze create in caso sia già aperto
    if not hold_on:
        with open('instances.txt', 'w') as file:
            file.close()

    # Genero randomicamente i processing time e le precedenze per ogni istanza
    for i in range(N):
        random.seed()
        Pi = []
        precs = []
        for j in range(n):
            if var == 0:
                Pi.append(random.randint(40, 60))
            else:
                Pi.append(random.randint(1, 100))

        # genero il grafo
        job_graph = graph_implementation.Graph(n)

        j = 0
        # GENERAZIONE RANDOM DI k PRECEDENZE
        while j < k:
            prec = [random.randint(0, n - 1), random.randint(0, n - 1)]
            neg_prec = [prec[1], prec[0]]
            if (prec[0] != prec[1]) and (prec not in precs) and (neg_prec not in precs):
                job_graph.addEdge(prec[0], prec[1])
                # Check presenza di cicli
                if not job_graph.isCyclic():
                    precs.append(prec)
                    j += 1
                else:
                    job_graph.removeEdge(prec[0], prec[1])

        with open('instances.txt', 'a') as file:
            for j in range(n):
                file.write(str(Pi[j]))
                if j < n - 1:
                    file.write("_")
            file.write("\n")
            for j in range(len(precs)):
                p = precs[j]
                file.write(str(p[0]) + "," + str(p[1]))
                if j < len(precs) - 1:
                    file.write("_")
            file.write("\n")
        if not hold_on:
            file.close()

    return


""" 
    Prende lista di precedenze sul file ed esegue parsing in lista di liste di due interi,
    che rappresentano la relazione "i precede j"

    Param: 
        p: stringa di precedenze separate da "_"
    
    Output:
        lista di liste di due elementi rappresentanti le precedenze (es: la precedenza 2->3 è espressa come [2,3])
"""


def parse_prec(p):
    if p[-1:] == "\n":
        p = p[:-1]
    p_list = p.split("_")
    ret_list = []
    for i in p_list:
        ret_list.append(i.split(","))
        for j in ret_list:
            j[0] = int(j[0])
            j[1] = int(j[1])
    return ret_list


""" 
    Prende lista di processing time sul file ed esegue parsing in lista di interi, 
    che rappresentano i processing time dei job 1..n

    Param: 
        p: stringa di processing time separate da "_"

    Output:
        lista di processing time
"""


def parse_pr_time(p):
    if p[-1:] == "\n":
        p = p[:-1]
    p_list = p.split("_")
    map_object = map(int, p_list)
    ret_list = list(map_object)
    return ret_list


""" 
    Dato n intero, genera una lista di n moltiplicatori lagrangiani

    Param: 
        n: intero rappresentante la dimensione della lista da creare

    Output:
        lista di n lambda
"""


def lambda_gen(n):
    random.seed()
    ret_list = []
    for i in range(n):
        ret_list.append(random.uniform(0, 10))
    return ret_list


def main():
    N = int(input("Inserire numero di istanze da generare: "))
    n = int(input("Inserire numero di processing time per istanza da generare: "))
    k = int(input("Inserire numero di precedenze per istanza da generare: "))
    while True:
        var = int(input("Se si vogliono generare processing time altamente variabili, premere 1\n"
                        "Altrimenti, premere 0"))
        if var == 0 or var == 1:
            break
        else:
            break
    if path.exists("instances.txt"):
        while True:
            hold_on = int(input("Il file instances.txt già esiste.\n"
                                "Se si vogliono aggiungere le istanze al file, premere 1.\n"
                                "Se si vuole sovrascrivere il file, premere 0"))
            if hold_on == 0 or hold_on == 1:
                break
            else:
                print("Input errato. Riprova")
    else:
        hold_on = 0

    generation(N, n, k, var, hold_on)
    exit(0)


if __name__ == "__main__":
    main()
