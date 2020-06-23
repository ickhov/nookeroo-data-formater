import json
from urllib.error import HTTPError
import urllib.request
import os
import re
import unidecode

class dir: # globals
    cwd = os.getcwd() + "/"
    image =  cwd + "images/"
    json = cwd + "data/"

    # clothing
    clothing = "clothing/"
    clothing_accessories = ["accessories/", "accessories.json"]
    clothing_bags = ["bags/", "bags.json"]
    clothing_bottoms = ["bottoms/", "bottoms.json"]
    clothing_dresses = ["dresses/", "dresses.json"]
    clothing_hats = ["hats/", "hats.json"]
    clothing_shoes = ["shoes/", "shoes.json"]
    clothing_socks = ["socks/", "socks.json"]
    clothing_tops = ["tops/", "tops.json"]
    clothing_umbrellas = ["umbrellas/", "umbrellas.json"]

    # furniture
    furniture = "furniture/"
    furniture_floorings = ["floorings/", "floorings.json"]
    furniture_housewares = ["housewares/", "housewares.json"]
    furniture_miscellaneous = ["miscellaneous/", "miscellaneous.json"]
    furniture_rugs = ["rugs/", "rugs.json"]
    furniture_wallmounted = ["wallmounted/", "wall_mounted.json"]
    furniture_wallpapers = ["wallpapers/", "wallpapers.json"]

    # recipe
    recipe = "recipe/"
    recipe_clothing = ["clothing/", "equipments.json"]
    recipe_housewares = ["housewares/", "housewares.json"]
    recipe_miscellaneous = ["miscellaneous/", "miscellaneous.json"]
    recipe_others = ["others/", "others.json"]
    recipe_tools = ["tools/", "tools.json"]
    recipe_wallmounted = ["wallmounted/", "wall_mounteds.json"]
    recipe_decorations = ["decorations/", "wallpaper_rugs_floorings.json"]

def generateClothingData():

    images_dir = dir.image + dir.clothing
    json_dir = dir.json + dir.clothing

    # create a list of directories to loop through
    dirs = [
        dir.clothing_accessories,
        dir.clothing_bags,
        dir.clothing_bottoms,
        dir.clothing_dresses,
        dir.clothing_hats,
        dir.clothing_shoes,
        dir.clothing_socks,
        dir.clothing_tops,
        dir.clothing_umbrellas
    ]

    for d in dirs:
        category_image_dir = images_dir + d[0]
        category = {}

        with open(dir.cwd + dir.clothing + d[1]) as f:
            data = json.load(f)

        for k, value in data.items():
            # get the cross reference data for better accuracy
            key = unidecode.unidecode(k)
            alter_key = key.lower().replace("-", "_").replace(" ", "_")
            cross_reference_key = re.sub(r'[^\w]', '', alter_key).replace("_", "-").replace("--", "-")
            
            error = False
            try:
                with open(dir.cwd + "items/" + cross_reference_key + ".json") as f:
                    cross_reference = json.load(f)
            except FileNotFoundError as err:
                error = True

            cross_reference_data = cross_reference["games"]["nh"] if not error else {}

            new_key = key.lower().replace(" ", "-")

            image_links = value["variationImageLinks"] if "variationImageLinks" in value else None

            buy_price = cross_reference_data["buyPrices"][0]["value"] if "buyPrices" in cross_reference_data else value["priceBuy"]
            sell_price = cross_reference_data["sellPrice"]["value"] if "sellPrice" in cross_reference_data else value["priceSell"]
            sources = cross_reference_data["sources"] if "sources" in cross_reference_data else value["source"]
            variation_names = []
            variation_images = []
            
            if "variations" in value:
                for index, item in enumerate(value["variations"]):
                    # set image name and dir to save in
                    image_name = new_key + "-" + item.lower().replace(",", "").replace(" ", "-") + ".png"

                    # download images from the web
                    if not os.path.exists(category_image_dir):
                        os.makedirs(category_image_dir)
                    try:
                        urllib.request.urlretrieve(image_links[index], category_image_dir + image_name)
                    except HTTPError as err:
                        print(image_links[index])
                    except IndexError as err:
                        print(new_key)
                        
                    # add the variant name and image name to the list
                    variation_names.append(item)
                    variation_images.append(image_name)

            if len(variation_names) == 0:
                image_name = new_key + ".png"

                # download images from the web
                if not os.path.exists(category_image_dir):
                    os.makedirs(category_image_dir)
                
                try:
                    urllib.request.urlretrieve(value["imageLink"], category_image_dir + image_name)
                except HTTPError as err:
                    print(value["imageLink"])
                except IndexError as err:
                    print(new_key)

                variation_images.append(image_name)

            category[new_key] = {
                "name": {
                    "name-USen": key.lower()
                },
                "sources": sources,
                "buy-price": buy_price,
                "sell-price": sell_price,
                "variant": len(variation_names) > 0,
                "variation_names": variation_names,
                "variation_images": variation_images
            }

        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_dir + d[1], 'w') as json_file:
            json.dump(category, json_file, indent = 4, sort_keys = False)

        print(len(data))

