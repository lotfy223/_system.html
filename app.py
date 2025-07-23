import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Data Science Educational Platform | منصة تعليم علم البيانات",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for orange theme and Arabic fonts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Tajawal:wght@300;400;500;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #fff5f0 0%, #ffe4d6 100%);
    }
    
    .stApp {
        font-family: 'Cairo', 'Tajawal', sans-serif;
    }
    
    .arabic-text {
        font-family: 'Cairo', 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .english-text {
        font-family: 'Cairo', sans-serif;
        direction: ltr;
        text-align: left;
    }
    
    .orange-header {
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .process-step {
        background: #fff;
        border-left: 4px solid #ff6b35;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .visualization-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stSelectbox > div > div {
        background-color: #fff5f0;
    }
</style>
""", unsafe_allow_html=True)

# Language selection
def get_language():
    return st.sidebar.selectbox(
        "🌐 Language / اللغة",
        ["English", "العربية"],
        key="language"
    )

# Translation dictionary
translations = {
    "English": {
        "title": "Data Science Educational Platform",
        "subtitle": "Interactive Learning Experience",
        "nav_home": "🏠 Home",
        "nav_visuals": "📊 Visualizations", 
        "nav_upload": "📤 Upload Images",
        "nav_about": "ℹ️ About",
        "ds_definition": "Data Science is a multidisciplinary field that uses scientific methods, processes, algorithms, and tools to extract knowledge and insights from structured and unstructured data.",
        "ds_process": "Data Science Process",
        "step1": "1. Define the Problem",
        "step2": "2. Get Data (from Lakehouse)",
        "step3": "3. Prepare/Clean Data", 
        "step4": "4. Train Models",
        "step5": "5. Generate Insights",
        "correlation_title": "Correlation Heatmap",
        "correlation_desc": "This visualization shows the correlation between different variables in the penguins dataset. Darker colors indicate stronger correlations.",
        "pca_title": "PCA Dimensionality Reduction",
        "pca_desc": "Principal Component Analysis reduces the dimensionality of data while preserving most of the variance.",
        "boxplot_title": "Box Plot & Histogram",
        "boxplot_desc": "Box plots show the distribution of data including median, quartiles, and outliers.",
        "scatter_title": "House Size vs Price",
        "scatter_desc": "This scatter plot shows the relationship between house size and price.",
        "line_title": "House Prices Over Time",
        "line_desc": "This line chart shows how house prices changed from 2020 to 2022.",
        "pairplot_title": "Pairplot Analysis",
        "pairplot_desc": "Pairplot shows relationships between all pairs of variables in the dataset.",
        "stats_title": "Descriptive Statistics",
        "stats_desc": "Summary statistics provide insights into the central tendency and spread of the data."
    },
    "العربية": {
        "title": "منصة تعليم علم البيانات",
        "subtitle": "تجربة تعلم تفاعلية",
        "nav_home": "🏠 الرئيسية",
        "nav_visuals": "📊 التصورات البيانية",
        "nav_upload": "📤 رفع الصور",
        "nav_about": "ℹ️ حول",
        "ds_definition": "علم البيانات هو مجال متعدد التخصصات يستخدم الأساليب والعمليات والخوارزميات والأدوات العلمية لاستخراج المعرفة والرؤى من البيانات المنظمة وغير المنظمة.",
        "ds_process": "عملية علم البيانات",
        "step1": "١. تحديد المشكلة",
        "step2": "٢. الحصول على البيانات (من مستودع البيانات)",
        "step3": "٣. تحضير وتنظيف البيانات",
        "step4": "٤. تدريب النماذج",
        "step5": "٥. توليد الرؤى",
        "correlation_title": "خريطة الارتباط الحرارية",
        "correlation_desc": "يُظهر هذا التصور الارتباط بين المتغيرات المختلفة في بيانات البطاريق. الألوان الداكنة تشير إلى ارتباطات أقوى.",
        "pca_title": "تقليل الأبعاد باستخدام PCA",
        "pca_desc": "تحليل المكونات الرئيسية يقلل من أبعاد البيانات مع الحفاظ على معظم التباين.",
        "boxplot_title": "مخطط الصندوق والرسم البياني",
        "boxplot_desc": "مخططات الصندوق تُظهر توزيع البيانات بما في ذلك الوسيط والأرباع والقيم الشاذة.",
        "scatter_title": "حجم المنزل مقابل السعر",
        "scatter_desc": "يُظهر هذا المخطط المبعثر العلاقة بين حجم المنزل والسعر.",
        "line_title": "أسعار المنازل عبر الزمن",
        "line_desc": "يُظهر هذا المخطط الخطي كيف تغيرت أسعار المنازل من ٢٠٢٠ إلى ٢٠٢٢.",
        "pairplot_title": "تحليل المخططات المزدوجة",
        "pairplot_desc": "المخططات المزدوجة تُظهر العلاقات بين جميع أزواج المتغيرات في مجموعة البيانات.",
        "stats_title": "الإحصائيات الوصفية",
        "stats_desc": "الإحصائيات الملخصة توفر رؤى حول النزعة المركزية وانتشار البيانات."
    }
}

def main():
    language = get_language()
    t = translations[language]
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation / التنقل",
        [t["nav_home"], t["nav_visuals"], t["nav_upload"], t["nav_about"]]
    )
    
    if page == t["nav_home"]:
        show_home_page(language, t)
    elif page == t["nav_visuals"]:
        show_visualizations_page(language, t)
    elif page == t["nav_upload"]:
        show_upload_page(language, t)
    elif page == t["nav_about"]:
        show_about_page(language, t)

def show_home_page(language, t):
    # Header
    st.markdown(f"""
    <div class="orange-header">
        <h1>{t["title"]}</h1>
        <h3>{t["subtitle"]}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Science Definition
    text_class = "arabic-text" if language == "العربية" else "english-text"
    st.markdown(f"""
    <div class="{text_class}">
        <h2>📊 What is Data Science? / ما هو علم البيانات؟</h2>
        <p style="font-size: 1.2em; line-height: 1.6;">{t["ds_definition"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Science Process
    st.markdown(f"""
    <div class="{text_class}">
        <h2>🔄 {t["ds_process"]}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Process steps
    steps = [t["step1"], t["step2"], t["step3"], t["step4"], t["step5"]]
    for step in steps:
        st.markdown(f"""
        <div class="process-step {text_class}">
            <h4>{step}</h4>
        </div>
        """, unsafe_allow_html=True)

def show_visualizations_page(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="orange-header">
        <h1>📊 {t["nav_visuals"]}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Visualization selection
    viz_options = [
        t["correlation_title"],
        t["pca_title"],
        t["boxplot_title"],
        t["scatter_title"],
        t["line_title"],
        t["pairplot_title"],
        t["stats_title"]
    ]

    selected_viz = st.selectbox("Choose Visualization / اختر التصور", viz_options)

    if selected_viz == t["correlation_title"]:
        show_correlation_heatmap(language, t)
    elif selected_viz == t["pca_title"]:
        show_pca_analysis(language, t)
    elif selected_viz == t["boxplot_title"]:
        show_boxplot_histogram(language, t)
    elif selected_viz == t["scatter_title"]:
        show_scatter_plot(language, t)
    elif selected_viz == t["line_title"]:
        show_line_chart(language, t)
    elif selected_viz == t["pairplot_title"]:
        show_pairplot(language, t)
    elif selected_viz == t["stats_title"]:
        show_descriptive_stats(language, t)

def show_correlation_heatmap(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["correlation_title"]}</h3>
            <p>{t["correlation_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load penguins data
    try:
        penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')

        # Show code
        st.code("""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')
corr = penguins.corr()
sns.heatmap(corr, annot=True)
plt.show()
        """, language='python')

        # Create correlation heatmap
        numeric_cols = penguins.select_dtypes(include=[np.number]).columns
        corr = penguins[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='Oranges', center=0, ax=ax)
        ax.set_title(t["correlation_title"], fontsize=16, pad=20)
        st.pyplot(fig)

        # Show data sample
        st.subheader("Data Sample / عينة البيانات")
        st.dataframe(penguins.head())

    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_pca_analysis(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["pca_title"]}</h3>
            <p>{t["pca_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')
        penguins_clean = penguins.dropna()

        # Show code
        st.code("""
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

penguins = penguins.dropna()
X = penguins.select_dtypes(include=[np.number])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
        """, language='python')

        # Prepare data for PCA
        X = penguins_clean.select_dtypes(include=[np.number])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        # Create PCA plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # PCA scatter plot
        if 'Species' in penguins_clean.columns:
            species = penguins_clean['Species']
            for i, spec in enumerate(species.unique()):
                mask = species == spec
                ax1.scatter(X_pca[mask, 0], X_pca[mask, 1],
                           label=spec, alpha=0.7, s=50)
            ax1.legend()
        else:
            ax1.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.7, s=50, color='orange')

        ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
        ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
        ax1.set_title('PCA Results')

        # Explained variance plot
        ax2.bar(['PC1', 'PC2'], pca.explained_variance_ratio_, color=['#ff6b35', '#f7931e'])
        ax2.set_ylabel('Explained Variance Ratio')
        ax2.set_title('Explained Variance by Component')

        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error in PCA analysis: {e}")

def show_boxplot_histogram(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["boxplot_title"]}</h3>
            <p>{t["boxplot_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Height data
    heights = [63, 64, 66, 67, 68, 69, 71, 72, 73, 55, 75]

    # Show code
    st.code("""
heights = [63, 64, 66, 67, 68, 69, 71, 72, 73, 55, 75]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Box plot
ax1.boxplot(heights, patch_artist=True,
           boxprops=dict(facecolor='orange', alpha=0.7))
ax1.set_ylabel('Height (inches)')
ax1.set_title('Box Plot of Heights')

# Histogram
ax2.hist(heights, bins=8, color='orange', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Height (inches)')
ax2.set_ylabel('Frequency')
ax2.set_title('Histogram of Heights')
    """, language='python')

    # Create plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Box plot
    box_plot = ax1.boxplot(heights, patch_artist=True)
    box_plot['boxes'][0].set_facecolor('#ff6b35')
    box_plot['boxes'][0].set_alpha(0.7)
    ax1.set_ylabel('Height (inches)')
    ax1.set_title('Box Plot of Heights')
    ax1.grid(True, alpha=0.3)

    # Histogram
    ax2.hist(heights, bins=8, color='#ff6b35', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Height (inches)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Histogram of Heights')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Statistics
    st.subheader("Statistics / الإحصائيات")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean / المتوسط", f"{np.mean(heights):.1f}")
    with col2:
        st.metric("Median / الوسيط", f"{np.median(heights):.1f}")
    with col3:
        st.metric("Std Dev / الانحراف المعياري", f"{np.std(heights):.1f}")
    with col4:
        st.metric("Range / المدى", f"{max(heights) - min(heights)}")

def show_scatter_plot(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["scatter_title"]}</h3>
            <p>{t["scatter_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Generate synthetic house data
    np.random.seed(42)
    house_sizes = np.random.randint(1000, 3000, size=50)
    noise = np.random.normal(0, 20000, size=50)
    house_prices = house_sizes * 100 + noise

    # Show code
    st.code("""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
house_sizes = np.random.randint(1000, 3000, size=50)
noise = np.random.normal(0, 20000, size=50)
house_prices = house_sizes * 100 + noise

plt.figure(figsize=(10, 6))
plt.scatter(house_sizes, house_prices, alpha=0.7, color='orange', s=60)
plt.xlabel('House Size (sq ft)')
plt.ylabel('House Price ($)')
plt.title('House Size vs Price')

# Add trend line
z = np.polyfit(house_sizes, house_prices, 1)
p = np.poly1d(z)
plt.plot(house_sizes, p(house_sizes), "r--", alpha=0.8)
    """, language='python')

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(house_sizes, house_prices, alpha=0.7, color='#ff6b35', s=60)
    ax.set_xlabel('House Size (sq ft)')
    ax.set_ylabel('House Price ($)')
    ax.set_title('House Size vs Price')

    # Add trend line
    z = np.polyfit(house_sizes, house_prices, 1)
    p = np.poly1d(z)
    ax.plot(house_sizes, p(house_sizes), "r--", alpha=0.8, linewidth=2)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    # Correlation coefficient
    correlation = np.corrcoef(house_sizes, house_prices)[0, 1]
    st.metric("Correlation Coefficient / معامل الارتباط", f"{correlation:.3f}")

def show_line_chart(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["line_title"]}</h3>
            <p>{t["line_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Generate time series data
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=30*i) for i in range(36)]  # 3 years, monthly

    # Create trend with some noise
    np.random.seed(42)
    base_price = 300000
    trend = np.linspace(0, 50000, 36)  # Increasing trend
    seasonal = 10000 * np.sin(np.arange(36) * 2 * np.pi / 12)  # Seasonal pattern
    noise = np.random.normal(0, 5000, 36)
    prices = base_price + trend + seasonal + noise

    # Show code
    st.code("""
from datetime import datetime, timedelta
import numpy as np

start_date = datetime(2020, 1, 1)
dates = [start_date + timedelta(days=30*i) for i in range(36)]

base_price = 300000
trend = np.linspace(0, 50000, 36)
seasonal = 10000 * np.sin(np.arange(36) * 2 * np.pi / 12)
noise = np.random.normal(0, 5000, 36)
prices = base_price + trend + seasonal + noise

plt.figure(figsize=(12, 6))
plt.plot(dates, prices, marker='o', color='orange', linewidth=2, markersize=4)
plt.xlabel('Date')
plt.ylabel('Average House Price ($)')
plt.title('House Prices Over Time (2020-2022)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
    """, language='python')

    # Create line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, prices, marker='o', color='#ff6b35', linewidth=2, markersize=4)
    ax.set_xlabel('Date')
    ax.set_ylabel('Average House Price ($)')
    ax.set_title('House Prices Over Time (2020-2022)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Price change metrics
    price_change = prices[-1] - prices[0]
    price_change_pct = (price_change / prices[0]) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Starting Price / السعر الابتدائي", f"${prices[0]:,.0f}")
    with col2:
        st.metric("Ending Price / السعر النهائي", f"${prices[-1]:,.0f}")
    with col3:
        st.metric("Total Change / التغيير الإجمالي", f"{price_change_pct:+.1f}%")

def show_pairplot(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["pairplot_title"]}</h3>
            <p>{t["pairplot_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        # Load penguins data
        penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')
        penguins_clean = penguins.dropna()

        # Show code
        st.code("""
import seaborn as sns
import pandas as pd

penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')
penguins_clean = penguins.dropna()

# Select numeric columns for pairplot
numeric_cols = penguins_clean.select_dtypes(include=[np.number]).columns
sns.pairplot(penguins_clean[numeric_cols], diag_kind='hist')
plt.show()
        """, language='python')

        # Create pairplot with numeric columns only
        numeric_cols = penguins_clean.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            # Limit to first 4 numeric columns for better visualization
            cols_to_plot = numeric_cols[:4] if len(numeric_cols) > 4 else numeric_cols

            fig = plt.figure(figsize=(12, 10))

            # Create a custom pairplot
            n_vars = len(cols_to_plot)
            for i in range(n_vars):
                for j in range(n_vars):
                    plt.subplot(n_vars, n_vars, i * n_vars + j + 1)

                    if i == j:
                        # Diagonal: histogram
                        plt.hist(penguins_clean[cols_to_plot[i]], bins=20,
                                color='#ff6b35', alpha=0.7, edgecolor='black')
                        plt.xlabel(cols_to_plot[i])
                    else:
                        # Off-diagonal: scatter plot
                        plt.scatter(penguins_clean[cols_to_plot[j]],
                                  penguins_clean[cols_to_plot[i]],
                                  alpha=0.6, color='#ff6b35', s=20)
                        plt.xlabel(cols_to_plot[j])
                        plt.ylabel(cols_to_plot[i])

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Not enough numeric columns for pairplot")

    except Exception as e:
        st.error(f"Error creating pairplot: {e}")

def show_descriptive_stats(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="visualization-container">
        <div class="{text_class}">
            <h3>{t["stats_title"]}</h3>
            <p>{t["stats_desc"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        # Load penguins data
        penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')

        # Show code
        st.code("""
import pandas as pd

penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')

# Descriptive statistics
print(penguins.describe())

# Additional statistics
print("\\nData Info:")
print(f"Shape: {penguins.shape}")
print(f"Missing values: {penguins.isnull().sum().sum()}")
        """, language='python')

        # Display descriptive statistics
        st.subheader("Descriptive Statistics / الإحصائيات الوصفية")
        st.dataframe(penguins.describe())

        # Additional info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows / الصفوف", penguins.shape[0])
        with col2:
            st.metric("Columns / الأعمدة", penguins.shape[1])
        with col3:
            st.metric("Missing Values / القيم المفقودة", penguins.isnull().sum().sum())
        with col4:
            st.metric("Numeric Columns / الأعمدة الرقمية",
                     len(penguins.select_dtypes(include=[np.number]).columns))

        # Data types
        st.subheader("Data Types / أنواع البيانات")
        dtypes_df = pd.DataFrame({
            'Column': penguins.columns,
            'Data Type': penguins.dtypes.astype(str),
            'Non-Null Count': penguins.count()
        })
        st.dataframe(dtypes_df)

        # Sample data
        st.subheader("Sample Data / عينة البيانات")
        st.dataframe(penguins.head(10))

    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_upload_page(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="orange-header">
        <h1>📤 {t["nav_upload"]}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="{text_class}">
        <h3>Upload Images / رفع الصور</h3>
        <p>Upload your images for analysis or documentation / ارفع صورك للتحليل أو التوثيق</p>
    </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose images / اختر الصور",
        type=['png', 'jpg', 'jpeg', 'gif'],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s) / تم رفع {len(uploaded_files)} ملف")

        # Display uploaded images
        cols = st.columns(3)
        for idx, uploaded_file in enumerate(uploaded_files):
            with cols[idx % 3]:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_column_width=True)

                # Image info
                st.write(f"**Size / الحجم:** {image.size}")
                st.write(f"**Format / التنسيق:** {image.format}")
                st.write(f"**Mode / النمط:** {image.mode}")

    # Drag and drop area simulation
    st.markdown("""
    <div style="border: 2px dashed #ff6b35; border-radius: 10px; padding: 2rem; text-align: center; margin: 2rem 0;">
        <h4>📁 Drag & Drop Area</h4>
        <p>منطقة السحب والإفلات</p>
        <p>Use the file uploader above to select images</p>
        <p>استخدم أداة رفع الملفات أعلاه لاختيار الصور</p>
    </div>
    """, unsafe_allow_html=True)

def show_about_page(language, t):
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="orange-header">
        <h1>ℹ️ {t["nav_about"]}</h1>
    </div>
    """, unsafe_allow_html=True)

    if language == "العربية":
        st.markdown(f"""
        <div class="{text_class}">
            <h3>حول المنصة</h3>
            <p>هذه منصة تعليمية تفاعلية لعلم البيانات تهدف إلى:</p>
            <ul>
                <li>تعليم مفاهيم علم البيانات الأساسية</li>
                <li>عرض التصورات البيانية المختلفة</li>
                <li>توفير أمثلة عملية بالكود</li>
                <li>دعم اللغتين العربية والإنجليزية</li>
            </ul>

            <h3>التقنيات المستخدمة</h3>
            <ul>
                <li>🐍 Python</li>
                <li>📊 Streamlit</li>
                <li>🐼 Pandas</li>
                <li>📈 Matplotlib & Seaborn</li>
                <li>🤖 Scikit-learn</li>
                <li>🎨 CSS للتصميم</li>
            </ul>

            <h3>الميزات</h3>
            <ul>
                <li>✅ واجهة ثنائية اللغة</li>
                <li>✅ تصورات بيانية تفاعلية</li>
                <li>✅ أمثلة كود قابلة للتنفيذ</li>
                <li>✅ رفع الصور</li>
                <li>✅ تصميم متجاوب</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="{text_class}">
            <h3>About the Platform</h3>
            <p>This is an interactive educational platform for Data Science that aims to:</p>
            <ul>
                <li>Teach fundamental Data Science concepts</li>
                <li>Showcase different data visualizations</li>
                <li>Provide practical examples with code</li>
                <li>Support both Arabic and English languages</li>
            </ul>

            <h3>Technologies Used</h3>
            <ul>
                <li>🐍 Python</li>
                <li>📊 Streamlit</li>
                <li>🐼 Pandas</li>
                <li>📈 Matplotlib & Seaborn</li>
                <li>🤖 Scikit-learn</li>
                <li>🎨 CSS for styling</li>
            </ul>

            <h3>Features</h3>
            <ul>
                <li>✅ Bilingual interface</li>
                <li>✅ Interactive data visualizations</li>
                <li>✅ Executable code examples</li>
                <li>✅ Image upload functionality</li>
                <li>✅ Responsive design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Contact info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h4>📧 Contact / التواصل</h4>
        <p>For questions or suggestions / للأسئلة أو الاقتراحات</p>
        <p>📧 contact@datascience-edu.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
