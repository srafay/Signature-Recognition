import cv2

class MyImage:
    def __init__(self, img_name, optional=0):
        self.img = cv2.imread(img_name, optional)
        self.__name = img_name

    def __str__(self):
        return self.__name

img1 = MyImage('5.jpg', 0)          # queryImage
img2 = MyImage('data/5.jpg', 0) # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1.img,None)
kp2, des2 = sift.detectAndCompute(img2.img,None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.60*n.distance:
        good.append([m])

if len(good) >= 8:
    print ("Signature of : " + str(img1))