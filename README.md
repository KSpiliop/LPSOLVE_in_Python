
<h2 style="color:blue;">Introduction</h2> 

**LPSOLVE** is an excellent open source solver for mathematical programming problems. It can be used for linear (LP), integer (IP) and mixed integer linear (MILP) problems. It is distributed under the [GNU Lesser General Public License](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License "GNU Lesser General Public License"). 

All documentation for LPSOLVE can be found [here](http://lpsolve.sourceforge.net/5.5/ "LPSOLVE"). This short tutorial shows how to use LPSOLVE from Python in Windows. It is also available as a Jupiter notebook [here](https://github.com/KSpiliop/LPSOLVE_in_Python/blob/master/Code/Calling_LPSOLVE_from_Python.ipynb "Notebook") and as a Python file [here](https://github.com/KSpiliop/LPSOLVE_in_Python/blob/master/Code/Calling_LPSOLVE_from_Python.py ".py file").

<h2 style="color:blue;">Installation of LPSOLVE in Windows</h2> 

There are several articles on running LPSOLVE from Python and even a package for it, [PyLPSolve](http://www.stat.washington.edu/~hoytak/code/pylpsolve/ "PyLPSolve"). But PyLPSolve cannot yet be installed on Windows. There are also reported problems with the instructions in [LPSOLVE pages](http://lpsolve.sourceforge.net/5.5/Python.htm "Using lpsolve from Python"). Some other unofficial distributions do not work with Windows 64-bit. Probably the best solution is the one found in [this post](http://stackoverflow.com/questions/23411205/how-to-use-lpsolve-from-python-in-windows-64bit "Post").

So, visit the page [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/ "Unofficial Windows Binaries for Python Extension Packages") and find the appropriate Python wheel package under the heading:    

> lp_solve, a Mixed Integer Linear Programming (MILP) solver.

The .whl files differ by Python version and Windows architecture (32/64). For example, the package below is for Python 3.5 and Windows 64 bit:   

> lpsolve55‑5.5.2.5‑cp35‑cp35m‑win_amd64.whl

Locate the folder with the wheel file and follow the usual pip -install procedure. 

<h2 style="color:blue;">The example problem: Warehouse location</h2> 

The data for the example are taken from this [ILOG CPLEX Optimization Studio](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.2/ilog.odms.ide.help/OPL_Studio/opllanguser/topics/opl_languser_app_areas_IP_warehse.html "ILOG CPLEX link") link. 

In warehouse location problems we are looking for the optimal places of warehouses to serve outlets/ demand points and the allocation of demand points to these places.

Suppose we have 5 potential locations for warehouses, **L1,L2,...,L5** and 10 demand points **D1,D2,...,D10**.

The **fixed costs** for the operation of the warehouses are all equal to **30 monetary units**. The variable costs (for example transportation costs) for all pairs of demand points and locations are shown in the following table.</h1>     

<p style="text-align: center;">  
Operating costs</p>

|        | L1 | L2 | L3 | L4 | L5 |
|:--:    |:--:|:--:|:--:|:--:|:--:|
| **D1** | 20 | 24 | 11 | 25 | 30 |
| **D2** | 28 | 27 | 82 | 83 | 74 |
| **D3** | 74 | 97 | 71 | 96 | 70 |
| **D4** | 2  | 55 | 73 | 69 | 61 |
| **D5** | 46 | 96 | 59 | 83 | 4  |
| **D6** | 42 | 22 | 29 | 67 | 59 |
| **D7** | 1  | 5  | 73 | 59 | 56 |
| **D8** | 10 | 73 | 13 | 43 | 96 |
| **D9** | 93 | 35 | 63 | 85 | 46 |
| **D10**| 47 | 65 | 55 | 71 | 95 |

The locations are also subject to capacity constraints. The maximum number of demand points assigned to each location are shown below: 

<p style="text-align: center;">  
Capacity constraints</p>

| L1 | L2 | L3 | L4 | L5 |
|:--:|:--:|:--:|:--:|:--:|
| 1  |  4 | 2  |  1 |  3 |

The **mathematical programming formulation** is given below. Denote by cij , i=1,...,10 ; j=1,...,5 the variable cost for demand point i and location j and by fj, j=1,...,5 the capacity at location j.

- The binary variables wij denote the assignment of demand points to locations : wij=1 if demand point i is assigned to location j, otherwise 0. 
- The binary variables dj indicate the selection of locations: dj=1 if location j is used, otherwise 0.
- The objective function minimizes the total cost, i.e. the fixed and variable costs. 
- The first set of constraints ensures that each demand point is allocated to exactly one location.
- The second set of constraints forces each location j to have at most fj demand points and also pushes the wij variables to zero when a location is not selected (note that in a larger problem we would use separate wij <= dj constraints for this).      

<img style="float: left;" src="https://cloud.githubusercontent.com/assets/12450688/24873799/ee2099c6-1e2a-11e7-980a-43c0090be6c1.jpg" width="400" height="300" />



First we import numpy and the LPSOLVE library. The library exposes only one wrapper function lpsolve() therefore we import 'all' to avoid writing lpsolve55.lpsolve() at each call. 

A complete list of the LPSOLVE API can be found in [LPSOLVE pages](http://lpsolve.sourceforge.net/5.5/ "LPSOLVE").


```python
import numpy as np
from lpsolve55 import *

help(lpsolve)
```

    Help on built-in function lpsolve in module lpsolve55:
    
    lpsolve(...)
        lpsolve('functionname', arg1, arg2, ...) ->  execute lpsolve functionname with args
    
    

Then we define the data. We put the operating costs in a 2-dimensional  array **c** and the capacities in a 1-dimensional array **f**. We use floats because the coefficients must be passed as real numbers.

We also put the (1-index) variable names in a list **col_names**. First are the wij variables (with the index j of the location running first) and then are the dj variables.


```python


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

```

We can now initialize an LPSOLVE model with **ncols** number of variables and no constraints yet. The return value **lp** is a handle to the model and we will use it as an argument from now on.

The internal 'set_verbose' function is used to set the details of the messages. 'IMPORTANT' is an internal constant meaning only warnings and errors will be reported. 


```python
lp = lpsolve('make_lp', 0, ncols)
lpsolve('set_verbose', lp, 'IMPORTANT')
```

Next, we put the variable names using the internal function set_col_name. Note that the indices of variables (columns) and constraints in LPSOLVE are 1-based. 

We define in a list the coefficients of the objective function ('set_obj_fn') and we set the direction of optimization to min (set_minim).



```python
for i in range(ncols):
    lpsolve('set_col_name', lp, i+1, col_names[i])

obj_values = c.flatten(order='C').tolist()+[30.]*5

lpsolve('set_obj_fn', lp, obj_values)
lpsolve('set_minim', lp)
```

We can now define the constraints one by one. First is the set of 10 constraints which ensures that each demand point is assigned to exactly one location. For each one, we pass to 'add_constraint' a list with the coefficients, the type of the constraint (here 'EQ' meaning equality) and the RHS. We also set the name of each constraint with 'set_row_name'.  

Note that the LPSOLVE API has a version of this function (add_constraintex) which allows to specify only the non-zero elements of a row in the matrix. 



```python
## sum(j:wij)=1 for all i
for i in range(1,11):
    const_names = ['w'+str(i)+str(j) for j in range(1,6)]
    indices = [col_names.index(name) for name in const_names]
    values = np.zeros(ncols) ; values[indices]=1.
    lpsolve('add_constraint',lp, values, 'EQ', 1.0)
    lpsolve('set_row_name',lp,i,'FIRST'+str(i))
```

The second set of constraints is entered similarly. 


```python
## sum(i:wij) <= fjdj for all j
for j in range(1,6):
    const_names = ['w'+str(i)+str(j) for i in range(1,11)] 
    indices = [col_names.index(name) for name in const_names]    
    values = np.zeros(ncols) ; values[indices]=1.
    index = col_names.index('d'+str(j))
    values[index] = -f[j-1]
    lpsolve('add_constraint',lp, values, 'LE', 0.0)
    lpsolve('set_row_name',lp,10+j,'SECOND'+str(j))
```

The last step is to define all variables as binary using 'set_binary'. The last argument (1) in these calls is a True flag.

We also export the model in a file, in LP format. This can be used for confirmation or read from the [LPSOLVE IDE](http://lpsolve.sourceforge.net/5.5/IDE.htm "LPSOLVE IDE"). LPSOLVE also allows the model export into MPS format.

Finally, we call 'solve'. The return code is 0 (success). We can now retrieve the value of the objective function ('get_objective') and the values of the non-zero variables in the solution ('get_variables') using the first element returned. We do NOT dimension any variable to accept the variables as the lpsolve driver takes care of the dimensioning. The same applies for the call to 'get_constraints' to retrieve the LHS of the constraints at the optimal solution.  

The optimal solution is to use L1,L2,L3 and L5 and assign:
- D4 to L1
- D2,D6,D7 and D9 to L2
- D8 and D10 to L3
- D1,D3,D5 and D8 to L5

The capacities are satisfied exactly and the total cost is 383 monetary units.


```python
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


```

    return code:  0
    
    objective function value: 383.00
    
    non-zero variable values:
    
    w15  =   1.00
    w22  =   1.00
    w35  =   1.00
    w41  =   1.00
    w55  =   1.00
    w62  =   1.00
    w72  =   1.00
    w83  =   1.00
    w92  =   1.00
    w103 =   1.00
    d1   =   1.00
    d2   =   1.00
    d3   =   1.00
    d5   =   1.00
    
    constraints LHS:
    
    FIRST1   =   1.00
    FIRST2   =   1.00
    FIRST3   =   1.00
    FIRST4   =   1.00
    FIRST5   =   1.00
    FIRST6   =   1.00
    FIRST7   =   1.00
    FIRST8   =   1.00
    FIRST9   =   1.00
    FIRST10  =   1.00
    SECOND1  =   0.00
    SECOND2  =   0.00
    SECOND3  =   0.00
    SECOND4  =   0.00
    SECOND5  =   0.00
    

Finally, we delete the model data structures. This is good practice. 


```python
lpsolve('delete_lp', lp)
```

There is much functionality which is not shown in this brief tutorial, especially in the parameters of the solver. The interested reader can read the LPSOLVE API and experiment with it. 
