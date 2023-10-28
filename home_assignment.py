import numpy as np
import pandas as pd
import os
from datetime import datetime

import json
from PIL import Image, ImageDraw
import csv



class ImageAndDataProcess:
    # constructor
    def __init__(self, json_path, image_path, csv_path, another_json, hotels_csv_path):
        self.json_path = json_path  # the path for the first created json file
        self.image_path = image_path
        self.csv_path = csv_path  # the csv path for the normalized_coordinates
        self.another_json = another_json
        self.hotels_csv_path = hotels_csv_path  # the original hotel_data.csv

    # add new columns
    def hotel_data_add_columns(self):
        hotels_data = pd.read_csv(self.hotels_csv_path)

        # convert the type of the 'Snapshot Date' and 'Checkin Date' to datetime
        hotels_data['Snapshot Date'] = pd.to_datetime(hotels_data['Snapshot Date'])
        hotels_data['Checkin Date'] = pd.to_datetime(hotels_data['Checkin Date'])
        hotels_data['DayDiff'] = (hotels_data['Checkin Date'] - hotels_data['Snapshot Date']).dt.days

        hotels_data['WeekDay'] = hotels_data['Checkin Date'].dt.day_name()
        # the discount
        hotels_data['DiscountDiff'] = hotels_data['Original Price'] - hotels_data['Discount Price']
        # the discount percentage
        hotels_data['DiscountPerc'] = (hotels_data['DiscountDiff'] / hotels_data['Original Price']) * 100

        #convert back to string
        hotels_data['Snapshot Date'] = hotels_data['Snapshot Date'].dt.strftime('%m/%d/%Y 0:00')
        hotels_data['Checkin Date'] = hotels_data['Checkin Date'].dt.strftime('%m/%d/%Y 0:00')

        # convert to csv
        hotels_data.to_csv('Hotels_data_Changed.csv', index=False)


    # create json file using the manually calculated dimensions
    def create_json(self):
        data = {
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

        # save as json file
        with open(self.json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def normalize_coordinates(self, json_path, csv_path, image_path, another_json):
        # open json
        with open(json_path, 'r')as file:
            json_code = json.load(file)

        # load image using image_path

        with Image.open(image_path) as image:

            # width and height of the image
            width = image.size[0]
            height = image.size[1]

        fieldnames = ['label', 'x_min', 'y_min', 'x_max', 'y_max']

        # create new json
        data = {
            "image_name": "0000001847912.jpg",
            "annotations": []}

        # open csv using csv_path
        with open(csv_path, 'w', newline="") as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=fieldnames)
            writer.writeheader()
            # writer.writerow(row)

            # label and coordinates of each object
            for objectt in json_code['annotations']:
                label = objectt['label']
                x_min = objectt['coordinates']['x_min']
                y_min = objectt['coordinates']['y_min']
                x_max = objectt['coordinates']['x_max']
                y_max = objectt['coordinates']['y_max']

                # calculate new coordinates of each object
                new_x_min = x_min / width
                new_y_min = y_min / height
                new_x_max = x_max / width
                new_y_max = y_max / height

                # new json data(2.2)
                data['annotations'].append({'label': label,
                                            'coordinates': {'x_min': x_min, 'y_min': y_min, 'width': x_max - x_min,
                                                            'height': y_max - y_min}})

                # csv data(2.1)
                new_dict = {'label': label, 'x_min': new_x_min, 'y_min': new_y_min, 'x_max': new_x_max,
                            'y_max': new_y_max}

                # add the row to csv
                writer.writerow(new_dict)

        # open json file and write the data
        with open(another_json, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    # visualization for csv file
    def create_visualization_csv(self):
        with Image.open(image_path) as image:
            create_draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]


        # open csv file using csv_path and use DictReader for reading from it
        with open(csv_path, 'r') as file_csv:
            r = csv.DictReader(file_csv)
            for row in r:
                x_min = float(row['x_min']) * width
                y_min = float(row['y_min']) * height
                x_max = float(row['x_max']) * width
                y_max = float(row['y_max']) * height
                create_draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=5)

        image.show()

    # visualization for json file
    def create_visualization_json(self):
        with Image.open(image_path) as image:

            create_draw = ImageDraw.Draw(image)

        # open json file using another_json
        with open(another_json, 'r') as file_json:
            read = json.load(file_json)
            for objectt in read["annotations"]:
                x_min = objectt['coordinates']['x_min']
                y_min = objectt['coordinates']['y_min']
                width = objectt['coordinates']['width']
                height = objectt['coordinates']['height']
                create_draw.rectangle([x_min, y_min, x_min + width, y_min + height], outline="red", width=5)

        image.show()


if __name__ == '__main__':
    """
    1.
    1st part of the assignment
    """

    # the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #relative paths from the script directory
    hotels_csv_path = os.path.join(current_directory, "hotels_data.csv")
    json_path = os.path.join(current_directory, "dimensions.json")
    image_path = os.path.join(current_directory, "0000001847912.jpg")
    csv_path = os.path.join(current_directory, "output_csv.csv")
    another_json = os.path.join(current_directory, "output_json.json")

    new_ImageAndDataProcess = ImageAndDataProcess(json_path, image_path, csv_path, another_json, hotels_csv_path)
    new_ImageAndDataProcess.hotel_data_add_columns()

    """
    2.
    2nd part of the assignment
    """
    # the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # relative paths from the script directory
    hotels_csv_path = os.path.join(current_directory, "hotels_data.csv")
    json_path = os.path.join(current_directory, "dimensions.json")
    image_path = os.path.join(current_directory, "0000001847912.jpg")
    csv_path = os.path.join(current_directory, "output_csv.csv")
    another_json = os.path.join(current_directory, "output_json.json")

    new_ImageAndDataProcess = ImageAndDataProcess(json_path, image_path, csv_path, another_json, hotels_csv_path)
    new_ImageAndDataProcess.create_json()

    """
    3.
    3rd part of the assignment
    """
    # the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # relative paths from the script directory
    hotels_csv_path = os.path.join(current_directory, "hotels_data.csv")
    json_path = os.path.join(current_directory, "dimensions.json")
    image_path = os.path.join(current_directory, "0000001847912.jpg")
    csv_path = os.path.join(current_directory, "output_csv.csv")
    another_json = os.path.join(current_directory, "output_json.json")

    new_ImageAndDataProcess = ImageAndDataProcess(json_path, image_path, csv_path, another_json, hotels_csv_path)
    new_ImageAndDataProcess.normalize_coordinates(json_path,csv_path, image_path, another_json)
    new_ImageAndDataProcess.create_visualization_csv()
    new_ImageAndDataProcess.create_visualization_json()