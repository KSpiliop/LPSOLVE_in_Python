
<h2 style="color:blue;">Introduction</h2> 

**LPSOLVE** is an excellent open source solver for mathematical programming problems. It can be used for linear (LP), integer (IP) and mixed integer linear (MILP) problems. It is distributed under the [GNU Lesser General Public License](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License "GNU Lesser General Public License"). 

[http://lpsolve.sourceforge.net/5.5/](http://lpsolve.sourceforge.net/5.5/ "LPSOLVE")

This tutorial shows how to use LPSOLVE from Python. 


<h2 style="color:blue;">Installation</h2> 

Visit the page [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/ "Unofficial Windows Binaries for Python Extension Packages") and find the appropriate Python wheel package under the heading:    

> lp_solve, a Mixed Integer Linear Programming (MILP) solver.

The .whl files differ by Python version and Windows architecture (32/64). For example, the package below is for Python 3.5 and Windows 64 bit:   

> lpsolve55‑5.5.2.5‑cp35‑cp35m‑win_amd64.whl


<h2 style="color:blue;">The example problem: Warehouse location</h2> 

The data for the example are taken from:   
[https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.2/ilog.odms.ide.help/OPL_Studio/opllanguser/topics/opl_languser_app_areas_IP_warehse.html](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.2/ilog.odms.ide.help/OPL_Studio/opllanguser/topics/opl_languser_app_areas_IP_warehse.html "IBM Link")

In warehouse location problems we are looking for the optimal places of warehouses to serve outlets/ demand points.

Suppose we have 5 potential locations for warehouses, **L1,L2,...,L5** and 10 demand points **D1,D2,...,D10**.

The **fixed costs** for the opening of the warehouses are all equal to **30 monetary units**. The operating costs for any assignment of demand point to location are shown in the following table.</h1>     

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

The **mathematical programming formulation** is given below. cij , i=1,...,10  j=1,...,5 are the operating costs and fj, j=1,...,5 are the capacities of the locations.

- The wij binary variables denote the assignments of demand points to locations : wij=1 if demand point i is assigned to location j, otherwise 0. 
- The dj binary variables indicate the selected locations: dj=1 if location j is used, otherwise 0. 
- The first set of constraints ensures that each demand point is allocated to exactly one location.
- The second set of constraints forces each location j to have at most fj demand points.

<img style="float: left;" src="https://cloud.githubusercontent.com/assets/12450688/24873799/ee2099c6-1e2a-11e7-980a-43c0090be6c1.jpg" width="400" height="800" />



First we import numpy and the LPSOLVE library. The library exposes only a function lpsolve() therefore we import 'all' to avoid writing lpsolve55.lpsolve() at each call. 


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

We define the coefficients of the objective function ('set_obj_fn') and we set the direction of optimization to min (set_minim).



```python
for i in range(ncols):
    lpsolve('set_col_name', lp, i+1, col_names[i])

obj_values = c.flatten(order='C').tolist()+[30.]*5

lpsolve('set_obj_fn', lp, obj_values)
lpsolve('set_minim', lp)
```

We can now define the constraints one by one. First is the set of 10 constraints which ensures that each demand point is assigned to exactly one location. For each one, we pass to 'add_constraint' a list with the coefficients, the type of the constraint (here 'EQ' meaning equality) and the RHS. 


```python
## sum(j:wij)=1 for all i
for i in range(1,11):
    const_names = ['w'+str(i)+str(j) for j in range(1,6)]
    indices = [col_names.index(name) for name in const_names]
    values = np.zeros(ncols) ; values[indices]=1.
    lpsolve('add_constraint',lp, values, 'EQ', 1.0)
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
```

The last step is to define all variables as binary using 'set_binary'. The last argument (1) is a True flag.

We also export the model in a file, in LP format. xxxxx

Finally, we call 'solve'. The return code is 0 (success).


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

lpsolve('delete_lp', lp)
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
    
