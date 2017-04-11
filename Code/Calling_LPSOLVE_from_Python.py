import numpy as np
from lpsolve55 import *

help(lpsolve)


c = np.array([[20,24,11,25,30],
              [28,27,82,83,74],
              [74,97,71,96,70],
              [ 2,55,73,69,61],
              [46,96,59,83,4],
              [42,22,29,67,59],
              [ 1, 5,73,59,56],
              [10,73,13,43,96],
              [93,35,63,85,46],
              [47,65,55,71,95]],dtype=float)


f = np.array([1,4,2,1,3],dtype=float)

## i: demand point, j: location
col_names = ['w'+str(i)+str(j) for i in range(1,11) for j in range(1,6)]
col_names = col_names + ['d'+str(j) for j in range(1,6)]

ncols = len(col_names) ## number of variables

lp = lpsolve('make_lp', 0, ncols)
lpsolve('set_verbose', lp, 'IMPORTANT')

for i in range(ncols):
    lpsolve('set_col_name', lp, i+1, col_names[i])

obj_values = c.flatten(order='C').tolist()+[30.]*5

lpsolve('set_obj_fn', lp, obj_values)
lpsolve('set_minim', lp)


## sum(j:wij)=1 for all i
for i in range(1,11):
    const_names = ['w'+str(i)+str(j) for j in range(1,6)]
    indices = [col_names.index(name) for name in const_names]
    values = np.zeros(ncols) ; values[indices]=1.
    lpsolve('add_constraint',lp, values, 'EQ', 1.0)
    lpsolve('set_row_name',lp,i,'FIRST'+str(i))


## sum(i:wij) <= fjdj for all j
for j in range(1,6):
    const_names = ['w'+str(i)+str(j) for i in range(1,11)] 
    indices = [col_names.index(name) for name in const_names]    
    values = np.zeros(ncols) ; values[indices]=1.
    index = col_names.index('d'+str(j))
    values[index] = -f[j-1]
    lpsolve('add_constraint',lp, values, 'LE', 0.0)
    lpsolve('set_row_name',lp,10+j,'SECOND'+str(j))


for j in range(ncols):
    lpsolve('set_binary',lp,j+1,1) 

lpsolve('write_lp', lp, 'warehouse.lp')
ret = lpsolve('solve', lp)   
print('return code: {:2d}\n'.format(ret))

obj = lpsolve('get_objective', lp)
print('objective function value: {:06.2f}\n'.format(obj))

vars = lpsolve('get_variables', lp)[0]
print('non-zero variable values:\n')
for i in range(len(vars)):
    if vars[i] > 1e-6:
        print('{:4s} = {:6.2f}'.format(col_names[i],vars[i]))
        
cons = lpsolve('get_constraints', lp)[0]      
print('\nconstraints LHS:\n')
for i in range(len(cons)):
    nm = lpsolve('get_row_name',lp,i+1)
    print('{:8s} = {:6.2f}'.format(nm,cons[i]))


lpsolve('delete_lp', lp)

