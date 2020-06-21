import json
import urllib.request
import os

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

def main():

    clothing_images_dir = dir.image + dir.clothing
    clothing_json_dir = dir.json + dir.clothing

    # create a list of directories to loop through
    clothing_dirs = [
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

    clothing_sources = ["sister", "label", "kick"]
    clothing_sources_full = ["Able Sisters", "Label", "Kicks"]

    for d in clothing_dirs:
        clothing_category_image_dir = clothing_images_dir + d[0]
        clothing_category = {}

        with open(dir.cwd + dir.clothing + d[1]) as f:
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
                if not os.path.exists(clothing_category_image_dir):
                    os.makedirs(clothing_category_image_dir)
                urllib.request.urlretrieve(image_links[index], clothing_category_image_dir + image_name)

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
                if not os.path.exists(clothing_category_image_dir):
                    os.makedirs(clothing_category_image_dir)
                urllib.request.urlretrieve(value["imageLink"], clothing_category_image_dir + image_name)

                variant["variant"] = None
                variant["image_uri"] = image_name
                variant["sources"] = sources
                variant["name"] = {
                        "name-USen": key.lower(),
                    }
                variant["buy-price"] = buy_price
                variant["sell-price"] = sell_price
                new_value.append(variant)

            clothing_category[new_key] = new_value

        if not os.path.exists(clothing_json_dir):
            os.makedirs(clothing_json_dir)
        with open(clothing_json_dir + d[1], 'w') as json_file:
            json.dump(clothing_category, json_file, indent = 4, sort_keys = False)

        print(len(data))

if __name__ == "__main__": main()