
"""
clean_loadshapes.py

Utility to remove extraneous data from "loadshapes" CSV/ZIP file and rename
columns to match the expected output for upload to CEDARS. This is meant to be
customized to your measure and to document workaround to fix column name mismatch
between outputs from data transformation (e.g. Com.py and MfM.py) outputs
and CEDARS upload requirements.

To use this script:

    1. Modify the input filename in the main block at the bottom of this script.
    2. Modify the query_exclusions variable to remove any TechID/BldgLoc
      combinations that should be excluded from the output.
    3. Modify the query_transformation variable to rename columns and add any
      additional columns as needed.
    4. Run this script to create a new ZIP file containing the cleaned CSV data.
      The script will print the input column names and raise an error if the input columns do not match the expected list.
    5. If the script raises an error message, copy the list of input column names
      into the variable expected_input_columns for reference.

@Author: Nicholas Fette and Yasemin Agi
@Date: 2026-06-29

"""

import zipfile
import pandas
import sqlite3
import os
import Path from pathlib

def clean_loadshapes_zip(zip_filename,
                         output_dir=Path('cleaned_loadshapes'),
                         query_exclusions='',
                         query_transformation='SELECT * FROM loadshapes_long'
                         ):
    """
    Clean loadshapes data by removing extraneous rows and writing to a new ZIP file.
    
    Args:
        zip_filename: Path to the input ZIP file containing CSV data
        output_dir: Directory for the output ZIP files (default: 'cleaned_loadshapes')
    """
    
    # Extract CSV from ZIP file
    df1 = None
    csv_filename = None
    
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        # Find the first CSV file in the zip
        for filename in zip_file.namelist():
            if filename.endswith('.csv'):
                csv_filename = filename
                # Read the CSV into a dataframe
                df1 = pandas.read_csv(zip_file.open(filename))
                break
    
    if df1 is None:
        print(f"Error: No CSV file found in {zip_filename}")
        return
    
    print(f"Loaded CSV: {csv_filename}")
    print(f"Initial data shape: {df1.shape}")
    print(f"Input columns: {df1.columns.tolist()}")
    
    missing_columns_input = set(expected_input_columns) - set(df1.columns)
    if len(missing_columns_input) > 0:
        raise ValueError(f"Input columns do not match expected columns. Missing columns: {missing_columns_input}")

    # Create SQLite connection and write data
    conn = sqlite3.connect('temp.sqlite3')
    df1.to_sql(name='loadshapes_long', con=conn, if_exists='replace', index=False)
    
    # Execute query to apply exclusion rules (combinations of TechID and BldgLoc to skip in output)
    conn.executescript(query_exclusions)
    
    # Apply data transformations (column renaming, additional columns)
    statement_create_view = f"""CREATE VIEW loadshapes_long_cleaned AS {query_transformation};"""
    conn.execute("DROP VIEW IF EXISTS loadshapes_long_cleaned;") #(YA) Added
    conn.execute(statement_create_view)

    # Read cleaned data back from SQLite
    chunks = pandas.read_sql('select * from loadshapes_long_cleaned;', conn, chunksize=500*8760)
    for i,df2 in enumerate(chunks):

        print(f"Cleaned data shape: {df2.shape}")
        print(f"Output columns: {df2.columns.tolist()}")
        if set(expected_output_columns) - set(df2.columns):
            raise ValueError(f"Output columns do not match expected columns. Found: {df2.columns.tolist()}, Expected: {expected_output_columns}")

        # Write cleaned data to new ZIP file
        # Use the original CSV filename (without path)
        output_csv_filename = f"{os.path.basename(csv_filename)}_clean_{i+1}.csv"
        df2.to_csv(output_csv_filename, index=False)
        output_zip_filename = output_dir / f"{os.path.basename(csv_filename)}_clean_{i+1}.zip"
        with zipfile.ZipFile(output_zip_filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output_zip:    
            output_zip.write(output_csv_filename)
        # Clean up temporary CSV file
        os.remove(output_csv_filename)
        
        print(f"Cleaned data written to {output_zip_filename}")
    conn.close()
    

if __name__ == '__main__':
    # Step 1. Modify the input filename(s) as needed
    input_zips = [
        'CEDARS_LoadShape_DMo.zip', 
        'CEDARS_LoadShape_MFm.zip',
        'CEDARS_LoadShape_SFm.zip'
    ]

    # Step 2. Modify this query based on TechID & BldgLoc exclusions specific to the measure.
    query_exclusions = """

    """
    
    # Enter list of assumed column names in the input file to raise an error if the assumption is wrong.
    expected_input_columns = ['Sector', 'BldgType', 'BldgVint', 'BldgHVAC', 'BldgLoc',
        'Type (Whole Building or End Use)', 'Source Year', 'TechGroup',
        'TechType', 'TechID', 'Hour of Year', 'UECproportion']
    
    # Enter list of required output column names to raise an error if the data transformation fails to yield these columns.
    expected_output_columns = ['Sector', 'BldgType', 'BldgVint', 'BldgHVAC', 'BldgLoc', 'NormUnit',
        'Type (Whole Building or End Use)', 'Source Year', 'TechGroup',
        'TechType', 'TechID', 'Hour of Year', 'UECproportion']
    
    # Step 3. Modify this query based on mismatch between the column names in the CSV and the desired output.
    # In each row of the query, the left side is the input and the right side is the output.
    # To take an input from an existing column, enter the column name in double quotes, e.g. "Sector".
    # To enter a constant value, enter the value in single quotes, e.g. 'Cap-Tons'.
    # Comment text on each line after a double dash is ignored.
    query_transformation = f"""SELECT
    "Sector" AS "Sector",
    "BldgType" AS "BldgType",
    "BldgVint" AS "BldgVint",
    "BldgHVAC" AS "BldgHVAC", -- customize to match measure case BldgHVAC
    "BldgLoc" AS "BldgLoc",
    "NormUnit" AS "NormUnit", -- use this line if the input CSV already has a column named "NormUnit"
    -- 'Cap-Tons' AS "NormUnit", -- uncomment this line if the input CSV does not have a column named "NormUnit"
    "Type (Whole Building or End Use)" AS "Type (Whole Building or End Use)", -- use this line if the input CSV already has the column
    -- "Type" AS "Type (Whole Building or End Use)", -- uncomment this line if "Type" column needs to be renamed in output
    "Source Year" AS "Source Year",
    "TechGroup" AS "TechGroup",
    "TechType" AS "TechType",
    "TechID" AS "TechID",
    "Hour of Year" AS "Hour of Year",
    "UECproportion" AS "UECproportion"
    FROM loadshapes_long
    ORDER BY "BldgType", "BldgVint", "BldgHVAC", "BldgLoc", "TechID", "Hour of Year"
    """

    # (YA) Modified 

    for input_zip in input_zips:
        if os.path.exists(input_zip):
            clean_loadshapes_zip(
                zip_filename=input_zip,
                output_dir=Path('cleaned_loadshapes'),
                query_exclusions=query_exclusions,
                query_transformation=query_transformation
            )
        else:
            print(f"Error: {input_zip} not found")
