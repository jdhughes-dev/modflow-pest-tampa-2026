import os
import shutil

cwd = os.getcwd()

clear = False
pdf = False
html = False
allow_errors = False


def run_nb(nb_file, nb_dir="."):
    os.chdir(nb_dir)
    worker_dirs = [
        d for d in os.listdir(".") if os.path.isdir(d) and d.startswith("worker")
    ]
    for worker_dir in worker_dirs:
        shutil.rmtree(worker_dir)
    if allow_errors:
        os.system(
            "jupyter nbconvert --execute --ExecutePreprocessor.timeout=180000 --allow-errors --inplace {0}".format(
                nb_file
            )
        )
    else:
        os.system(
            "jupyter nbconvert --execute --ExecutePreprocessor.timeout=180000 --inplace {0}".format(
                nb_file
            )
        )
    if html:
        os.system("jupyter nbconvert --to html {0}".format(nb_file))
        md_file = nb_file.replace(".ipynb", ".html")
        shutil.move(md_file, os.path.join(md_file))
        print("preped htmlfile: ", os.path.join(md_file))
    if pdf:
        os.system("jupyter nbconvert --to pdf {0}".format(nb_file))
    if clear:
        os.system(
            "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --allow-errors --inplace {0}".format(
                nb_file
            )
        )
    os.chdir(cwd)
    return


nb_dir = "."
nb_file = "SV_setup_control_file.ipynb"
run_nb(nb_file, nb_dir)

nb_dir = "."
nb_file = "SV_obsvals_weights_noise.ipynb"
run_nb(nb_file, nb_dir)

nb_file = "SV_run_ies.ipynb"
run_nb(nb_file, nb_dir)

nb_file = "SV_run_opt.ipynb"
run_nb(nb_file, nb_dir)
