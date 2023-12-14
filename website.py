#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 6 19:22:20 2023

@author: natpitchaya
"""

# My two categories
X = "Normal"
Y = "Pneumonia"

# Two example images for the website, they are in the static directory next
# where this file is and must match the filenames here
sampleX = 'static/normal.jpeg'
sampleY = 'static/pneumonia.jpeg'

# Where I will keep user uploads
UPLOAD_FOLDER = 'static/uploads'
# Allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Machine Learning Model Filename
ML_MODEL_FILENAME = 'saved_model.h5'

# Load operation system library
import os

# website libraries
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# Load math library
import numpy as np

# Load machine learning libraries
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf

# Create the website object
app = Flask(__name__)

def load_model_from_file():
    myModel = load_model(ML_MODEL_FILENAME)
    myGraph = tf.Graph() 
    return myModel

# Try to allow only images
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySampleY=sampleY)
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('I only accept files of type' + str(ALLOWED_EXTENSIONS))
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    test_image = image.load_img(UPLOAD_FOLDER+'/'+filename, target_size=(150, 150))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    
    mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    myGraph = app.config['GRAPH']


    with myGraph.as_default():
        myModel = load_model('saved_model.h5')
        result = myModel.predict(test_image)
        image_src = '/'+UPLOAD_FOLDER+'/'+filename
        if result[0] < 0.5 :
            answer = "<div class='col text-center'><img width=150 height=150 src='"+image_src+"' class=img-'thumbnail'/><h4>guess:"+X+" "+str(result[0])+"</h4></div><div class='col'></div><div class='w-100'></div>"
        else:
            answer = "<div class='col text-center'><img width=150 height=150 src='"+image_src+"' class=img-'thumbnail'/><h4>guess:"+Y+" "+str(result[0])+"</h4></div><div class='col'></div><div class='w-100'></div>"
        results.append(answer)
        return render_template('index.html', myX=X, myY=Y, mySampleX=sampleX, mySampleY=sampleY, len=len(results), results=results)

def main():
    myModel = load_model_from_file()
    myGraph = tf.compat.v1.Graph()
    mySession = tf.compat.v1.Session(graph=myGraph)
    
    app.config['SECRET_KEY'] = 'super secret key'

    app.config['SESSION'] = mySession
    app.config['MODEL'] = myModel
    app.config['GRAPH'] = myGraph

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit
    app.run()

results=[]

# Launch everything
if __name__ == "__main__":
    main()




