import os
import numpy
import cv2

ima = cv2.imread("window.jpg")


def open_image(path):
    """Open image by path."""
    if validate_path(path):
        img = cv2.imread(path)
        if validate_image(img):
            return img
    return None


def rotate(image, degree):
    """Rotate image N degrees."""
    validate_image(image)
    if -360 < degree < 360:
        return cv2.rotate(image, degree)
    raise ValueError("Degree must be a number between -360 and 360")


def resize(image, scale=1, height=None, width=None):
    """Resize image to specific size."""
    validate_image(image)
    if width is None and height is None:
        return cv2.resize(image, None, fx=scale, fy=scale)
    width = abs(width)
    height = abs(height)
    try:
        return cv2.resize(image, (height, width))
    except TypeError:
        raise TypeError("Height and Width must be integers")


def get_size(image):
    """Return image height and width"""
    validate_image(image)
    return image.shape[:2]


def crop(image, window):
    """Crop an image by window.

    window: 4 values in a tuple (xStart, yStart, xEnd, yEnd)
    """
    validate_image(image)

    try:
        if window[0] < window[2] or window[1] < window[3]:
            return image[window[0]:window[2], window[1]:window[3]]
        raise ValueError("Ending values must be greater than the start ones")
    except IndexError:
        raise IndexError(
            "window must be a 4 value tuple (xStart, yStart, xEnd, yEnd)")


def mirror_vertically(image):
    """Mirror the image vertically."""
    validate_image(image)
    return cv2.flip(image, 0)


def mirror_horizontally(image):
    """Mirror the image horizontally."""
    validate_image(image)
    return cv2.flip(image, +1)


def showing(image):
    """Show the image in a window"""
    validate_image(image)
    cv2.imshow("Image", image)
    cv2.waitKey(0)


def save(image, name):
    """Save image on file."""
    validate_image(image)
    if not os.path.exists(name):
        cv2.imwrite(name, image)
    else:
        raise FileExistsError("There is another file with the same name")


def create_window(image, window, name):
    """Create image from point(s) and save.

    window: 4 values in a tuple (xStart, yStart, xEnd, yEnd)
    name: filename of new image
    """
    validate_image(image)
    save(crop(image, window), name)


def validate_path(path):
    """Validate if the path exists"""
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")
    return True


def validate_image(image):
    """Validate if the read file is an image"""
    if isinstance(image, numpy.ndarray):
        return True
    raise Exception("File not supported")
