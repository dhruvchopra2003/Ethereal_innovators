from flask import Flask, request, jsonify
from flask_cors import CORS
from integrated import ranking
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Info']  # Specify the database name
collection = db['ranking']  # Specify the collection name



@app.route('/rank', methods=['POST'])
def rank_item():
    # Get title, image, and desc from request body
    data = request.get_json()
    title = data.get('product_title')
    image = data.get('product_image')
    category = data.get('category')
    price = data.get('price')
    desc = data.get('product_description')
    id = data.get('product_id')
    certival = data.get('product_certi')

    # Call your ranking function
    Title_to_image, Title_to_description, rankings = ranking(title, image, desc, certival)
    json_data = {
        "Id" : id,
        "Title_to_image" : Title_to_image,
        "Title_to_description" : Title_to_description,
        "Rankings" : rankings,
        "Category" : category,
        "price" : price,
        "certival" : certival
    }
    response = jsonify(json_data)
    product_data={
        "product_title": title,
        "product_image": image,
        "product_description": desc,
        "ranking" : rankings,
        "Certificate" : certival
    }
    collection.insert_one(product_data) # insert into the db
    
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500/Frontend-form/productform.html'  # Replace with allowed origin
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # Allowed methods (adjust as needed)
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allowed headers (adjust as needed)
    
    # Return JSON response with rankings
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
