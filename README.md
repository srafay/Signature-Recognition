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

	Different approaches to choosing the test locations (n = 128 bits)
	![Test Locations BRIEF](http://url/to/img.png)