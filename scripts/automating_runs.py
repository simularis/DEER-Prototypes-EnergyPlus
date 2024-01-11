# %%
import os
import subprocess
from pathlib import Path
from tqdm import tqdm
# TODO: Add option to handle existing run folders
#measure_folder_path = "..\\residential measures\\SWBE006-02 Ceiling Insulation" # or "..\\commercial measures\\SWXX000-00 Measure Name", an absolute path is recommended.
measure_folder_path = Path("..\\commercial measures\\SWXX000-00 Measure Name") # an absolute path is recommended.
dir_prototypes = [dir for dir in measure_folder_path.iterdir() if dir.is_dir()]

#%%
print("*** IMPORTANT ***\n- Always check modelkit_cmd_output.txt for potential modelkit output errors\n")
print("- This script will not override existing runs\n")

for prototype in tqdm(dir_prototypes):
    print("* Running: ",prototype)

    try:
        #f_stdout = prototype.joinpath('modelkit_clean_stdout.txt')
        #with f_stdout.open('w') as f:
        #    result = subprocess.run("modelkit rake clean", shell=True, check=True,text=True, cwd=prototype, stdout=f, stderr=subprocess.STDOUT, input='y')

        #f_stdout = prototype.joinpath('modelkit_compose_stdout.txt')
        #with f_stdout.open('w') as f:
        #    result = subprocess.run("modelkit rake compose", shell=True, check=True,text=True, cwd=prototype, stdout=f, stderr=subprocess.STDOUT)

        f_stdout = prototype.joinpath('modelkit_rake_stdout.txt')
        with f_stdout.open('a') as f:
            result = subprocess.run("modelkit rake", shell=True, check=True,text=True, cwd=prototype, stdout=f, stderr=subprocess.STDOUT)

        if "error" in f_stdout.read_text().lower():
            print("*** Potential error ***\n- Check modelkit_cmd_output.txt in ", prototype, " for a potential modelkit case running error\n")

    except subprocess.CalledProcessError as err:
        print("*** cmd error ***\n-Prototype '", prototype, "'\n-modelkit error:\n" + err.stderr)

    print()
# %%
