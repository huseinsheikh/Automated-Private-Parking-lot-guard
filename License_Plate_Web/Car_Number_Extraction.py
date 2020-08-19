import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


def get_number(image_path):
    # Read the image file
    image = cv2.imread(image_path)

    # Resize the image - change width to 500
    image = imutils.resize(image, width=300)

    # RGB to Gray scale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Find Edges of the grayscale image
    edged = cv2.Canny(gray, 170, 200)

    # Find contours based on Edges
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None  # we currently have no Number plate contour

    # loop over our contours to find the best possible approximate contour of number plate
    idx = 7
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  # Select the contour with 4 corners
            NumberPlateCnt = approx  # This is our approx Number Plate Contour

            # Crop those contours and store it in Cropped Images folder
            x, y, w, h = cv2.boundingRect(c)  # This will find out co-ord for plate
            new_img = gray[y:(y + h), x:(x + w)]  # Create new image
            cv2.imwrite('Cropped-Images-Text.png', new_img)  # Store new image
            idx += 1

            break

    Cropped_img_loc = 'Cropped-Images-Text.png'

    # Use tesseract to covert image into string
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng', config='--psm 10 --oem 3 -c '
                                                                           'tessedit_char_whitelist=0123456789-')

    # To clean output of non digits
    text = text.strip(' ')
    split_text = text.split('-')
    if len(split_text) == 2:
        split_text[0] = split_text[0][-5:]
        split_text[1] = split_text[1][:2]
        text = ''.join(split_text)
    elif len(split_text) >= 3:
        split_text[1] = split_text[1][-4:]
        split_text[-1] = split_text[-1][:2]
        text = ''.join(split_text)
    return text
