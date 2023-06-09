import streamlit as st # library for deploying ml app

import tensorflow as tf # deep learning framework
import tensorflow_hub as hub #used to load saved model
import numpy as np # for numerical computation

# for image mainpulation
import cv2 
from PIL import Image

# setting title bar and page layout
st.set_page_config(page_title="Lagos-Landmarks", layout="wide", page_icon="🌉")

st.sidebar.header("Landmarks of Lagos 🌉")
# Frontend Texts
st.title("The Landmarks of Lagos")
st.subheader("Tourism at a low in Lagos? Lets appreciate the little landmarks we have")

st.text("* Aro meta statue\n* Cathedral Church of Christ, marina\n* Civic Center lagos\n* Lekki-Ikoyi bridge\n* National Theatre Lagos\n* Necom house lagos\n* Tafewa Balewa Square (TBS)")

# loading saved model
model = tf.keras.models.load_model(
       ("lagos.h5"),
       custom_objects={'KerasLayer': hub.KerasLayer}
)

# labels that can be predicted
labels = ["Aro meta statue", "Cathedral Church of Christ, marina", "Civic Center lagos", "Lekki-Ikoyi bridge", "National Theatre Lagos",
         "Necom house lagos", "Tafewa Balewa Square (TBS)"]

def predict(picture):    
    image = cv2.resize(np.array(picture), (224, 224)) # resize image to tensor of 224 * 224 pixels
    image = image / 255 # scale the image

    try:
        x = np.reshape(image, (-1, 224, 224, 3)) #if tensor is RGB (,3), process for prediction
    except:
        x = np.reshape(image, (1, 224, 224, 1)) #if tensor is not RGB, convert then process for prediction
        x = np.concatenate([x]*3, axis=-1)

    x = model.predict(x).flatten() # predict value and get predictions
    prediction = x.argmax() # Get the label of the highest accuracy 
    confidences = {labels[i]: float(x[i]) for i in range(6)} # get prediction for each label and store in a dictionary
    return prediction, confidences


upload= st.file_uploader('Insert image for classification', type=['png','jpg', 'jpeg']) # for user to upload picture
c1, c2= st.columns(2, gap="large") # creating 2 columns


if upload is not None:
    img = Image.open(upload) # collect image
    
    c1.header('Your Picture')
    c1.image(img) # show image on screen
    answer, pred = predict(img) # predict label image

    c2.header('Predictions :')
    c2.subheader(f"This is the {labels[answer]}") # display  prediction
    
    # get the 3 most accurate predictions
    sorted_values = sorted(pred.items(), key=lambda x: x[1], reverse=True)[:3]

    # Loop over the sorted values and create a progress bar for each label and prediction
    for key, value in sorted_values:
        c2.write(key)
        progress_bar = c2.progress(0)
        for i in range(3):
            progress_bar.progress(value, text=f"I have {value * 100:.2f}% confidence ")
    