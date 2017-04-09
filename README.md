<h2 style="color:blue;">Introduction</h2> 

**LPSOLVE** is an excellent open source solver for mathematical programming problems. It can be used for linear (LP), integer (IP) and mixed integer linear (MILP) problems. It is distributed under the GNU Lesser General Public License. 

[http://lpsolve.sourceforge.net/5.5/](http://lpsolve.sourceforge.net/5.5/ "LPSOLVE")

This tutorial shows how to install LPSOLVE and use it with Python. 


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

				
![formulation](https://cloud.githubusercontent.com/assets/12450688/24839344/e9526b1a-1d60-11e7-83fa-ff01bdb3be5d.png)				
 