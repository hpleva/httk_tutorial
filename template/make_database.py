#!/usr/bin/env python

import os, sys
import re
import httk, httk.iface.vasp_if
import httk.db
import httk.task
from httk.atomistic.results.totalenergyresult import Result_TotalEnergyResult

def make_database(db_name):
    try:
        os.remove(db_name)
    except:
        pass

    backend = httk.db.backend.Sqlite(db_name)
    store = httk.db.store.SqlStore(backend)
    store.delay_commit()

    reader = httk.task.reader('./', 'Runs', 'Total energy and elastic constants')

    index = 1
    for rundir, computation in reader:
        root = os.path.join(rundir, '..')
        # Check whether the calculation included atomic relaxations or not:

        initial_struct = httk.load(os.path.join(root, 'POSCAR'))
        struct = httk.load(os.path.join(rundir, "CONTCAR.relax-final"))

        # Handle tags
        tags = eval(initial_struct.get_tags()['comment'].value)
        initial_struct._tags = None
        initial_struct._codependent_data = []
        struct._tags = None
        struct._codependent_data = []
        for tag in tags:
            tmp = re.search("^\(Tag\)\s(.*):\s(.*)", tag)
            if tmp is not None:
                initial_struct.add_tag(tmp.groups()[0], tmp.groups()[1])
                struct.add_tag(tmp.groups()[0], tmp.groups()[1])

        try:
            outcar = httk.iface.vasp_if.read_outcar(os.path.join(rundir, "OUTCAR.cleaned.relax-final"))
            final_energy = float(outcar.final_energy)
        except:
            final_energy = 0.0

        result = Result_TotalEnergyResult(
                computation,
                struct,
                final_energy,
                )
        store.save(result)
        print("{0:3} Processed outcar: {1:10}".format(index, initial_struct.formula))
        index += 1

    store.commit()

if __name__ == '__main__':
    db_name = 'example.sqlite'
    make_database(db_name)
