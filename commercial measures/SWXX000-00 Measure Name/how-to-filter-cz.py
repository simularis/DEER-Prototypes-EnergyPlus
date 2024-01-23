from pathlib import Path
import pandas

if "__main__" == __name__:
    CLIMATES_ALL = ['CZ01', 'CZ02', 'CZ03', 'CZ04', 'CZ05', 'CZ06', 'CZ07', 'CZ08',
                    'CZ09', 'CZ10', 'CZ11', 'CZ12', 'CZ13', 'CZ14', 'CZ15', 'CZ16']
    climates_enabled = ['CZ01']
    #climates_enabled = CLIMATES_ALL
    
    root = Path()
    climates_files = root.glob("**/climates.csv")
    for climate_file in climates_files:
        print(climate_file)
        df_climate = pandas.read_csv(
            climate_file,
            dtype=str)
        df_climate['skip'] = df_climate.apply(
            lambda x: "" if x['climate'] in climates_enabled else "#",
            axis=1)
        df_climate.to_csv(climate_file, index=False)



