import os, sys
import re
import httk.task

# Generate input files for a group of metal-N binaries in B1 structure.
elems = ["Ti", "Al"]
poscar_template = "POSCAR.template"

for elem in elems:
    # Read the placeholder POSCAR and substitute the dummy element with
    # the wanted element.
    with open(f"template/{poscar_template}", "r") as f:
        poscar = f.read()
    new_poscar = re.sub('Am', elem, poscar)
    with open("POSCAR", "w") as f:
        f.write(new_poscar)

    httk_struct = httk.load("POSCAR")

    # One can add tags to the structure thusly:
    httk_struct.add_tag('source_POSCAR', poscar_template)

    # Easy way to get a unique name for the job is to use the
    # hash of the structure:
    # job_name = httk_struct.hexhash

    # One can also use human-readable names, if there is no danger
    # of overlaps:
    job_name = f"{elem}N_B1"

    # One can divide the jobs between queues, e.g. to balance the usage
    # of CPU hours between projects.
    # Here we just use one queue to run our test calculations:
    queue = "tetralith"

    try:
        dir = httk.task.create_batch_task(f"Runs/{queue}", "template",
                {"structure": httk_struct},
                name=job_name,
                overwrite_head_dir=True)
        print(f"Generated run for: {httk_struct.formula} in {dir}")
        try:
            os.remove("POSCAR")
        except:
            pass

    except Exception as e:
        raise

