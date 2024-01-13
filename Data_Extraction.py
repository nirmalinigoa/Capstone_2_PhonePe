import json
import os
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Nirmal@0912',
    'database': 'capstone_2'
}

# Establish database connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# 1 - Transaction Details
path = "data/aggregated/transaction/country/india/state/"
customer_transaction = os.listdir(path)

for i in customer_transaction:
    state = path + i + "/"
    year = os.listdir(state)
    for j in year:
        cur_year = state + j + "/"
        details = os.listdir(cur_year)
        for k in details:
            jsons = cur_year + k
            info = open(jsons, 'r')
            data = json.load(info)
            for z in data['data']['transactionData']:
                name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']

                Cus_transaction = {
                    "State": i,
                    "Year": j,
                    "Transaction_type": name,
                    "Count": count,
                    "Amount": amount
                }
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Transaction_Details (
                        State VARCHAR(255) NOT NULL,
                        Year INT NOT NULL,
                        Transaction_type VARCHAR(255) NOT NULL,
                        Count INT NOT NULL,
                        Amount VARCHAR(255) 
                    )
                '''
                cursor.execute(create_table_query)

                sql_insert = '''
                    INSERT INTO Transaction_Details (State, Year, Transaction_type, Count, Amount)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                cursor.execute(sql_insert, (
                    Cus_transaction["State"],
                    Cus_transaction["Year"],
                    Cus_transaction["Transaction_type"],
                    Cus_transaction["Count"],
                    Cus_transaction["Amount"]
                ))
                connection.commit()

# 2 - User Details
path_2 = "data/aggregated/user/country/india/state/"
customer_details = os.listdir(path_2)

