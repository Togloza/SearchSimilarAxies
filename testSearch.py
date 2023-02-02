# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 19:20:43 2023

@author: TomOg
"""

import streamlit as st
import requests
import json


# This app allows users to search for Axie data using a specific Axie ID. 
# It also provides a donate button using the ronin cryptocurrency.


st.write("**If you found this app helpful and would like to donate!**")
st.markdown("ronin:6e4468dcf3c37e713612e62ca9565e2c512c2e1c")
st.write("**If you are unable to donate, consider using my marketplace referral code!**")
st.write("Referral Code: VWP3JJKF")

st.write("If you have feedback or want to request a feature, Email: searchaxies@gmail.com")


# This function takes an Axie ID and a set of filters as input
def get_axie_data(axie_id, filters = set()):
       
    search_url, parts = get_url(axie_id, filters)
    price_data = get_price_data(parts, filters)
  
    return search_url, price_data

# Gets the URL info based on the axie id and a set of filters
@st.experimental_memo
def get_url(axie_id, filters = set()):
    payload={}
    headers = {}
    
    # This requests the axie data from the ronin API
    axie_url = "https://ronin.rest/ronin/axie/" + axie_id
    axie_response = requests.request("GET", axie_url, headers=headers, data=payload)

    data = json.loads(axie_response.text)
    
    # Clean up the data by lowercasing, replacing spaces and apostrophes
    parts = {
        "horn": data["genes"]["horn"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "eyes": data["genes"]["eyes"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "ears": data["genes"]["ears"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "mouth": data["genes"]["mouth"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "back": data["genes"]["back"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "tail": data["genes"]["tail"]["d"]["name"].lower().replace(" ", "-").replace("'", ""),
        "class": data['genes']['cls'].capitalize()
    }
    
    # Create a search URL based on the filters provided
    search_parts = [f"parts={part}-{parts[part]}" for part in parts if part.title() not in filters]
    search_url = f"https://app.axieinfinity.com/marketplace/axies/?partTypes=Tail&auctionTypes=Sale&{'&'.join(search_parts)}" + "&classes=" + str(parts["class"])
    return search_url, parts

# Gets the price info using GraphQL and the parts variable from get_url
def get_price_data(parts, filters = set()):
    ql_endpoint = 'https://graphql-gateway.axieinfinity.com/graphql'
    ql_filter = ["Horn", "Eyes", "Ears", "Mouth", "Back", "Tail"]
    ql_parts = ['horn-' + parts['horn'],'eyes-' + parts['eyes'],'ears-' + parts['ears'], 'mouth-' + parts['mouth'], 'back-' + parts['back'], 'tail-' + parts['tail']]
    ql_combined = [{"Filter": f, "Parts": part} for f, part in zip(ql_filter, ql_parts)]
    # Format the data to be put into the graphql payload
    part_ql_inject = [item['Parts'] for item in ql_combined if item['Filter'] not in filters]
    
    payload = {"operationName":"GetAxieBriefList","variables":{"from":0,"sort":"PriceAsc","size":24,"auctionType":"Sale","criteria":{"bodyShapes":None,"breedCount":None,"classes":parts["class"],"numJapan":None,"numMystic":None,"numShiny":None,"numSummer":None,"numXmas":None,"parts":part_ql_inject ,"ppAquatic":None,"ppBeast":None,"ppBird":None,"ppBug":None,"ppDawn":None,"ppDusk":None,"ppMech":None,"ppPlant":None,"ppReptile":None,"pureness":None,"purity":None,"stages":None,"title":None}},"query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n axies(\n auctionType: $auctionType\n criteria: $criteria\n from: $from\n sort: $sort\n size: $size\n owner: $owner\n ) {\n total\n results {\n ...AxieBrief\n __typename\n }\n __typename\n }\n}\n\nfragment AxieBrief on Axie {\n id\n name\n stage\n class\n breedCount\n image\n title\n genes\n newGenes\n battleInfo {\n banned\n __typename\n }\n order {\n id\n currentPrice\n currentPriceUsd\n __typename\n }\n parts {\n id\n name\n class\n type\n specialGenes\n __typename\n }\n __typename\n}\n"}
    response = requests.post(ql_endpoint, json=payload)
    # If the request is successful gather the axie id and price of the axies into price_data 
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        ids = [axie['id'] for axie in data['data']['axies']['results']]
        price = [axie['order']['currentPriceUsd'] for axie in data['data']['axies']['results']]
        price_data = [{"id": id, "price": price} for id, price in zip(ids, price)]
    else:
        print('Error:', response.status_code)
    return price_data

# Takes a list of IDs in CSV format to find if they are the cheapest on the market
@st.experimental_memo    
def multi_select(multi_axie_input):
    multi_axie = multi_axie_input.split(",")
    multi_axie = [item.strip() for item in multi_axie]
    price_list = {axie: get_axie_data(axie)[1][0] if get_axie_data(axie)[1] else {'id': '-1', 'price': '-1'} for axie in multi_axie}
    undercut_axies = [axie for axie in price_list if axie != price_list[axie]['id'] and price_list[axie]['id'] != "-1"]
    return price_list, undercut_axies 

# Gets the axies on the account of the User ID
@st.experimental_memo
def get_axies_from_address(address = "1ed242dd-a96c-6f9f-9a64-775bfcf06d95", limit = "20"):
    url = "https://api-gateway.skymavis.com/origin/v2/community/users/fighters?userID=" + address + "&axieType=ronin&limit=" + str(limit)
    
    headers = {
        "accept": "application/json",
        "X-API-Key": st.secrets["api_key"]
        }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    axie_ids = [axie['id'] for axie in data['_items']]
    return axie_ids
    
    

filter_options = ["Horn", "Eyes", "Ears", "Mouth", "Back", "Tail"]

# Use the multi-select input to allow the user to select multiple filters




     
# Input box to put in the axie id
st.title("Find Similar Axies by ID")
st.subheader("Select a Box from the Sidebar")
url = "https://app.axieinfinity.com/marketplace/axies/"


st.sidebar.title("**Tools**")

axie_id = False
if st.sidebar.checkbox("**Axie Select**"):
    st.write("Enter Axie ID:")
    axie_id = st.text_input("ID", key = "singleselect")
    filters = st.multiselect("Exclude Parts", filter_options)


# If the axie id field has an input grab the data and provide a link to the appropriate page
if axie_id:
    url, price_data = get_axie_data(axie_id, filters)
    st.markdown(f"""
        <a href="{url}" target="_blank">Search Marketplace {axie_id}</a>
        """, unsafe_allow_html=True)
    # If there are axies in the marketplace then provide show the lowest priced axie and if the input axie id is the lowest price      
    if len(price_data) != 0: 
        st.write("Lowest Priced Axie")
        st.write("ID: " + price_data[0]['id'])
        st.write("Price: " + price_data[0]['price'])
        if price_data[0]['id'] != axie_id and axie_id in price_data:
            st.write("**Undercut!**")
    else:
        st.write("No similar axies found")
        
        

if st.sidebar.checkbox("**Multi Axie Select**"):
        multi_axie_input = st.text_input("Input Multiple IDs in CSV Format", key = "multiselect")
        if multi_axie_input:
            price_list, undercut_axies = multi_select(multi_axie_input)
            if undercut_axies:
                for axie in undercut_axies:
                    st.write(axie, "Cheaper Axies Available")
                    st.write("Lower Axie ID: ", price_list[axie]['id'])
                    st.write("Price: ", price_list[axie]['price'])
                    _url, dummy = get_url(axie)
                    st.markdown(f"""
                        <a href="{_url}" target="_blank">Search Marketplace {axie}</a>
                        """, unsafe_allow_html=True)
            else:
                st.write("All Axies Cheapest On Market")

if st.sidebar.checkbox("**Get Axie IDs**", key = "axieids"):
    address = st.text_input("Input Axie User ID")
    limit = st.text_input("Input Max Number of Axies")
    if address and limit:
        address_list = get_axies_from_address(address, limit)
        address_list_copy = address_list
        last = address_list_copy.pop()
        for item in address_list_copy:
            st.write(str(item) + ",")
        st.write(str(last))
            
        
       
        
# Help box
if st.sidebar.checkbox("Help"):
    st.sidebar.write("Enter an axie id in the box")
    st.sidebar.write("The app provides a link to the marketplace for axies with the same parts as the entered axie")
    st.sidebar.write("It also shows if there is a lower priced axie on the market than the on entered")

# Multiselect Help Box
if st.sidebar.checkbox("Multiselect Help"):
     st.sidebar.write("Save axie ids in text file to copy paste easily")
     st.sidebar.write("Example: 2346183, 2597247, 4866741, 3279037")
     
if st.sidebar.checkbox("User ID Help"):
    st.sidebar.write("Find your User ID by Loading the Game and Clicking on your Portrat")
     

if st.button("Change Log", key = "changelog"):
    st.write("Change Log: Added Caching and reformatted")
    st.write("Change Log: Integrated undercut feature with filters")         
    st.write("Change Log: Added feature to see if the axie has been undercut on the market. Note: Not yet integrated with filters")  
    st.write("Change Log: Added option to exclude parts in the sidebar")        
    st.write("This app is useful for determining an axie's list price based on similar axies on the market. This app removes the need to filter the market by each part individually. Still a work in progress, more functionality to be added soon.")
