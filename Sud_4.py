#Suduko Solver
#By: AlaaElshorbagy

import numpy as np

S=np.array([[2,0,0,0,0,0,0,6,8],\
            [0,0,0,6,8,7,3,0,0],\
            [8,0,0,2,5,0,1,9,0],\
            [3,1,0,0,0,9,6,0,0],\
            [0,0,0,0,6,0,7,0,4],\
            [0,7,4,0,0,8,2,1,9],\
            [0,0,0,0,9,1,4,0,0],\
            [0,3,0,0,0,0,8,5,1],\
            [0,0,0,0,4,0,0,0,0]])

print('Original problem:\n', S)


#Specifing the submatrix of each element
def assigned_block(row_indx,col_indx,A):
    row_start_indx=3*(row_indx//3)
    row_end_indx=row_start_indx+3
    col_start_indx=3*(col_indx//3)
    col_end_indx=col_start_indx+3
    block_array=A[row_start_indx:row_end_indx,col_start_indx:col_end_indx]
    return block_array


#Computing missing elements of an array
def compl(a):
    b=np.array([1,2,3,4,5,6,7,8,9])
    ca=np.setdiff1d(b, a,True)
    return ca


#Computing Potential Values of a particular empty space
def potential_values(row_array,column_array,block_array):
    inter_array=np.intersect1d(np.intersect1d(compl(row_array), compl(column_array), True),\
                     compl(block_array), True)
    return inter_array


#Checking well-posedness of the problem + creating a dict that assign to each empty space it's potential values
def iterating_over_elements(B):
    nu_missing_elements=0
    Failed='F'
    dict_valid_potential_values=dict()
    for i in range(B.shape[0]):
         for j in range(S.shape[1]):
            if B[i,j]==0:
                PotentialValues=potential_values(B[i,:],B[:,j],assigned_block(i,j,B))
                #print(PotentialValues)
                if len(PotentialValues)==1:
                    B[i,j]=int(PotentialValues)
                elif len(PotentialValues)==0:
                    Failed='T'
                else:
                    nu_missing_elements=nu_missing_elements+1
                    dict_valid_potential_values[i,j]=PotentialValues
    return     Failed, nu_missing_elements, dict_valid_potential_values
#print(iterating_over_elements(S))

#Filling the empty spaces that can be filled without guessing + keeping a dict with the potential values of the remaining spaces
def EasyLevel_fn(C):
    Y=iterating_over_elements(C)
    Failed=Y[0]
    if Failed=='F':
        old_number_missing_elements=Y[1]
    else:
        return  Failed
    Easy_Level=True
    while Easy_Level:
        Z=iterating_over_elements(C)
        if Z[0]=='F':
            New_number_missing_elements=iterating_over_elements(C)[1]
        else:
            Failed= Z[0]
            return  Failed
        if New_number_missing_elements==0:
            return True, C
        elif New_number_missing_elements - old_number_missing_elements==0:
            Easy_Level=False
        old_number_missing_elements= New_number_missing_elements
    return Easy_Level, New_number_missing_elements, Z[2],C
#print(EasyLevel_fn(S))

#For each potential value of S_ij, it tests the outcome scenario and keep a list of the well-posed ones
def MediumLevel_step_one(i,j,dict,D):
    S_ij_valid_possibilities_of_S=list()
    num_missing_elements=None  #number of missing elements is kinda irrelevant but it is good to track the code
    for x in dict[i,j]:
        DD=np.copy(D) #we will do some guessing here so we need to be sure that the original problem don't change if the prediction was wrong
        DD[i,j]=x
        Y=EasyLevel_fn(DD)
        if Y=='T': #means the scenario is not well-posed by causing blank space
            continue
        if num_missing_elements==None:
            num_missing_elements=Y[1]
        elif num_missing_elements>Y[1]:
            num_missing_elements=Y[1]
        if Y[0]==True:
            D=DD    #no need to continue problem solved
            return True, D
        else:
            S_ij_valid_possibilities_of_S.append(DD)   #it's a well-posed scenario, we keep it
            #print(S_ij_valid_possibilities_of_S)
    return   False, num_missing_elements, S_ij_valid_possibilities_of_S
#print(MediumLevel_step_one(1,0,EasyLevel_fn(S)[2],S))


#It run MediumLevel_step_one over each nonzero element, if the problem can be solved by one guessing then it's Medium-level, if not we keep a list of all well-posed scenarios
def MediumLevel_fn(nu_missing_elements,dict,E):
    num_missing_elements=nu_missing_elements
    nominated_to_hard_level_list=list() #contains the best compinations we could do at that level, if the problem is not solved at that level
    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            if E[i,j]==0:
                Z=MediumLevel_step_one(i,j,dict,E)
                #print(Z)
                if Z[0]==True:
                    return True, Z[1]
                else:
                    if   num_missing_elements>Z[1]:
                        num_missing_elements=Z[1]
                    for X in Z[2]:
                        d=0
                        for Q in nominated_to_hard_level_list:
                            if np.array_equal(X,Q):
                                d=1
                        if d==0:
                            nominated_to_hard_level_list.append(X)
    return False, num_missing_elements, nominated_to_hard_level_list


def UpperMediumLevel_fn(nu_missing_elements, nominated_to_hard_level_list):
    num_missing_elements= nu_missing_elements
    Mutable_solution_list_1=nominated_to_hard_level_list
    Mutable_solution_list_2=list()
#    c=0
#    i=0
    while True:
        print('length of Mutable_solution_list_1=', len(Mutable_solution_list_1),'missing elemnts',num_missing_elements)
        for X in Mutable_solution_list_1:
            Y=EasyLevel_fn(X)
            X_output=MediumLevel_fn(Y[1],Y[2],Y[3])
            if X_output[0]==True:
                return True, X_output[1]
            if num_missing_elements > X_output[1]:
                num_missing_elements=X_output[1]
            for QQ in X_output[2]:
                d=0
                for Q in Mutable_solution_list_2:
                    if np.array_equal(QQ,Q):
                            d=1
                if d==0:
                    Mutable_solution_list_2.append(QQ)
            print('length of Mutable_solution_list_2',len(Mutable_solution_list_2),'missing elemnts',num_missing_elements)
        Mutable_solution_list_1=Mutable_solution_list_2
        Mutable_solution_list_2=list()
        if len(Mutable_solution_list_1)==0:
            print("Something wrong with the problem or I am stupid")
            print(F)
            return
    return

def Main(G):
    alpha=EasyLevel_fn(G)
    if alpha[0]==True:
        print('Easy problem, the solution is:\n', alpha[1])
    else:
        beta=MediumLevel_fn(alpha[1],alpha[2],alpha[3])
        if beta[0]==True:
            print('Medium level problem, the solution is:\n', beta[1])
        else:
            print('Not easy one, could take long time...')
            gamma=UpperMediumLevel_fn(beta[1],beta[2])
            if gamma[0]==True:
                print('Hard problem, the solution is:\n', gamma[1])


Main(S)
