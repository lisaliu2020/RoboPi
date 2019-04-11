import urllib
import cv2
import numpy as np
import os

def store_raw_imgs():
	# neg_imgs_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
	neg_imgs_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00007846'
	neg_img_urls = urllib.urlopen(neg_imgs_link).read().decode()

	if not os.path.exists('neg'):
		os.makedirs('neg')

	pic_num = 454;

	for i in neg_img_urls.split('\n'):
		try:
			print(i)
			#save raw img
			urllib.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
			#turn to gray scale img
			img = cv2.imread("neg/"+str(pic_num)+'.jpg', cv2.IMREAD_GRAYSCALE)
			#resize img to 100 by 100
			resized = cv2.resize(img, (100,100))
			#save resized img
			cv2.imwrite("neg/"+str(pic_num)+'.jpg', resized)
			pic_num += 1

		except Exception as e:
			print(str(e))

store_raw_imgs()
