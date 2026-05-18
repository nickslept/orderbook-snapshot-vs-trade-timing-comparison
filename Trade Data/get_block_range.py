"""
Gets the block range for specified timestamps using binary search.
Adjust START_DATE_READABLE and END_DATE_READABLE to adjust the date range. Times are in UTC.
Note that the API key is hardcoded here for simplicity.

These block numbers will then be used to fetch trades from the blockchain within the specified block range.
This allows for consistent comparison between snapshot data and on-chain trade data.
"""
import requests
from datetime import datetime, timezone

#year, month, day, hour, minute, second
START_DATE_READABLE  = datetime(2026, 1,  15,  0,  0,  0, tzinfo=timezone.utc)
END_DATE_READABLE    = datetime(2026, 1, 29,  0,  0,  0, tzinfo=timezone.utc)

START_DATE_UNIX = int(START_DATE_READABLE.timestamp())
END_DATE_UNIX   = int(END_DATE_READABLE.timestamp())

API_KEY = input("Enter your Etherscan API key: ")

def get_block_by_timestamp(timestamp, closest):
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": 137,
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": int(timestamp),
        "closest": closest,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "1":
        return int(data["result"])
    else:
        raise Exception(f"API Error: {data}")

start_block = get_block_by_timestamp(START_DATE_UNIX,  "after")
end_block   = get_block_by_timestamp(END_DATE_UNIX, "before")

print(f"Block range for {START_DATE_READABLE} UTC to {END_DATE_READABLE} UTC:")
print(f"Start block: {start_block}")
print(f"End block:   {end_block}")
print(f"Total blocks: {end_block - start_block:,}")
