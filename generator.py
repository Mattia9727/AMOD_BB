import random
import graph_implementation

def checkCicli(precs):
    for n in range(len(precs)):
        circleList = []
        circleList.append(precs[n])
        before = 0
        for i in range(len(precs)):
            if circleList[before][1] == precs[i][0]:
                circleList.append(precs[i])
                before += 1
                for j in range(len(circleList)):
                    if precs[i][1] == circleList[j][0]:
                        return 1
    return 0

#N: numero di istanze da generare
#n: numero di job
#k: numero di precedenze
def generation(N, n, k, var=0, mod=0, c=0):
    #Il numero massimo di precedenze è n*(n-1)/2
    if k > (n*(n-1)/2):
        print("Ci sono cicli.")
        return
    #Chiudo il file in cui salvo le istanze create in caso sia già aperto
    with open('instances\instances_'+str(n)+'_'+str(k)+'_'+str(var)+'.txt', 'w') as file:
         file.close()

    #Genero randomicamente i processing time e le precedenze per ogni istanza
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

        j=0
        # GENERAZIONE RANDOM DI k PRECEDENZE
        if mod == 0:
            while j<k:
                prec = [random.randint(0,n-1),random.randint(0,n-1)]
                neg_prec = [prec[1], prec[0]]
                if (prec[0] != prec[1]) and (prec not in precs) and (neg_prec not in precs):
                    job_graph.addEdge(prec[0], prec[1])
                    # Check presenza di cicli
                    if not job_graph.isCyclic():
                        precs.append(prec)
                        j+=1
                        print(str(j))
                    else:
                        job_graph.removeEdge(prec[0],prec[1])

            # if job_graph.isCyclic():
            #     i-=1
            #     break

        elif mod == 1:
            while j<k:
                randomVar = random.randint(0,n-2)
                prec = [randomVar,randomVar+1]
                if prec not in precs and [prec[0]+1,prec[1]+1] not in precs and [prec[0]-1,prec[1]-1] not in precs:
                    precs.append(prec)
                    j += 1
                    for l in range(c-1):
                        if prec[1] == n-1:
                            if ([prec[0]-1-l, prec[0]-l] not in precs):
                                precs.append([prec[0]-1-l, prec[0]-l])
                                j+=1
                        else:
                            if ([prec[1], prec[1]+1] not in precs):
                                prec=[prec[1], prec[1]+1]
                                precs.append(prec)
                                j+=1

                        if j>=k:
                            break
        with open('instances\\instances_'+str(n)+'_'+str(k)+'_'+str(var)+'.txt', 'a') as file:
        #with open('instances.txt', 'a') as file:
            for j in range(n):
                file.write(str(Pi[j]))
                if(j < n-1):
                    file.write("_")
            file.write("\n")
            for j in range(len(precs)):
                p = precs[j]
                file.write(str(p[0]) + "," + str(p[1]))
                if j < len(precs)-1:
                    file.write("_")
            file.write("\n")
        file.close()

    return

#Prende lista di precedenze sul file ed esegue parsing in lista di liste di due interi, che rappresentano la relazione "i precede j"
def parse_prec(p):
    if p[-1:]=="\n":
        p=p[:-1]
    p_list = p.split("_")
    ret_list=[]
    for i in p_list:
        ret_list.append(i.split(","))
        for j in ret_list:
            j[0]=int(j[0])
            j[1]=int(j[1])
    return ret_list

#Prende lista di processing time sul file ed esegue parsing in lista di interi, che rappresentano i processing time dei job 1..n
def parse_pr_time(p):
    if p[-1:]=="\n":
        p=p[:-1]
    p_list = p.split("_")
    map_object = map(int, p_list)
    ret_list = list(map_object)
    return ret_list

def mu_gen(n):
    random.seed()
    ret_list=[]
    for i in range(n):
        ret_list.append(random.randint(-10,10))
    return ret_list

def lambda_gen(n):
    random.seed()
    ret_list=[]
    for i in range(n):
        ret_list.append(random.randint(0,10))
    return ret_list

def main():
    # generation(1,4,1,1)
    # generation(1, 5, 1, 1)
    # generation(1, 6, 1, 1)
    # generation(1, 7, 2, 1)
    # generation(1, 8, 2, 1)
    # generation(1, 9, 2, 1)
    # generation(1, 10, 2, 1)
    # generation(1, 11, 3, 1)
    # generation(1, 12, 3, 1)
    #generation(1,8,14,0)
    #generation(1,20,90,0)
    generation(1,20,19,0)
    # generation(10, 20, 10, 1)
    # generation(10, 21, 10, 1)
    # generation(10, 22, 10, 1)
    # generation(10, 23, 10, 1)
    # generation(10, 20, 10, 0)
    # generation(10, 20, 5, 1)
    # generation(10, 20, 5, 0)
    # generation(100, 9, 2, 1)
    # generation(100, 6, 2, 1)
    # generation(100, 7, 2, 1)
    # generation(100, 8, 4, 1)
    # generation(100, 8, 4, 0)
    # generation(100, 8, 2, 1)
    # generation(100, 8, 2, 0)

if __name__ == "__main__":
    main()
    # print(checkCicli([[1,0],[0,3],[5,8],[0,6],[3,6],[1,0],[0,9],[1,5],[0,6]]))


