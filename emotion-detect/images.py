import urllib.request
import cv2
import numpy as np
import os
import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

# store raw images
def store_raw_imgs():
	# neg_imgs_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
	# neg_imgs_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02123394'
	neg_imgs_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02109961'
	neg_img_urls = urllib.request.urlopen(neg_imgs_link).read().decode()
	pic_num = 1961

	if not os.path.exists('neg'):
		os.makedirs('neg')

	for i in neg_img_urls.split('\n'):
		try:
			print(i)
			#save raw img
			urllib.request.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
			#turn to gray scale img
			img = cv2.imread("neg/"+str(pic_num)+'.jpg', cv2.IMREAD_GRAYSCALE)
			#resize img to 100 by 100
			resized = cv2.resize(img, (100,100))
			#save resized img
			cv2.imwrite("neg/"+str(pic_num)+'.jpg', resized)
			pic_num += 1

		except Exception as e:
			print(str(e))

# delete photos that aren't found
def find_ugly():
	for file_type in ['neg']:
		for img in os.listdir(file_type):
			for ugly in os.listdir('ugly'):
				try:
					# get curr img
					current_img_path = str(file_type)+'/'+str(img)
					ugly = cv2.imread('ugly/'+str(ugly))
					question = cv2.imread(current_img_path)

					# if they have the same dimensions  |  xor - one or the other not both
					# everything is identical
					if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
						print('u ugly')
						print(current_img_path)
						os.remove(current_img_path)

				except Exception as e:
					print(str(e))

# description file
def create_pos_n_neg():
	for file_type in ['neg']:
		for img in os.listdir(file_type):
			if file_type == 'neg':
				line = file_type + '/' +img + '\n'
				with open('bg.txt','a') as f:
					f.write(line)
			elif file_type == 'pos':
				line = file_type + '/' +img + ' 1 0 0 50 50\n'
				with open('info.dat', 'a') as f:
					f.write(line)

# store_raw_imgs()
# find_ugly()
# create_pos_n_neg()
