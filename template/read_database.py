import httk.db
from httk.atomistic.results.totalenergyresult import Result_TotalEnergyResult

backend = httk.db.backend.Sqlite('example.sqlite')
store = httk.db.store.SqlStore(backend)

search = store.searcher()
search_in_results = search.variable(Result_TotalEnergyResult)
# search_in_structures = search.variable(Structure, parent = search_in_results,
#                                        parentkey = 'structure_structure_sid',
#                                        subkey='structure_id',
#                                       )

search.output(search_in_results, 'header')

for match, header in list(search):
    result = match[0]
    struct = result.structure
    print(f"Formula: {struct.formula:10}, total_energy = {result.total_energy:8.3f}")

