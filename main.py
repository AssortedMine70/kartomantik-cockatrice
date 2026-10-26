import json
import requests
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def download_image(image_url, image_name):
    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)

def get_cards(serialize=False):
    url = "https://www.kartomantik.com/api/card_search"

    n_cards_response = requests.post(url, json={
        "perPage":1,
        "language":"it",
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
        "language": "it",
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

def to_xml(json_cards_list, output_filename="./dist/kartomantik_database.xml"):
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
            os.makedirs(f"./dist/images/{set_code}", exist_ok=True)
            registered_sets.add(set_code)
            
        card = ET.SubElement(cards_element, "card")
        
        ET.SubElement(card, "name").text = card_data["name"]
        
        pic_url = card_data.get("img", "")
        if not os.path.exists(f"./dist/images/{set_code}/{card_data['name']}.jpg"):
            download_image(pic_url, f"./dist/images/{set_code}/{card_data['name']}.jpg")

        set_tag = ET.SubElement(card, "set")
        set_tag.set("picURL", pic_url)
        set_tag.set("num", str(card_data["collection_number"]))
        set_tag.set("uuid", card_data["id"])
        set_tag.text = set_code
        
        raw_color = card_data.get("power_cost", "")
        clean_color = raw_color.replace("{", "").replace("}", "")
        ET.SubElement(card, "manacost").text = clean_color
        #ET.SubElement(card, "color").text = "".join(dict.fromkeys(clean_color)) # Remove duplicates while preserving order
        ET.SubElement(card, "color").text = "G"
        ET.SubElement(card, "manaValue").text = str(card_data["numerical_power_cost"])
        ET.SubElement(card, "cmc").text = str(card_data["numerical_power_cost"])

        card_type = card_data.get("type", "").capitalize()
        sub_type = card_data.get("sub_type", "")
        full_type = f"{card_type} - {sub_type}" if sub_type else card_type
        ET.SubElement(card, "type").text = full_type
        
        tablerow = "1" if card_type.lower() == "manifestation" else "2"
        ET.SubElement(card, "tablerow").text = tablerow
        
        pt_val = f"{card_data.get('point_value', 0)}"
        ET.SubElement(card, "pt").text = pt_val
        
        raw_effect = card_data.get("effect", "")
        clean_effect = raw_effect.replace("\r\n", "\n").replace("\r", "\n")
        ET.SubElement(card, "text").text = clean_effect
        
    xml_string = ET.tostring(root, encoding="utf-8")
    parsed_string = minidom.parseString(xml_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Compiled {len(json_cards_list)} cards into '{output_filename}' across {len(registered_sets)} sets: {list(registered_sets)}.")

if __name__ == "__main__":
    os.makedirs("./dist", exist_ok=True)
    to_xml(get_cards(serialize=True))