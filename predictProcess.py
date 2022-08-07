import os
import tensorflow as tf
import numpy as np

from tensorflow.keras import *
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class Predict():
    def __init__(self, path) -> None:
         # Load .h5 model
            self.Model = models.load_model(str(path))
    
    def predict_process(self, path_img):
        try:
            # answer class list
            Class_list = ['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold', 'Septoria_leaf_spot', 'Spider_mites', 'Target_Spot', 'Yellow_Leaf_Curl_Virus', 'mosaic_virus', 'healthy']
            img_size = (120, 120)
            # Load Image with 64 x 64
            test_img = load_img(path_img, target_size = img_size)
            # Convert Image to array
            test_img = img_to_array(test_img) / 255.0
            # Convert Tensor 3D to Tensor 4D for predict data
            test_img = np.expand_dims(test_img, axis = 0)
            # Predict Test Data
            predict = self.Model.predict(test_img)
            class_disease = np.argmax(np.round(predict[0]))
            return Class_list[class_disease]
        except:
            return 'Error'
        
    