**Data Processing Script**

This script processes claims, pharmacy, and reverts data from CSV and JSON files to generate various metrics and recommendations.

It produces three output JSON files:

1. metrics.json - Metrics aggregated by npi and ndc.

2. recommend.json - Recommended pharmacies with the two lowest average prices per ndc.

3. most-commom.json - Five most common quantities prescribed per ndc.


**Requirements**

Python 3.7+

pandas (installed automatically by the script if missing)

The script will attempt to install pandas automatically if it's not found.


**Sample Data Format**

1. claims JSON

{"id": "c3fd9586-b163-45d1-8445-37f573ec8c2b", "ndc": "55154445200", "npi": "7777777777", "quantity": 1, "price": 676.1, "timestamp": "2024-02-01T14:55:56"}

2. pharmacies CSV

chain	npi

health	1234567890

3. reverts JSON 

{"id": "509ec2fe-f2db-4da0-bef3-9cb4fd54dfe7", "claim_id": "983ccb14-dacd-49f7-9ddb-a5299ed6cdb7", "timestamp": "2024-04-02T21:41:19"}


**How to Run**

Clone or download this repository to your local machine.

Prepare your data files:

Place claims files (.json or .csv) into data/claims/

Place pharmacies files (.json or .csv) into data/pharmacies/

Place reverts files (.json or .csv) into data/reverts/

Run the script:

python data-project-paulo.py


Check the outputs in the output/ folder:

metrics.json

recommend.json

most-commom.json


**Notes**

The script automatically creates the output/ folder if it doesn't exist.

It merges and processes all .csv and .json files in each data folder.

Data types for npi and ndc are treated as strings to preserve leading zeros.

The most-commom.json file is post-processed to make the lists more readable.


**License**

This project is provided as-is for demonstration and testing purposes.
