from csv import reader
from os import walk


def import_csv_layout(path):
    with open(path) as level_map:
        level_map = reader(level_map, delimiter=',')
        layout = []
        for row in level_map:
            layout.append(row)

        return layout


def import_folder(path):
    for _, __, img_files in walk(path):  # returns current_folder, sub_folders and all the files inside a folder
        for image in img_files:
            print(image)
