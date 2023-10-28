import unittest
from home_assignment import ImageAndDataProcess
import os
import json
import pandas as pd

class TestPlaceholder(unittest.TestCase):

    def setUp(self):
        # the directory of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # relative paths from the script directory
        hotels_csv_path = os.path.join(current_directory, "hotels_data.csv")
        json_path = os.path.join(current_directory, "dimensions.json")
        image_path = os.path.join(current_directory, "0000001847912.jpg")
        csv_path = os.path.join(current_directory, "output_csv.csv")
        another_json = os.path.join(current_directory, "output_json.json")

        self.place_holder = ImageAndDataProcess(json_path, image_path, csv_path, another_json, hotels_csv_path)


    def test_hotel_add_columns(self):
        #check if the new csv file was created
        self.place_holder.hotel_data_add_columns()
        self.assertTrue(os.path.exists("Hotels_data_Changed.csv"))

    def test_hotel_add_columns2(self):
        #check if new columns exists in new csv file
        self.place_holder.hotel_data_add_columns()
        data=pd.read_csv("Hotels_data_Changed.csv")
        self.assertTrue("DayDiff" in data)
        self.assertTrue("WeekDay" in data)
        self.assertTrue("DiscountDiff" in data)
        self.assertTrue("DiscountPerc" in data)



    def test_create_json(self):
        #check if the first json file was created
        self.place_holder.create_json()
        self.assertTrue(os.path.exists(self.place_holder.json_path))


    def test_create_json_2(self):
        #check if the json file information is correct
        self.place_holder.create_json()
        with open(self.place_holder.json_path, 'r')as file:
            data = json.load(file)

        data_expected = {
            "image_name": "000000184792.jpg",
            "annotations": [
                {
                    "label": "jug",
                    "coordinates": {
                        "x_min": 148,
                        "y_min": 87,
                        "x_max": 360,
                        "y_max": 320
                    }
                },
                {
                    "label": "right_orange",
                    "coordinates": {
                        "x_min": 430,
                        "y_min": 240,
                        "x_max": 530,
                        "y_max": 330
                    }
                }
            ]
        }
        self.assertEqual(data,data_expected)

    def test_normalize_coordinates(self):
        #check if new csv file and another json file were created
        self.place_holder.normalize_coordinates(self.place_holder.json_path,self.place_holder.csv_path, self.place_holder.image_path, self.place_holder.another_json)
        self.assertTrue(os.path.exists(self.place_holder.csv_path))
        self.assertTrue(os.path.exists(self.place_holder.another_json))


    def test_normalize_coordinates2(self):
        #check if the information in new json file is correct
        self.place_holder.normalize_coordinates(self.place_holder.json_path, self.place_holder.csv_path,
                                                self.place_holder.image_path, self.place_holder.another_json)

        with open(self.place_holder.another_json, 'r')as file:
            data = json.load(file)

        data_expected = {
          "image_name": "0000001847912.jpg",
          "annotations": [
            {
              "label": "jug",
              "coordinates": {
                "x_min": 148,
                "y_min": 87,
                "width": 212,
                "height": 233
              }
            },
            {
              "label": "right_orange",
              "coordinates": {
                "x_min": 430,
                "y_min": 240,
                "width": 100,
                "height": 90
              }
            }
          ]
        }

        self.assertEqual(data, data_expected)

    def test_normalize_coordinates3(self):
        #check if the information in csv file is correct
        self.place_holder.normalize_coordinates(self.place_holder.json_path, self.place_holder.csv_path,
                                                self.place_holder.image_path, self.place_holder.another_json)

        #read created csv
        data=pd.read_csv(self.place_holder.csv_path)

        #calculate expected values

        x_min_expected_jug=148/640
        y_min_expected_jug =87/500
        x_max_expected_jug =360/640
        y_max_expected_jug =320/500

        x_min_expected_orange=430/640
        y_min_expected_orange =240/500
        x_max_expected_orange =530/640
        y_max_expected_orange =330/500

        #create DataFrame

        df={
            'label':['jug','right_orange'],
            'x_min':[x_min_expected_jug,x_min_expected_orange],
            'y_min':[y_min_expected_jug,y_min_expected_orange],
            'x_max':[x_max_expected_jug,x_max_expected_orange],
            'y_max':[y_max_expected_jug,y_max_expected_orange]
        }
        data_expected=pd.DataFrame(df)

        #check if equalls
        self.assertTrue(data.equals(data_expected))

if __name__ == '__main__':
    unittest.main()