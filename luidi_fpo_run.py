

execfile('luidi_fpo_model.py')
execfile('luidi_fpo_sp33n_data.py')
execfile('luidi_fpo_data.py')



if __name__ == "__main__":

    # For a range of sv values, return ca, cb, cc, and cd
    results = []

    model= optimal_power_flow()
    solver = SolverFactory('ipopt')
    solver.solve(model)
    results.append([model.V2])

    results = pd.DataFrame(results, columns=['V2'])

    print(results)
    datatoexcel=pd.ExcelWriter('resultsV2.xlsx',engine='xlsxwriter')
    results.to_excel(datatoexcel,sheet_name='Sheet1')
    datatoexcel.save()

