from flask import Flask, request, jsonify
import pymysql
import os
from datetime import datetime
from flask_cors import CORS
import requests
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/images')

# Railway DB connection

def get_db_connection():
    return pymysql.connect(
        host='shinkansen.proxy.rlwy.net',
        port=32506,
        user='root',
        password='xmtXAMWyaggdIGLUuZNJLktTmbCrTnWj',
        database='railway',
        cursorclass=pymysql.cursors.DictCursor
    )

# Sign Up
@app.route('/api/signup', methods=['POST'])
def signup():
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_password = request.form['user_password']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s, %s)', (user_name, user_email, user_password))
    connection.commit()
    return jsonify({'Success': 'User Saved Successfully'})


# Sign In
@app.route('/api/signin', methods=['POST'])
def signin():
    user_name = request.form['user_name']
    user_password = request.form['user_password']

    connection = get_db_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM users WHERE user_name = %s AND user_password = %s'
    data = user_name, user_password
    cursor.execute(sql, data)

    user = cursor.fetchone()
    if not user:
        return jsonify({'Message': 'User Doesnt Exist'})
    return jsonify({'Message': 'User Logged In Successfully'})


@app.route('/api/add_product', methods=['POST'])
def product():
    product_name = request.form['product_name']
    product_description = request.form['product_description']
    product_cost = request.form['product_cost']

    photo = request.files['product_photo']
    filename = photo.filename
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(photo_path)

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO products(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)', (product_name, product_description, product_cost, filename))
    connection.commit()
    return jsonify({'message': 'Product Added Successfully'})


@app.route('/api/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
    products = cursor.fetchall()
    return jsonify(products)


@app.route('/api/get_products')
def get_products():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return jsonify(products)


@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM products WHERE product_id = %s', (product_id,))
    connection.commit()
    return jsonify({'message': 'Product Deleted'})


@app.route('/api/add_faqs', methods=['POST'])
def faqs():
    faq_question = request.form['faq_question']
    faq_answer = request.form['faq_answer']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO faqs (faq_question, faq_answer) VALUES (%s, %s)', (faq_question, faq_answer))
    connection.commit()
    return jsonify({'Success': 'FAQ added Successfully'})


@app.route('/api/get_faqs')
def get_faqs():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM faqs')
    faqs = cursor.fetchall()
    return jsonify(faqs)


@app.route('/api/add_blogposts', methods=['POST'])
def blogs():
    blog_name = request.form['blog_name']
    blog_content = request.form['blog_content']
    author_name = request.form['author_name']
    author_bio = request.form['author_bio']
    blog_date = datetime.now()

    blog_photo = request.files['blog_photo']
    blog_filename = blog_photo.filename
    blog_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], blog_filename))

    author_photo = request.files['author_photo']
    author_filename = author_photo.filename
    author_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], author_filename))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO blogs(blog_name, blog_content, blog_date, blog_photo, author_name, author_bio, author_photo) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                   (blog_name, blog_content, blog_date, blog_filename, author_name, author_bio, author_filename))
    connection.commit()
    return jsonify({'message': 'Blog Post Added Successfully'})


@app.route('/api/get_blogposts')
def get_blogposts():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM blogs')
    blogs = cursor.fetchall()
    return jsonify(blogs)


@app.route('/api/get_blogpost/<int:blog_id>', methods=['GET'])
def get_blogs(blog_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM blogs WHERE blog_id = %s', (blog_id,))
    blogs = cursor.fetchall()
    return jsonify(blogs)


@app.route('/api/add_showrooms', methods=['POST'])
def showrooms():
    showroom_name = request.form['showroom_name']
    showroom_location = request.form['showroom_location']
    showroom_description = request.form['showroom_description']
    showroom_hours = request.form['showroom_hours']
    showroom_contact = request.form['showroom_contact']

    photo = request.files['showroom_photo']
    filename = photo.filename
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO showrooms(showroom_name, showroom_location, showroom_description, showroom_hours, showroom_contact, showroom_photo) VALUES (%s, %s, %s, %s, %s, %s)',
                   (showroom_name, showroom_location, showroom_description, showroom_hours, showroom_contact, filename))
    connection.commit()
    return jsonify({'message': 'Showroom Added Successfully'})


@app.route('/api/get_showrooms')
def get_showrooms():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM showrooms')
    showrooms = cursor.fetchall()
    return jsonify(showrooms)


@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    amount = request.form['amount']
    phone = request.form['phone']

    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = "Bearer " + response.json()['access_token']

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    business_short_code = "174379"
    password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": "https://coding.co.ke/api/confirm.php",
        "AccountReference": "Botanical Gardens",
        "TransactionDesc": "Payments for Products"
    }

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
