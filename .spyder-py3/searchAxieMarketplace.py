# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:46:40 2023

@author: TomOg
"""

import requests
import sys
import json
import webbrowser 


while True:
    url = input("Enter URL: ")
    text = url.split(sep=('/'))
    axie_id = text[0]
    
    if not axie_id.isnumeric():
        axie_id = text[6]
        if not axie_id.isnumeric():
            axie_id = text[5]
            if not axie_id.isnumeric():
                sys.exit("Error, Id field not a number")
    
    
    payload={}
    headers = {}
    
    
    axie_url = "https://ronin.rest/ronin/axie/" + axie_id
    axie_response = requests.request("GET", axie_url, headers=headers, data=payload)
    
    data = json.loads(axie_response.text)
    
    horn = data["genes"]["horn"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    eyes = data["genes"]["eyes"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    ears = data["genes"]["ears"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    mouth = data["genes"]["mouth"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    back = data["genes"]["back"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    tail = data["genes"]["tail"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    
    search_url = "https://app.axieinfinity.com/marketplace/axies/?partTypes=Tail&auctionTypes=Sale&parts=horn-" + horn + "&parts=eyes-" + eyes + "&parts=ears-" + ears + "&parts=mouth-" + mouth + "&parts=back-" + back + "&parts=tail-" + tail 
    
    webbrowser.open(search_url, new=2, autoraise=True)


