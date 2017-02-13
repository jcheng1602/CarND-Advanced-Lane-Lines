import numpy as np
import cv2
import pickle
import glob


# Read in the saved matrix and distortion coefficients
dist_pickle = pickle.load(open('./camera_cal/calibration_pickle.p', 'rb'))
mtx = dist_pickle['mtx']
dist = dist_pickle['dist']


def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
    """
    Returns an array of the same size as the input image of ones where gradients
    were in the threshold range, and zeros everywhere else.
    :param img: input image in rgb format.
    :param orient: orientation in which to take the gradient (x or y).
    :param sobel_kernel: size of the sobel kernel to apply (must be odd number >= 3).
    :param thresh: threshold (0 to 255) for determining which gradients to include when creating binary output.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Take the absolute value of the derivative in the given x or y orientation
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    # Scale to 8-bit (0-255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a mask of 1's where the scaled gradient magnitude is within the given thresholds
    grad_binary = np.zeros_like(scaled_sobel)
    grad_binary[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
    # Return binary output image
    return grad_binary


def mag_thresh(img, sobel_kernel=3, thresh=(0, 255)):
    """
    Returns an array of the same size as the input image of ones where gradients
    were in the threshold range, and zeros everywhere else.
    :param img: input image in rgb format.
    :param sobel_kernel: size of the sobel kernel to apply (must be odd number >= 3).
    :param thresh: threshold (0 to 255) for determining which gradients to include when creating binary output.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the magnitude of the gradient
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # Scale to 8-bit (0-255) then convert to type = np.uint8
    scaled_gradmag = np.uint8(255*gradmag/np.max(gradmag))
    # Create a mask of 1's where the scaled gradient magnitude is within the given thresholds
    mag_binary = np.zeros_like(scaled_gradmag)
    mag_binary[(scaled_gradmag >= thresh[0]) & (scaled_gradmag <= thresh[1])] = 1
    # Return binary output image
    return mag_binary


def dir_thresh(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    """
    Returns an array of the same size as the input image of ones where gradients
    were in the threshold range, and zeros everywhere else.
    :param img: input image in rgb format.
    :param sobel_kernel: size of the sobel kernel to apply (must be odd number >= 3).
    :param thresh: threshold (0 to pi/2) for determining which gradients to include when creating binary output.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Use np.arctan2(abs_sobely, abs_sobelx) to calculate direction of gradient
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    # Create a mask of 1's where the scaled gradient magnitude is within the given thresholds
    dir_binary = np.zeros_like(absgraddir)
    dir_binary[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1
    # Return binary output image
    return dir_binary


def color_thresh(img, s_thresh=(0, 255)):
    """
    Returns binary image of the same size as the input image of ones where gradients
    were in the threshold range, and zeros everywhere else.
    :param img: input image in rgb format.
    :param s_thresh: threshold (0 to 255) for determining which pixels from s_channel to include when creating binary output.
    """
    # Convert to HLS color space
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    # Apply a threshold to the S channel
    s_channel = hls[:,:,2]
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel > s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    # Return binary output image
    return s_binary



