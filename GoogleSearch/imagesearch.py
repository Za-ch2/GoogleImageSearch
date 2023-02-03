from flask import Flask, render_template, redirect, request
import requests
import requests
from bs4 import BeautifulSoup
from PIL import Image

app = Flask(__name__)

max_size = 1824000
def imageInput(productName, max_size):
    searchURL = f"https://www.google.com/search?q={productName}&tbm=isch"
    res = requests.get(searchURL)
    soup = BeautifulSoup(res.text, "html.parser")
    images = soup.find_all("img")
    if images:
        for image in images:
            # Check the width and height of each image
            width = image.get("width", 0)
            height = image.get("height", 0)
            # If the dimensions match the desired dimensions, select this image
            if width * height >= max_size:
                productImageURL = image["src"]
                # check the actual size of the image
                response = requests.get(productImageURL, stream=True)
                content_length = int(response.headers.get("Content-Length", 0))
                if content_length >= max_size:
                    return productImageURL
        # If no image with desired dimensions is found, choose the first image
        productImageURL = images[1]["src"]
        return productImageURL
    else:
        return None

def uploadImage(productName, imageURL):
    with open("search.html", "w") as file:
        file.write("<html>\n")
        file.write("<body>\n")
        file.write(f"<h1>{productName}</h1>\n")
        file.write(f'<img src="{imageURL}" alt="{productName}">\n')
        file.write("</body>\n")
        file.write("</html>\n")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searchAgain = request.form.get('search_again')
        if not searchAgain:
            productName = request.form['product_name']
            imageURL = imageInput(productName, max_size)
            uploadImage(productName, imageURL)
            if imageURL:
                return render_template("search.html", productName=productName, productImageURL=imageURL)
            else:
                return "No image found for product."
        else:
            return redirect("/search")
    return '''
        <h1>Please Search a Term</h1>
        <style>
            h1 {
                position: absolute;
                top: 40%;
                left: 48%;
                transform: translate(-40%, -48%);
                text-align: center;
            }
        </style>
        <form method="post">
            <input type="text" name="product_name">
            <input type="submit" value="Search">
        </form>
        <style>
            h1 {
                text-align: center;
            }
            form {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            input[type="text"] {
                margin: 0 10px;
            }
        </style>
    '''


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        productName = request.form['product_name']
        imageURL = imageInput(productName,max_size)
        uploadImage(productName, imageURL)
        if imageURL:
            return render_template("search.html", productName=productName, productImageURL=imageURL)
        else:
            return "No image found for product."
    return '''
        <h1>Please Enter Another Search Term</h1>
        <style>
            h1 {
                position: absolute;
                top: 40%;
                left: 48%;
                transform: translate(-40%, -48%);
                text-align: center;
            }
        </style>
        <form method="post">
            <input type="text" name="product_name">
            <input type="submit" value="Search">
        </form>
        <style>
            h1 {
                text-align: center;
            }
            form {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            input[type="text"] {
                margin: 0 10px;
            }
        </style>
    '''

if __name__ == "__main__":
    app.run(debug=True)
