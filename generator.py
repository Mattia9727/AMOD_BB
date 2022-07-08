import random

def generation(N,n,k,mod=0,value1=0,value2=0):
    if n<=k:
        print("Ci sono cicli.")
        return

    with open('instances.txt', 'w') as file:
        file.close()


    for i in range(N):
        random.seed()
        Pi = []
        precs = []
        for j in range(n):
            Pi.append(random.randint(1,50))

        j=0
        # GENERAZIONE RANDOM DI k PRECEDENZE
        if mod == 0:
            while j<k:
                prec = [random.randint(0,n-1),random.randint(0,n-1)]
                neg_prec = [prec[1], prec[0]]
                if (prec[0] != prec[1]) and (prec not in precs) and (neg_prec not in precs):
                    precs.append(prec)
                    j+=1

        elif mod == 1:
            while j<k:
                randomVar = random.randint(0,n-2)
                prec = [randomVar,randomVar+1]
                if prec not in precs and [prec[0]+1,prec[1]+1] not in precs and [prec[0]-1,prec[1]-1] not in precs:
                    precs.append(prec)
                    j += 1
                    for l in range(value1):
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
        elif mod == 2:
            for j in range(int(k/value1)):
                for l in range(value1):
                    prec = [j*value1+l+j, j*value1+l+1+j]
                    precs.append(prec)
            for j in range(k%value1):
                prec = [random.randint(0, n - 1), random.randint(0, n - 1)]
                neg_prec = [prec[1], prec[0]]
                if (prec[0] != prec[1]) and (prec not in precs) and (neg_prec not in precs):
                    precs.append(prec)
                else:
                    j-=1





        # GENERAZIONE DI k PRECEDENZE A CATENE DI DIMENSIONE value1 (es: value1 = 4 --> genero catena di 4 job)
        elif mod == 1:
            while j < k:
                prec = [random.randint(0, n - 1), random.randint(0, n - 1)]
                nPrec = [prec[1], prec[0]]
                if prec[0] != prec[1] and prec not in precs and nPrec not in precs:
                    precs.append(prec)



        # GENERAZIONE DI k PRECEDENZE CON value1 CATENE DIVERSE
        elif mod == 2:
            pass


        with open('instances.txt', 'a') as file:
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

    return N

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
    generation(1, 13, 8, 2, 3)

if __name__ == "__main__":
    main()


