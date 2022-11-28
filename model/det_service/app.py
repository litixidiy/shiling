import io
from PIL import Image
import cv2
import torch
from flask import Flask, render_template,request,make_response
from werkzeug.exceptions import BadRequest
import os
import  cv2

app = Flask(__name__)

for r, d, f in os.walk("models_train"):
    for file in f:
        if ".pt" in file:
            # example: file = "model1.pt"
            # the path of each model: os.path.join(r, file)
            model= torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(r, file), force_reload=True)
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

def take_pic():
    cap = cv2.VideoCapture(0)

    while(True):
        cv2.waitKey(1)
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF!=255:
            cv2.imwrite("test.jpg",frame)

            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


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

results = get_prediction_test("./test.jpg",model)
print(results.pandas().xyxy[0])

results.render()

"""
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
"""