import pandas as pd
import pymysql
import json
import requests
import plotly.express as px
# [Dash board libraries]
import streamlit as st
from streamlit_option_menu import option_menu

# CONNECT TO SQL

conn = pymysql.connect(host='localhost', user='root', password='Nirmal@0912', db='capstone_2')
cursor = conn.cursor()

st.set_page_config(layout="wide")

selected = option_menu(None,
                       options=["Home", "Geo", "Insights", "About"],
                       icons=["house", "globe", "activity", "info"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%","background-color": "#643cb5" },
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#643cb5","color": "black"}})

# HOME TAB
if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h1 style='color: #643cb5;'>Phonepe Pulse Data Visualisation</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='color:white;'>PhonePe Pulse is a feature offered by the Indian digital payments platform "
            "called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital "
            "transactions and usage patterns on the PhonePe app.</h5>", unsafe_allow_html=True)
        st.markdown(
            "<h5 style='color: white;'>"
            "In this Streamlit application, we will explore features similar to those "
            "offered by Phonepe Pulse, conducting our own data analysis using information provided by Phonepe.</h5>",
            unsafe_allow_html=True)
    with col2:
        st.image('https://cdn.freelogovectors.net/wp-content/uploads/2023/11/phonepe_logo-freelogovectors.net_.png')

    st.write("---")

# GEO_TAB

url = ("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
       "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
response = requests.get(url)
data1 = json.loads(response.content)

# Read CSV file
df = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/Transaction_Details.csv")
# Map state names
state_mapping = {
    'andaman and nicobar island': 'Andaman & Nicobar',
    'andhra pradesh': 'Andhra Pradesh',
    'arunachal pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    # Add more mappings as needed
}
df['State'] = df['State'].replace(state_mapping)

geo_states = [feature['properties']['ST_NM'] for feature in data1['features']]
geo_states.sort()
# Create a DataFrame with the state names column
geo_states = pd.DataFrame({'State': geo_states})

# dashboard
if selected == "Geo":
    st.markdown("<h1 style='color: #643cb5;'>Geo visualization:</h1>", unsafe_allow_html=True)
    # Selection option
    option = st.radio('', (
        'Transaction Details', 'User Details', 'Top Transaction Details', 'Top User Details',
        'Map Transaction Details',
        'Map User Details'), horizontal=True)

    if option == 'Transaction Details':
        # Select tab
        tab1, tab2 = st.tabs(['Transaction Amount', 'Transaction Count'])

        # -------------------------       /     All India Transaction        /        ------------------ #
        with tab1:
            # Geo plot for Transaction Amount

            grp_df = df.groupby('State', as_index=False).sum()
            ddf = grp_df.drop('Year', axis=1)
            merged_df = pd.merge(geo_states, ddf, on='State', how='left')
            # Fill NaN values in the 'Amount' column
            merged_df['Amount'].fillna(0, inplace=True)

            # Fill NaN values in the 'Count' column
            merged_df['Count'].fillna(0, inplace=True)

            fig_tra = px.choropleth(
                merged_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                        "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                hover_name="State",
                color='Amount',  # Specify the column to represent with color
                title='Analysis On Transaction Amount'
            )
            fig_tra.update_traces(
                hoverinfo="text",
                hovertemplate="<b>%{hovertext}</b><br>Transaction_Amount: %{z:,.0f}"

            )
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

            # Show the plot
            st.plotly_chart(fig_tra, use_container_width=True)
        with tab2:
            # Geo plot for Transaction Count
            fig_tra = px.choropleth(
                merged_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                        "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                hover_name="State",
                color='Count',  # Specify the column to represent with color
                title='Analysis On Transaction Count'
            )
            fig_tra.update_traces(
                hoverinfo="text",
                hovertemplate="<b>%{hovertext}</b><br>Transaction_Count: %{z:,.0f}"

            )

            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

            # Show the plot
            st.plotly_chart(fig_tra, use_container_width=True)

    # RADIO_2
    # 2
    # Read CSV file
    dfu = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/user_details.csv")

    dfu['State'] = dfu['State'].replace(state_mapping)
    grp = dfu.groupby('State').sum()
    dy = grp.drop('Year', axis=1)
    dp = dy.drop('Percentage', axis=1)
    merged_dfu = pd.merge(geo_states, dp, on='State', how='left')
    # Fill NaN values in the 'Count' column
    merged_dfu['Count'].fillna(0, inplace=True)
    if option == 'User Details':
        # Geo plot for User Count
        fig_tra = px.choropleth(
            merged_dfu,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                    "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            hover_name="State",
            color='Count',  # Specify the column to represent with color
            title='Analysis On User Count'
        )
        fig_tra.update_traces(
            hoverinfo="text",
            hovertemplate="<b>%{hovertext}</b><br>User_Count: %{z:,.0f}"

        )

        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

        # Show the plot
        st.plotly_chart(fig_tra, use_container_width=True)
    # RADIO-3
    # 3
    # Read CSV file
    dftt = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/Top_Transaction_Details.csv")

    dftt['State'] = dftt['State'].replace(state_mapping)
    grptt = dftt.groupby('State').sum()
    dytt = grptt.drop('Year', axis=1)
    merged_dftt = pd.merge(geo_states, dytt, on='State', how='left')
    # Fill NaN values in the 'Amount' column
    merged_dftt['Amount'].fillna(0, inplace=True)
    # Fill NaN values in the 'Amount' column
    merged_dftt['Count'].fillna(0, inplace=True)

    if option == 'Top Transaction Details':
        # Select tab
        tab1, tab2 = st.tabs(['Top Transaction Amount', 'Top Transaction Count'])
        with tab1:
            fig_tra = px.choropleth(
                merged_dftt,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                        "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                hover_name="State",
                color='Amount',  # Specify the column to represent with color
                title='Analysis On Top Transaction Amount'
            )
            fig_tra.update_traces(
                hoverinfo="text",
                hovertemplate="<b>%{hovertext}</b><br>Transaction_Amount: %{z:,.0f}"

            )

            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

            # Show the plot
            st.plotly_chart(fig_tra, use_container_width=True)
        with tab2:
            # Geo plot for Top Transaction count
            fig_tra = px.choropleth(
                merged_dftt,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                        "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                hover_name="State",
                color='Count',  # Specify the column to represent with color
                title='Analysis On Transaction Count'
            )
            fig_tra.update_traces(
                hoverinfo="text",
                hovertemplate="<b>%{hovertext}</b><br>Transaction_Count: %{z:,.0f}"

            )

            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

            # Show the plot
            st.plotly_chart(fig_tra, use_container_width=True)
    # RADIO-4
    # 4
    # Read CSV file
    dftu = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/Top_User_Details.csv")

    dftu['State'] = dftu['State'].replace(state_mapping)
    grptu = dftu.groupby('State').sum()
    dytu = grptu.drop('Year', axis=1)
    merged_dftu = pd.merge(geo_states, dytu, on='State', how='left')
    # Fill NaN values in the 'Amount' column
    merged_dftu['Registered_User'].fillna(0, inplace=True)

    if option == 'Top User Details':
        # Geo plot for Top reg_user count
        fig_tra = px.choropleth(
            merged_dftu,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                    "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            hover_name="State",
            color='Registered_User',  # Specify the column to represent with color
            title='Analysis On Registered_User'
        )
        fig_tra.update_traces(
            hoverinfo="text",
            hovertemplate="<b>%{hovertext}</b><br>Registered_User: %{z:,.0f}"

        )

        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color="#643cb5", height=800)

        # Show the plot
        st.plotly_chart(fig_tra, use_container_width=True)

    # RADIO-5
    # 5
    # Read CSV file
    dfmu = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/Map_User_Details.csv")
    state_mapping = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam'
        # Add more mappings as needed
    }

    dfmu['State'] = dfmu['State'].replace(state_mapping)
    grpmu = dfmu.groupby('State').sum()
    dymu = grpmu.drop('Year', axis=1)
    merged_dfmu = pd.merge(geo_states, dymu, on='State', how='left')
    # Fill NaN values in the 'Amount' column
    merged_dfmu['App_Usage'].fillna(0, inplace=True)
    merged_dfmu['Registered_User'].fillna(0, inplace=True)
    print(merged_dfmu)

    if option == 'Map User Details':
        fig_tra = px.choropleth(
            merged_dfmu,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                    "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            hover_name="State",
            color='App_Usage',  # Specify the column to represent with color
            title='Analysis On App_Usage'
        )
        fig_tra.update_traces(
            hoverinfo="text",
            hovertemplate="<b>%{hovertext}</b><br>App_Usage: %{z:,.0f}"

        )
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color='#643cb5', height=800)

        # Show the plot
        st.plotly_chart(fig_tra, use_container_width=True)

    # RADIO-6
    # 6
    # Read CSV file
    dfmt = pd.read_csv("C:/Users/LENOVO/Documents/Cap_2/Map_Transaction_Details.csv")

    state_mapping = {
        'andaman-nicobar island': 'Andaman & Nicobar',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        # Add more mappings as needed
    }
    dfmt['State'] = dfmt['State'].replace(state_mapping)
    grpmt = dfmt.groupby('State').sum()
    dymt = grpmt.drop('Year', axis=1)
    merged_dfmt = pd.merge(geo_states, dymt, on='State', how='left')
    # Fill NaN values in the 'Amount' column
    merged_dfmt['Amount'].fillna(0, inplace=True)
    merged_dfmt['Count'].fillna(0, inplace=True)

    if option == 'Map Transaction Details':
        # Geo plot for map Transaction
        fig_tra = px.choropleth(
            merged_dfmt,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw"
                    "/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Amount',  # Specify the column to represent with color
            hover_name="State",
            title='Analysis On Total Transaction Amount '
        )
        fig_tra.update_traces(
            hoverinfo="text",
            hovertemplate="<b>%{hovertext}</b><br>Amount: %{z:,.0f}"

        )

        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color='#643cb5', height=800)

        # Show the plot
        st.plotly_chart(fig_tra, use_container_width=True)

