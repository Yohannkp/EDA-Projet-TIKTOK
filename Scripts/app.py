import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 📌 Charger les données
DATA_PATH = "tiktok_dataset.csv"  # 👉 Remplacez par votre fichier
df = pd.read_csv(DATA_PATH)

# 📌 Sélectionner les variables
numeric_columns = ['video_view_count', 'video_like_count', 'video_share_count', 'video_comment_count']
categorical_columns = ['claim_status', 'author_ban_status']

# 📌 Interface Streamlit
st.set_page_config(page_title="Analyse des Vidéos", layout="wide")
st.title("📊 Dashboard d'Analyse des Vidéos et de leur Bannissement")

# 📌 Filtres interactifs
st.sidebar.header("🎛️ Filtres")
selected_claim_status = st.sidebar.multiselect("Filtrer par Claim Status :", df["claim_status"].unique(), default=df["claim_status"].unique())
selected_ban_status = st.sidebar.multiselect("Filtrer par Ban Status :", df["author_ban_status"].unique(), default=df["author_ban_status"].unique())

# 📌 Appliquer les filtres
filtered_df = df[(df["claim_status"].isin(selected_claim_status)) & (df["author_ban_status"].isin(selected_ban_status))]

# 📌 Sélection d’une métrique à afficher
st.sidebar.header("📈 Choix des métriques")
selected_metric = st.sidebar.selectbox("Sélectionnez une métrique :", numeric_columns)

# 📌 Affichage des Graphiques Interactifs
st.subheader(f"📊 Distribution de {selected_metric}")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogramme
sns.histplot(filtered_df[selected_metric], bins=30, kde=True, ax=axes[0], color="royalblue")
axes[0].set_title(f"📈 Histogramme de {selected_metric}")

# Boxplot
sns.boxplot(x=filtered_df[selected_metric], ax=axes[1], color="orange")
axes[1].set_title(f"📊 Boxplot de {selected_metric}")

st.pyplot(fig)

# 📌 Comparaison entre deux variables
st.subheader("📊 Comparaison entre deux variables")
x_var = st.selectbox("Sélectionnez la variable X :", numeric_columns)
y_var = st.selectbox("Sélectionnez la variable Y :", numeric_columns)

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=filtered_df, x=x_var, y=y_var, alpha=0.5, color="green")
ax.set_title(f"Scatter Plot de {x_var} vs {y_var}")
st.pyplot(fig)

# 📌 Médiane des vues par statut de bannissement
st.subheader("⚠️ Médiane du Nombre de Vues par Statut de Bannissement")
median_views = df.groupby("author_ban_status")["video_view_count"].median().reset_index()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=median_views, x="author_ban_status", y="video_view_count", palette=["green", "orange", "red"], ax=ax)
ax.set_title("📊 Median view count by ban status")
ax.set_ylabel("Médiane des vues")
ax.set_xlabel("Statut de bannissement")
st.pyplot(fig)

# 📌 Heatmap de corrélation
st.subheader("🔍 Matrice de Corrélation")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

st.markdown("👀 *Cette application interactive permet d'explorer les tendances des vidéos en fonction des vues, likes et statuts des auteurs.* 🚀")
