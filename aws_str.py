import os
import json
import time
import streamlit as st
import streamlit_authenticator as stauth
import math
import yaml
from yaml.loader import SafeLoader
import sup_module as sup
import plotly.express as px

def main():
    # Define a class to handle session state
    class SessionState:
        def __init__(self):
            self.messages = []

    # Create or get the session state
    if "session" not in st.session_state:
        st.session_state.session = SessionState()
        
    ######### Menu Suspenso #########     

    # Cria o menu suspenso na barra lateral com as opções e as tabelas em ordem
    authenticator.logout("Logout", "sidebar")
    selected_tabela = st.sidebar.selectbox("Escolha uma opção:", ["Primeiro", "Segundo"])

             

    ####### Pagina principal #######

    
    # Header
    st.header("RNG Data Visualization")
    st.divider()
    st.subheader("Coisas Aqui")
    st.image("src/img/sup_cpu.jpg")
    

    st.divider()
    
    # Cria um botão "Calcular"
    if st.button("Calcular"):
        with st.spinner('Wait for it...'):
            df = sup.read_csv_aws()
            bit_count = 2048
            chart_data = sup.csv_to_df(df, bit_count)
            fig = px.line(chart_data, x='Time', y='Zscore')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(chart_data, use_container_width=True)
            
        st.write("Done!")
        
    
if __name__ == "__main__":
    # Autenticação
    with open('.streamlit/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
)

    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
    
