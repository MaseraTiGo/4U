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

import ast
from pprint import pprint

# Python code for which you want to generate the AST
python_code = """
import streamlit as st
# Define tabs as radio buttons
selected_tab = st.radio("Select a Tab:", ["Tab 1", "Tab 2", "Tab 3"], horizontal=True)

# Content for each tab
if selected_tab == "Tab 1":
    st.header("Tab 1 Content")
    st.write("This is the content of Tab 1.")

elif selected_tab == "Tab 2":
    st.header("Tab 2 Content")
    st.write("This is the content of Tab 2.")

elif selected_tab == "Tab 3":
    st.header("Tab 3 Content")
    st.write("This is the content of Tab 3.")
"""

# Parse the Python code and generate the AST
parsed_ast = ast.parse(python_code)

# Print the AST in a readable format
pprint(ast.dump(parsed_ast))
