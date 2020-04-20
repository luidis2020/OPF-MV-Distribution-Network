


exec(open('luidi_fpo_model.py').read())
exec(open('luidi_fpo_data.py').read())
exec(open('luidi_fpo_sp33n_data.py').read())

results = []
solver = SolverFactory('ipopt')
solver.solve(model)
results.append([model.V2])

results = pd.DataFrame(results, columns=['V2'])

print(results)
datatoexcel=pd.ExcelWriter('resultsV2.xlsx',engine='xlsxwriter')
results.to_excel(datatoexcel,sheet_name='Sheet1')
datatoexcel.save()

