import os
from flask import Flask, request, render_template, jsonify
from your_image_processing_code import split_image  # Import your existing code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the file upload and custom text message here
        uploaded_image = request.files["image"]
        custom_text_message = request.form["custom_text"]

        # Save the uploaded image to a temporary location (you may want to implement a more secure way to handle file uploads)
        image_path = "temp_image.jpeg"
        uploaded_image.save(image_path)

        # Call your existing code for image processing
        split_image(image_path, rows=2, cols=3, overlap_percentage=10)

        # Optionally, return a response to the user
        return "Image processing complete."

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
