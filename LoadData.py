import numpy as np
import cv2
import pickle
import os

metadata_dir = './data/FACD_metadata/'
image_dir = './data/FACD_image/'
filter_dir = ['1977', 'Amaro', 'Apollo', 'Brannan', 'Earlybird', 'Gotham', 'Hefe', 'Hudson', 'Inkwell', 'Lofi', 'LordKevin', 'Mayfair', 'Nashville', 'Origin', 'Poprocket', 'Rise', 'Sierra', 'Sutro', 'Toaster', 'Valencia', 'Walden', 'Willow', 'XProII']

# Load ImageData
print('Load Image...')
image_index = []
for i in os.listdir(image_dir + '1977/'):
    image_index.append(i[:-4])

image_list = []
for i in range(len(image_index)):
    image_list.append([])
    for j in filter_dir:
        # image_list[i].append(cv2.imread(image_dir + j +'/' + image_index[i] + '.jpg'))
        image_list[i].append(image_dir + j +'/' + image_index[i] + '.jpg')

# Load metadata
print('Load metadata...')
image_score = []
pairwise_comparison = []

with open(metadata_dir + 'image_score.pkl', 'rb') as f:
    image_score = pickle.load(f)

with open(metadata_dir + 'pairwise_comparison.pkl', 'rb') as f:
    pairwise_comparison = pickle.load(f)

# print(image_score) # {'filterName': 'Nashville', 'imgId': '28202', 'class': '0', 'score': -3}
# print(pairwise_comparison) # {'category': 6, 'f1': '1977', 'f2': 'Hudson', 'workerId': 'A23DZO4PNK67M5', 'passDup': False, 'imgId': '242192', 'ans': 'right'}

print('build scores')
pairwise_comparison_score = np.zeros((len(image_list), len(filter_dir)))
for i in pairwise_comparison:
    index = image_index.index(i['imgId'])
    right_filter_index = filter_dir.index(i['f2'])
    left_filter_index = filter_dir.index(i['f1'])

    if(i['ans'] == 'right'):
        pairwise_comparison_score[index,right_filter_index] = pairwise_comparison_score[index,left_filter_index] + 1
    else:
        pairwise_comparison_score[index,left_filter_index] = pairwise_comparison_score[index,right_filter_index] - 1

pairwise_comparison_score = pairwise_comparison_score / np.linalg.norm(pairwise_comparison_score)


print(pairwise_comparison_score[-5:])