# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:31:21 2023

@author: TomOg
"""
import streamlit as st
import requests
import json


def get_axie_data(axie_id):
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
    return search_url

#def open_webpage():
    # st.markdown(url, unsafe_allow_html=False)
    





st.title("Find Similar Axies by ID")
axie_id = st.text_input("Enter Axie ID:")
url = "https://app.axieinfinity.com/marketplace/axies/"
if axie_id:
    url = get_axie_data(axie_id)
    st.markdown(f"""
        <a href="{url}" target="_blank">Search Marketplace {axie_id}</a>
        """, unsafe_allow_html=True)
        #st.markdown(url, unsafe_allow_html=Truse)
        
if st.button("Donate"):
    st.markdown("ronin:6e4468dcf3c37e713612e62ca9565e2c512c2e1c")
    
