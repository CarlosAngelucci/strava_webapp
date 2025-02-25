import streamlit as st
from pages import distance_pace, resumo_semanal, rotas

st.set_page_config(page_title='Half Marathon Training Analysis', layout='wide')

# Sidebar para navegação
st.sidebar.title("📊 Running Metrics Dashboard")
page = st.sidebar.radio("Selecione a análise", ["🏃 Distance & Pace", "📆 Resumo Semanal", "🗺️ Rotas", "❤️ Heart Frequency Analysis"])

# #  adicionar botao na sidebar para atualizar os dados
# if st.sidebar.button("Atualizar dados"):
#     get_latest_runs()


# Adicionando a imagem como um header
st.markdown(
    """
    <style>
    .header-image {
        width: 100%;
        height: 200px; /* Ajuste a altura conforme necessário */
        object-fit: cover; /* Garante que a imagem cubra toda a área sem distorção */
        margin-bottom: 20px; /* Espaço abaixo da imagem */
    }
    </style>
    <img src="https://wallpapers.com/images/hd/nike-running-quote-dotdcd6b3c9m5t0s.jpg" class="header-image">
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: white;'>🏃 Half Marathon Training Analysis</h1>", unsafe_allow_html=True)


# Carregar a página selecionada
if page == "🏃 Distance & Pace":
    distance_pace.show()
elif page == "📆 Resumo Semanal":
    resumo_semanal.show()
elif page == "🗺️ Rotas":
    rotas.show()
    st.markdown("<h3 style='text-align: center; color: white;'>Under Construction</h3>", unsafe_allow_html=True)
elif page == "❤️ Heart Frequency Analysis":
    st.markdown("<h3 style='text-align: center; color: white;'>Under Construction</h3>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: white;'>Data collected from Strava <img src='https://i.pinimg.com/736x/ed/2a/64/ed2a64f9a34b00ad2013bf23cc0dc162.jpg' alt='Strava' style='vertical-align:middle; height:10'; width:'10';'></h3>", unsafe_allow_html=True)

