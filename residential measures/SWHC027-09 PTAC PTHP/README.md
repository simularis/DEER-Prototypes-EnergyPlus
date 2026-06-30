Processing steps for this measure

```
cd C:\DEER-Prototypes-EnergyPlus
cd "residential measures/SWHC027-09 PTAC PTHP"
modelkit rake run
if there is an issue with warm up for SFm from dummy plenums. Update template file to 'singlefamily_ductonly_SWHC027.imf'

python result2.py --queryfile "query_SWHC027_res.txt"
```

Then find "simdata.csv". Use Excel workbook provided in eTRM to compute UEC and UES.

## Load Shapes
Create the `results-summary.csv` which will be used for load shapes post-processing.
```
cd C:\DEER-Prototypes-EnergyPlus
cd "residential measures/SWHC027-09 PTAC PTHP/SWHC027-09 PTAC PTHP_MFm_Ex"
python ../../../scripts/result.py . --queryfile query.txt
```
Confirm output file `results-sizing-agg.csv` has been created. Rename to `results-summary.csv`
Delete `results-sizing-detail.csv` made by this query file.

Repeat for
SWHC027-09 PTAC PTHP_MFm_New
SWHC027-09 PTAC PTHP_SFm_1975
SWHC027-09 PTAC PTHP_SFm_1985
SWHC027-09 PTAC PTHP_SFm_New

```
cd C:\DEER-Prototypes-EnergyPlus
cd "scripts/data tranformation"
python MFm.py
python SFm.py
Repeat each for new and existing.
```