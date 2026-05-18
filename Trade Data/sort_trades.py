import os
import duckdb

con = duckdb.connect()

# ----------------------------------- PATH CONFIG -----------------------------------
#dbl check that you dont need more specific paths here later on
raw_file = "trades.parquet"
temp_sorted_file = "sorted_trades.parquet.tmp" 
final_sorted_file = "sorted_trades.parquet"
# ------------------------------------------------------------------------------------

print("Trying to sort trades based on market_id, asset_id, and timestamp...")

try:
    # 1. Delete any temp files from a previously unsuccessful run
    if os.path.exists(temp_sorted_file):
        os.remove(temp_sorted_file) 
        
    # 2. Sort and write trades.parquet to the TEMPORARY file
    con.execute(f"""
        COPY (
            SELECT * 
            FROM read_parquet('{raw_file}')
            ORDER BY market_id, asset_id, timestamp
        ) 
        TO '{temp_sorted_file}' (FORMAT PARQUET);
    """)
    
    # 3. If the write was successful, change the .tmp file to .parquet
    os.rename(temp_sorted_file, final_sorted_file)
    print(f"Sorted successfully! Saved as '{final_sorted_file}'")

except Exception as e:
    print(f"An error occurred during processing: {e}")
    # Delete the .tmp file so it doesn't take up disk space
    if os.path.exists(temp_sorted_file):
        os.remove(temp_sorted_file) 