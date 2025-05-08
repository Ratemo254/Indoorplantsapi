from flask import Flask, request, jsonify
import pymysql
import os
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/images')

# Sign Up
@app.route('/api/signup', methods=['POST'])
def signup():
    if request.method =='POST':
        user_name= request.form['user_name']
        user_email = request.form['user_email']
        user_password = request.form['user_password']


    connection = pymysql.connect(
        host ='localhost',
        user = 'root',
        password = '',
        database = 'indoor plants website'
    )

    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s, %s)', (user_name, user_email, user_password)
    )

    connection.commit()
    return jsonify({'Success':'User Saved Successfully'})


# Sign In
@app.route('/api/signin', methods=['POST'])
def signin():
    user_name = request.form['user_name']
    user_password = request.form['user_password']

    connection = pymysql.connect(
        host ='localhost',
        user = 'root',
        password = '',
        database = 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql ='SELECT * FROM users WHERE user_name =%s AND user_password = %s'
    data = user_name, user_password
    cursor.execute(sql,data)

    count = cursor.rowcount

    if count== 0:
        return jsonify ({'Message':'User Doesnt Exist'})
    else:
        user = cursor.fetchone()
        return jsonify({'Message':'User Logged In Successfully'})
    

@app.route('/api/add_product',methods = ['POST'])
def product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_cost = request.form['product_cost']

    #   Extracting the image data
    photo = request.files['product_photo']
    filename = photo.filename

    #Path to our Images
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)


    # saving the photo path
    photo.save(photo_path)

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor()
    cursor.execute('INSERT INTO products(product_name, product_description, product_cost, product_photo)VALUES(%s, %s, %s, %s)',(product_name, product_description, product_cost,filename))

    connection.commit()
    return jsonify({'message':'Product Added Successfully'})


@app.route('/api/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))

    # Variable to store our products
    products = cursor.fetchall()

    return jsonify (products)
        
# Fetching The Products
@app.route('/api/get_products')
def get_products():

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM products')

    # Variable to store our products
    products = cursor.fetchall()

    return jsonify (products)

# Delete Product
@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    connection = pymysql.connect(
        host= 'localhost',  
        user='root',
        password='',
        database='indoor plants website'
        )
    
    cursor = connection.cursor()
    cursor.execute('DELETE FROM products WHERE product_id = %s', (product_id,))
    connection.commit()


# Add FAQs
@app.route('/api/add_faqs', methods=['POST'])
def faqs():
    faq_question = request.form['faq_question']
    faq_answer = request.form['faq_answer']

    connection = pymysql.connect(
        host ='localhost',
        user = 'root',
        password = '',
        database = 'indoor plants website'
    )

    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO faqs (faq_question, faq_answer) VALUES (%s, %s)', (faq_question, faq_answer)
    )

    connection.commit()
    return jsonify({'Success':'FAQ added Successfully'})


# Fetching The faqs
@app.route('/api/get_faqs')
def get_faqs():

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM faqs')

    # Variable to store our products
    faqs = cursor.fetchall()

    return jsonify (faqs)

# Add blog posts
@app.route('/api/add_blogposts',methods = ['POST'])
def blogs():
    if request.method == 'POST':
        blog_name = request.form['blog_name']
        blog_content = request.form['blog_content']
        author_name = request.form['author_name']
        author_bio = request.form['author_bio']
        
        blog_date = datetime.now()

    #   Extracting the image data
    photo = request.files['blog_photo']
    filenames = photo.filename

     #   Extracting the image data
    photo = request.files['author_photo']
    filenamee = photo.filename

    #Path to our Images
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'],filenames)

    photo_path = os.path.join(app.config['UPLOAD_FOLDER'],filenamee)


    # saving the photo path
    photo.save(photo_path)

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor()
    cursor.execute('INSERT INTO blogs(blog_name, blog_content, blog_date, blog_photo, author_name, author_bio, author_photo)VALUES(%s, %s, %s, %s, %s, %s, %s)',(blog_name,blog_content,blog_date,filenames,author_name,author_bio,filenamee))


    connection.commit()
    return jsonify({'message':'Blog Post Added Successfully'})

# Fetching Blog Posts
@app.route('/api/get_blogposts')
def get_blogposts():

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM blogs')

    blogs = cursor.fetchall()

    return jsonify(blogs)


@app.route('/api/get_blogpost/<int:blog_id>', methods=['GET'])
def get_blogs(blog_id):
    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM blogs WHERE blog_id = %s', (blog_id,))

    # Variable to store our blogss
    blogs = cursor.fetchall()

    return jsonify (blogs)

# Adding Showrooms
@app.route('/api/add_showrooms',methods = ['POST'])
def showrooms():
    if request.method == 'POST':
        showroom_name = request.form['showroom_name']
        showroom_location = request.form['showroom_location']
        showroom_description = request.form['showroom_description']
        showroom_hours = request.form['showroom_hours']
        showroom_contact = request.form['showroom_contact']

    #   Extracting the image data
    photo = request.files['showroom_photo']
    filenam = photo.filename

    #Path to our Images
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'],filenam)


    # saving the photo path
    photo.save(photo_path)

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor()
    cursor.execute('INSERT INTO showrooms(showroom_name, showroom_location, showroom_description,showroom_hours,showroom_contact, showroom_photo)VALUES(%s, %s, %s, %s,%s,%s)',(showroom_name, showroom_location, showroom_description,showroom_hours,showroom_contact,filenam))

    connection.commit()
    return jsonify({'message':'Showroom Added Successfully'})


# Fetching The showrooms
@app.route('/api/get_showrooms')
def get_showrooms():

    connection = pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'indoor plants website'
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM showrooms')

    # Variable to store our products
    showrooms = cursor.fetchall()

    return jsonify (showrooms)



    


 # Mpesa Integration.

# Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        # Extract POST Values sent
        amount = request.form['amount']
        phone = request.form['phone']

        # Provide consumer_key and consumer_secret provided by safaricom
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        # Authenticate Yourself using above credentials to Safaricom Services, and Bearer Token this is used by safaricom for security identification purposes - Your are given Access
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        # Provide your consumer_key and consumer_secret 
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        # Get response as Dictionary
        data = response.json()
        # Retrieve the Provide Token
        # Token allows you to proceed with the transaction
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')  # Current Time
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Passkey(Safaricom Provided)
        business_short_code = "174379"  # Test Paybile (Safaricom Provided)
        # Combine above 3 Strings to get data variable
        data = business_short_code + passkey + timestamp
        # Encode to Base64
        encoded = base64.b64encode(data.encode())
        password = encoded.decode()

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password":password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://coding.co.ke/api/confirm.php",
            "AccountReference": "Botanical Gardens",
            "TransactionDesc": "Payments for Products"
        }

        # POPULAING THE HTTP HEADER, PROVIDE THE TOKEN ISSUED EARLIER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        # Specify STK Push  Trigger URL
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  
        # Create a POST Request to above url, providing headers, payload 
        # Below triggers an STK Push to the phone number indicated in the payload and the amount.
        response = requests.post(url, json=payload, headers=headers)
        print(response.text) # 
        # Give a Response
        return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})






app.run(debug=True)
