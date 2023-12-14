# pneumoniadetector
Pneumonia Detector for CS50

My project is to distinguish whether the chest X-ray picture uploaded has a pneumonia infection (could be viral or bacterial) or a normal chest X-ray. Users can access using the web application. The model was built using Tensorflow, Jinja2, Flask, Bootstrap4, and HTML.

The file contains
1. website.py - python and flask allow users to upload their CXR to the system. The results will be interpreted as normal if the value is <0.5, if the value is greater than 0.5 - it will be interpreted as pneumonia. The result will be given in a list of results (results[]). on index.html page

2. trainTheBrain.py - use Keras and TensorFlow - the model is built on TensorFlow. Each category will be trained on a dataset containing 20 images each. The system also has an augmentation configuration that will be used for training as well. 
    
3. index.html - HTML site displaying images, titles. Allowing users to upload CXR pictures.
