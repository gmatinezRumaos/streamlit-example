#lanzar con streamlit run streamlit_app.py en el terminal

import streamlit as st
from streamlit_chat import message
import pandas as pd
from io import BytesIO


def inicializar_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def click():
    if st.session_state.user != '':
        pregunta = st.session_state.user
        respuesta = g.consulta(pregunta,vn)
        st.session_state.df=respuesta

        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta.to_string())
        # Limpiar el input de usuario después de enviar la pregunta
        #st.session_state.user = ''
    
        

def main():
    inicializar_session_state()

    st.title("CHAT RUMAOS")
    st.write("Puedes hacerme a mi todas las preguntas")

    if 'preguntas' not in st.session_state:
        st.session_state.preguntas = []
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = []
        with st.form('addition'):
            query = st.text_area('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
            submit_button = st.form_submit_button('Enviar',on_click=click)

    if st.session_state.preguntas:
        for i in range(len(st.session_state.respuestas)-1, -1, -1):
            myDF=st.dataframe(st.session_state.df.style.highlight_max(axis=0), use_container_width=True)

            df_xlsx = to_excel(st.session_state.df)
            st.download_button(label='Download',
                               data=df_xlsx ,
                               file_name= 'df_test.xlsx')


    with st.sidebar:
        # Mostrar la lista usando st.text()
        for resp in st.session_state.respuestas:
            st.write(resp)

if __name__ == "__main__":
    main()


        


