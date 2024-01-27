#%%
import cv2
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt
import re


# %%
im_file ="./images/actual.png"

im = Image.open(im_file)
im.show()




# %%
image_file = "./images/actual.png"
img = cv2.imread(image_file)



# %%
def display(im_path):
    try:
        dpi = 80
        im_data = plt.imread(im_path)

        height, width  = im_data.shape[:2]
        
        # What size does the figure need to be in inches to fit the image?
        figsize = width / float(dpi), height / float(dpi)

        # Create a figure of the right size with one axes that takes up the full figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])

        # Hide spines, ticks, etc.
        ax.axis('off')

        # Display the image.
        ax.imshow(im_data, cmap='gray')

        plt.show()
    except SyntaxError:
        print(f"The file {im_path} is not a valid PNG file.")


# %%
inverted_image = cv2.bitwise_not(img)
cv2.imwrite("./temp/inverted.png", inverted_image)



# %%
inverted="./temp/inverted.png"





# %%
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(img)
cv2.imwrite("./temp/gray.png", gray_image)

# %%
thresh, im_bw = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("./temp/bw.png", im_bw) 
 #Play around the values for a better result this is for making it black and white




# %%
def noise_removal(image):
    import numpy as np
    kernal = np.ones((1, 1), np.uint8)
    image =cv2.dilate(image, kernal, iterations=1)
    kernal = np.ones((1, 1), np.uint8)
    image =cv2.erode(image, kernal, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernal)
    image = cv2.medianBlur(image, 3)
    return image

no_noise = noise_removal(im_bw)
cv2.imwrite("./temp/no_noise.png", no_noise)


# %%
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernal, iterations=1)
    image= cv2.bitwise_not(image)
    return image

eroded = thin_font(no_noise)
cv2.imwrite("./temp/eroded.png", eroded)




# %%
def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernal, iterations=1)
    image= cv2.bitwise_not(image)
    return image

eroded = thin_font(no_noise)
cv2.imwrite("./temp/dilated.png", eroded)
# %%


# %%
#cleaning rotated text

new = cv2.imread("./images/actual_rotated.png")


# %%

import numpy as np

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


# %%
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)



# %%
fixed = deskew(new)
cv2.imwrite("./temp/rotated_fixed.png", fixed)


# %%
display("./images/actual.png")
def remove_actual(image):
    contours, heirarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntSorted[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = image[y:y+h,x:x+w]
    return crop

no_actuals = remove_actual(no_noise)
cv2.imwrite("./temp/no_actuals.png", no_actuals)




# %%
img_file = "./images/actual.png"
no_noise ="./temp/no_actuals.png"
img = Image.open(no_noise)
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)
# %%