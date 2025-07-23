**User:**

<task>
# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from datetime import datetime, timedelta
import random
import matplotlib.dates as mdates

# ---------------------------------------------
# 1. Load and explore the penguins dataset
# ---------------------------------------------
penguins = pd.read_csv('https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/penguins.csv')
print("Initial Dataset:\n", penguins.head())

# Drop missing values
penguins = penguins.dropna()

# ---------------------------------------------
# 2. Correlation Heatmap
# ---------------------------------------------
corr = penguins.corr(numeric_only=True)
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap of Penguin Features")
plt.show()

# ---------------------------------------------
# 3. Principal Component Analysis (PCA)
# ---------------------------------------------
X = penguins.drop('Species', axis=1)
y = penguins['Species']

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(8, 6))
for color, target in zip(['navy', 'turquoise', 'darkorange'], penguins['Species'].unique()):
    plt.scatter(X_pca[y == target, 0], X_pca[y == target, 1], color=color, label=target, alpha=0.7)
plt.legend(loc='best')
plt.title('PCA of Penguins Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# ---------------------------------------------
# 4. Boxplot & Histogram (Heights)
# ---------------------------------------------
heights_in_inches = [63, 64, 66, 67, 68, 69, 71, 72, 73, 55, 75]
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Boxplot
axs[0].boxplot(heights_in_inches, whis=0.5)
axs[0].set_title('Box plot of heights')

# Histogram
bins = range(min(heights_in_inches), max(heights_in_inches) + 5, 5)
axs[1].hist(heights_in_inches, bins=bins, alpha=0.6, color='orange')
axs[1].set_title('Frequency distribution of heights')
axs[1].set_xlabel('Height (in)')
axs[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# ---------------------------------------------
# 5. Scatter Plot: House Size vs Price
# ---------------------------------------------
np.random.seed(0)
house_sizes = np.random.randint(1000, 3000, size=50)
house_prices = house_sizes * 100 + np.random.normal(0, 20000, size=50)

plt.scatter(house_sizes, house_prices, color='teal')
plt.title('House Prices vs Size')
plt.xlabel('Size (sqft)')
plt.ylabel('Price ($)')
plt.show()

# ---------------------------------------------
# 6. Time Series Plot: House Prices Over Time
# ---------------------------------------------
dates = [datetime(2020, 1, 1) + timedelta(days=30 * i) for i in range(36)]
prices = [200000 + 5000 * i + random.randint(-5000, 5000) for i in range(36)]

plt.figure(figsize=(10, 5))
plt.plot(dates, prices, color='purple')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gcf().autofmt_xdate()

plt.title('House Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.show()

# ---------------------------------------------
# 7. Pair Plot for Housing Data
# ---------------------------------------------
house_data = {
    'Size': [1000, 2000, 3000, 1500, 1200],
    'Bedrooms': [2, 4, 3, 2, 1],
    'Age': [5, 10, 2, 6, 4],
    'Price': [200000, 400000, 350000, 220000, 150000]
}
df_house = pd.DataFrame(house_data)
sns.pairplot(df_house)
plt.suptitle("Pair Plot of Housing Data", y=1.02)
plt.show()

# ---------------------------------------------
# 8. Descriptive Statistics
# ---------------------------------------------
people_df = pd.DataFrame({
    'Height_in_cm': [170, 180, 175, 185, 178],
    'Weight_in_kg': [65, 75, 70, 80, 72],
    'Age_in_years': [25, 30, 28, 35, 32]
})
desc_stats = people_df.describe()
print("Descriptive Statistics:\n", desc_stats)
</task>
<environment_details>
# VSCode Visible Files
(No visible files)

# VSCode Open Tabs
(No open tabs)

# Current Time
7/22/2025, 8:56:37 PM (Africa/Cairo, UTC+3:00)

# Current Context Size (Tokens)
(Not available)

# Current Mode
<slug>ask</slug>
<name>咨询</name>


NOTE: You are currently in '咨询' mode, which does not allow write operations. To write files, the user will need to switch to a mode that supports file writing, such as '代码' mode.

# Current Working Directory (c:/Users/AL - ELMIA/Downloads/Compressed/موقع) Files
未找到文件。
</environment_details>

