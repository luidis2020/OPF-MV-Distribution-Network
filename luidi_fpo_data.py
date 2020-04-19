# normalização e cálculo da impedância ao quadrado
for l in model.L
    for n in model.L
        for m in model.L
            model.Imax[l,n,m] = model.Imax[l,n,m] * model.r3
            model.R[l,n,m]= model.R[l,n,m] / 1000
            model.X[l,n,m]= model.X[l,n,m] / 1000
            model.Z2[l,n,m]= model.R[l,n,m]**2 + model.X[l,n,m]**2


#Setting Substation voltage over 0.96 up to 1.04 p.u
    model.V2[0] = (model.vb*1.04)**2

    for n in model.N if n!= SE
    model.V2[n] = model.vb**2

    model.V2[SE] = model.vb**2
    model.V2[SE].fixed = True

    for n in model.N if n!= SE
        model.Pg[n] = 0
        model.Pg[n].fixed=True
        model.Qg[n] = 0
        modek.Qg[n].fixed=True


for n in model.N if n!= SE
    model.Pd[n]=model.Pd[n]
    model.Qd[n]=model.Qd[n]


for n in model.N if n!= SE
    model.SMAXGD[n]=model.SMAXGD[n]

for n in model.N if SMAXGD[n]==0
        model.PG[n]=0
for n in model.N if SMAXGD[n]==0
        model.QG[n]=0


model.Pg[SE].fixed=False
model.Qg[SE].fixed=False

