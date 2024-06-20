import pycosat
import sys
import math

f=open(sys.argv[1],"r")
w=open("sol.txt","w")

while(1):
    
    su_inst=f.readline()[:-1]
    if (su_inst==""):
        break

    n=int((len(su_inst))**(0.5))
    sqrt_n=int(n**(0.5))
    cl=[]                       # cl represents the clause list in (x,y,v) format

    cnf=[]                      # cnf represents the clause list in dimacs cnf format

    d={}                        # a dictionary which holds (x,y,z) as key along with value as unique id
                                # for pycosat to work on it 

    d_rev={}                    # reverse of previous dictionary to restore which unique id corresponds to
                                # what clause 
                                

    #clause is represented as (x,y,v) where
    # x represents the row (1 based index)
    # y represents the column (1 based index)
    # v represents the value in that cell (1 based value)
    # (-x,-y,-v) represents ~(x,y,z) 

    #each cell has atleast one value
    for i in range(1,n+1):
        for j in range(1,n+1):
            l=[]
            for k in range(1,n+1):
                l.append((i,j,k))
            cl.append(l)

    #each cell has atmost one value
    for i in range(1,n+1):
        for j in range(1,n+1):
            for k in range(1,n+1):
                for l in range(k+1,n+1):
                    cl.append([(-i,-j,-k),(-i,-j,-l)])

    #each row has all the values
    for i in range(1,n+1):
        for k in range(1,n+1):
            l=[]
            for j in range(1,n+1):
                l.append((i,j,k))
            cl.append(l)

    #each column has all the values
    for j in range(1,n+1):
        for k in range(1,n+1):
            l=[]
            for i in range(1,n+1):
                l.append((i,j,k))
            cl.append(l)

    #each subsquares have all the values

    for t in range(1,n+1):

        row=math.ceil(t/sqrt_n)
        if (t%sqrt_n!=0):
            col=t%sqrt_n
        else:
            col=sqrt_n

        for k in range(1,n+1):
            l=[]
            for i in range((row-1)*sqrt_n+1,row*sqrt_n+1):
                for j in range((col-1)*sqrt_n+1,col*sqrt_n+1):
                    l.append((i,j,k))
            cl.append(l)


    #each clues must be taken into account
    for i in range(0,n):
        for j in range(0,n):
            if (su_inst[(i*n)+j].isdigit()):
                cl.append([(i+1,j+1,int(su_inst[(i*n)+j]))])


    # converting to dimacs cnf format
    counter=1
    for i in cl:
        l=[]
        for j in i:
            if j[0]>0:
                if j in d:                                          
                    l.append(d[j])                        # adding the unique id to cnf list if it exists
                else:
                    d[j]=counter                          # creating a unique id if it doesnt exists and then adding it              
                    d_rev[counter]=j
                    counter+=1
                    l.append(d[j])
            else:
                if (-j[0],-j[1],-j[2]) in d:
                    l.append((-1)*d[(-j[0],-j[1],-j[2])])
                else:
                    d[(-j[0],-j[1],-j[2])]=counter
                    d_rev[counter]=(-j[0],-j[1],-j[2])
                    counter+=1
                    l.append((-1)*d[(-j[0],-j[1],-j[2])])
        cnf.append(l)

    #solving using pycosat
    sol=pycosat.solve(cnf)

    #writing back to terminal
    if sol=="UNSAT":                                             # if no solution exists
        w.write("No solution exists")
        w.write("\n")                  
    else:
        s=""
        for i in range(1,int(n*n)+1):
            for j in range((i-1)*n,i*n+1):
                if (sol[j]>0):
                    s=s+str((d_rev[sol[j]][2]))        # retreving the values correspong to unique id from d_rev
                    break
                
        w.write(s)
        w.write("\n")
        


f.close()
w.close()

