import unittest
from sapyautomation.core.images.split import split_by_regions, \
    images_to_string, east_text_detection, improving_text_recognition, \
    click_middle_roi


class TestImagesHandling(unittest.TestCase):

    def setUp(self):
        """
        Initialize method creates variables for image handling
        """
        self.image = "../../sapyautomation/core/resources/error.PNG"
        self.image_one = "../../sapyautomation/core/resources/Capture.PNG"
        self.text = "../../sapyautomation/core/resources/big.txt"

    def test_split_ny_regions(self):
        """
        Test to raise an exception after receiving an non
        image file in the split by regions method
        """
        self.assertRaises(Exception, split_by_regions, 33, "Hi")

    def test_split_locate_a_valid_image(self):
        """
        Test to execute the split by regions method,
        and verify the len of the list
        """
        coordinates = split_by_regions(self.image, 5)
        self.assertTrue(len(coordinates) == 5)

    def test_east_image_detector(self):
        """
        Test to execute the split by regions (EAST) method,
        and verify the len of the list
        """
        coordinates = east_text_detection(self.image)
        self.assertTrue(len(coordinates) == 8)

    def test_east_image_validator(self):
        """
        Test to raise an exception after receiving an non
        image file in the split by regions method (EAST)
        """
        self.assertRaises(Exception, east_text_detection,
                          self.text)

    def test_image_to_string(self):
        """
        Test to execute the image to string method,
        and verify the len of the text list.
        """
        texts = images_to_string(self.image, [(0, 103, 0,
                                               997),
                                              (103, 206,
                                               0,
                                               997), (
                                                  206,
                                                  309,
                                                  0,
                                                  997),
                                              (309, 412,
                                               0, 997),
                                              (
                                                  412,
                                                  515,
                                                  0,
                                                  997)])
        self.assertTrue(len(texts) == 5)

    def test_image_to_string_validator(self):
        """
        Test to raise an exception after receiving an
        image file in the image to string method

        """
        self.assertRaises(Exception, images_to_string, self.text, 0)

    def test_click_roi_validator(self):
        """
        Test to execute the click middle roi method,
        and getting the 2 len coordinates

        """
        locate = click_middle_roi(self.image_one)
        self.assertTrue(len(locate) == 2)

    def test_click_roi_image(self):
        """
        Test to raise an exception after receiving an non image file
        in click middle roi method method

        """
        self.assertRaises(Exception, click_middle_roi, self.text)

    def test_similarity_done(self):
        """
        Test to execute the improving text recognition
        to compare a 2 strings similarity

        """
        similarity = improving_text_recognition("Hola", "Hola")
        self.assertTrue(similarity == 1)

    def test_similarity_error(self):
        """
        Test to raise an exception after receiving
        an int instead of 2 strings.

        """
        self.assertRaises(Exception, improving_text_recognition, 33, "Hola")


if __name__ == "__main__":
    unittest.main()
