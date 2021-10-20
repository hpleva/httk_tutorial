import httk.db
from httk.atomistic import Structure
from httk.atomistic.results.totalenergyresult import Result_TotalEnergyResult

backend = httk.db.backend.Sqlite('example.sqlite')
store = httk.db.store.SqlStore(backend)

# A simple search that shows all results:
search = store.searcher()
search_in_results = search.variable(Result_TotalEnergyResult)
search.output(search_in_results, 'header')

print("\nSimple search: Show all results:")
for match, header in list(search):
    result = match[0]
    struct = result.structure
    print(f"Formula: {struct.formula:10}, total_energy = {result.total_energy:8.3f}")

# A more advanced search that only shows structures that contain Ti
search = store.searcher()
search_in_results = search.variable(Result_TotalEnergyResult)
search_in_structures = search.variable(Structure, parent = search_in_results,
                                       parentkey = 'structure_structure_sid',
                                       subkey='structure_id',
                                      )
criterion = search_in_structures.formula_symbols.is_in("Ti")
search.add(criterion)
search.output(search_in_results, 'header')

print("\nA more advanced search: Show only Ti-containing alloys:")
for match, header in list(search):
    result = match[0]
    struct = result.structure
    print(f"Formula: {struct.formula:10}, total_energy = {result.total_energy:8.3f}")
