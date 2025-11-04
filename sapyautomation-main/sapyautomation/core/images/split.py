
from difflib import SequenceMatcher
import time
import numpy as np
import cv2
import pyautogui
from PIL import Image
import pytesseract
from imutils.object_detection import non_max_suppression


pytesseract.pytesseract.tesseract_cmd = r"C:\Program " \
                                        r"Files\Tesseract-OCR\tesseract.exe "


def split_by_regions(image: str, pieces: int = 1) -> list:
    """This method split an image in specific blocks called pieces

    To be specific, in to horizontal blocks.Receiving the Path of an image and
    the pieces to be splitted.

    Args:
        pieces (int): The pieces to be exactly divided the image.
        image (str): Path for image.

    Returns:
        lists: List of coordinates, horizontal pieces.
    """
    try:
        Image.open(image)
        pic = cv2.imread(image)
        high, anchor = pic.shape[:2]
        fac_high = round(high / pieces)
        coordinates = list()
        for i in range(0, pieces):
            coordinates.append(
                (fac_high * i, fac_high * (i + 1), 0, anchor))
        return coordinates

    except Exception:
        raise Exception('Error, this is not an Image')


def images_to_string(image: str, coordinates: list) -> list:
    """Images to string, scanning specific blocks and parsing to text

    This method recieve the processed image and the coordinates, in order to
    inspect the coordinates to find text, (Working with split_by_regions and
    east_text_detection.

        Args:
         coordinates (list): The coordinates coming from the split of images
                                methods.
         image (str): Path for image.

        Returns:
            list: An array with the text detected.
        """
    try:
        Image.open(image)
        texts = []
        image = cv2.imread(image)
        for xy in coordinates:
            img = image[xy[0]:xy[1], xy[2]:xy[3]]

            texts.append((pytesseract.image_to_string(img)).replace("\n", ""))
        return texts
    except cv2.error:
        raise TypeError('Error, this is not an Image')


def east_text_detection(image: str) -> tuple:
    """East library regions of text detection

       This method split an image in particular blocks using neuronal networks
       library called "East" giving coordinates of an specific and probably
       text area.

        Args:
            image (str): Path for image.

        Returns:
            tuple: List of coordinates of the specific text "boxes".
        """
    try:
        Image.open(image)
        coordinates = list()
        imag = cv2.imread(image)
        orig = imag.copy()
        (H, W) = imag.shape[:2]
        (newW, newH) = (320, 320)
        rW = W / float(newW)
        rH = H / float(newH)
        imag = cv2.resize(imag, (newW, newH))
        (H, W) = imag.shape[:2]

        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        # print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet(  # pylint: disable=E1101,I0023
            "C:/Users/gecastanon/Desktop/opencv-text-detection"
            "/frozen_east_text_detection.pb")
        # pylint: disable=E1101,I0023
        blob = cv2.dnn.blobFromImage(imag, 1.0, (W, H),
                                     (123.68, 116.78, 103.94), swapRB=True,
                                     crop=False)
        start = time.time()
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        end = time.time()
        print("[INFO] text detection took {:.6f} seconds".format(end - start))

        (num_rows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(0, num_rows):
            scores_data = scores[0, 0, y]
            x_data_0 = geometry[0, 0, y]
            x_data_1 = geometry[0, 1, y]
            x_data_2 = geometry[0, 2, y]
            x_data_3 = geometry[0, 3, y]
            angles_data = geometry[0, 4, y]

            for x in range(0, numCols):
                if scores_data[x] < 0.5:
                    continue

                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                angle = angles_data[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = x_data_0[x] + x_data_2[x]
                w = x_data_1[x] + x_data_3[x]

                endX = int(offsetX + (cos * x_data_1[x]) + (sin * x_data_2[x]))
                endY = int(offsetY - (sin * x_data_1[x]) + (cos * x_data_2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scores_data[x])

        boxes = non_max_suppression(np.array(rects), probs=confidences)
        for (startX, startY, endX, endY) in boxes:
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            coordinates.append((startY, endY, startX, endX))
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        cv2.waitKey(0)
        return coordinates

    except cv2.error:
        raise TypeError('Error, this is not an Image')


def improving_text_recognition(string_a: str, string_b: str) -> float:
    """Compare two strings to view the text similarity

    This method compare the confidentiality of 2 strings,How much a
    string of text looks like another, to be exact.

        Args:
            string_a (str): The second string to be compared.
            string_b (str): The first string to be compared.

        Returns:
            float: The result of the confidentiality in scale (0-1) .
    """
    try:

        string_a.isalpha()
        string_b.isalpha()
        similarity = SequenceMatcher(None, string_a, string_b).ratio()
        return similarity
    except TypeError:
        raise TypeError('Error, Check if you recieve strings')


def click_middle_roi(image: str) -> tuple:
    """Click in the middle of an image received

    This method receive an image to find it at the screen, locate his
    position in the screen, and return the coordinates.

            Args:
                image (str): Path for image.

            Returns:
                tuple: The position of the image-middle in the screen (x,y) .
            """
    try:
        Image.open(image)
        locate = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        print(locate)
        pyautogui.moveTo(locate)
        pyautogui.click(locate)
        return locate
    except cv2.error:
        raise TypeError('Error, this is not an Image')
