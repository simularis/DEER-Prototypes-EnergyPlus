# SWHC045 Heat Pump HVAC Fuel Substitution

This document describes the steps necessary to reproduce simulations and model outputs for this measure.
# Running models
cd C:/.../SWHC045-07 Heat Pump HVAC Fuel Sub/SWHC045-07 Heat Pump HVAC Fuel Sub_DMo_Ex
modelkit rake run

Generate 'results-sizing-agg.csv' using result.py and query_default.txt
Rename to 'results-summary.csv'

repeat for 
SWHC045-07 Heat Pump HVAC Fuel Sub_MFm_Ex
SWHC045-07 Heat Pump HVAC Fuel Sub_SFm_1975
SWHC045-07 Heat Pump HVAC Fuel Sub_SFm_1985

## Post Processing
cd cd C:/.../SWHC045-07 Heat Pump HVAC Fuel Sub
Generate 'simdata.csv' using result2.py and query_default.txt

# Load Shapes
cd C:/.../scripts/data transformation
python DMo.py
python MFm.py
python SFm.py