# INSIGHTS TAB

if selected == "Insights":
    st.markdown("<h1 style='color: #643cb5;'>BASIC INSIGHTS</h1>", unsafe_allow_html=True)
    options = ["--select--",
               "(1) Top 10 states based on amount of transaction",
               "(2) Least 10 states based on amount of transaction",
               "(3) Top 10 States and Districts based on Registered Users",
               "(4) Least 10 States and Districts based on Registered Users",
               "(5) Top 10 Districts based on the Transaction Amount",
               "(6) Least 10 Districts based on the Transaction Amount",
               "(7) Top 10 Districts based on the Transaction count",
               "(8) Least 10 Districts based on the Transaction count",
               "(9) Top Transaction types based on the Transaction Amount",
               "(10) Top 10 Mobile Brands based on the User count of transaction"]
    select = st.selectbox(":violet[Select the option]", options)

    # 1
    if select == "(1) Top 10 states based on amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, SUM(Amount) AS Total_Transaction_Amount FROM top_transaction_details GROUP BY  "
            "State ORDER BY Total_Transaction_Amount DESC LIMIT 10")

        data = cursor.fetchall()
        columns = ['State', 'Amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Top 10 states based on amount of transaction</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="State", y="Amount")

    # 2
    elif select == "(2) Least 10 states based on amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, SUM(Amount) AS Total_Transaction_Amount FROM top_transaction_details GROUP BY  "
            "State ORDER BY Total_Transaction_Amount ASC LIMIT 10")
        data = cursor.fetchall()
        columns = ['States', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Least 10 states based on amount of transaction</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="States", y="Transaction_amount")

        # 3
    elif select == "(3) Top 10 States and Districts based on Registered Users":
        cursor.execute(
            "SELECT DISTINCT State, District, SUM(Registered_User) AS Users FROM Top_User_Details GROUP BY State, "
            "District ORDER BY Users DESC LIMIT 10")
        data = cursor.fetchall()
        columns = ['State', 'District_Pincode', 'Registered_User']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Top 10 States and Districts based on Registered Users</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="State", y="Registered_User")

        # 4
    elif select == "(4) Least 10 States and Districts based on Registered Users":
        cursor.execute(
            "SELECT DISTINCT State, District, SUM(Registered_User) AS Users FROM Top_User_Details GROUP BY State, "
            "District ORDER BY Users ASC LIMIT 10")
        data = cursor.fetchall()
        columns = ['State', 'District_Pincode', 'Registered_User']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Least 10 States and Districts based on Registered Users</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="State", y="Registered_User")

        # 5
    elif select == "(5) Top 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT State ,District,SUM(Amount) AS Total FROM Map_Transaction_Details GROUP BY State ,"
            "District ORDER BY Total DESC LIMIT 10")
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Top 10 Districts based on Transaction Amount</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="District", y="Transaction_Amount")

        # 6
    elif select == "(6) Least 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT State,District,SUM(amount) AS Total FROM Map_Transaction_Details GROUP BY State, "
            "District ORDER BY Total ASC LIMIT 10")
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Least 10 Districts based on Transaction Amount</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="District", y="Transaction_amount")

        # 7
    elif select == "(7) Top 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT State,District,SUM(Count) AS Counts FROM Map_Transaction_Details GROUP BY State ,"
            "District ORDER BY Counts DESC LIMIT 10")
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color:#643cb5;'>Top 10 Districts based on Transaction Count</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="Transaction_Count", y="District")

        # 8
    elif select == "(8) Least 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT State ,District,SUM(Count) AS Counts FROM Map_Transaction_Details GROUP BY State ,"
            "District ORDER BY Counts ASC LIMIT 10")
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color: #643cb5;'>Top 10 Districts based on the Transaction Count</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="Transaction_Count", y="District")

        # 9
    elif select == "(9) Top Transaction types based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT Transaction_type, SUM(Amount) AS Amount FROM Transaction_Details GROUP BY "
            "Transaction_type ORDER BY Amount DESC LIMIT 5")
        data = cursor.fetchall()
        columns = ['Transaction_type', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color:#643cb5;'>Top Transaction Types based on the Transaction Amount</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="Transaction_type", y="Transaction_amount")

        # 10
    elif select == "(10) Top 10 Mobile Brands based on the User count of transaction":
        cursor.execute(
            "SELECT DISTINCT Mobile_Brand,SUM(Count) as Total FROM user_details GROUP BY Mobile_Brand ORDER BY Total "
            "DESC LIMIT 10")
        data = cursor.fetchall()
        columns = ['Mobile_Brand', 'Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("<h1 style='color:#643cb5;'>Top 10 Mobile Brands based on User count of transaction</h1>", unsafe_allow_html=True)
            st.bar_chart(data=df, x="Count", y="Mobile_Brand")

if selected == "About":
    st.markdown("<h1 style='color: #643cb5;'>About:</h1>", unsafe_allow_html=True)

    st.write(
        "   :violet[-] **The dashboard boasts an intuitive navigation menu with options such as :violet[\"Home,\" \"Geo,\" \"Insights,\"] and :violet[ \"About,\"] enhancing user experience and accessibility.** ")

    st.write(
        "  :violet[-] **Utilizing Plotly Express and Streamlit, the dashboard provides an interactive geo-visualization feature. Users can explore transaction details, user information, and top transaction/user details on a geographical map, offering a comprehensive view of data distribution across different states.**")

    st.write(
        "  :violet[-] **The :violet[\"Insights\"] tab offers a variety of pre-defined analyses for quick insights. Users can select options to view top and least states based on transaction amounts, districts based on user counts, and transaction types with the highest amounts, among other insightful analyses.**")

    st.write(
        "  :violet[-] **The dashboard seamlessly integrates with a MySQL database, ensuring efficient storage and retrieval of data. This enhances the performance and scalability of the solution.**")

    st.write(
        "  :violet[-] **The dashboard incorporates Streamlit's user-friendly design, making it easy for users to navigate and explore different aspects of the PhonePe Pulse data. Dropdown menus and graphical representations contribute to an engaging and informative user interface.**")

    st.write(
        "   :violet[-] **The code prioritizes security, especially in database connections. Proper credentials and secure practices are employed to safeguard sensitive data throughout the process.**")

    st.write("---")