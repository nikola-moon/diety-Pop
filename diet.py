import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DietyPop", page_icon="🍏", layout="wide")
st.title("DietyPop 🍏")
st.header("# 🍽️ Recettes ivoiriennes adaptées aux diabétiques")
st.write("**Une application pour vous aider à choisir des recettes saines et adaptée selon le type de diabète dont vous souffrez.**")

st.write("## Quelle est votre type de diabète ? :")
diabete_type = st.selectbox(
    "selectionne le type de diabète",
    ("diabète de type 1 ", "diabète de type 2", "diabète gestationnel")
)
plats_ivoiriens = ["Attiéké", "Foutou banane", "Placali", "Garba", "Sauce graine", "Sauce arachide", "Riz gras", "Kedjenou", "Soupe de poisson"]
plat_choisi = st.selectbox(
    "selectionne le plat que tu vas consommer",
    plats_ivoiriens
)
non_compris = st.text_input("si le plat n'est pas dans la liste, entrez le nom du plat: ")

# Récupérer la clé API depuis les secrets Streamlit
GOOGLE_API_KEY = st.secrets.get("google_api_key")
if not GOOGLE_API_KEY:
    st.error("La clé API Google n'est pas définie dans secrets.toml.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if st.button("Ce plat est-il adapté ?"):
    plat_final = non_compris if non_compris else plat_choisi
    st.info(f"Vérification de l'adaptation du plat : {plat_final}")
    prompt = f"Le plat {plat_final} est-il adapté pour une personne souffrant de {diabete_type} ?  Donne une réponse courte (oui ou non) et explique en 2 phrases."
    try:
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de l'appel à l'API : {e}")

if st.button("Génère une recette adaptée"):
    plat_final = non_compris if non_compris else plat_choisi
    prompt = f"Génère une recette ivoirienne pour {plat_final}, adaptée à une personne souffrant de {diabete_type}.  Donne le nom de la recette, la liste des ingrédients, et les instructions de préparation."
    try:
        response = model.generate_content(prompt)
        st.success("Recette générée avec succès !")
        st.write("Voici la recette :")
        st.write(response.text)
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de l'appel à l'API : {e}")




