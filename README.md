# Signature Recognition
*Recognizing handwritten signatures of individuals accurately considering that they might be forged*

I have used Open CV implementation of different algorithms for feature extraction and comparison

### Following methods are used to compute feature point descriptors:

1. **Binary Robust Independent Elementary Features (BRIEF)**
	* We need image descriptors that are fast to compute, match and are memory efficient
	* It provides a shortcut to find the binary strings directly without finding descriptors
	* It takes smoothened image patch and selects a set of n (x,y) location pairs in a unique way
	* Then on those location pairs (p and q), it calculates intensity comparisons
	* If I(p) < I(q), then its result is 1, else it is 0
	* This is applied for all the n location pairs to get a n-dimensional bitstring
	* This n can be 128, 256 or 512 bits (OpenCV has default value of 32 bytes = 256 bits)
	* Comparing strings can be done using the Hamming distance, which is very efficient to compute (instead of the L2 norm as is usually done)

<p align="center">
<img src="https://i.imgur.com/fo3ZxPJ.png">
</p>
<p align="center"><sup><sub>Image taken from original research paper</sub></sup></p>
<p align="center">Fig: Different approaches on choosing the test locations (n = 128 bits)</p>

* More details can be found in this Research paper [Binary Robust Independent Elementary Features (BRIEF)](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf)

2. **Oriented FAST and Rotated BRIEF (ORB)**
	* SIRF and SURF are patented and you need to pay for their usage
	* ORB is an efficient alternative to SIFT or SURF (as the title of the paper suggests)
	* ORB uses FAST keypoint detectors
		* Keypoints are the interest points, which decscribe what is interesting or stands out in the image. 
		* Keypoints are important because no matter how the image changes (rotates, expands/shrinks, distorted etc), the keypoints in the original and modified image should be the same.
		* When finding the keypoints in the modified image, the orientation of the keypoints might be changed.
		* To find the orientation of keypoints, ORB computes the intensity weighted centroid of the patch with located corner at center 
		* The direction of the vector from this corner point to centroid gives the orientation
		* The equations and more detailed information can be found in the heading **3.2. Orientation by Intensity Centroid** of the paper
	* ORB uses BRIEF descriptors
		* Descriptors are how you describe these keypoints
		* but we know that BRIEF works poorly with rotated images
		* so what ORB does is to “steer” BRIEF according to the orientation of keypoints
		* More information about steering the BRIEF can be found in the heading **4.1. Efficient Rotation of the BRIEF Operator** of the paper
	* For descriptors matching, multi probe LSH (Locality Sensitive Hashing) is used instead of traditional LSH
		* LSH is used for approximate similarity search
		* LSH hashes input items so that similar items map to the same “buckets” with high probability (the number of buckets being much smaller than the universe of possible input items)
		* The problem is the requirement for a large number of hash tables in order to achieve good search quality
		* Thus it intelligently probes multiple buckets that are likely to contain query results in a hash table
		* Multi-probe LSH uses less query time and 5 to 8 times fewer number of hash tables
		* Thus it is both space and time efficient compared to traditional LSH
		
<p align="center">
<img src="https://i.imgur.com/Ol73NDg.jpg">
</p>
<p align="center"><sup><sub>Image taken from <a href="http://www.vlfeat.org/overview/sift.html">VLFeat Toolbox Tutorial</a></sub></sup></p>
<p align="center">Fig: Scale and Orientation of Keypoints</p>

