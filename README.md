Data Processing Script

This script processes claims, pharmacy, and reverts data from CSV and JSON files to generate various metrics and recommendations.

It produces three output JSON files:

metrics.json — Metrics aggregated by npi and ndc.

recommend.json — Recommended pharmacies with the two lowest average prices per ndc.

most-commom.json — Five most common quantities prescribed per ndc.

📂 Project Structure
project/
│
├── data/
│   ├── claims/        # JSON or CSV files containing claims data
│   ├── pharmacies/    # JSON or CSV files containing pharmacy info
│   └── reverts/       # JSON or CSV files containing claim reverts
│
├── output/            # Folder where output files will be generated
│
├── script.py          # The provided Python script
└── README.md

📦 Requirements

Python 3.7+

pandas (installed automatically by the script if missing)

The script will attempt to install pandas automatically if it's not found.

🧾 Sample Data Format
claims (JSON or CSV)
id	npi	ndc	price	quantity
1	1234567890	00011-0001	15.50	30
2	9876543210	00011-0001	14.75	60
pharmacies (JSON or CSV)
npi	chain
1234567890	PharmacyOne
9876543210	PharmacyTwo
reverts (JSON or CSV)
claim_id	id_revert
1	101
2	102
▶️ How to Run

Clone or download this repository to your local machine.

Prepare your data files:

Place claims files (.json or .csv) into data/claims/

Place pharmacies files (.json or .csv) into data/pharmacies/

Place reverts files (.json or .csv) into data/reverts/

Run the script:

python script.py


Check the outputs in the output/ folder:

metrics.json

recommend.json

most-commom.json

🛠 Notes

The script automatically creates the output/ folder if it doesn't exist.

It merges and processes all .csv and .json files in each data folder.

Data types for npi and ndc are treated as strings to preserve leading zeros.

The most-commom.json file is post-processed to make the lists more readable.

📄 License

This project is provided as-is for demonstration and testing purposes.
