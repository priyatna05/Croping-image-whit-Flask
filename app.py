from flask import Flask, render_template, request
import os
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def crop_image(image_path, size, position):
    img = Image.open(image_path)
    width, height = img.size

    if position == 'top_left':
        return img.crop((0, 0, size, size))
    elif position == 'top_center':
        left = (width - size) // 2
        return img.crop((left, 0, left + size, size))
    elif position == 'top_right':
        return img.crop((width - size, 0, width, size))
    elif position == 'center_left':
        top = (height - size) // 2
        return img.crop((0, top, size, top + size))
    elif position == 'center':
        left = (width - size) // 2
        top = (height - size) // 2
        return img.crop((left, top, left + size, top + size))
    elif position == 'center_right':
        top = (height - size) // 2
        return img.crop((width - size, top, width, top + size))
    elif position == 'bottom_left':
        return img.crop((0, height - size, size, height))
    elif position == 'bottom_center':
        left = (width - size) // 2
        return img.crop((left, height - size, left + size, height))
    elif position == 'bottom_right':
        return img.crop((width - size, height - size, width, height))
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No image selected.')

        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error='No image selected.')

        if file:
            # Save the uploaded image to the UPLOAD_FOLDER
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.jpg')
            file.save(image_path)

            return render_template('index.html', uploaded=True, filename='original.jpg')

    return render_template('index.html')

@app.route('/crop', methods=['POST'])
def crop():
    size = int(request.form['size'])
    position = request.form['position']
    uploaded_filename = request.form['uploaded_filename']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)

    cropped_image = crop_image(image_path, size, position)
    if cropped_image:
        # Convert the image to RGB mode
        cropped_image = cropped_image.convert('RGB')

        cropped_filename = 'cropped.jpg'
        cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
        cropped_image.save(cropped_path)
        return render_template('index.html', cropped=True, filename=cropped_filename)
    else:
        return render_template('index.html', error='Invalid crop position.')


if __name__ == '__main__':
    app.run()
