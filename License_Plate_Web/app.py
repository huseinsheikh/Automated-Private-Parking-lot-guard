import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify

from Database import DataBase
from Car_Number_Extraction import get_number

db = DataBase()
app = Flask(__name__)


@app.route('/')
def hello_world():
    data = db.get_license_numbers()
    log = db.get_log()
    return render_template('index.html', data=data, log=log)


@app.route('/add-item', methods=['Get'])
def add_item():
    license_number = '0000000'

    license_number = request.args.get('license_number')

    op_done = db.add_number(license_number)
    op_done = 1 if op_done is True else 2

    resp = jsonify(success=True, op_done=op_done)
    return resp


@app.route('/del-item', methods=['get'])
def del_item():
    license_number = '0000000'

    license_number = request.args.get('license_number')

    if license_number != '0000000':
        db.del_number(license_number)
    return render_template('index.html')


@app.route('/edit-item', methods=['get'])
def edit_item():
    new_number = '0000000'

    old_number = request.args.get('old_number')
    new_number = request.args.get('new_number')

    if new_number != '0000000':
        op_done = db.edit_number(old_number, new_number)

    op_done = 1 if op_done is True else 2
    resp = jsonify(success=True, op_done=op_done)
    return resp


@app.route('/find-item', methods=['GET'])
def find_item():
    data = db.get_license_numbers()
    log = db.get_log()
    value = str(request.args.get('license_number'))
    number_to_find = value if value is not None else '0'

    if number_to_find == '0':
        return render_template('index.html', data=data, item_found=0)

    item_found = db.search_for_car_number(number_to_find)
    item_found = 1 if item_found is True else 2
    return render_template('index.html', data=data, log=log, item_found=item_found, value=number_to_find)

@app.route('/search-item', methods=['POST'])
def search_item():
    value_to_find = '0'

    if request.method == 'POST':
        data = request.form['data']
    value_to_find = data.split(',')[0]
    original_number = data.split(',')[1]
    db.add_log(original_number, value_to_find)
    item_found = db.search_for_car_number(value_to_find)
    return str(item_found)

@app.route('/detect', methods=['GET', 'POST'])
def handle_request():
    img_path = 'file.png'

    imageData = None
    if request.method == 'POST':
        imageData = request.form['image_path']


    save(imageData, img_path)
    number = get_number(img_path)
    number = number.replace(' ', '')
    corpped_image = image_to_base64('Cropped-Images-Text.png')
    return {'number':str(number), 'image':corpped_image}


def save(encoded_data, filename):
    """
    convert a base64 string to an image, and store it on the server to be used
    :param encoded_data: base64 string to be converted to an image
    :param filename: the file name of the converted image.
    :return:
    """
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    return cv2.imwrite(filename, img)

def image_to_base64(img_path):
    """
    to convert an image to base64 string
    :param img_path: the location of the image to be converted
    :return:
    """
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string
