from flask import Flask, jsonify, request
import os
import uuid
import json

folder_name = "uploads"
image_folder = os.path.abspath(folder_name)

import mysql.connector
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
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

    # Close the database connection
    cursor.close()
    db_connection.close()

    # Convert the user(s) data to a JSON response
    response = []
    for user in users:
        user_data = {
            'id': user[0],
            'name': user[1],
            'pw': user[2],
            'age': user[3],
            'intro': user[4],
            'address': user[5],
            'image_path': user[6],
            'created_at': str(user[7]),
            'edited_at': str(user[8]),
            'deleted_at': str(user[9])
        }
        response.append(user_data)

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
    print('image {}'.format(image))
    children = user_data.get('children')
    hobbies = user_data.get('hobbies')
    # image_bytes = bytes(image)
    # image_data_str = json.dumps(image)
    # print(image_data_str)

    # Get the uploaded image file
    # image_file = request.files['image']
    
    # # Generate a unique filename
    # unique_filename = str(uuid.uuid4()) + '.jpg'

    # # Save the image to the folder
    # image_path = os.path.join(image_folder, unique_filename)
    # image_file.save(image_path)


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
    cursor.execute(user_query, (name, password, age, intro, address, image))
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

