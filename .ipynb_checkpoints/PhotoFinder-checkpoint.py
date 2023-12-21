#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
from openai import OpenAI
import base64
import time
import requests
import numpy as np


# In[2]:


api_key = os.environ.get("OPENAI_API_KEY")


# In[3]:


def split_image(image_name, rows, cols, overlap_percentage):
    # Load the image
    image = cv2.imread(image_name)

    # Calculate the dimensions of each square
    height, width, _ = image.shape
    square_height = height // rows
    square_width = width // cols

    # Calculate the overlap size in pixels
    overlap_height = square_height * overlap_percentage // 100
    overlap_width = square_width * overlap_percentage // 100

    # Create a directory to save sub-images
    os.makedirs("sub_images", exist_ok=True)

    # Split the image into squares with overlap and save them
    for i in range(rows):
        for j in range(cols):
            y_start = i * (square_height - overlap_height)
            y_end = (i + 1) * square_height
            x_start = j * (square_width - overlap_width)
            x_end = (j + 1) * square_width

            sub_image = image[y_start:y_end, x_start:x_end]

            # Save the sub-image to disk
            sub_image_filename = f'sub_images/sub_image_{i}_{j}.jpg'
            cv2.imwrite(sub_image_filename, sub_image)


# In[4]:


# Function to encode the image
def encode_image(image_name):
  with open(image_name, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# In[5]:


# Define a function to read and encode images from a directory
def read_and_encode_images(image_directory):
    # List to store base64-encoded images
    encoded_images = []

    # Get a list of filenames in the directory and sort them alphabetically
    image_files = sorted(os.listdir(image_directory))

    # Loop through the sorted filenames
    for filename in image_files:
        if filename.endswith(".jpg"):  # Adjust the file extension as needed
            image_name = os.path.join(image_directory, filename)

            # Encode the image using the encode_image function and append it to the list
            base64_image = encode_image(image_name)
            encoded_images.append(base64_image)

    return encoded_images


# In[6]:


# Define a function to make the OpenAI API request
def make_openai_api_request(api_key, custom_text_message):
    # List to store message objects for each image
    messages = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Add a single text message
    text_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": custom_text_message,
            }
        ]
    }
    messages.append(text_message)

    # Iterate through encoded images and add image messages
    for base64_image in encoded_images:
        image_message = {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
        messages.append(image_message)

    # Create the payload with the list of messages
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": messages,
        "max_tokens": 300
    }

    # Record the start time
    start_time = time.time()

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"API request took {elapsed_time:.2f} seconds")

    return response


# In[7]:


# Define the name of the input image file.
image_name = 'storephoto.jpeg'

# Define the directory where the sub-images will be saved.
image_directory = "sub_images"

# Define a custom text message to be used in the OpenAI API request.
custom_text_message = "In these images, please specify in which image I can find the lemon grass, and provide a detailed description of the product and the location."


# In[8]:


# Example usage with a variable for the image path:
# Split the input image into a grid of sub-images.
split_image(image_name, rows=2, cols=3, overlap_percentage=10)


# In[9]:


# Usage:
# Read and encode the sub-images located in the specified directory.
encoded_images = read_and_encode_images(image_directory)


# In[10]:


# Usage:
# Make an OpenAI API request with the provided API key and custom text message.
response = make_openai_api_request(api_key, custom_text_message)


# In[11]:


print(response.json())


# In[ ]:




