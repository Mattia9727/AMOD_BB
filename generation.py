import random

def generation(N,n,k):

    with open('instances.txt', 'w') as file:
        file.close()

    for i in range(N):
        random.seed()
        Pi = []
        precs = []
        for j in range(n):
            Pi.append(random.randint(1,50))
        j=0
        while j<k:
            prec = [random.randint(0,n),random.randint(0,n)]
            nPrec = [prec[1], prec[0]]
            if prec[0] != prec[1] and prec not in precs and nPrec not in precs:
                precs.append(prec)
                j+=1

        with open('instances.txt', 'a') as file:
            for j in range(n):
                file.write(str(Pi[j]) + "_");
            file.write("\n")
            for p in precs:
                file.write(str(p[0]) + "," + str(p[1]) + "_")
            file.write("\n\n")
        file.close()

    return

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

def parse_pr_time(p):
    if p[-1:]=="\n":
        p=p[:-1]
    p_list = p.split("_")
    map_object = map(int, p_list)
    ret_list = list(map_object)
    return ret_list



if __name__ == "__main__":
    generation(10,10,3)
