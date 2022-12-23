import io
from PIL import Image
import cv2
import torch
from flask import Flask,request,make_response
from werkzeug.exceptions import BadRequest
import os

from .utils.util  import take_pic

def create_app():
    
    app = Flask(__name__)

    for r, d, f in os.walk("./models_train"):
        for file in f:
            if ".pt" in file:
                # example: file = "model1.pt"
                # the path of each model: os.path.join(r, file)
                model= torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(r, file), force_reload=True)
                print("Model Loaded")
                # you would obtain: dictOfModels = {"model1" : model1 , etc}

    def get_prediction(img_bytes,model):
        img = Image.open(io.BytesIO(img_bytes))
        # inference
        results = model(img, size=640)  
        return results

    def get_prediction_test(dir,model):
        img = Image.open(dir)
        # inference
        results = model(img, size=640)  
        print("Processed")
        return results

    @app.route('/', methods=['GET'])
    def index():
        return r"<p>hi it works!</p>"

    @app.route('/', methods=['POST'])
    def predict():

        file = extract_img(request)
        img_bytes = file.read()
        # choice of the model
        results = get_prediction(img_bytes,model)
        print(f'User selected model : {request.form.get("model_choice")}')
        print(results)
        # updates results.imgs with boxes and labels
        results.render()

        # encoding the resulting image and return it
        for img in results.imgs:
            RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im_arr = cv2.imencode('.jpg', RGB_img)[1]
            response = make_response(im_arr.tobytes())
            response.headers['Content-Type'] = 'image/jpeg'
        # return your image with boxes and labels


    def extract_img(request):
        # checking if image uploaded is valid
        if 'file' not in request.files:
            raise BadRequest("Missing file parameter!")
        file = request.files['file']
        if file.filename == '':
            raise BadRequest("Given file is invalid")
        return file

    #take_pic()
    path = 'det/test.jpg'
    results = get_prediction_test(path,model)

    print(results.pandas().xyxy[0])

    results.render()

    return app