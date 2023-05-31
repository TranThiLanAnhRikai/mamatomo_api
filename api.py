from flask import Flask, jsonify, request
import mysql.connector
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    # Establish a connection to the database
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Duyan278#',
        database='mamatomo_database'
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Execute the SQL query to retrieve users from the database
    query = "SELECT * FROM users"
    cursor.execute(query)

    # Fetch all the rows returned by the query
    users = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    cnx.close()

    # Convert the fetched rows to a list of dictionaries
    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'name': user[1]}
        user_list.append(user_dict)

    # Return the list of users as a JSON response
    return jsonify(user_list)

# @app.route('/users', methods=['POST'])
# def create_user():
#     # Establish a connection to the database
#     cnx = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='Duyan278#',
#         database='mamatomo_database'
#     )

#     # Create a cursor object to execute SQL queries
#     cursor = cnx.cursor()

#     # Create a new user
#     user = request.json  # Assuming the request body contains user data

#     # Process the user data and save it to the database
#     query = "INSERT INTO users (name) VALUES (%s)"
#     values = (user['name'],)
#     cursor.execute(query, values)
#     cnx.commit()

#     # Close the cursor and database connection
#     cursor.close()
#     cnx.close()

#     # Return the created user with a success message
#     return jsonify({'message': 'User created', 'user': user})

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
