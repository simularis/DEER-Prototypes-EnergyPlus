
"""
clean_loadshapes.py

Utility to remove extraneous data from "loadshapes" CSV/ZIP file.

Here is an outline of this script:
•	Import zipfile, pandas, sqlite3
•	Take the name of the zip file as a variable “df1”
•	Open the zipfile and with the zip file open:
  o	Iterate through zipfile contents and find the first filename ending in CSV
  o	Use pandas.read_csv to read the CSV data into a dataframe object
•	Create a sqlite3 connection ‘conn’ to filename “temp.sqlite3”
•	Using the sqlite3 connection:
  o	Df1.to_sql(name='loadshapes_long',con=conn,if_exists='replace',index=false)
•	Write a sqlite3 query statement to drop rows that are not required. You can open the file ‘temp.sqlite3’ with Db Browser to test the query. Enter the query as a string into the script. E.g.,
  o	DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Glassdoor-LED-AirCond' and "BldgLoc" = 'CZ15';
  o	DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Glassdoor-LED-EvapCond' and "BldgLoc" != 'CZ15'; 
•	Using the sqlite3 connection:
  o	Conn.executescript(query)
  o	Df2 = Pandas.read_sql(‘select * from loadshapes_long’, conn)
•	Write df2 to a new CSV file inside a new ZIP file
"""

import zipfile
import pandas
import sqlite3
import os


def clean_loadshapes(zip_filename, output_zip_filename='cleaned_loadshapes.zip'):
    """
    Clean loadshapes data by removing extraneous rows and writing to a new ZIP file.
    
    Args:
        zip_filename: Path to the input ZIP file containing CSV data
        output_zip_filename: Path for the output ZIP file (default: 'cleaned_loadshapes.zip')
    """
    
    # Step 1: Extract CSV from ZIP file
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
    
    # Step 2: Create SQLite connection and write data
    conn = sqlite3.connect('temp.sqlite3')
    df1.to_sql(name='loadshapes_long', con=conn, if_exists='replace', index=False)
    
    # Step 3: Define and execute cleanup queries
    query = """
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Glassdoor-LED-AirCond' and "BldgLoc" = 'CZ15';
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Glassdoor-LED-EvapCond' and "BldgLoc" != 'CZ15';
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Open-LED-AirCond' and "BldgLoc" = 'CZ15';
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Open-LED-EvapCond' and "BldgLoc" != 'CZ15';
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Open-Flrsnt-AirCond' and "BldgLoc" = 'CZ15';
    DELETE FROM "loadshapes_long" where "TechID" = 'NE-Ref_Storage-VertDisplay-Open-Flrsnt-EvapCond' and "BldgLoc" != 'CZ15';
    """
    
    conn.executescript(query)
    
    # Step 4: Read cleaned data back from SQLite
    df2 = pandas.read_sql('select * from loadshapes_long', conn)
    conn.close()
    
    print(f"Cleaned data shape: {df2.shape}")
    
    # Step 5: Write cleaned data to new ZIP file
    # Use the original CSV filename (without path)
    output_csv_filename = os.path.basename(csv_filename)
    
    with zipfile.ZipFile(output_zip_filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output_zip:
        df2.to_csv(output_csv_filename, index=False)
        output_zip.write(output_csv_filename)
    
    # Clean up temporary CSV file
    os.remove(output_csv_filename)
    
    print(f"Cleaned data written to {output_zip_filename}")


if __name__ == '__main__':
    # Example usage - modify the input filename as needed
    input_zip = 'CEDARS_LoadShape_Com - SWCR015 v2 (1).zip'
    
    if os.path.exists(input_zip):
        clean_loadshapes(input_zip)
    else:
        print(f"Error: {input_zip} not found")

