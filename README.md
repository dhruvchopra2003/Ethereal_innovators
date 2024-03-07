# RANKHUB

An innovative e-commerce Catalogue ranking algorithm that leverages advanced technologies to increase the efficiency of the recommender algorithms of various ecommerce platforms. This repository contains the backend implementation of the algo. using Flask, MongoDB, Deep Learning and integrated ranking algorithms.

## Features

- *Catalog Ranking*: Utilizes sophisticated ranking algorithms to assess product catalog quality based on compliance, correctness, and completeness.
- *MongoDB Integration*: Stores product data in MongoDB for efficient retrieval and management.
- *API Endpoint*: Provides a Flask API endpoint for ranking products based on their titles, images, and descriptions.
- *Integration with Frontend*: Easily connects to frontend applications built using JavaScript for seamless integration into the shopping platform.

## Getting Started

1. Clone the repository:


git clone `https://github.com/dhruvchopra2003/Ethereal_innovators`


2. Install dependencies:


pip install -r requirements.txt


3. Set up MongoDB:

   - Install MongoDB locally or use a cloud-based MongoDB service.
   - Update the MongoDB URI in app.py to connect to your MongoDB database.

4. Run the Flask application:


python app.py


5. Access the API endpoint at http://localhost:5000/rank.

## Usage

### POST /rank

- *Description*: Rank a product based on its title, image, and description.
- *Request Body*:
  json
  {
    "product_title": "Product Title",
    "product_image": "Image URL",
    "product_description": "Product Description"
  }
  
- *Response*:
  json
  {
    "Title_to_image": 0.75,
    "Title_to_description": 0.85,
    "Rankings": 20.6780
    }
  }
  

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/new-feature).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature/new-feature).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
