import os
from flask import Flask, request, render_template
from Photofinderparm import process_image_and_text  # Import your function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response_content = None  # Initialize response_content variable

    if request.method == "POST":
        # Handle the file upload and custom text message here
        uploaded_image = request.files["image"]
        custom_text_message = request.form["custom_text"]

        if uploaded_image and custom_text_message:
            # Save the uploaded image to a temporary location (you may want to implement a more secure way to handle file uploads)
            image_path = "temp_image.jpeg"
            uploaded_image.save(image_path)

            # Call the process_image_and_text function and store the response content
            response_content = process_image_and_text(image_path, custom_text_message)

    return render_template("index.html", response_content=response_content)  # Pass response_content to the template

if __name__ == "__main__":
    app.run(debug=True)