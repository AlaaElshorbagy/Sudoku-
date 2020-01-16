#Suduko Solver
#By: AlaaElshorbagy

import numpy as np

S_1=np.array([[2,0,7,0,0,0,0,6,8],[0,9,0,6,8,7,3,0,2],[8,0,0,2,5,0,1,9,0],\
[3,1,0,0,0,9,6,0,0],[0,0,0,0,6,0,7,0,4],[0,7,4,0,0,8,2,1,9],\
[0,0,0,0,9,1,4,0,0],[0,3,0,0,0,0,8,5,1],[7,0,0,0,4,0,0,0,6]])

S_2=np.array([[2,0,0,0,0,0,0,6,8],[0,0,0,6,8,7,3,0,0],[8,0,0,2,5,0,1,9,0],\
[3,1,0,0,0,9,6,0,0],[0,0,0,0,6,0,7,0,4],[0,7,4,0,0,8,2,1,9],\
[0,0,0,0,9,1,4,0,0],[0,3,0,0,0,0,8,5,1],[0,0,0,0,4,0,0,0,0]])

S_3=np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,2,5,0,1,9,0],\
[0,1,0,0,0,9,0,0,0],[0,0,0,0,6,0,0,0,0],[0,0,0,0,0,8,2,1,9],\
[0,0,0,0,9,0,0,0,0],[0,3,0,0,0,0,8,0,1],[0,0,0,0,4,0,0,0,0]])

S_4=np.array([[8,0,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,0,0],[0,7,0,0,9,0,2,0,0],\
[0,5,0,0,0,7,0,0,0],[0,0,0,0,4,5,7,0,0],[0,0,0,1,0,0,0,3,0],\
[0,0,1,0,0,0,0,6,8],[0,0,8,5,0,0,0,1,0],[0,9,0,0,0,0,4,0,0]])

S_5=np.array([[9,0,0,0,2,7,0,5,0],[0,5,0,0,0,0,9,0,4],[0,0,0,0,0,0,0,0,0],\
[8,0,0,0,7,5,6,4,9],[1,0,0,0,4,0,0,0,0],[0,0,0,0,0,9,8,0,0],\
[0,0,0,4,0,0,0,0,0],[0,0,0,0,3,0,0,1,0],[5,0,1,0,0,2,0,3,7]])

S_6=np.array([[0,1,0,0,0,0,0,6,9],\
              [4,0,6,0,0,0,0,7,5],\
              [7,0,0,0,0,0,0,0,0],\
              [0,0,0,0,7,0,4,0,0],\
              [1,0,0,0,2,0,0,0,0],\
              [3,0,0,5,0,1,9,0,0],\
              [0,2,7,0,0,3,0,0,0],\
              [0,0,0,9,0,0,0,0,7],\
              [0,0,9,0,0,0,8,0,0]])


S=S_1
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


#Checking well-posedness of the problem + returing 1st zero element and its potential values
def iterating_over_elements(B):
    nu_missing_elements=0
    Failed='F'
    First_zero_element_indx=()
    First_zero_element_potential_values=list()
    len_potential=9
    for i in range(B.shape[0]):
         for j in range(S.shape[1]):
            if B[i,j]==0:
                PotentialValues=potential_values(B[i,:],B[:,j],assigned_block(i,j,B))
                #print(PotentialValues)
                len_=len(PotentialValues)
                if len_==1:
                    B[i,j]=int(PotentialValues)
                elif len_==0:
                    Failed='T'
                else:
                    nu_missing_elements=nu_missing_elements+1
                    if len_<len_potential:
                        First_zero_element_indx=(i,j)
                        First_zero_element_potential_values=PotentialValues
                        len_potential=len_
                        one_elment=True
    return     Failed, nu_missing_elements, First_zero_element_indx,First_zero_element_potential_values
#print(iterating_over_elements(S))

#Filling the empty spaces that can be filled without guessing
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
            New_number_missing_elements=Z[1]
        else:
            Failed= Z[0]
            return  Failed
        if New_number_missing_elements==0:
            return True, C
        elif New_number_missing_elements - old_number_missing_elements==0:
            Easy_Level=False
        old_number_missing_elements= New_number_missing_elements
    return Easy_Level, Z[2] , C , Z[3]
#print(EasyLevel_fn(S))

#the guessing game starts :D
def backward_loop(L):
    while True:
        while len(L[-1][-1])!=0:
            Sud_clone=L[-1][1].copy()
            Sud_clone[L[-1][0]]=L[-1][-1][-1].copy()
            Output_Easy=EasyLevel_fn(Sud_clone)
            if Output_Easy=='T':
                L[-1][-1]=L[-1][-1][:-1]
                continue
            elif  Output_Easy[0]==True:
                return   True, Output_Easy[-1]
            else:
                a=Output_Easy[1]
                b=Output_Easy[2]
                c=Output_Easy[3]
                L.append([a,b,c])
        while  len(L[-1][-1])==0:
            L=L[:-1]
            L[-1][-1]=L[-1][-1][:-1]
    return


def main(SS):
    E=EasyLevel_fn(SS)
    if E[0]==True:
        print("Easy problem, one solution is \n \n ",E[1])
    else:
        print('Not Easy...')
        F=[[E[1],E[2],E[3]]]
        G=backward_loop(F)
        print("One solution is \n", G[1])

main(S)
