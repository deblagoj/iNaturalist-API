# encoding: utf-8

import io
import os
import operator
import flask
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms as T

from inception import *


# Initialize our Flask application and the PyTorch model.
app = flask.Flask(__name__)
model = None
use_gpu = False

with open('species.txt', 'r') as f:
    idx2label = eval(f.read())


def load_model():
    global model
    print('test1')
    model = inception_v3(pretrained=False)
    model.fc = nn.Linear(2048, 8142)
    model.aux_logits = False
    model = model.to('cpu')

    checkpoint = torch.load('../iNat_2018_InceptionV3.pth.tar', map_location='cpu')
    print('test')
    state_dict = checkpoint['state_dict']
    model.load_state_dict(state_dict)

    model.eval()

    if use_gpu:
        model.cuda()


def prepare_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert("RGB")

    # Resize the input image nad preprocess it.
    image = T.Resize(target_size)(image)
    image = T.ToTensor()(image)

    # Convert to Torch.Tensor and normalize.
    image = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(image)

    # Add batch_size axis.
    image = image[None]
    if use_gpu:
        image = image.cuda()
    return torch.autograd.Variable(image, volatile=True)


@app.route("/predict", methods=["POST"])
def predict():
    # Initialize the data dictionary that will be returned from the view.
    data = {"success": False}

    # Ensure an image was properly uploaded
    if flask.request.method == 'POST':
        if flask.request.files.get("image"):
            # Read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # Preprocess the image and prepare it for classification.
            # image = prepare_image(image, target_size=(224, 224))
            image = prepare_image(image, target_size=(224, 224))

            # Classify the input image and then initialize the list of predictions to return to the client.
            preds = F.softmax(model(image), dim=1)
            results = torch.topk(preds.cpu().data, k=6, dim=1)
            results = (results[0].cpu().numpy(), results[1].cpu().numpy())
            data['predictions'] = list()

            # Loop over the results and add them to the list of returned predictions
            for prob, label in zip(results[0][0], results[1][0]):
                label_name = idx2label[label]
                r = {"label": label_name, "probability": float(prob)}
                data['predictions'].append(r)

            # Indicate that the request was a success.
            data["success"] = True

    # Return the data dictionary as a JSON response.
    return flask.jsonify(data)



if __name__ == '__main__':
    load_model()
    app.run(debug=True)
