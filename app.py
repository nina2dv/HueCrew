import streamlit as st
import openai
from colorthief import ColorThief
from PIL import ImageColor
import matplotlib.pyplot as plt
import colorsys
from urllib.request import urlopen
import io
import numpy as np


def show_palette(palette_hex):
    """show palette strip"""
    palette = np.array([ImageColor.getcolor(color, "RGB") for color in  palette_hex])
    fig, ax = plt.subplots(dpi=100)
    ax.imshow(palette[np.newaxis, :, :])
    ax.axis('off')
    return fig

openai.api_key = st.secrets['openai_KEY']

st.set_page_config(
    page_title="HueCrew",
    page_icon="🏞️",
    layout="wide")
# Main Page
st.title("HueCrew")

img_num = 1

col_left, col_right = st.columns([3,1])
with col_left:
    col_num = st.slider("Select the number of colours", min_value=2, max_value=10, value=4, step=1, help=None)

    form = st.form(key='my_form')
    input_text = form.text_area(label='Enter your prompt', height=120)
    submit_button = form.form_submit_button(label='Submit')
with col_right:
    img_size = st.radio(
        "Image Size",
        ('256x256', '512x512', '1024x1024'), index=1)


if input_text is not None and submit_button:
    try:
        palette_list = []
        col1, col2 = st.columns(2)
        image_resp = openai.Image.create(prompt=input_text, n=img_num, size=img_size)

        with col1:
            st.image(image_resp["data"][0]["url"])
        # st.write(image_resp)
        fd = urlopen(image_resp["data"][0]["url"])
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dom_col = color_thief.get_color(quality=1)
        palette = color_thief.get_palette(color_count=col_num-1)
        dom_col = f"#{dom_col[0]:02x}{dom_col[1]:02x}{dom_col[2]:02x}"
        with col2:
            st.color_picker(f"Dominant Colour: {dom_col}", value=dom_col, key=None, help=None, on_change=None, args=None, disabled=True,
                            label_visibility="visible")
            st.code(f"{dom_col}")

        wcol = col_num
        cols = st.columns(col_num)
        temp_count = 0
        for count, value in enumerate(palette):
            if temp_count >= len(palette):
                temp_count = 0
            else:
                temp_count += 1
            col = cols[temp_count % wcol]
            with col:
                colour = f"#{value[0]:02x}{value[1]:02x}{value[2]:02x}"
                palette_list.append(colour)
                st.color_picker(f"{colour}", value=colour, key=None, help=None, on_change=None, args=None, disabled=True,
                                label_visibility="visible")
                st.code(f"{colour}")
                st.code(value)
                st.code(colorsys.rgb_to_hsv(*value))
                st.code(colorsys.rgb_to_hls(*value))
            # st.pyplot(show_palette(palette_hex))
        st.pyplot(show_palette(palette_list))
    except NameError:
        st.error("Error - Try a smaller content size")
