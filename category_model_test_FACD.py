import cv2
import glob
import numpy as np
from utils.Category_Model import CreatModel
from utils.Category_DataManager import batchGenerator
import time
import pickle
from keras.models import load_model

BATCH_SIZE = 16
input_shape = (64, 64, 3)
image_dir = './data/category_image/'

filter_dir = ['1977', 'Amaro', 'Apollo', 'Brannan', 'Earlybird', 'Gotham', 'Hefe', 'Hudson', 'Inkwell', 'Lofi', 'LordKevin', 'Mayfair', 'Nashville', 'Origin', 'Poprocket', 'Rise', 'Sierra', 'Sutro', 'Toaster', 'Valencia', 'Walden', 'Willow', 'XProII']
category_list = ['animal','floral', 'landscape', 'architecture', 'fooddrink', 'portrait', 'cityscape', 'stilllife']

def getTestData(image_list, label_list):
    test_images = []
    test_labels = []
    for i in range(len(image_list)):
        # Read image data
        image = cv2.imread(image_list[i][13])
        
        # Preprocessing image data
        image = cv2.resize(image, (input_shape[1],input_shape[0]))
        # image = np.expand_dims(image, axis = -1)
        image = np.array(image, dtype = np.float32) / 255.0
        
        test_images.append(image)
        test_labels.append(label_list[i])

    # convert data type to float32
    test_images = np.array(test_images, dtype = np.float32)
    test_labels = np.array(test_labels, dtype = np.float32)
    return test_images, test_labels

def test():
    with open('./data/FACD_metadata/image_list.pkl', 'rb') as f:
        test_images = pickle.load(f)
    with open('./data/FACD_metadata/category.pkl', 'rb') as f:
        test_labels = pickle.load(f)

    # Prepare the data
    pred_images, test_labels = getTestData(test_images, test_labels)

    # Create the model
    # model = CreatModel(input_shape = input_shape, output_shape = 23)
    save_model_path = 'category_model.h5'
    # model.load_weights(save_model_path)
    model = load_model(save_model_path)
    # Predict
    s = time.time()
    sigmoid_output = model.predict(pred_images)
    print('time spend ' + str(time.time() - s) + ' s')
    # Decode
    pred_labels = np.argmax(sigmoid_output, axis = 1) # Decode softmax output
    # test_labels = np.argmax(test_labels, axis = 1)
    print('pred', pred_labels)
    print('test', test_labels)
    print((pred_labels == test_labels))
    
    # Compute the test data accuracy
    accuracy = np.count_nonzero((pred_labels == test_labels))
    print('Your test accuracy is %.6f' % (accuracy / len(test_labels) * 100))

    for i in range(len(pred_labels)):
        print('pred', pred_labels[i], 'truth', test_labels[i]) 
        print(category_list[pred_labels[i]], category_list[int(test_labels[i])])
        originImg = cv2.imread(test_images[i][13])
        # predImg = cv2.imread(test_images[i][pred_labels[i]])
        # ansImg = cv2.imread(test_images[i][int(test_labels[i])])
        # print(test_images[i][pred_labels[i]])
        cv2.imshow('origin', originImg)
        # cv2.imshow('recommand', predImg)
        # cv2.imshow('ans', ansImg)
        cv2.waitKey(0)

    pass

if __name__ == "__main__":
    test()
