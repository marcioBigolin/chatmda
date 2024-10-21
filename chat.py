import streamlit as st


def conf():
    import toml

    dados = []

    caminho_arquivo_tom = '.streamlit/secrets.toml'

        # Ler o arquivo TOM
    with open(caminho_arquivo_tom, 'r') as arquivo:
        dados = toml.load(arquivo)
    return dados

def chat():
    from pandasai import SmartDataframe
    from pandasai.llm.openai import OpenAI
    import matplotlib.pyplot as plt
    import os

    if "prompt_history" not in st.session_state:
        st.session_state.prompt_history = []


    with st.form("Question"):
        question = st.text_input(("Digite aqui uma pergunta sobre os dados"), value="", type="default")
        submitted = st.form_submit_button(("Gerar"))
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=conf()['key'])
                pandas_ai = SmartDataframe("./assets/demo.csv", config={
                      "llm": llm, 
                    "conversational": False, 
                    "enable_cache": True,
                })

                x = pandas_ai.chat(question)

                if os.path.isfile('exports/charts/temp_chart.png'):
                    im = plt.imread('exports/charts/temp_chart.png')
                    st.image(im)
                    os.remove('exports/charts/temp_chart.png')

                if x is not None:
                    st.write(x)

                st.session_state.prompt_history.append(question)
    

        st.subheader(("Prompt history:"))
        st.write(st.session_state.prompt_history)

        if "prompt_history" in st.session_state.prompt_history and len(st.session_state.prompt_history) > 0:
            if st.button(("Limpar")):
                st.session_state.prompt_history = []


st.header("Chat")
chat()

