import json
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

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
        with open("kartomantik_cards.json", "w", encoding="utf-8") as f:
            json.dump(response.json()["cards"], f, ensure_ascii=False, indent=4)
    return response.json()["cards"]

import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_kartomantik_to_cockatrice_xml(json_cards_list, output_filename="kartomantik_database.xml"):
    """
    Converts an array of KartomantiK JSON objects into a dynamic multi-set Cockatrice XML.
    Automatically registers and appends a new set block whenever a unique set identity is found.
    """
    # 1. Initialize Root Framework
    root = ET.Element("cockatrice_carddatabase", version="4")
    sets_element = ET.SubElement(root, "sets")
    cards_element = ET.SubElement(root, "cards")
    
    # Track unique sets to avoid redundant set blocks in the XML header
    registered_sets = set()
    
    # 2. Iterate Through the Card Pool
    for card_data in json_cards_list:
        set_obj = card_data["expand"]["set"]
        set_code = str(set_obj["name"]).upper()
        set_longname = f"KartomantiK - {set_code.capitalize()}"
        set_release_date = set_obj["release_date"].split(" ")[0]

        # DYNAMIC ACTION: Register the set to the header if it hasn't been added yet
        if set_code not in registered_sets:
            set_element = ET.SubElement(sets_element, "set")
            ET.SubElement(set_element, "name").text = set_code
            ET.SubElement(set_element, "longname").text = set_longname
            ET.SubElement(set_element, "settype").text = "Custom"
            ET.SubElement(set_element, "release").text = set_release_date
            registered_sets.add(set_code) # Lock registration state
            
        # 3. Create the Individual Card Block
        card = ET.SubElement(cards_element, "card")
        
        # Primary Meta Data Line Allocation
        ET.SubElement(card, "name").text = card_data["name"]
        
        # Set Block with Dynamic Attributes
        set_tag = ET.SubElement(card, "set")
        pic_url = card_data.get("img", "")
        set_tag.set("picURL", pic_url)
        set_tag.set("num", str(card_data["collection_number"]))
        set_tag.set("uuid", card_data["id"])
        set_tag.text = set_code
        
        # Power Costs Filter Trimming
        raw_color = card_data.get("power_cost", "")
        clean_color = raw_color.replace("{", "").replace("}", "")
        ET.SubElement(card, "manacost").text = clean_color
        ET.SubElement(card, "color").text = "".join(dict.fromkeys(clean_color)) # Remove duplicates while preserving order
        ET.SubElement(card, "manaValue").text = str(card_data["numerical_power_cost"])
        ET.SubElement(card, "cmc").text = str(card_data["numerical_power_cost"])

        # Combined Custom Type Engine Mapping
        card_type = card_data.get("type", "").capitalize()
        sub_type = card_data.get("sub_type", "")
        full_type = f"{card_type} - {sub_type}" if sub_type else card_type
        ET.SubElement(card, "type").text = full_type
        
        # Board Placement Zone Matrix
        tablerow = "1" if card_type.lower() == "manifestation" else "2"
        ET.SubElement(card, "tablerow").text = tablerow
        
        # Empathic Score Value Integration
        pt_val = f"{card_data.get('point_value', 0)}"
        ET.SubElement(card, "pt").text = pt_val
        
        # Clean Encoding Formatting Rules
        raw_effect = card_data.get("effect", "")
        clean_effect = raw_effect.replace("\r\n", "\n").replace("\r", "\n")
        ET.SubElement(card, "text").text = clean_effect
        
    # 4. Compile Pretty Dom Architecture Spacing Output
    xml_string = ET.tostring(root, encoding="utf-8")
    parsed_string = minidom.parseString(xml_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Compiled {len(json_cards_list)} items into '{output_filename}' across {len(registered_sets)} sets: {list(registered_sets)}.")



if __name__ == "__main__":
    cards = get_cards(serialize=True)
    convert_kartomantik_to_cockatrice_xml(cards)