def generateFunitureData():

    images_dir = dir.image + dir.furniture
    json_dir = dir.json + dir.furniture

    # create a list of directories to loop through
    dirs = [
        dir.furniture_rugs,
        dir.furniture_floorings,
        dir.furniture_wallpapers
    ]

    for d in dirs:
        category_image_dir = images_dir + d[0]
        category = {}

        with open(dir.cwd + dir.furniture + d[1]) as f:
            data = json.load(f)

        for k, value in data.items():
            # get the cross reference data for better accuracy
            key = unidecode.unidecode(k)
            alter_key = key.lower().replace("-", "_").replace(" ", "_")
            cross_reference_key = re.sub(r'[^\w]', '', alter_key).replace("_", "-").replace("--", "-")
            
            error = False
            try:
                with open(dir.cwd + "items/" + cross_reference_key + ".json") as f:
                    cross_reference = json.load(f)
            except FileNotFoundError as err:
                error = True

            cross_reference_data = cross_reference["games"]["nh"] if not error else {}

            new_key = key.lower().replace(" ", "-")

            image_link = value["image_url"] or None

            buy_price = cross_reference_data["buyPrices"][0]["value"] if "buyPrices" in cross_reference_data else value["price"]["buy"]
            sell_price = cross_reference_data["sellPrice"]["value"] if "sellPrice" in cross_reference_data else value["price"]["sell"]
            sources = cross_reference_data["sources"] if "sources" in cross_reference_data else value["source"]

            image_name = new_key + ".png"

            # download images from the web
            if not os.path.exists(category_image_dir):
                os.makedirs(category_image_dir)
            
            if image_link:
                try:
                    urllib.request.urlretrieve(image_link, category_image_dir + image_name)
                except HTTPError as err:
                    print(image_link)
                except IndexError as err:
                    print(new_key)

            category[new_key] = {
                "name": {
                    "name-USen": key.lower()
                },
                "sources": sources,
                "buy-price": buy_price,
                "sell-price": sell_price,
                "image-uri": image_name
            }

        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_dir + d[1], 'w') as json_file:
            json.dump(category, json_file, indent = 4, sort_keys = False)

        print(len(data))

def generateRecipeData():

    images_dir = dir.image + dir.recipe
    json_dir = dir.json + dir.recipe

    # create a list of directories to loop through
    dirs = [
        dir.recipe_clothing,
        dir.recipe_housewares,
        dir.recipe_miscellaneous,
        dir.recipe_others,
        dir.recipe_tools,
        dir.recipe_wallmounted,
        dir.recipe_decorations
    ]

    for d in dirs:
        category_image_dir = images_dir + d[0]
        category = {}

        with open(dir.cwd + dir.recipe + d[1]) as f:
            data = json.load(f)

        for k, value in data.items():
            # get the cross reference data for better accuracy
            key = unidecode.unidecode(k)
            alter_key = key.lower().replace("-", "_").replace(" ", "_")
            cross_reference_key = re.sub(r'[^\w]', '', alter_key).replace("_", "-").replace("--", "-")
            
            error = False
            try:
                with open(dir.cwd + "items/" + cross_reference_key + ".json") as f:
                    cross_reference = json.load(f)
            except FileNotFoundError as err:
                error = True

            cross_reference_data = cross_reference["games"]["nh"] if not error else {}

            new_key = key.lower().replace(" ", "-")

            image_link = value["image_url"] or None
            sell_price = cross_reference_data["sellPrice"]["value"] if "sellPrice" in cross_reference_data else value["price"]
            sources = value["obtained_from"]

            image_name = new_key + ".png"

            # download images from the web
            if not os.path.exists(category_image_dir):
                os.makedirs(category_image_dir)
            
            if image_link:
                try:
                    urllib.request.urlretrieve(image_link, category_image_dir + image_name)
                except HTTPError as err:
                    print(image_link)
            else:
                print("No image linnk for " + material_name)

            materials = []

            for m_key, m_value in value["materials"].items():
                material_name = unidecode.unidecode(m_key).lower().replace(" ", "-")
                material_count = m_value["amount"]
                material_image_link = m_value["image_url"] or None
                material_image_name = material_name + ".png"
                material_image_dir = dir.image + "materials/"

                if not os.path.exists(material_image_dir):
                    os.makedirs(material_image_dir)

                if material_image_link:
                    try:
                        urllib.request.urlretrieve(material_image_link, material_image_dir + material_image_name)
                    except HTTPError as err:
                        print(material_image_link)
                else:
                    print("No image link for " + material_name)

                materials.append({
                    "name": material_name,
                    "count": material_count,
                    "image-uri": material_image_name
                })

            if len(materials) == 0:
                materials = None

            category[new_key] = {
                "name": {
                    "name-USen": key.lower()
                },
                "sources": sources,
                "sell-price": sell_price,
                "image-uri": image_name,
                "materials": materials
            }

        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_dir + d[1], 'w') as json_file:
            json.dump(category, json_file, indent = 4, sort_keys = False)

        print(len(data))

def main():
    #generateClothingData()
    #generateFunitureData()
    generateRecipeData()


if __name__ == "__main__": main()