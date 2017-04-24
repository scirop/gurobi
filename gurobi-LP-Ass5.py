#Python code using Gurobi package for PART 1
#NOTE: the names RHS and b vector have been used interchangeably

import sys 
import random
from gurobipy import * #import family of Gurobi functions

#defining the parametric function
def dense_optimize(rows, cols, A, sense, rhs, lb, ub, vtype, solution): 
#takes paramter inputs = number of rows and columns, A matrix, inequalities, RHS vector
#lower and upper bound on variables, variable type(continuous/discrete), initiated solution vector

  model = Model() #linear optimization model in Gurobi

  # Add variables to model
  vars = [] #initialization
  for j in range(cols): #iteration
    vars.append(model.addVar(lb=lb[j], ub=ub[j], vtype=vtype[j])) #add variables to model

  # Populate A matrix
  for i in range(rows): #iteration through rows
    expr = LinExpr()   #linear expression to store LHS
    for j in range(cols): #iteration through cells
      if A[i][j] != 0: #taking exxpressions for non-zero constraints only
        expr += A[i][j]*vars[j] #summation of pairs of coefficient and variable products
    model.addConstr(expr, sense[i], rhs[i]) #adding full constraint lines with LHS>=RHS

  model.optimize() # Solve with standard Gurobi function
  model.write('dense.lp')  # Write model to a file

  if model.status == GRB.Status.OPTIMAL: #if optimal solution reached
    x = model.getAttr('x', vars) #retrieve variable values
    for i in range(cols): #number of variables = number of columns
      solution[i] = x[i] #store in a solution vector
    return True
  else:
    return False

# Model data set
rows=10 #rows as given in question
cols=10 #columns as given in question
p=0.6   #density of A matrix as given in question
q=0.8   #density of b vector as given in question
L=-10   #lower bound on A matrix elements as given in question
U=30    #upper bound on A matrix elements as given in question
lbb=0   #lower bound on b vector elements
ubb=50  #upper bound on b vector elements

#Generating random matrix
flag=1 #for check of non-zero row or column
while flag == 1: #enter loop with assumption that a row or column is zero
#random matrix with values between 0 and 1
  A = [[random.uniform(0.0,1.0) for e in range(cols)] for e in range(rows)] 
  for i in range(rows):     #iteration through row
    for j in range(cols):   #iteration though each cell
      if A[i][j]>p:         #density check
        A[i][j]=0           #setting as zero
      else:
        A[i][j]=round(L+(A[i][j]/p)*(U-L),4)  #scaling for non-zero
  iflag=0
  for i in range(rows):
    zerorow=0 #initial row value sum zero
    for j in range(cols):
      zerorow=zerorow+A[i][j]
    if zerorow==0:
      iflag=1 #internal flag for sum check

  for j in range(cols):
    zerocol=0 #initial column value sum zero
    for i in range(rows):
      zerocol=zerorow+A[i][j]
    if zerocol==0:
      iflag=1 #internal flag for sum check

  if iflag==0: #it means that we didn't find a zero row or column
    flag=0 #flag gets zero and we get out of loop
  else:
    flag=1 #flag stays 1 and we reloop

sense = [GRB.GREATER_EQUAL for e in range(rows)] #Sense gives the sign of the constraint

rhs = [random.uniform(0.0,1.0) for e in range(rows)] #rhs is the b vector
for i in range(rows): #for iteration through elements
  if rhs[i] > q:      #check for density threshold
    rhs[i]=0          #setting zero for approx 20% of elements
  else:
    rhs[i]=round(lbb+(rhs[i]/q)*(ubb-lbb),4)  #scaling for the non-zero elements

lb = [0 for e in range(cols)] #lower bound for variables
ub = [GRB.INFINITY for e in range(cols)] #upper bound for variables (infinity)
vtype = [GRB.CONTINUOUS for e in range(cols)] #continuous variable taken
sol = [0]*cols #initialization for solution values of variables
print('A matrix:=')
print('\n'.join([' '.join(['{:10}'.format("%.2f" % item) for item in row]) 
      for row in A])) #structured printing for A matrix
print('RHS:=')
print(rhs) #printing the RHS

# Optimize (run the function as defined)
success = dense_optimize(rows, cols, A, sense, rhs, lb, ub, vtype, sol)

if success: #prints solutions if feasible
  for i in range(cols):
    print("X%s = %s" % (i+1,sol[i])) #print solution values