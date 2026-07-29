# SWCR003-05 Fan Motor Retrofit for a Refrigerated Display Case

There are no special instructions for measure setup or running simulations.

## Load Shape Workaround
The load shape files (found in CEDARS_LoadShape_Com.zip) are missing the 'NormUnit' column required for uploading to CEDARS. The missing column must be added manually into each of the 3 load shape files (one for each building type). The column must be added in between the 'BldgLoc' and 'Type (Whole Building or End Use)' columns with the column header 'NormUnit' and value 'Cap-Tons' for each line.