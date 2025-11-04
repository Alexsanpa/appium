import os
import unittest
import cv2
import numpy as np
from PIL import Image
from sapyautomation.core import image as im


class TestImageCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.image_name = "test_image.jpg"
        cls.image = Image.new('RGB', size=(200, 200))
        cls.image.save(cls.image_name)
        cls.ima = im.open_image(cls.image_name)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.image_name)

    def test_validate_path(self):
        self.assertTrue(im.validate_path(self.image_name))
        self.assertRaises(Exception, im.validate_path, "fakePath")

    def test_validate_image(self):
        self.assertTrue(im.validate_image(self.ima))
        self.assertRaises(Exception, im.validate_image, "test_image.py")

    def test_open_image(self):
        self.assertTrue(np.array_equal(im.open_image(self.image_name),
                                       cv2.imread(self.image_name)))
        self.assertRaises(FileNotFoundError, im.open_image, "fakePath")

    def test_rotate(self):
        degree = 45
        self.assertTrue(np.array_equal(im.rotate(self.ima, degree),
                                       cv2.rotate(self.ima, degree)))
        self.assertRaises(Exception, im.rotate, [degree], degree)
        self.assertRaises(ValueError, im.rotate, self.ima, degree * 1000)

    def test_resize(self):
        self.assertEqual(im.resize(self.ima, 2).shape[:2],
                         (self.ima.shape[0] * 2, self.ima.shape[1] * 2))
        self.assertEqual(im.resize(self.ima, None, 50, 50).shape[:2], (50, 50))
        self.assertEqual(im.resize(self.ima, None, -50, -50).shape[:2],
                         (50, 50))
        self.assertRaises(TypeError, im.resize, self.ima, None)
        self.assertRaises(TypeError, im.resize, self.ima, None, 100.5, 1 / 2)

    def test_get_size(self):
        self.assertEqual(im.get_size(self.ima), (self.ima.shape[0],
                                                 self.ima.shape[1]))

    def test_crop(self):
        self.assertEqual((im.crop(self.ima, (0, 0, 50, 50))).shape[:2],
                         (50, 50))
        self.assertRaises(IndexError, im.crop, self.ima, (0, 0, 50))
        self.assertRaises(ValueError, im.crop, self.ima, (50, 50, 0, 0))

    def test_mirror_vertically(self):
        self.assertTrue(np.array_equal(im.mirror_vertically(self.ima),
                                       np.flipud(self.ima)))

    def test_mirror_horizontally(self):
        self.assertTrue(np.array_equal(im.mirror_horizontally(self.ima),
                                       np.fliplr(self.ima)))

    def test_save(self):
        name = "save.jpg"
        im.save(self.ima, name)
        self.assertTrue(os.path.exists(name))
        self.assertRaises(FileExistsError, im.save, self.ima, name)
        os.remove(name)

    def test_create_window(self):
        im.create_window(self.ima, (0, 0, 50, 50), "window.jpg")
        self.assertTrue(os.path.exists("window.jpg"))
        os.remove("window.jpg")


if __name__ == '__main__':
    unittest.main()
