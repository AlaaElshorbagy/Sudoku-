import numpy as np

S=np.array([[8,0,0,0,0,0,0,0,0],\
            [0,0,3,6,0,0,0,0,0],\
            [0,7,0,0,9,0,2,0,0],\
            [0,5,0,0,0,7,0,0,0],\
            [0,0,0,0,4,5,7,0,0],\
            [0,0,0,1,0,0,0,3,0],\
            [0,0,1,0,0,0,0,6,8],\
            [0,0,8,5,0,0,0,1,0],\
            [0,9,0,0,0,0,4,0,0]])
print('Original problem:\n', S)


def compl(a):
    b=[1,2,3,4,5,6,7,8,9]
    ca=np.setdiff1d(b, a,True)
    return ca

def potential_values(row_array,column_array,block_array):
    inter_array=np.intersect1d(np.intersect1d(compl(row_array), compl(column_array), True),\
                     compl(block_array), True)
    return inter_array

def assigned_block(row_indx,col_indx,A):
    row_start_indx=3*(row_indx//3)
    row_end_indx=row_start_indx+3
    col_start_indx=3*(col_indx//3)
    col_end_indx=col_start_indx+3
    block_array=A[row_start_indx:row_end_indx,col_start_indx:col_end_indx]
    return block_array

def iterating_over_elements(B):
    nu_missing_elements=0
    Failed='F'
    for i in range(B.shape[0]):
         for j in range(S.shape[1]):
            if B[i,j]==0:
                PotentialValues=potential_values(B[i,:],B[:,j],assigned_block(i,j,B))
                #print(PotentialValues) #may be it is better to make a sort of dictionary and assign to each S_ij its potential values
                if len(PotentialValues)==1:
                    B[i,j]=int(PotentialValues)
                elif len(PotentialValues)==0:
                    Failed='T'
                else:
                    nu_missing_elements=nu_missing_elements+1
    return     nu_missing_elements, Failed
#print(iterating_over_elements(S))

def EasyLevel_fn(C):
    Y=iterating_over_elements(C)
    Failed=Y[1]
    if Failed=='F':
        old_number_missing_elements=Y[0]
    else:
        return  Failed
    Easy_Level=True
    while Easy_Level:
        Z=iterating_over_elements(C)
        if Z[1]=='F':
            New_number_missing_elements=iterating_over_elements(C)[0]
        else:
            Failed= Z[1]
            return  Failed
        if New_number_missing_elements==0:
            break
        elif New_number_missing_elements - old_number_missing_elements==0:
            Easy_Level=False
        old_number_missing_elements= New_number_missing_elements
    return Easy_Level, New_number_missing_elements

#print(EasyLevel_fn(S))

def MediumLevel_step_one(i,j,D): #Each non-zero S_ij is assigned to a list of potential values. this function test each value and return the possibly good scenarios/compinations
    PotentialValues=potential_values(D[i,:],D[:,j],assigned_block(i,j,D))
    S_ij_valid_possibilities_of_S=list()
    #print(PotentialValues)
    for x in PotentialValues:
        DD=np.copy(D) #we will do some guessing here so we need to be sure that the original problem don't change if the prediction was wrong
        DD[i,j]=x
        Y=EasyLevel_fn(DD)
        if Y=='T': #means the scenario failed by causing blank space
            continue
        S_ij_valid_possibilities_of_S.append([Y,DD]) #==[(True/False the problem is totally solved in the scenario, #num_of_missing_elements), The_solution_so_far   ]
    #print(S_ij_valid_possibilities_of_S)
    return   S_ij_valid_possibilities_of_S

#Y=MediumLevel_step_one(0,2,S)
#print(Y[0][0][0])

def MediumLevel_fn(E):
    Easy_output=EasyLevel_fn(E)
    if Easy_output[0]==True:
        print('Easy Level?',Easy_output[0] ,'\n The solution is\n ', E )
        return True,0,[]
    Medium_Level=False
    num_missing_elements=Easy_output[1] #momken ne5aleh men el EasyLevel_fn ?????
    no_of_solutions=0
    List_of_solutions=list() #contains all the solutions if the problem is solvable at the Medium_Level
    nominated_to_hard_level_list=list() #contains the best compinations we could do at that level
    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            if E[i,j]==0:
                Z=MediumLevel_step_one(i,j,E)
                #print(Z)
                for X in Z:       #For each scenario: 1. we check wether the whole problem is solved or not\
                                  #2. If not we keep joing keeping a copy of the best we can do saved at a certain list
                    if X[0][0]==True:
                        Medium_Level=True
                        num_missing_elements=0
                        c=0
                        for W in List_of_solutions:
                            if np.array_equal(X[1],W):
                                c=1
                        if c==0:
                            List_of_solutions.append(X[1])
                            no_of_solutions=no_of_solutions+1
                            print('Medium level:',Medium_Level,'\n The solution number ', no_of_solutions, 'corresponds to',i,j,':\n', X[1])
                    elif Medium_Level==False:
                        #if X[0][1]<= num_missing_elements:
                            d=0
                            for Q in nominated_to_hard_level_list:
                                if np.array_equal(X[1],Q):
                                    d=1
                            if d==0:
                                nominated_to_hard_level_list.append(X[1])
                            if  X[0][1]< num_missing_elements:
                                #    nominated_to_hard_level_list.clear() #this step decreases the total number of scenarios but I don't like it because a ceratin scenario having a larger number of missing elements at this step doesn't neccesarily means it can't be better in the next steps :/
                                #    nominated_to_hard_level_list.append(X[1])
                                num_missing_elements=X[0][1]

    return Medium_Level, num_missing_elements, nominated_to_hard_level_list

#QQ=MediumLevel_fn(S)
#print("----------A7A---------")
#print('is it medium?', QQ[0], '\n number of missing elements ',\
#QQ[1])
#print("\n The whole list of candidates is:\n",MediumLevel_fn(S)[2])
#print("no of candidates",len(QQ[2]), QQ[2][-1])


def UpperMediumLevel_fn(F):
    Medium_output=MediumLevel_fn(F)
    if Medium_output[0]==True:
        return
    else:
        print('A7AAAAAA  Hard')
    num_missing_elements= Medium_output[1]
    Mutable_solution_list_1=Medium_output[2].copy()
    Mutable_solution_list_2=list()
#    c=0
#    i=0
    while num_missing_elements!=0:
        old_num=num_missing_elements
        for X in Mutable_solution_list_1:
            X_output=MediumLevel_fn(X)
            if X_output[0]==True:
                num_missing_elements=0
                return
            for QQ in X_output[2]:
                d=0
                for Q in Mutable_solution_list_2:
                    if np.array_equal(QQ,Q):
                            d=1
                if d==0:
                        Mutable_solution_list_2.append(QQ)
            if  X_output[1]< num_missing_elements:
                #Mutable_solution_list_2.clear() #this step decreases the total number of scenarios but I don't like it because a ceratin scenario having a larger number of missing elements at this step doesn't neccesarily means it can't be better in the next steps :/
                #Mutable_solution_list_2.extend(X_output[2])
                num_missing_elements=X_output[1]
            print('number of candidates',len(Mutable_solution_list_2),'missing elemnts',num_missing_elements)
            if  num_missing_elements ==0:
                break
            Mutable_solution_list_1=Mutable_solution_list_2
            Mutable_solution_list_2=list()
        if len(Mutable_solution_list_2)==0:
                print("Something wrong with the problem or I am stupid")
                print(F)
                return
        #print(old_num,num_missing_elements)
        #if old_num==num_missing_elements:
        #    if len(MediumLevel_fn(Mutable_solution_list_2[0])[2])==0:
        #        print("Something wrong with the problem or it's too Hard for me, need to run through more scenarios")
        #        print(F)
        #        return
            #print(Mutable_solution_list_2)
        #    c=c+1
        #    if c==10:
        #    print('i=',i)
        #            print('I am too slow\n Best so far:\n')
        #            break
    return


UpperMediumLevel_fn(S)
