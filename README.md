# iNaturalist 2017 CV model to recognize Invasive alien species

To install the dependencies, run: pip install -r requirements.txt

The research objective is to recognize Invasive Alien Species (IAS) in Europe with CV capabilities based on iNaturalist 2017 model. The initial idea is to test the iNaturalist 2017 CV model accuracy on an already available European IAS dataset. The European IAS dataset contains 1192 images of 59 distinct IAS gathered by 696 submitted observations. The performed analysis showed that the iNaturalist 2017 CV model can recognize 18 IAS. The IAS sub-dataset of these 18 species contains 65 quality controlled images. The iNaturalist CV 2017 model processed these 65 IAS images and produced results with 35.4% Top-1 and 47.7% Top-5 accuracy. The IAS recognition results are visualized and explained.

## data_analysis.ipynb
Data analysis

## run_pytorch_server.py
Create local flusk python server API with iNaturalist 2017 model

## simple_request.py
Makes a simple request to the flusk python server API with an image, and stores results. 

## inception.py
Inception file.