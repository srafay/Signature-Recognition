import cv2

MIN_MATCH_COUNT = 10

def recognizeSignature(image1, image2):
    img1 = cv2.imread(image1 ,0)
    img2 = cv2.imread(image2 ,0)
    
    global MIN_MATCH_COUNT
    
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.70*n.distance:
            good.append(m)
            
    if len(good) >= MIN_MATCH_COUNT:
        return True
    
    return False

for i in range(2,6):
    if (recognizeSignature("data/{}.jpg" .format(i), "5.jpg")):
        print ("Found image in database, matched to {}.jpg" .format(i))