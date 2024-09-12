PhonePe Data Analysis Dashboard
Overview
This project is a Streamlit-based dashboard that allows users to analyze PhonePe transaction data. It connects to a MySQL database (PhonePeDB) and provides various visualization options for exploring transaction trends, state-wise data, user concentration, and more.

Features
Data Exploration: View transaction data based on aggregators (Insurance, Transaction, User).
Map Analysis: Analyze transaction and insurance data on a map, including district-level and state-level data.
Top Analysis: Visualize top regions, transactions, and users based on total transaction amounts and registered users.
Customizable Inputs: Select data by year, quarter, state, or specific metrics.
Interactive Visualizations: Display data with bar charts, line charts, and pie charts.
Requirements
Streamlit: For creating the web application interface.
MySQL Connector: To connect the app to the PhonePe MySQL database.
Matplotlib & Seaborn: For plotting charts and visualizations.
Pandas: For data manipulation and analysis.
Setup Instructions
Install the required libraries:

bash
Copy code
pip install streamlit mysql-connector-python matplotlib seaborn pandas streamlit-option-menu
Clone the repository and navigate to the project directory:

bash
Copy code
git clone <repo-url>
cd PhonePe-Dashboard
Update the database connection details in the script:

python
Copy code
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="your_password",
    database="PhonePeDB"
)
Start the Streamlit app:

bash
Copy code
streamlit run app.py
Usage
Home Page: Displays a welcome image and overview of the dashboard.
Data Exploration: Allows users to explore data based on different aggregators such as insurance transactions, overall transactions, and user data.
Map Analysis: Provides district-level and state-level insights into insurance and transaction data.
Top Analysis: Displays the top states, pincodes, and users based on transaction metrics.
Available Functions
get_yearly_transaction_trends: Fetches quarterly transaction trends for a specified year.
get_state_wise_analysis: Analyzes state-wise transaction metrics.
get_transaction_type_analysis: Fetches transaction types for a specific year and quarter.
get_insurance_transactions_over_time: Shows insurance transaction trends over time for a state.
get_brand_popularity: Provides brand popularity based on transaction count.
get_geospatial_analysis: Fetches top states for transaction analysis based on a map.
get_district_level_insurance_analysis: Analyzes district-level insurance transactions.
get_top_regions_for_insurance: Shows the top regions for insurance based on transaction amounts.
get_user_concentration: Displays the concentration of registered users per state.
Example Usage
Data Exploration
Choose between Insurance, Transaction, or User metrics.
Provide necessary inputs (e.g., year, state) to filter and visualize data.
Map Analysis
Analyze district-level insurance metrics or state-wise transaction distribution.
Top Analysis
Visualize top regions for insurance or transaction amounts by state and pincode.
