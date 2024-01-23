from pathlib import Path
import pandas

if "__main__" == __name__:
    BUILDINGS_COM_ALL = ['Asm', 'ECC',  'EPr',  'ERC', 'ESe', 'EUn',  'Fin',  'Gro',
                     'Hsp',  'Htl',  'Lib',  'MBT',  'MLI',  'Mtl',  'Nrs', 'OfL',
                     'OfS',  'Rel',  'RFF',  'RSD',  'Rt3', 'RtL',  'RtS',  'SCn',  'SUn']
    #buildings_enabled = ['Asm']
    buildings_enabled = BUILDINGS_COM_ALL

    buildings_enabled_subset_htl = list(filter(lambda x: x == 'Htl', buildings_enabled))
    buildings_enabled_subset_other = list(filter(lambda x: x != 'Htl', buildings_enabled))
    print(buildings_enabled_subset_htl, buildings_enabled_subset_other)

    root = Path()
    cohorts_files = root.glob("**/cohorts.csv")
    for cohorts_file in cohorts_files:
        print(cohorts_file)
        df_cohorts = pandas.read_csv(
            cohorts_file,
            dtype=str)
        if '_Htl_' in cohorts_file.as_posix():
            df_cohorts['skip'] = df_cohorts.apply(
                lambda x: "" if x['cohort'] in buildings_enabled_subset_htl else "#",
                axis=1)
        else:
            df_cohorts['skip'] = df_cohorts.apply(
                lambda x: "" if x['cohort'] in buildings_enabled_subset_other else "#",
                axis=1)

        df_cohorts.to_csv(cohorts_file, index=False)

