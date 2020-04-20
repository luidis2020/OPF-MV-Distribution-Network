"""
ReferenceModel.py                           Deterministic reference Pyomo model
ReferenceModel.dat                          Reference model data
InitializeModel.dat                         Initialize model data

ScenarioStructure.py                        PySP model to specify the structure of the scenario tree
ScenarioStructure.dat                       Data to instantiate the parameters set of the scenario tree

AboveAverageScenario.dat                    Data for above average scenario
AverageScenario.dat                         Data for average scenario
BelowAverageScenario.dat                    Data for below average scenario

"""

import pandas as pd
from pyomo.environ import *
from pyomo.core import *


model= AbstractModel()

model.N=set()
model.L=set()

model.Pd = Param(model.N)
model.Qd = Param(model.N)
model.SMAXGD=Param(model.N,domain=NonNegativeReals)
model.fpgdm = Param(model.N)
model.fpgdM = Param(model.N)

model.SE=Param(initialize=0)
model.SE.fixed=True
model.vb=Param(initialize=12.66)
model.vb.fixed=True

model.R=Param(model.L)
model.X=Param(model.L)
model.Z2=Param(model.L)
model.Imax=Param(model.L)

model.r3=Param(initialize=1.7320508076)
model.r3.fixed=True

model.Pg=Var(model.N)
model.Qg=Var(model.N)
model.V2=Var(model.N,domain=NonNegativeReals)

model.I2=Var(model.L,domain=NonNegativeReals)
model.P=Var(model.L)
model.Q=Var(model.L)
model.PG=Var(model.N,domain=NonNegativeReals)
model.QG=Var(model.N)

    #Objective loss energy minimization
def lossenergy(model):
    return sum(model.I2[l,m,n]*model.R[l,m,n] for (l,m,n) in model.L for n in model.L)

model.value=Objective(rule=lossenergy, sense=minimize)

    #Constraints  active power balance
def activepower(model):
    return (model.P[l, m, n] -sum(model.P[l, n, m]+ model.I2[l, n, m] * model.R[l, n, m])+ model.Pg[nn]\
            + model.PG[nn] == model.Pd[nn] for (l,m,n) in model.L for nn in model.N )
model.constraint_1=Constraint(rule=activepower)


    # Constraints reactive power balance
def reactivepower(model):
    return (model.Q[l, m, n] - sum(model.Q[l, n, m]+ model.I2[l, n, m] * model.X[l, n, m])\
            + model.Qg[nn] + model.QG[nn] == model.Qd[nn] for (l,m,n) in model.L for nn in model.N)
model.constraint_2=Constraint(rule=reactivepower)

    # Constraints voltage limit
def voltage_limit(model):
    return (model.V2[m]-model.V2[n]==2*(model.P[l,m,n]*model.R[l,m,n]\
            +model.Q[l,m,n]*model.X[l,m,n])+model.I2[l,m,n]*model.Z2[l,m,n] for (l,m,n) in model.L)
model.constraint_3=Constraint(rule=voltage_limit)

    # Constraints current limit
def current_limit(model):
    return (model.V2[n] * model.I2[l, m, n] >= model.P[l, m, n]**2\
            + model.Q[l, m, n]**2 for (l,m,n) in model.L)
model.constraint_4=Constraint(rule=current_limit)

    #Despatchable generation constraints
def DG_limit_one(model):
    return (model.PG[n]**2 + model.QG[n]**2 <= model.SMAXGD[n]**2 for n in model.N)
model.constraint_5=Constraint(rule=DG_limit_one)

def DG_limit_two(model):
    return (model.QG[n] <= model.PG[n] * tan(acos(model.fpgdm[n])) for n in model.N)
model.constraint_6=Constraint(rule=DG_limit_two)

def DG_limit_three(model):
    return (model.QG[n] >= -model.PG[n] * tan(acos(model.fpgdM[n])) for n in model.N)
model.constraint_7=Constraint(rule=DG_limit_three)



#exec(open('luidi_fpo_data.py').read())
#exec(open('luidi_fpo_sp33n_data.py').read())





