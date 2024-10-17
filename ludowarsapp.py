import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def update_gsheet():
   spreadsheet_link=st.secrets['spreadsheet_rankings']
   # Create a connection object.
   conn = st.connection("gsheets", type=GSheetsConnection)
   df = conn.read(
      spreadsheet=spreadsheet_link
      ,ttl=300
   )
   return df

def get_itinerary():
   # Spreadsheet link
   spreadsheet_link = st.secrets['spreadsheet_itinerary']
   # Create a connection object.
   conn = st.connection("gsheets", type=GSheetsConnection)
   df = conn.read(
      spreadsheet=spreadsheet_link
   )
   return df

# Styles
mystyle = '''
    <style>
        p {
            text-align: left;
        }

        .st-emotion-cache-1y4p8pa {
         padding: 3rem;
        }

        .st-emotion-cache-16txtl3{
         padding: 3rem;
        }
    </style>
    '''
st.markdown(mystyle, unsafe_allow_html=True)

with st.sidebar:
   st.image("assets\static\logo_ludowars.png")
   df = update_gsheet()
   itinerarios=get_itinerary()
   
   st.markdown("# LudoWars App")
   st.markdown("Escribe tu número de identificación y selecciona el grupo al que perteneces para mostrarte tu itinerario.")

   col_s1,col_s2=st.columns([3,3])
   disable_search=True
   with col_s1:
      st.session_state.id_jugador=st.text_input("Número")
      if st.session_state.id_jugador:
         disable_search=False
   with col_s2:
      st.session_state.grupo_jugador=st.selectbox("Grupo",['A','B'])

   st.session_state.boton_buscar=st.button("Buscar", type="primary", disabled=disable_search)
   if st.session_state.boton_buscar:
      # Obtener nombre de jugador
      st.session_state.nombre_jugador=df.loc[(df['Número']==int(st.session_state.id_jugador))
                           & (df['Grupo']==st.session_state.grupo_jugador), "Nombre"].item()
      # Obtener itinerario
      st.session_state.itinerario_jugador=itinerarios.loc[(itinerarios['Numero']==int(st.session_state.id_jugador))
                           & (itinerarios['Grupo']==st.session_state.grupo_jugador),:]
      st.markdown(f"Nombre: {st.session_state.nombre_jugador}")
   else:
      st.markdown("Haz click en _buscar_ para encontrar tu itinerario")

if st.session_state.boton_buscar:
   st.title(f"¡Bienvenido, {st.session_state.nombre_jugador}!")
   st.subheader("Juega para ganar, juega para divertirte, juega en LudoWars")

   tab1, tab2, tab3, tab4 = st.tabs(["Itinerario", "Ranking Grupo", "Global", "Juegos"])

   with tab1:
      
      st.header("Mapa")
      st.image("assets\static\croquis.jpeg", width=400)

      round=4
      gameName="Coffee Rush"
      roundNames=["R1","R2","R3","R4","R5","R6","R7"]
      totalGameRounds=range(1,8)
      startTime=["12:15 PM", "1:10 PM", "2:05 PM", "3:35 PM", "4:30 PM", "5:25 PM", "6:20 PM"]
      final=["Clank!", "7:15 PM"]
      # Adding current itinerary
      # roundString=f"Ronda {round}: {gameName} - Ahora"
      # st.subheader(roundString)

      # Full itinerary
      st.subheader("Itinerario completo")

      col1, col2, col3 = st.columns([.2,.2,.8])

      for round in totalGameRounds:
         col1.markdown(f"Ronda {round}")

      for t in startTime:
         col2.markdown(t)

      for game in roundNames:
         col3.markdown(st.session_state.itinerario_jugador.loc[:,game].item())

      st.markdown(f"### :trophy: **Final** {final[1]}  {final[0]} :trophy:")

      st.markdown("#### Premiación 8:15 PM")

   with tab2:

      total_puntos=df.loc[(df['Número']==int(st.session_state.id_jugador))
                           & (df['Grupo']==st.session_state.grupo_jugador), "Total Puntos"].item()
      
      ranking_grupo=df.loc[(df['Número']==int(st.session_state.id_jugador))
                           & (df['Grupo']==st.session_state.grupo_jugador), "Ranking"].item()
      
      
      col_header_1t1, col_header_2t1 = st.columns([.5,.5])
      with col_header_1t1:
         st.markdown(f"**Total de puntos: {total_puntos}**")
      with col_header_2t1:
         st.markdown(f"**Ranking en Grupo {st.session_state.grupo_jugador}: {ranking_grupo}**")

      df_ranking_grupo=df.loc[df['Grupo']==st.session_state.grupo_jugador,["Nombre","Ranking","Total Puntos"]]
      df_ranking_grupo=df_ranking_grupo.sort_values(by="Ranking", ascending=True).dropna()
      st.dataframe(df_ranking_grupo,hide_index=True)
      
   with tab3:
      ranking_global=df.loc[(df['Número']==int(st.session_state.id_jugador))
                           & (df['Grupo']==st.session_state.grupo_jugador), "Global"].item()
      
      col_header_1t3, col_header_2t3 = st.columns([.5,.5])
      with col_header_1t3:
         st.markdown(f"**Total de puntos: {total_puntos}**")    
      with col_header_2t3:
         st.markdown(f"**Global: {ranking_global}**")

      df_global=df.loc[:,["Nombre","Global","Total Puntos"]]
      df_global=df_global.sort_values(by="Global", ascending=True).dropna()
      st.dataframe(df_global,hide_index=True)

   with tab4:
      st.markdown(f"Tabla de grupo {st.session_state.grupo_jugador}:")
      df_juegos=df.loc[df['Grupo']==st.session_state.grupo_jugador,["Nombre","Total de juegos","Primer","Segundo","Tercer","No calificado"]].dropna()
      st.dataframe(df_juegos,hide_index=True)

else:
   st.title(f"LudoWars 4ta Edicion")
   st.subheader("Juega para ganar, juega para divertirte, juega en LudoWars")
   st.markdown("Agrega tus datos para mostrarte el itinario. ¡Éxito en el torneo!")