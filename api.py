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

@app.route('/get_user', methods=['POST'])
# def get_user():
#     db_connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='Duyan278#',
#         database='mamatomo_database'
#     )
#     username = request.json.get('username')

#     cursor = db_connection.cursor()

#     if username:
#         # Retrieve a specific user by username
#         query = "SELECT * FROM users WHERE name = %s"
#         cursor.execute(query, (username,))
#         user = cursor.fetchone()

#         if user:
#             user_dict = {
#                 'id': user[0],
#                 'name': user[1],
#                 'pw': user[2],
#                 'age': user[3],
#                 'intro': user[4],
#                 'address': user[5],
#                 'image_path': user[6],
#                 'created_at': user[7].strftime('%Y-%m-%d %H:%M:%S'),
#                 'edited_at': user[8].strftime('%Y-%m-%d %H:%M:%S'),
#                 'deleted_at': user[9]
#             }

#             # Retrieve hobbies for the user
#             query = """
#                 SELECT hobbies_id
#                 FROM users_hobbies
#                 INNER JOIN users ON users.id = users_hobbies.user_id
#                 WHERE users_hobbies.user_id = %s
#             """
#             cursor.execute(query, (user[0],))
#             hobbies = cursor.fetchall()
#             hobby_list = [hobby[0] for hobby in hobbies]
#             user_dict['hobbies'] = hobby_list

#             return jsonify(user_dict)
#         else:
#             return jsonify({'error': 'User not found'})
#     else:
#         # Retrieve all users
#         query = "SELECT * FROM users"
#         cursor.execute(query)
#         users = cursor.fetchall()

#         user_list = []
#         for user in users:
#             user_dict = {
#                 'id': user[0],
#                 'name': user[1],
#                 'pw': user[2],
#                 'age': user[3],
#                 'intro': user[4],
#                 'address': user[5],
#                 'image_path': user[6],
#                 'created_at': user[7].strftime('%Y-%m-%d %H:%M:%S'),
#                 'edited_at': user[8].strftime('%Y-%m-%d %H:%M:%S'),
#                 'deleted_at': user[9]
#             }

#             # Retrieve hobbies for each user
#             query = """
#                 SELECT hobbies.name
#                 FROM hobbies
#                 INNER JOIN users_hobbies ON hobbies.id = users_hobbies.hobby_id
#                 WHERE users_hobbies.user_id = %s
#             """
#             cursor.execute(query, (user[0],))
#             hobbies = cursor.fetchall()
#             hobby_list = [hobby[0] for hobby in hobbies]
#             user_dict['hobbies'] = hobby_list

#             user_list.append(user_dict)

#         return jsonify(user_list)

def get_user():
    # Retrieve the username from the request body
    username = request.json.get('username')

    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Duyan278#',
        database='mamatomo_database'
    )

    cursor = db_connection.cursor()

    if username:
        # Query to retrieve a single user and their associated children
        query = """
        SELECT u.id, u.name, u.pw, u.age, u.intro, u.address, u.image_path,
               u.created_at, u.edited_at, u.deleted_at,
               c.id, c.name, c.gender_id, c.birthday, c.created_at, c.edited_at, c.deleted_at
        FROM users u
        LEFT JOIN children c ON u.id = c.parent_id
        WHERE u.name = %s
        """

        cursor.execute(query, (username,))
        rows = cursor.fetchall()

        if rows:
            user = {}
            user['id'] = rows[0][0]
            user['name'] = rows[0][1]
            user['pw'] = rows[0][2]
            user['age'] = rows[0][3]
            user['intro'] = rows[0][4]
            user['address'] = rows[0][5]
            user['image_path'] = rows[0][6]
            user['created_at'] = rows[0][7].strftime('%Y-%m-%d %H:%M:%S')
            user['edited_at'] = rows[0][8].strftime('%Y-%m-%d %H:%M:%S')
            user['deleted_at'] = rows[0][9]

            children = []
            for row in rows:
                if row[10]:  # Check if the child ID is not null (indicating a child record exists)
                    child = {
                        'id': row[10],
                        'name': row[11],
                        'gender_id': row[12],
                        'birthday': row[13],
                        # 'birthday': row[13].strftime('%Y-%m-%d'),
                        'created_at': row[14].strftime('%Y-%m-%d %H:%M:%S'),
                        'edited_at': row[15].strftime('%Y-%m-%d %H:%M:%S'),
                        'deleted_at': row[16]
                    }
                    children.append(child)

            user['children'] = children

            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'})
    else:
        # Query to retrieve all users and their associated children
        query = """
        SELECT u.id, u.name, u.pw, u.age, u.intro, u.address, u.image_path,
               u.created_at, u.edited_at, u.deleted_at,
               c.id, c.name, c.gender_id, c.birthday, c.created_at, c.edited_at, c.deleted_at
        FROM users u
        LEFT JOIN children c ON u.id = c.parent_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id': row[0],
                'name': row[1],
                'pw': row[2],
                'age': row[3],
                'intro': row[4],
                'address': row[5],
                'image_path': row[6],
                'created_at': row[7].strftime('%Y-%m-%d %H:%M:%S'),
                'edited_at': row[8].strftime('%Y-%m-%d %H:%M:%S'),
                'deleted_at': row[9]
            }

            if row[10]:  # Check if the child ID is not null (indicating a child record exists)
                child = {
                    'id': row[10],
                    'name': row[11],
                    'gender_id': row[12],
                    'birthday': row[13].strftime('%Y-%m-%d'),
                    'created_at': row[14].strftime('%Y-%m-%d %H:%M:%S'),
                    'edited_at': row[15].strftime('%Y-%m-%d %H:%M:%S'),
                    'deleted_at': row[16]
                }
                user.setdefault('children', []).append(child)

            users.append(user)

        return jsonify(users)
    

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
        birthday = child_data.get('birthday')
        child_query = "INSERT INTO children (parent_id, name, gender_id, birthday) VALUES (%s, %s, %s, %s)"
        cursor.execute(child_query, (user_id, child_name, gender_id, birthday))

    # Commit the changes and close the cursor and database connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

    # Return the ID of the newly created user as a JSON response
    response = {'user_id': user_id}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
