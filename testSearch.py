# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 19:20:43 2023

@author: TomOg
"""

import streamlit as st
import requests
import json


st.write("If you found this app helpful and would like to donate!")
st.markdown("ronin:6e4468dcf3c37e713612e62ca9565e2c512c2e1c")


def get_axie_data(axie_id, filters = set()):
    payload={}
    headers = {}

    axie_url = "https://ronin.rest/ronin/axie/" + axie_id
    axie_response = requests.request("GET", axie_url, headers=headers, data=payload)

    data = json.loads(axie_response.text)
    
    parts = {
        "horn": data["genes"]["horn"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "eyes": data["genes"]["eyes"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "ears": data["genes"]["ears"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "mouth": data["genes"]["mouth"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "back": data["genes"]["back"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "tail": data["genes"]["tail"]["d"]["name"].lower().replace(" ", "-").replace("'", "")
    }
    
    search_parts = [f"parts={part}-{parts[part]}" for part in parts if part.title() not in filters]
    search_url = f"https://app.axieinfinity.com/marketplace/axies/?partTypes=Tail&auctionTypes=Sale&{'&'.join(search_parts)}"

    
    search_url = f"https://app.axieinfinity.com/marketplace/axies/?partTypes=Tail&auctionTypes=Sale&{'&'.join(search_parts)}"
    
    
    ql_endpoint = 'https://graphql-gateway.axieinfinity.com/graphql'
    ql_filter = ["Horn", "Eyes", "Ears", "Mouth", "Back", "Tail"]
    ql_parts = ['horn-' + parts['horn'],'eyes-' + parts['eyes'],'ears-' + parts['ears'], 'mouth-' + parts['mouth'], 'back-' + parts['back'], 'tail-' + parts['tail']]
    ql_combined = [{"Filter": f, "Parts": part} for f, part in zip(ql_filter, ql_parts)]
    
    part_ql_inject = [item['Parts'] for item in ql_combined if item['Filter'] not in filters]
    
    payload = {"operationName":"GetAxieBriefList","variables":{"from":0,"sort":"PriceAsc","size":24,"auctionType":"Sale","criteria":{"bodyShapes":None,"breedCount":None,"classes":None,"numJapan":None,"numMystic":None,"numShiny":None,"numSummer":None,"numXmas":None,"parts":part_ql_inject ,"ppAquatic":None,"ppBeast":None,"ppBird":None,"ppBug":None,"ppDawn":None,"ppDusk":None,"ppMech":None,"ppPlant":None,"ppReptile":None,"pureness":None,"purity":None,"stages":None,"title":None}},"query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n axies(\n auctionType: $auctionType\n criteria: $criteria\n from: $from\n sort: $sort\n size: $size\n owner: $owner\n ) {\n total\n results {\n ...AxieBrief\n __typename\n }\n __typename\n }\n}\n\nfragment AxieBrief on Axie {\n id\n name\n stage\n class\n breedCount\n image\n title\n genes\n newGenes\n battleInfo {\n banned\n __typename\n }\n order {\n id\n currentPrice\n currentPriceUsd\n __typename\n }\n parts {\n id\n name\n class\n type\n specialGenes\n __typename\n }\n __typename\n}\n"}
    response = requests.post(ql_endpoint, json=payload)
    
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        ids = [axie['id'] for axie in data['data']['axies']['results']]
        price = [axie['order']['currentPriceUsd'] for axie in data['data']['axies']['results']]
        combined_data = [{"id": id, "price": price} for id, price in zip(ids, price)]
    else:
        print('Error:', response.status_code)
    
    return search_url, combined_data

filter_options = ["Horn", "Eyes", "Ears", "Mouth", "Back", "Tail"]

# Use the multi-select input to allow the user to select multiple filters
filters = st.sidebar.multiselect("Exclude Parts", filter_options)


st.title("Find Similar Axies by ID")
axie_id = st.text_input("Enter Axie ID:")
url = "https://app.axieinfinity.com/marketplace/axies/"
if axie_id:
    url, price_data = get_axie_data(axie_id, filters)
    st.markdown(f"""
        <a href="{url}" target="_blank">Search Marketplace {axie_id}</a>
        """, unsafe_allow_html=True)
    if len(price_data) != 0: 
        st.write("Lowest Priced Axie")
        st.write(price_data[0])
        if price_data[0]['id'] != axie_id:
            st.write("Undercut!")
    else:
        st.write("No similar axies found")
        
if st.button("Change Log"):
    st.write("Change Log: Integrated undercut feature with filters")         
    st.write("Change Log: Added feature to see if the axie has been undercut on the market. Note: Not yet integrated with filters")  
    st.write("Change Log: Added option to exclude parts in the sidebar")        
    st.write("This app is useful for determining an axie's list price based on similar axies on the market. This app removes the need to filter the market by each part individually. Still a work in progress, more functionality to be added soon.")