# # import mysql.connector

# # try:
# #     connection = mysql.connector.connect(
# #         host="127.0.0.1",          # Replace with your MySQL host
# #         user="root", # Replace with your MySQL username
# #         password="", # Replace with your MySQL password
# #         database="asach"      # Replace with your database name
# #     )
# #     print("Connection successful!")
# # except mysql.connector.Error as err:
# #     print(f"Error: {err}")
# # finally:
# #     if 'connection' in locals() and connection.is_connected():
# #         connection.close()


# import mysql.connector

# # Add a print statement at the start
# print("Starting script...")

# try:
#     # print("Attempting to connect to the database...")
#     connection = mysql.connector.connect(
#         host="localhost",          # Replace with your MySQL host
#         user="root", # Replace with your MySQL username
#         password="", # Replace with your MySQL password
#         database="asach"      # Replace with your database name
#     )
    
#     # If connection is successful, print this
#     print("Connection successful!")
    
# except mysql.connector.Error as err:
#     # Print the error if it occurs
#     print(f"Error: {err}")

# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()
#         print("Connection closed.")
