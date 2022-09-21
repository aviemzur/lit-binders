import os

import requests
import streamlit as st

import scryfall

st.set_page_config(page_title='Lit Binders')

st.markdown(
    '<style>body{background-color: Blue;}</style>', unsafe_allow_html=True)
    
binders = sorted([binder.replace('.txt', '') for binder in os.listdir('cards')])

def save_selection(init=False):
    index = 0
    if not init:
        index = binders.index(st.session_state.selection)
    with open('_index', 'w') as f:
        f.write(str(index))

if not os.path.exists('_index'):
    save_selection(init=True)

def get_selection():
    with open('_index') as f:
        result = f.read()
    return int(result)

selected_binder = st.selectbox('Lit Binders', binders, index=get_selection(), on_change=save_selection, key='selection')

with open(f'cards/{selected_binder}.txt') as f:
    lines = f.readlines()
    ids = [scryfall.url_to_id(line) for line in lines]

st.title(selected_binder)

cols = st.columns(5)

for i in range(0, len(ids)):
    with cols[i % 5]:
        id = ids[i]
        if id != 'blank':
            face = 1
            image_path = f"images/{id.replace('|', '-').strip()}.png"
            if '|' in id:
                id, face = id.split('|')
            if not os.path.exists(image_path):
                card = scryfall.get_cards(id)
                if 'image_uris' in card:
                    image_url = card['image_uris']['png']
                else:
                    image_url = card['card_faces'][int(face) - 1]['image_uris']['png']
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                response = requests.get(image_url)
                open(image_path, 'wb').write(response.content)
            ct = st.container()
            ct.image(image_path)
        else:
            st.image('empty.png')