for a in customer_details:
    user_state = path_2 + a + "/"
    yr = os.listdir(user_state)
    for b in yr:
        cur_yr = user_state + b + "/"
        dtl = os.listdir(cur_yr)
        for c in dtl:
            jsons = cur_yr + c
            user_info = open(jsons, 'r')
            user_data = json.load(user_info)
            if user_data['data'].get('usersByDevice') is not None:
                for d in user_data['data']['usersByDevice']:
                    brand = d.get('brand', 'N/A')
                    count = d.get('count', 0)
                    percentage = d.get('percentage', 0)

                    user_details = {
                        "State": a,
                        "Year": b,
                        "Mobile_Brand": brand,
                        "Count": count,
                        "Percentage": percentage * 100
                    }
                    create_table_query = '''
                        CREATE TABLE IF NOT EXISTS user_details (
                            State VARCHAR(255) NOT NULL,
                            Year INT NOT NULL,
                            Mobile_Brand VARCHAR(255) NOT NULL,
                            Count INT NOT NULL,
                            Percentage VARCHAR(255) 
                        )
                    '''
                    cursor.execute(create_table_query)

                    sql_insert = '''
                        INSERT INTO user_details (State, Year, Mobile_Brand, Count, Percentage)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert, (
                        user_details["State"],
                        user_details["Year"],
                        user_details["Mobile_Brand"],
                        user_details["Count"],
                        user_details["Percentage"]
                    ))
                    connection.commit()

# 3 - Map Transaction Details
path_map = "data/map/transaction/hover/country/india/state/"
map_transaction = os.listdir(path_map)

for x in map_transaction:
    map_state = path_map + x + "/"
    map_yr = os.listdir(map_state)
    for y in map_yr:
        cur_map_yr = map_state + y + "/"
        map_dtl = os.listdir(cur_map_yr)
        for c in map_dtl:
            jsons = cur_map_yr + c
            map_info = open(jsons, 'r')
            map_data = json.load(map_info)
            for z in map_data["data"]["hoverDataList"]:
                district = z['name']
                count = z["metric"][0]["count"]
                amount = z["metric"][0]["amount"]

                map_transaction_details = {
                    "State": x,
                    "Year": y,
                    "District": district,
                    "Count": count,
                    "Amount": amount,
                }
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Map_Transaction_Details (
                        State VARCHAR(255) NOT NULL,
                        Year INT NOT NULL,
                        District VARCHAR(255) NOT NULL,
                        Count INT NOT NULL,
                        Amount VARCHAR(255) 
                    )
                '''
                cursor.execute(create_table_query)

                sql_insert = '''
                    INSERT INTO Map_Transaction_Details (State, Year, District, Count, Amount)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                cursor.execute(sql_insert, (
                    map_transaction_details["State"],
                    map_transaction_details["Year"],
                    map_transaction_details["District"],
                    map_transaction_details["Count"],
                    map_transaction_details["Amount"]
                ))
                connection.commit()

# 4 - Map User Details
path_map = "data/map/user/hover/country/india/state/"
map_user = os.listdir(path_map)

for x in map_user:
    map_state = path_map + x + "/"
    map_yr = os.listdir(map_state)
    for y in map_yr:
        cur_map_yr = map_state + y + "/"
        map_dtl = os.listdir(cur_map_yr)
        for c in map_dtl:
            jsons = cur_map_yr + c
            map_info = open(jsons, 'r')
            map_data = json.load(map_info)
            for z in map_data["data"]["hoverData"].items():
                district = z[0]
                reg_users = z[1]['registeredUsers']
                app_usage = z[1]['appOpens']

                map_user_details = {
                    "State": x,
                    "Year": y,
                    "District": district,
                    "Registered_User": reg_users,
                    "App_Usage": app_usage,
                }
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Map_User_Details (
                        State VARCHAR(255) NOT NULL,
                        Year INT NOT NULL,
                        District VARCHAR(255) NOT NULL,
                        Registered_User INT NOT NULL,
                        App_Usage VARCHAR(255) 
                    )
                '''
                cursor.execute(create_table_query)

                insert_query = (
                    "INSERT INTO Map_User_Details (State, Year, District, Registered_User, App_Usage) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )

                data_tuple = (x, y, district, reg_users, app_usage)
                cursor.execute(insert_query, data_tuple)
                connection.commit()

# 5 - Top Transaction Details
top_path = "data/top/transaction/country/india/state/"
top_transaction = os.listdir(top_path)

for x in top_transaction:
    top_state = top_path + x + "/"
    top_yr = os.listdir(top_state)
    for y in top_yr:
        cur_top_yr = top_state + y + "/"
        top_dtl = os.listdir(cur_top_yr)
        for c in top_dtl:
            jsons = cur_top_yr + c
            top_info = open(jsons, 'r')
            top_data = json.load(top_info)
            for z in top_data['data']['districts']:
                Name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                top_transaction_details = {
                    "State": x,
                    "Year": y,
                    "District": Name,
                    "Count": count,
                    "Amount": amount,
                }
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Top_Transaction_Details (
                        State VARCHAR(255) NOT NULL,
                        Year INT NOT NULL,
                        District VARCHAR(255) NOT NULL,
                        Count INT NOT NULL,
                        Amount VARCHAR(255) 
                    )
                '''
                cursor.execute(create_table_query)

                sql_insert = '''
                    INSERT INTO Top_Transaction_Details (State, Year, District, Count, Amount)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                cursor.execute(sql_insert, (
                    top_transaction_details["State"],
                    top_transaction_details["Year"],
                    top_transaction_details["District"],
                    top_transaction_details["Count"],
                    top_transaction_details["Amount"]
                ))
                connection.commit()

# 6 - Top User Details
top_path = "data/top/user/country/india/state/"
top_user = os.listdir(top_path)

for x in top_user:
    top_state = top_path + x + "/"
    top_yr = os.listdir(top_state)
    for y in top_yr:
        cur_top_yr = top_state + y + "/"
        top_dtl = os.listdir(cur_top_yr)
        for c in top_dtl:
            jsons = cur_top_yr + c
            top_info = open(jsons, 'r')
            top_data = json.load(top_info)
            for z in top_data['data']["districts"]:
                districts = z['name']
                registeredUser = z['registeredUsers']
                top_user_details = {
                    "State": x,
                    "Year": y,
                    "District": districts,
                    "Registered_User": registeredUser,
                }
                create_table_query = '''
                    CREATE TABLE IF NOT EXISTS Top_User_Details (
                        State VARCHAR(255) NOT NULL,
                        Year INT NOT NULL,
                        District VARCHAR(255) NOT NULL,
                        Registered_User INT NOT NULL 
                    )
                '''
                cursor.execute(create_table_query)

                sql_insert = '''
                    INSERT INTO Top_User_Details (State, Year, District, Registered_User)
                    VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(sql_insert, (
                    top_user_details["State"],
                    top_user_details["Year"],
                    top_user_details["District"],
                    top_user_details["Registered_User"]
                ))
                connection.commit()

print("Data Uploaded Successfully")
