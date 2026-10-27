import os
import sys
import json
import requests
from xml.dom import minidom
import xml.etree.ElementTree as ET

def download_image(image_url, image_name):
    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)

def get_cards(serialize=False, language="en"):
    url = "https://www.kartomantik.com/api/card_search"

    n_cards_response = requests.post(url, json={
        "perPage":1,
        "language":language,
        "sortBy":"",
        "selectedCards":[],
        "page":1,
        "temperament":[]
    })
    if n_cards_response.status_code != 200:
        return []

    n_items = n_cards_response.json()["totalItems"]

    response = requests.post(url, json={
        "perPage": n_items,
        "language": language,
        "sortBy": "",
        "selectedCards": [],
        "page": 1,
        "temperament": []
    })
    if response.status_code != 200:
        return []

    if serialize:
        with open("./dist/kartomantik_cards.json", "w", encoding="utf-8") as f:
            json.dump(response.json()["cards"], f, ensure_ascii=False, indent=4)
    return response.json()["cards"]

def to_xml(json_cards_list, output_filename="./dist/kartomantik_database.xml", output_images_dir="./dist/images"):
    root = ET.Element("cockatrice_carddatabase", version="4")
    sets_element = ET.SubElement(root, "sets")
    cards_element = ET.SubElement(root, "cards")
    
    registered_sets = set()
    for card_data in json_cards_list:
        set_obj = card_data["expand"]["set"]
        set_code = str(set_obj["name"]).upper()

        if set_code not in registered_sets:
            set_element = ET.SubElement(sets_element, "set")
            ET.SubElement(set_element, "name").text = set_code
            ET.SubElement(set_element, "longname").text = f"KartomantiK - {set_code.capitalize()}"
            ET.SubElement(set_element, "settype").text = "Custom"
            ET.SubElement(set_element, "release").text = set_obj["release_date"].split(" ")[0]
            os.makedirs(f"{output_images_dir}/{set_code}", exist_ok=True)
            registered_sets.add(set_code)
            
        card = ET.SubElement(cards_element, "card")
        
        ET.SubElement(card, "name").text = card_data["name"]
        
        pic_url = card_data.get("img", "")
        if not os.path.exists(f"{output_images_dir}/{set_code}/{card_data['name']}.jpg"):
            download_image(pic_url, f"{output_images_dir}/{set_code}/{card_data['name']}.jpg")

        set_tag = ET.SubElement(card, "set")
        #set_tag.set("picURL", pic_url) #? Put as fallback?
        set_tag.set("num", str(card_data["collection_number"]))
        set_tag.set("uuid", card_data["id"])
        set_tag.text = set_code

        prop_tag = ET.SubElement(card, "prop")
        
        temperaments = dict([
            ("phlegmatic", "G"), 
            ("vitreous", "B"), 
            ("melancholic", "P"), 
            ("capricious", "Y"), 
            ("choleric", "R"), 
            ("transcendent", "T"), 
            ("hollow", "H")
        ])

        temperament_string = ""
        for temperament in card_data["temperament"]:
            temperament_string += temperaments.get(temperament)
        ET.SubElement(prop_tag, "colors").text = temperament_string

        pretty_card_type = " ".join(word.capitalize() for word in card_data["type"].split('_'))
        ET.SubElement(prop_tag, "type").text = f"{pretty_card_type} {card_data["sub_type"]}"
        ET.SubElement(prop_tag, "maintype").text = pretty_card_type

        if card_data["type"] == "manifestation":
            ET.SubElement(prop_tag, "pt").text = f"{card_data['numerical_power_cost']}/{card_data['point_value']}"
            ET.SubElement(prop_tag, "cmc").text = str(card_data["numerical_power_cost"])
        else:
            pretty_power_cost = card_data["power_cost"].replace("{", "").replace("}", "")
            ET.SubElement(prop_tag, "manacost").text = pretty_power_cost

        raw_effect = card_data.get("effect", "")
        clean_effect = raw_effect.replace("\r\n", "\n").replace("\r", "\n")
        ET.SubElement(card, "text").text = clean_effect

        #? Tablerow could be implemented.
    
    xml_string = ET.tostring(root, encoding="utf-8")
    parsed_string = minidom.parseString(xml_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Compiled {len(json_cards_list)} cards into '{output_filename}' across {len(registered_sets)} sets: {list(registered_sets)}.")

if __name__ == "__main__":
    if not os.path.exists("./dist"):
        os.makedirs("./dist", exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == "--language=it":
        to_xml(
            get_cards(language="it"), 
            output_filename="./dist/kartomantik_database_it.xml",
            output_images_dir="./dist/images_it"
        )
    else:
        to_xml(
            get_cards(language="en"), 
            output_filename="./dist/kartomantik_database_en.xml",
            output_images_dir="./dist/images_en"
        )