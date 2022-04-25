import io
from base64 import encodebytes
from PIL import Image
from flask import jsonify, Flask,request,abort
import glob
import os

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.mp4']
app.config['UPLOAD_PATH'] = 'uploads'

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_images',methods=['GET','POST'])
def get_images():
    #upload videos
    uploaded_video1 = request.files.getlist("video1")[0]
    uploaded_video2 = request.files.getlist("video2")[0]
    video1_filename = uploaded_video1.filename
    video2_filename = uploaded_video2.filename
    if video1_filename != '' and video2_filename != '':
        _, video_file_ext = os.path.splitext(video1_filename)
        _, image_file_ext = os.path.splitext(video2_filename)
        if image_file_ext not in app.config['UPLOAD_EXTENSIONS'] or video_file_ext not in app.config[
            'UPLOAD_EXTENSIONS']:
            abort(400)
        video1_filename = os.path.join(app.config['UPLOAD_PATH'], video1_filename)
        video2_filename = os.path.join(app.config['UPLOAD_PATH'], video2_filename)
        uploaded_video1.save(video1_filename)
        uploaded_video2.save(video2_filename)

    ##result  contains list of path images
    result = glob.glob('images/*') # Replace this line with the function that returns the list of images

    #Encode the images
    encoded_imges = []
    for image_path in result:
        encoded_imges.append(get_response_image(image_path))
    # print(encoded_imges)

    #Returns the list of ended images
    return jsonify({'result': encoded_imges})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

