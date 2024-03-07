import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
import time
import io
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import google.generativeai as genai
from nltk.stem import PorterStemmer

##################### IMAGE TO TITLE CORRELATION ######################################
def check_img_similarity(query, product_image_path):
    """
    Checks the correlation with the title and the image of the product. The images are stored in a test folder

    Args:
        query (string): product_name to search
        product_image_path (string): includes the image path
    """
    if product_image_path.strip() == "": 
        return -3
    
    def get_ref_img_url(query):
        # Prepare Google search URL
        query = "+".join(query.split())
        url = f"https://www.google.com/search?q={query}&tbm=isch"

        # Send HTTP request and get response
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the URL of the second image
        img_tags = soup.find_all("img")
        img_url = img_tags[1]["src"]

        def download_image(download_path, url, file_name):
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = download_path + file_name

            with open(file_path, "wb") as f:
                image.save(f, "jpeg")

            print("done")

        download_image("./images", img_url, "test.jpg")

    get_ref_img_url(query)
    path1 = product_image_path
    path2 = "./images/test.jpg"

    def preprocess_image(img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array

    def extract_features(img_path, model):
        img = preprocess_image(img_path)
        features = model.predict(img)
        return features.flatten()

    def calculate_similarity(features1, features2):
        similarity_score = cosine_similarity([features1], [features2])
        return similarity_score[0][0]

    # Load pre-trained VGG16 model
    model = VGG16(weights="imagenet", include_top=False)
    features1 = extract_features(path1, model)
    features2 = extract_features(path2, model)

    # Calculate similarity score
    similarity_score = calculate_similarity(features1, features2)
    print("Similarity score:", similarity_score)

    return similarity_score



################# TEXT TO DESCRIPTION SIMILARITY ###################################
def reduce_desc(desc):
    
    words = word_tokenize(desc)
    words = [word.lower() for word in words if word.isalnum()]
    ps = PorterStemmer()
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [ps.stem(word.lower()) for word in words if word not in stop_words]

    return filtered_words

def generate_keywords(product_name):
    genai.configure(api_key="AIzaSyBkheEuRdAh4xULrOz-g1GveaIv8RZkka8")
    ps = PorterStemmer()
    model = genai.GenerativeModel("gemini-pro")
    product = product_name
    response = model.generate_content(
        f"Give the 30 words for the product {product_name} that should be present in it's description. Give space separated words"
    )
    time.sleep(3)
    x = response.text
    print(x)
    # Split the string into a list using newline character as separator
    word_list = x.split(" ")
    word_list = [ps.stem(word.lower()) for word in word_list]
    # Remove any elements containing digits using list comprehension

    print(word_list)
    return word_list


def relevance_coeff(desc_keys, gen_keys):
    # Create a corpus of words from the refined description
    description_words = set(desc_keys)
    if len(description_words) < 2:
        return 0
    
    print(description_words)

    # Calculate the number of relevant words present in the description
    relevant_words_in_description = description_words.intersection(gen_keys)

    # Calculate percentage relevance
    relevance_percentage = (len(relevant_words_in_description) / len(gen_keys)) * 100

    return relevance_percentage



############### Function to declare the final rankings #####################################
def ranking(product_name, product_image, product_description, certival):
    """
        Inputs the product metrics and outputs the ranking based on the metrics
    """
    
    Title_to_image = check_img_similarity(product_name, product_image) * 100
    Title_to_desc = relevance_coeff(reduce_desc(product_description), generate_keywords(product_name))
    
    product_ranking = Title_to_image + Title_to_desc
        
    if certival == 1:
        product_ranking += 10
    
    return Title_to_image, Title_to_desc, product_ranking
    
    
    
    
