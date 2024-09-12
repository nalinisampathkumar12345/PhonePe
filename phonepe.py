import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Define functions for data analysis

def get_yearly_transaction_trends(connection, year):
    query = """
    SELECT Quarter, SUM(TransactionCount) AS TotalTransactions, SUM(TransactionAmount) AS TotalAmount
    FROM agg_transactions
    WHERE Year = %s
    GROUP BY Quarter
    ORDER BY Quarter;
    """
    cursor = connection.cursor()
    cursor.execute(query, (year,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_state_wise_analysis(connection):
    query = """
    SELECT State, SUM(TransactionCount) AS TotalTransactions, SUM(TransactionAmount) AS TotalAmount
    FROM agg_transactions
    GROUP BY State
    ORDER BY TotalAmount DESC;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_transaction_type_analysis(connection, year, quarter):
    query = """
    SELECT TransactionType, SUM(TransactionCount) AS TotalTransactions, SUM(TransactionAmount) AS TotalAmount
    FROM agg_transactions
    WHERE Year = %s AND Quarter = %s
    GROUP BY TransactionType
    ORDER BY TotalAmount DESC;
    """
    cursor = connection.cursor()
    cursor.execute(query, (year, quarter))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_insurance_transactions_over_time(connection, state):
    query = """
    SELECT 
    EXTRACT(YEAR FROM `From`) AS Year,
    SUM(TransactionCount) AS TotalTransactions,
    SUM(TransactionAmount) AS TotalAmount
    FROM 
        agg_insurance
    WHERE 
        State = %s
    GROUP BY 
        EXTRACT(YEAR FROM `From`)
    ORDER BY 
        TotalTransactions DESC;
        """
    cursor = connection.cursor()
    cursor.execute(query, (state,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_brand_popularity(connection):
    query = """
    SELECT Brands, SUM(TransactionCount) AS TotalTransactions, AVG(Percentage) AS AvgMarketShare
    FROM agg_user
    GROUP BY Brands
    ORDER BY TotalTransactions DESC;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_geospatial_analysis(connection, year, quarter):
    query = """
    SELECT State, SUM(TransactionCount) AS TotalTransactions, SUM(TransactionAmount) AS TotalAmount
    FROM map_transactions
    WHERE Year = %s AND Quarter = %s
    GROUP BY State
    ORDER BY TotalTransactions DESC LIMIT 10;
    """
    cursor = connection.cursor()
    cursor.execute(query, (year, quarter))
    result = cursor.fetchall()
    cursor.close()
    return result
#analyzing district-wise performance or distribution of insurance activities.
def get_district_level_insurance_analysis(connection, state):
    query = """
    SELECT District, SUM(Metric) AS TotalMetric
    FROM map_insurance
    WHERE State = %s
    GROUP BY District
    ORDER BY TotalMetric DESC ;
    """
    cursor = connection.cursor()
    cursor.execute(query, (state,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_top_regions_for_insurance(connection):
    query = """
    SELECT State, Pincode, SUM(TransactionAmount) AS TotalAmount, SUM(TransactionCount) AS TotalCount
    FROM top_insurance
    GROUP BY State, Pincode
    ORDER BY TotalAmount DESC limit 10;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_user_concentration(connection):
    query = """
    SELECT State, SUM(registeredUsers) AS TotalUsers
    FROM top_user
    GROUP BY State
    ORDER BY TotalUsers DESC limit 10;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_map_user_concentration(connection):
    query = """
    SELECT State, AVG(Percentage) AS AvgPercentage
    FROM map_user
    GROUP BY State
    ORDER BY AvgPercentage DESC;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_transaction_hotspots(connection):
    query = """
    SELECT State, Pincode, SUM(TransactionAmount) AS TotalAmount
    FROM top_transaction
    GROUP BY State, Pincode
    ORDER BY TotalAmount DESC
    LIMIT 10;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Database connection setup
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="Sai@12345",
    database="PhonePeDB"
)

cursor = connection.cursor()
st.set_page_config(layout="wide")
st.title("PhonePe Visualization and Exploration")

# Sidebar menu
with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration"])

# Main menu options
if select == "Home":
    st.image('C:\\Users\\SampathKumar\\Phonepe.jpeg', caption='Welcome to the PhonePe Data Analysis Dashboard!', use_column_width=True)
    #st.write("Welcome to the PhonePe Data Analysis Dashboard!")
    
elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregator Analysis", "Map Analysis", "Top Analysis"])
    
    with tab1:
        method = st.radio("Select the method", ["Insurance", "Transaction", "User"])
        
        if method == "Insurance":
            state = st.text_input("Enter State:", key="insurance_state")
            if state:
                result = get_insurance_transactions_over_time(connection, state)
                df = pd.DataFrame(result, columns=["Year", "TotalTransactions", "TotalAmount"])

                # Convert 'Year' to integer if needed
                df['Year'] = df['Year'].astype(int)

                # Sort DataFrame by 'TotalTransactions' in descending order
                df_sorted_transactions = df.sort_values(by='TotalTransactions', ascending=False)

                # Plotting Total Transactions Over Time
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df_sorted_transactions['Year'], df_sorted_transactions['TotalTransactions'], marker='o', linestyle='-', color='blue')
                ax.set_title("Total Transactions")
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Transactions")
                plt.xticks(rotation=45)
                st.pyplot(fig)  # Display the plot in Streamlit

                # Sort DataFrame by 'TotalAmount' in descending order
                df_sorted_amount = df.sort_values(by='TotalAmount', ascending=False)

                # Plotting Total Transaction Amount Over Time
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df_sorted_amount['Year'], df_sorted_amount['TotalAmount'], marker='o', linestyle='-', color='orange')
                ax.set_title("Total Transaction Amount")
                ax.set_xlabel("Year")
                ax.set_ylabel("Total Amount")
                plt.xticks(rotation=45)
                st.pyplot(fig)  
                
        elif method == "Transaction":
            year = st.number_input("Enter Year:", min_value=2000, max_value=2100, key="transaction_year")
            if year:
                result = get_yearly_transaction_trends(connection, year)
                df = pd.DataFrame(result, columns=["Quarter", "TotalTransactions", "TotalAmount"])

                # Convert 'Quarter' to a suitable type if needed (e.g., string or datetime)
                #df['Quarter'] = df['Quarter'].astype(str)

                df['Quarter'] = df['Quarter'].astype(str)

                # Create a figure and axis
                fig, ax1 = plt.subplots(figsize=(12, 6))

                # Plot TotalTransactions as a bar chart
                ax1.bar(df['Quarter'], df['TotalTransactions'], color='blue', alpha=0.6, label='Total Transactions')
                ax1.set_xlabel('Quarter')
                ax1.set_ylabel('Total Transactions', color='blue')
                ax1.tick_params(axis='y', labelcolor='blue')
                ax1.set_title('Total Transactions Vs Total Amount by Quarter')

                # Create a second y-axis for TotalAmount
                ax2 = ax1.twinx()
                ax2.plot(df['Quarter'], df['TotalAmount'], color='orange', marker='o', label='Total Amount')
                ax2.set_ylabel('Total Amount', color='orange')
                ax2.tick_params(axis='y', labelcolor='orange')

                # Add legends and grid
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')
                ax1.grid(False)

                # Show the plot in Streamlit
                st.pyplot(fig)

                
        elif method == "User":
            result = get_brand_popularity(connection)
            df = pd.DataFrame(result, columns=['Brands', 'TotalTransactions', 'AvgMarketShare'])
            fig, ax = plt.subplots(figsize=(12, 6))

# Create the plot
            sns.barplot(x='Brands', y='TotalTransactions', data=df, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            ax.set_xlabel('Brands')
            ax.set_ylabel('Total Transactions')
            ax.set_title('Total Transactions per Brand')

# Render plot in Streamlit
            st.pyplot(fig)
    
    with tab2:
        method = st.radio("Select the method", ["Map Insurance", "Map Transaction", "Map User"])
        
        if method == "Map Insurance":
            state = st.text_input("Enter State:", key="map_insurance_state")
            if state:
                result = get_district_level_insurance_analysis(connection, state)
                df = pd.DataFrame(result, columns=['District', 'TotalMetric'])
                fig, ax = plt.subplots(figsize=(12, 6))

                # Create the plot
                sns.barplot(x='District', y='TotalMetric', data=df, ax=ax)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                ax.set_xlabel('District')
                ax.set_ylabel('Total Metric')
                ax.set_title('Total Metric by District')

                # Render plot in Streamlit
                st.pyplot(fig)
                #st.write(result)
                
        elif method == "Map Transaction":
            year = st.number_input("Enter Year:", min_value=2000, max_value=2100, key="map_transaction_year")
            quarter = st.number_input("Enter Quarter:", min_value=1, max_value=4, key="map_transaction_quarter")
            if year and quarter:
                result = get_geospatial_analysis(connection, year, quarter)
                df = pd.DataFrame(result, columns=['State', 'TotalTransactions', 'TotalAmount'])
                fig, ax = plt.subplots(figsize=(12, 6))
                # Create the bar plot
                sns.barplot(x='State', y='TotalTransactions', data=df, ax=ax)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                ax.set_xlabel('State')
                ax.set_ylabel('Total Transactions')
                ax.set_title('Total Transactions by State')
                st.pyplot(fig)

                sns.barplot(y='State', x='TotalTransactions', data=df, ax=ax)
                ax.set_xlabel('Total Transactions')
                ax.set_ylabel('State')
                ax.set_title('Total Transactions by State')
                st.pyplot(fig)


                # Create a Matplotlib figure and axis
                fig, ax = plt.subplots(figsize=(8, 8))
                # Create the pie chart
                ax.pie(df['TotalTransactions'], labels=df['State'], autopct='%1.1f%%', startangle=140)
                ax.set_title('Proportion of Total Transactions by State')
                # Render plot in Streamlit
                st.pyplot(fig)


                
        elif method == "Map User":
            result = get_map_user_concentration(connection)
            df = pd.DataFrame(result, columns=['State', 'AvgPercentage'])

            # Streamlit app
            st.title(' Percentage Distribution by State')

            # Create a Matplotlib figure and axis
            fig, ax = plt.subplots(figsize=(12, 8))

            # Bar plot
            ax.bar(df['State'], df['AvgPercentage'], color='skyblue')
            ax.set_xlabel('State')
            ax.set_ylabel('Average Percentage')
            ax.set_title('Average Percentage by State')
            plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

            # Display the plot
            plt.tight_layout()  # Adjust layout to prevent clipping
            st.pyplot(plt)
    
    with tab3:
        method = st.radio("Select the method", ["Top Insurance", "Top Transaction", "Top User"])
        
        if method == "Top Insurance":
            result = get_top_regions_for_insurance(connection)
            df = pd.DataFrame(result, columns=['State', 'Pincode', 'TotalAmount', 'TotalCount'])
            fig, ax = plt.subplots(figsize=(12, 8))

            # Create the plot for Total Amount
            sns.barplot(x='TotalAmount', y=df['State'] + ' - ' + df['Pincode'], data=df, ax=ax)
            ax.set_xlabel('Total Transaction Amount')
            ax.set_ylabel('State - Pincode')
            ax.set_title('Total Transaction Amount by State and Pincode')

            # Render plot in Streamlit
            st.pyplot(fig)
           
            
        elif method == "Top Transaction":
            result = get_transaction_hotspots(connection)  # Function to fetch data
            df = pd.DataFrame(result, columns=['State', 'Pincode', 'TotalAmount'])

            # Ensure that TotalAmount is numeric
            df['TotalAmount'] = pd.to_numeric(df['TotalAmount'], errors='coerce')

            # Combine State and Pincode into a single column for better visualization
            df['State_Pincode'] = df['State'] + ' - ' + df['Pincode']

            # Pivot the data for bar plot
            fig, ax = plt.subplots(figsize=(12, 8))
            df_sorted = df.sort_values(by='TotalAmount', ascending=False)
            sns.barplot(x='TotalAmount', y='State_Pincode', data=df_sorted, ax=ax, palette='viridis')
            ax.set_title('Bar Plot of Total Transaction Amount by State and Pincode')
            ax.set_xlabel('Total Transaction Amount')
            ax.set_ylabel('State - Pincode')

            # Render plot in Streamlit
            st.pyplot(fig)
            
        elif method == "Top User":
            result = get_user_concentration(connection)
            df = pd.DataFrame(result, columns=['State', 'TotalUsers'])
            # Streamlit app
            st.title('Total Registered Users by State')

            # Create the plot
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x='TotalUsers', y='State', data=df, ax=ax, palette='viridis')
            ax.set_xlabel('Total Users')
            ax.set_ylabel('State')
            ax.set_title('Total Registered Users by State')

            # Render plot in Streamlit
            st.pyplot(fig)
    
#elif select == "Top Charts":
 #   st.write("Top Charts Coming Soon...")

# Close connection when the app finishes
connection.close()
