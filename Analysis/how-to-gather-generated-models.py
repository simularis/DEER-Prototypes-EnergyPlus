#!/usr/bin/env python
# coding: utf-8

"""Display simulation progress bars, one for each subfolder under analysis root with model input files.

Usage:
    $terminal> cd C:/Users/user1/source/DEER-Prototypes-EnergyPlus/Analysis/
    $terminal> python how-to-gather-generated-models.py
    $terminal> tree /F results

Example output:

    C:\..\Analysis\results
    ├───CSV_files
    │       HSPF_9p0_SEER_16_Msr&SFm&1&rDXHP&Ex&dxHP_equip&CZ01.csv
    │       ...
    │       HSPF_9p0_SEER_16_Msr&SFm&1&rDXHP&Ex&dxHP_equip&CZ16.csv
    │       Msr-Res-GasFurnace-AFUE95-ECM&SFm&1&rDXGF&Ex&SpaceHtg_eq__GasFurnace&CZ01.csv
    │       ...
    │       Msr-Res-GasFurnace-AFUE95-ECM&SFm&1&rDXGF&Ex&SpaceHtg_eq__GasFurnace&CZ16.csv
    │
    └───IDF_files
            HSPF_9p0_SEER_16_Msr&SFm&1&rDXHP&Ex&dxHP_equip&CZ01.idf
            ...
            HSPF_9p0_SEER_16_Msr&SFm&1&rDXHP&Ex&dxHP_equip&CZ16.idf
            Msr-Res-GasFurnace-AFUE95-ECM&SFm&1&rDXGF&Ex&SpaceHtg_eq__GasFurnace&CZ01.idf
            ...
            Msr-Res-GasFurnace-AFUE95-ECM&SFm&1&rDXGF&Ex&SpaceHtg_eq__GasFurnace&CZ16.idf

@Author: Nicholas Fette <nfette@solaris-technical.com>
@Date: 2023-09-21
"""

import glob
from pathlib import Path
import shutil
#from datetime import datetime


FILENAME_FINISHED = 'instance-out.sql'

NEW_FILE_PATTERNS = {
 'instance.idf': 'results/IDF_files/{techid}&{cohort}&{cz}.idf',
 'instance-var.csv': 'results/CSV_files/{techid}&{cohort}&{cz}.csv',
}

def gather_generated_models(root, gather_patterns, progressbar=False, dryrun=False):
    """
    Copy model files and hourly output files to a different folder.

    Assumes that files are placed within a "runs" subfolder.
    """

    if progressbar:
        from tqdm import tqdm

    # Loop over subfolders and create progress bars.
    for subroot in root.glob('*'):
        subroot_relpath = subroot.relative_to(root)
        # Count composed models.
        subroot_finished_list = list(subroot.glob('**/runs/**/'+FILENAME_FINISHED))
        n_models = len(subroot_finished_list)

        if n_models > 0:
            if progressbar:
                # Create the progress bar here.
                myiter = tqdm(subroot_finished_list, desc=subroot_relpath.parts[0])
            else:
                myiter = subroot_finished_list

            for f1 in myiter:
                for patternfrom, patternto in NEW_FILE_PATTERNS.items():
                    filefrom = f1.parent.joinpath(patternfrom)
                    relpath = filefrom.relative_to(root)
                    # E.g. relpath = SFm_Furnace_1975\runs\CZ01\SFm&1&rDXGF&Ex&SpaceHtg_eq__GasFurnace\Msr-Res-GasFurnace-AFUE95-ECM\instance-out.sql
                    #print(relpath.parts)
                    meas_group, _, cz, cohort, techid, _ = relpath.parts
                    #print(meas_group, cz, cohort, techid)
                    
                    # Copy the file
                    # to-do
                    fileto = Path(patternto.format(meas_group=meas_group, cz=cz, cohort=cohort, techid=techid))
                    if not progressbar:
                        print(fileto)
                    
                    dryrun = False
                    if dryrun:
                        pass
                    else:
                        fileto.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copy(filefrom, fileto)

            if progressbar:
                myiter.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="""Copy model files and hourly output files to a different folder."""
    )

    # default_root: assume current directory = repo/Analysis and we want files from repo/Analysis:
    default_root = Path("./")

    parser.add_argument("analysis_root", metavar='analysis-root', nargs="?",
                        type=Path, default=default_root,
                        help="Analysis folder path, e.g. C:/Users/user1/source/DEER-Prototypes-EnergyPlus/Analysis")
    parser.add_argument("--progressbar", action="store_true")

    args=parser.parse_args()
    gather_generated_models(
        args.analysis_root,
        NEW_FILE_PATTERNS,
        progressbar=args.progressbar
    )