* More details can be found in this Research paper [ORB: An efficient alternative to SIFT or SURF](http://www.willowgarage.com/sites/default/files/orb_final.pdf)

3. **Scale Invariant Feature Transform (SIFT)**
* Why SIFT
	* Some keypoint detectors are rotation invariant
	* But they are not scale invariant (example is Harris Corner & Edge detector)
	* Thus SIFT aims to provide scale invariant keypoint detection

* Goals
	* Extracting distinct invariant features
		* to correctly match against a large database of features from many images
	* Invariance to image scaling and rotation
	* Robustness to
		* distortion
		* orientation
		* noise

* Advantages
	* Provides local features (computation on different patches of the image instead of Global features which generalizes the whole image)
	* We can get many features even for smaller objects
	* Efficient (can have real-time implementation)

* Extracting Keypoints
	* Scale space peak selection
		* Potential locations for finding features
	* Key point localization
		* Accurately locating the feature key points
	* Orientation Assignment
		* Assigning orientation to the key points
	* Key point descriptor
		* Describing the key point as a high dimensional vector

* Extrema Detection
	* For finding out the edges, we apply Gaussian filter (or Gaussian Smoothing) to the image as it reduces noise and then edges can be easily detected
	* For that, we need to know the value of sigma (width of the mask)
	* Low sigma values give small corner edges while high sigma values fits well for larger corners
		* <p align="center"><img src="https://i.imgur.com/eulfO3m.png"></p>
	* SIFT follows [Scale Space (Witkin, IJCAI 1983)](http://ijcai.org/Proceedings/83-2/Papers/091.pdf) which suggests to apply whole spectrum of scales
	* Now with these different images of different Gaussian blurs (values of sigma), we need to find Laplacian of Gaussian (LoG) which basically acts as a filter to find areas of rapid change (edges) in images.
	* Instead of LoG which is costly, we subtract one image from another and it's called Difference of Gaussians (approximation of LoG) - DoG
		* <p align="center"><img src="https://i.imgur.com/50NX2cP.jpg"></p>
	* For finding the keypoints (interest points), we find the local extrema (where the value of the pixel is max or min)
	* For that, one pixel in an image is compared with its 8 neighbours as well as 9 pixels in next scale and 9 pixels in previous scales
		* <p align="center"><img src="https://i.imgur.com/s7OSfI1.jpg"></p>
	* If it is a local extrema, it is a potential keypoint

* Keypoint Localization
	* Once potential keypoints locations are found, they have to be refined to get more accurate results
	* Taylor series expansion is used to get more accurate location of extrema
	* The intensity of this extrema is compared with the threshold value and the location is rejected if it is less than th
	* Thus many weak and false points are removed in this process

* Orientation assignment
	* Orientation is assigned to each keypoint to achieve invariance to image rotation

* Keypoint descriptor
	* A 16x16 neighbourhood around the keypoint is taken
	* It is divided into 16 subblocks (4x4), and 8 bin orientation histogram is created for each subblock
	* Bin is intensity range representation of the pixels in simpler terms
	* So a total of 128 bin values are available
	* It is represented as a vector to form keypoint descriptor

* Keypoint matching
	* Match the key points against a database of that obtained from training images
	* Find the nearest neighbor i.e. a key point with minimum Euclidean distance
		* Efficient Nearest Neighbor matching
		* Looks at ratio of distance between best and 2nd best match
		* If it is greater than 0.8, they are rejected
		* It eliminaters around 90% of false matches while discards only 5% correct matches (as per the paper)
			
* More details can be found in this Research paper [Distinctive Image Features from Scale-Invariant Keypoints](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf)


<hr/>



1. **BF Matcher (Brute Force)**
	* Brute-Force matcher is simple
	* It takes the descriptor of one feature in first set and is matched with all other features in second set using some distance calculation
	* And the closest one is returned
	* Distance calculations can be:
		* NORM_L1: Manhattan distance or Sum of absolute values
		* NORM_L2: Euclidean distance or Square root of sum of squares
		* NORM_HAMMING: Hamming distance or Number of positions at which corresponding symbols are different


2. **FLANN based Matcher**
	* FLANN stands for Fast Library for Approximate Nearest Neighbors
	* It contains a collection of algorithms optimized for fast nearest neighbor search in large datasets and for high dimensional features
	* It works more faster than BFMatcher for large datasets
