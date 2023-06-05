from flask import Flask, jsonify, request
import os
import uuid
import json
import mysql.connector
import base64


folder_name = "users_avatars"
image_folder = os.path.abspath(folder_name)

# image_folder = "users_avatars"

app = Flask(__name__)

@app.route('/get_user', methods=['GET'])
def get_user():
    # Retrieve the username from the query parameters
    username = request.args.get('username')

   

    # Connect to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Duyan278#',
        database='mamatomo_database'
    )

    # Execute the SQL query to fetch the user(s) by username
    cursor = db_connection.cursor()
    query = "SELECT * FROM users WHERE name = %s"
    cursor.execute(query, (username,))
    users = cursor.fetchall()
    print("username")
    print(username)
    print(users)
    print(type(users[0][2]))
    # Close the database connection
    cursor.close()
    db_connection.close()

    # # Convert the user(s) data to a JSON response
    # response = []
    # for user in users:
    #     user_data = {
    #         'id': user[0],
    #         'name': user[1],
    #         'pw': user[2],
    #         'age': user[3],
    #         'intro': user[4],
    #         'address': user[5],
    #         'image_path': user[6],
    #         'created_at': str(user[7]),
    #         'edited_at': str(user[8]),
    #         'deleted_at': str(user[9])
    #     }
    #     response.append(user_data)
    response = {"pw": users[0][2]}
    return jsonify(response)


@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the user data from the request body
    user_data = request.json

    # Extract the required fields from the user data
    name = user_data.get('name')
    password = user_data.get('password')
    age = user_data.get('age')
    intro = user_data.get('intro')
    address = user_data.get('address')
    image = user_data.get('image')
    children = user_data.get('children')
    hobbies = user_data.get('hobbies')

    unique_filename = str(uuid.uuid4()) + '.jpg'

    # Decode the base64 image data
    image_data = base64.b64decode(image)

    # Specify the path to save the image
    image_path = os.path.join(image_folder, unique_filename)

    # image_folder = "user_avatars"
    # uniq_filename = "3dd..fdasfsd.jpg"

    # image_path = user_avatars/3dd..fdasfsd.jpg

    # Save the image to the server folder
    with open(image_path, 'wb') as file:
        file.write(image_data)
    # Connect to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Duyan278#',
        database='mamatomo_database'
    )

    # Execute the SQL query to insert the new user into the database
    cursor = db_connection.cursor()
    user_query = "INSERT INTO users (name, pw, age, intro, address, image_path) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(user_query, (name, password, age, intro, address, image_path))
    user_id = cursor.lastrowid  # Get the ID of the newly inserted user

    # Insert the chosen hobbies into the users_hobbies table
    insert_hobbies_query = "INSERT INTO users_hobbies (user_id, hobbies_id) VALUES (%s, %s)"
    for hobby_id in hobbies:
        cursor.execute(insert_hobbies_query, (user_id, hobby_id))

    # Insert the children data into the children table
    for child_data in children:
        child_name = child_data.get('name')
        gender_id = child_data.get('gender_id')
        child_days = child_data.get('days')
        child_query = "INSERT INTO children (parent_id, name, gender_id, days) VALUES (%s, %s, %s, %s)"
        cursor.execute(child_query, (user_id, child_name, gender_id, child_days))

    # Commit the changes and close the cursor and database connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

    # Return the ID of the newly created user as a JSON response
    response = {'user_id': user_id}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
