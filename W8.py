import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# 1. Load Dataset
# ======================
try:
    df = pd.read_csv("metadata.csv")
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ metadata.csv not found. Please put it in the same folder as this notebook.")
except Exception as e:
    print(f"⚠️ Error loading dataset: {e}")

# Display first few rows
print(df.head())

# ======================
# 2. Explore Dataset
# ======================
print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# Drop rows with missing titles (they are important for analysis)
df = df.dropna(subset=['title'])

# ======================
# 3. Basic Analysis
# ======================
print("\nNumber of Papers per Year:")
df['publish_year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
papers_per_year = df['publish_year'].value_counts().sort_index()
print(papers_per_year)

# Top 10 journals by number of publications
top_journals = df['journal'].value_counts().head(10)
print("\nTop 10 Journals:\n", top_journals)

# ======================
# 4. Visualizations
# ======================
plt.figure(figsize=(10, 5))
papers_per_year.plot(kind='line', marker='o')
plt.title("Number of Papers Published Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.grid()
plt.show()

plt.figure(figsize=(10, 5))
top_journals.plot(kind='bar', color='skyblue')
plt.title("Top 10 Journals by Number of Publications")
plt.ylabel("Number of Papers")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df['publish_year'].dropna(), bins=20, kde=False)
plt.title("Distribution of Papers by Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ======================
# Streamlit App
# ======================

st.title("📚 CORD-19 Research Papers Analysis")
st.markdown("A simple interactive dashboard for exploring COVID-19 research metadata.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=['title'])
    df['publish_year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
    return df

df = load_data()

st.subheader("Dataset Overview")
st.write(df.head())

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Select Year", options=[None] + sorted(df['publish_year'].dropna().unique().tolist()))

if year_filter:
    df = df[df['publish_year'] == year_filter]

# Number of papers per year
papers_per_year = df['publish_year'].value_counts().sort_index()

st.subheader("Number of Papers per Year")
st.line_chart(papers_per_year)

# Top journals
top_journals = df['journal'].value_counts().head(10)
st.subheader("Top 10 Journals")
st.bar_chart(top_journals)

# Distribution histogram
st.subheader("Publication Year Distribution")
fig, ax = plt.subplots()
sns.histplot(df['publish_year'].dropna(), bins=20, ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

st.success("✅ Dashboard Loaded Successfully!")
