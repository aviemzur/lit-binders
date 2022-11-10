import os

import requests
import streamlit as st

import scryfall

st.set_page_config(page_title='Lit Binders')

st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)

st.markdown(
    '<style>body{background-color: Blue;}</style>', unsafe_allow_html=True)
    
binders = sorted([binder.replace('.txt', '') for binder in os.listdir('cards')])

def on_binder_selection_change():
    index = binders.index(st.session_state.selection)
    save_selection(index)

def get_selection():
    with open('_index') as f:
        result = f.read()
    return int(result)

def save_selection(index):
    with open('_index', 'w') as f:
        f.write(str(index))

if not os.path.exists('_index'):
    save_selection(0)

selected_binder = st.selectbox('Lit Binders', binders, index=get_selection(), on_change=on_binder_selection_change, key='selection')

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
        elif i < len(ids) - 1:
            st.image('empty.png')


with cols[2]:
    index = get_selection()
    if (index < len(binders) - 1):
        st.image('empty.png', width=50)
        next = st.button('Next Binder')
        if next:
            save_selection(index + 1)
            st.experimental_rerun()
        st.markdown("<center><a href='#linkto_top'>top</a></center>", unsafe_allow_html=True)
