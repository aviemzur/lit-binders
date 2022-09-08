import os

import requests
import streamlit as st

import scryfall

st.set_page_config(page_title='Lit Binders')

st.title('Cycles')


st.markdown(
    '<style>body{background-color: Blue;}</style>', unsafe_allow_html=True)

with open('cards/cycles.txt') as f:
    lines = f.readlines()
    ids = [scryfall.url_to_id(line) for line in lines]

cols = st.columns(5)

for i in range(0, len(ids)):
    with cols[i % 5]:
        id = ids[i]
        if id != 'blank':
            image_path = f'images/{id}.png'
            if not os.path.exists(image_path):
                card = scryfall.get_cards(id)
                if 'image_uris' in card:
                    image_url = card['image_uris']['png']
                else:
                    image_url = card['card_faces'][0]['image_uris']['png']
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                response = requests.get(image_url)
                open(image_path, 'wb').write(response.content)
            st.image(image_path)
        else:
            st.image('images/empty.png')