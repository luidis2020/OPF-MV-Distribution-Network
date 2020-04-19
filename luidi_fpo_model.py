


from pyomo.environ import *
from pyomo.core import *
import xlsxwriter

def optimal_power_flow():
    model = ConcreteModel()
    model.N=set()
    model.L=set()


    model.SMAXGD=Param(model.N,domain=NonNegativeReals)
    model.fpgdm = Param(model.N)
    model.fpgdM = Param(model.N)
    model.SE=Param(initialize=0)
    model.SE.fixed = True
    model.vb=Param(initialize=12.66)
    model.vb.fixed = True
    model.Pd=Param(model.N)
    model.Qd=Param(model.N)
    model.Pd = Param(model.N)
    model.R=Param(L)
    model.X=Param(L)
    model.Z2=Param(L)
    model.Imax=Param(L)
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

    #Objective active power balance
    model.obj = Objective(expr=(model.I2[l,m,n]*model.R[l,m,n] for l in model.L for m in model.L\
                                for n in model.L), sense=minimize)
    #Constraints
    model.activepower = Constraint(expre=(model.P[l, m, n] -sum(model.P[l, n, m] \
                                                + model.I2[l, n, m] * model.R[l, n, m])+ model.Pg[nn]\
                                                + model.PG[nn] == model.Pd[nn] for l in model.L for m in model.L\
                                                for n in model.L for nn in model.N ))
    # Constraints
    model.reactivepower = Constraint(expre=(model.Q[l, m, n] - sum(model.Q[l, n, m]\
                                                + model.I2[l, n, m] * model.X[l, n, m])\
                                                + model.Qg[nn] + model.QG[nn] == model.Qd[nn] for l in model.L\
                                                for m in model.L for n in model.L for nn in model.N))

    # Constraints
    model.voltage_limit = Constraint(expre=(model.V2[m]-model.V2[n]==2*(model.P[l,m,n]*model.R[l,m,n]\
                                              +model.Q[l,m,n]*model.X[l,m,n])+model.I2[l,m,n]*model.Z2[l,m,n]\
                                            for l in model.L for m in model.L for n in model.L))

    # Constraints
    model.current_limit = Constraint(expre=(model.V2[n] * model.I2[l, m, n] >= model.P[l, m, n]**2\
                                            + model.Q[l, m, n]**2 for l in model.L for m in model.L\
                                            for n in model.L))

    #Despatchable generation constraints
    model.DG_limit_one=Constraint(expre=(model.PG[n]**2 + model.QG[n]**2 <= model.SMAXGD[n]**2\
                                         for n in model.N))

    model.DG_limit_two=Constraint(expre=(model.QG[n] <= model.PG[n] * tan(acos(model.fpgdm[n]))\
                                         for n in model.N))

    model.DG_limit_three=Constraint(expre=(model.QG[n] >= -model.PG[n] * tan(acos(model.fpgdM[n]))\
                                           for n in model.N))

    return model


exec(open('luidi_fpo_sp33n_data.py').read())
exec(open('luidi_fpo_data.py').read())


if __name__ == "__main__":

    # For a range of sv values, return ca, cb, cc, and cd
    results = []

    model= optimal_power_flow()
    solver = SolverFactory('ipopt')
    solver.solve(model)
    results.append([V2])

    results = pd.DataFrame(results, columns=['V2'])

    print(results)
    datatoexcel=pd.ExcelWriter('resultsV2.xlsx',engine='xlsxwriter')
    results.to_excel(datatoexcel,sheet_name='Sheet1')
    datatoexcel.save()







