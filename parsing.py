import json
import urllib.request
import os

class dir: # globals
    cwd = os.getcwd()
    image =  cwd + "images/"
    json = cwd + "data/"

    # clothing
    clothing = "clothing/"
    clothing_accessories = "accessories/"
    clothing_bags = "bags/"
    clothing_bottoms = "bottoms/"
    clothing_dresses = "dresses/"
    clothing_hats = "hats/"
    clothing_shoes = "shoes/"
    clothing_socks = "socks/"
    clothing_tops = "tops/"
    clothing_umbrellas = "umbrellas/"

    # furniture
    furniture = "furniture/"
    furniture_floorings = "floorings/"
    furniture_housewares = "housewares/"
    furniture_miscellaneous = "miscellaneous/"
    furniture_rugs = "rugs/"
    furniture_wallmounted = "wallmounted/"
    furniture_wallpapers = "wallpapers/"

    # recipe
    recipe = "recipe/"
    recipe_clothing = "clothing/"
    recipe_housewares = "housewares/"
    recipe_miscellaneous = "miscellaneous/"
    recipe_others = "others/"
    recipe_tools = "tools/"
    recipe_wallmounted = "wallmounted/"
    recipe_decorations = "decorations/"

def main():

    clothing_images_dir = dir.image + dir.clothing
    clothing_json_dir = dir.json + dir.clothing
    clothing_accessories_image_dir = clothing_images_dir + "/accessories/"
    clothing_accessories = {}
    clothing_sources = ["sister", "label", "kick"]
    clothing_sources_full = ["Able Sisters", "Label", "Kicks"]

    with open("/Users/ickhov/Desktop/accessories.json") as f:
        data = json.load(f)

    for key, value in data.items():
        new_key = key.lower().replace(" ", "_")
        new_value = []

        image_links = value["variationImageLinks"]
        buy_price = value["priceBuy"]
        sell_price = value["priceSell"]
        sources = []

        # get list of source name
        for source in value["source"]:
            is_designer = False
            # check if the source contains "sister", "label", or "kick"
            for index, source_name in enumerate(clothing_sources):
                # if so, add appropriate name to list
                if source_name in source:
                    is_designer = True
                    # ensure we don't have duplicates
                    if clothing_sources_full[index] not in sources:
                        sources.append(clothing_sources_full[index])

            if not is_designer:
                sources.append(source)

        

        for index, item in enumerate(value["variations"]):
            variant = {}
            # set image name and dir to save in
            image_name = new_key + "_" + item.lower().replace(" ", "_") + ".png"

            # download images from the web
            if not os.path.exists(clothing_accessories_image_dir):
                os.makedirs(clothing_accessories_image_dir)
            urllib.request.urlretrieve(image_links[index], clothing_accessories_image_dir + image_name)

            # set the variant name and image name in the new dictionary
            variant["variant"] = item
            variant["image_uri"] = image_name
            variant["sources"] = sources
            variant["name"] = {
                    "name-USen": key.lower(),
                }
            variant["buy-price"] = buy_price
            variant["sell-price"] = sell_price
            new_value.append(variant)

        if len(new_value) == 0:
            variant = {}
            image_name = new_key + ".png"

            # download images from the web
            if not os.path.exists(clothing_accessories_image_dir):
                os.makedirs(clothing_accessories_image_dir)
            urllib.request.urlretrieve(value["imageLink"], clothing_accessories_image_dir + image_name)

            variant["variant"] = None
            variant["image_uri"] = image_name
            variant["sources"] = sources
            variant["name"] = {
                    "name-USen": key.lower(),
                }
            variant["buy-price"] = buy_price
            variant["sell-price"] = sell_price
            new_value.append(variant)

        clothing_accessories[new_key] = new_value

    if not os.path.exists(clothing_json_dir):
        os.makedirs(clothing_json_dir)
    with open(clothing_json_dir + '/accessories.json', 'w') as json_file:
        json.dump(clothing_accessories, json_file, indent = 4, sort_keys = False)

    print(len(data))

if __name__ == "__main__": main()