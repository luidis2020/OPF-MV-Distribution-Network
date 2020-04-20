
for n in model.N:
    if n==0:
        model.V2[n] = (model.vb*1.04)**2
        model.V2[n] = model.vb ** 2
        model.V2[n].fixed = True
        model.Pg[n].fixed=False
        model.Qg[n].fixed=False


for (l,n,m) in model.L:
    model.Imax[l,n,m] = model.Imax[l,n,m] * model.r3
    model.R[l,n,m]= model.R[l,n,m] / 1000
    model.X[l,n,m]= model.X[l,n,m] / 1000
    model.Z2[l,n,m]= model.R[l,n,m]**2 + model.X[l,n,m]**2


    for n in model.N:
        if n!=model.SE:
            model.V2[n] = model.vb**2

    for n in model.N:
        if n!=model.SE:
            model.Pg[n] = 0
            model.Pg[n].fixed=True
            model.Qg[n] = 0
            model.Qg[n].fixed=True


    for n in model.N:
        if n!=model.SE:
            model.Pd[n]=model.Pd[n]
            model.Qd[n]=model.Qd[n]


    for n in model.N:
        if n!=model.SE:
            model.SMAXGD[n]=model.SMAXGD[n]

    for n in model.N:
        if SMAXGD[n]==0:
            model.PG[n]=0

    for n in model.N:
        if SMAXGD[n]==0:
            model.QG[n]=0


