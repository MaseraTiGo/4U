# -*- coding: utf-8 -*-
# @File    : st_ui
# @Project : x_web
# @Time    : 2023/9/12 10:08
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import streamlit as st

# Streamlit app
st.title("Streamlit Buttons")

# Create a button
if st.button("Click me"):
    st.write("Button clicked!")

# You can use the button's return value to perform specific actions
if st.button("Show/Hide Text"):
    st.write("This text can be shown or hidden by clicking the button.")

# You can use buttons in conditional logic to trigger actions
if st.button("Toggle Mode"):
    mode = "On" if mode == "Off" else "Off"
    st.write(f"Mode is {mode}")

