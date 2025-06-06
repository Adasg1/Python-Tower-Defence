import csv

import pygame
import os

from src.utils.paths import get_path


class AssetManager:
    _images = {}
    _csv_data = {}
    _fonts = {}

    @classmethod
    def load_assets(cls, base_folder="assets"):
        cls.load_all_images_from(base_folder)
        cls.load_all_csv_from(base_folder)

    @classmethod
    def load_all_images_from(cls, base_folder):
        SCALE_MAP = {
            "images/monsters/basic": (60, 60),
            "images/monsters/flying": (70, 70),
            "images/monsters/healer": (64, 64),
            "images/monsters/quick": (50, 50),
            "images/monsters/tank": (110, 110),
            "images/monsters/root": (140, 140),
            "images/monsters/treeboss": (150, 150),
            "images/monsters/knightboss": (150, 150),
            "images/monsters/golemboss": (150, 150),
            "images/monsters/yettiboss": (150, 150),
            "images/tower_options": (200, 200),
        }

        base_folder = get_path(base_folder)
        for root, dirs, files in os.walk(base_folder):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_folder)
                    key = relative_path.replace("\\", "/").rsplit(".", 1)[0]

                    folder_key = os.path.dirname(relative_path).replace("\\", "/")
                    scale = None
                    for folder, size in SCALE_MAP.items():
                        if folder_key.startswith(folder):
                            scale = size
                            break

                    image = pygame.image.load(full_path).convert_alpha()
                    if scale:
                        image = pygame.transform.smoothscale(image, scale)
                    else:
                        scale = image.get_size()
                        m = 2/3
                        image = pygame.transform.smoothscale(image, (int(scale[0]*m), int(scale[1]*m)))

                    cls._images[key] = image
                    #print(f"Załadowano obraz: {key}")

    @classmethod
    def get_image(cls, key, scale=None):
        if key not in cls._images:
            return None
        image = cls._images[key]
        if scale:
            image = pygame.transform.smoothscale(image, scale)

        return image

    @classmethod
    def load_all_csv_from(cls, base_folder):
        import os
        base_folder = get_path(base_folder)
        for root, _, files in os.walk(base_folder):
            for file in files:
                if file.lower().endswith(".csv"):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_folder).replace("\\", "/")
                    key = relative_path.rsplit(".", 1)[0]
                    with open(full_path, newline='', encoding="utf-8") as csvfile:
                        reader = csv.DictReader(csvfile)
                        data = [(int(row["x"]), int(row["y"])) for row in reader]  # Współrzędne w formacie (x, y)
                        cls._csv_data[key] = data
                        #print(f"Załadowano CSV: {key}")

    @classmethod
    def get_csv(cls, key):
        #if key not in cls._csv_data:
            #print(f"Nie znaleziono pliku '{key}'")
        return cls._csv_data.get(key)

    @classmethod
    def get_font(cls, name, size):
        key = (name, size)
        if key not in cls._fonts:
            cls._fonts[key] = pygame.font.Font(get_path(f"assets/fonts/{name}.ttf"), size)
        return cls._fonts[key]



