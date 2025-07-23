# Data Science Educational Platform | منصة تعليم علم البيانات

An interactive bilingual (Arabic/English) web-based educational platform for Data Science concepts and visualizations.

## 🌟 Features | الميزات

- **Bilingual Support** | **دعم ثنائي اللغة**: Complete Arabic and English interface
- **Interactive Visualizations** | **تصورات تفاعلية**: 7 different data science visualizations
- **Real Code Examples** | **أمثلة كود حقيقية**: Executable Python code for each visualization
- **Orange Theme** | **تصميم برتقالي**: Beautiful orange-themed UI design
- **Image Upload** | **رفع الصور**: Drag and drop image upload functionality
- **Responsive Design** | **تصميم متجاوب**: Works on desktop and mobile devices

## 📊 Visualizations Included | التصورات المتضمنة

1. **Correlation Heatmap** | **خريطة الارتباط الحرارية**
   - Using penguins dataset from Microsoft Learning
   - Shows correlations between numeric variables

2. **PCA Dimensionality Reduction** | **تقليل الأبعاد باستخدام PCA**
   - Principal Component Analysis visualization
   - Scatter plot with explained variance

3. **Box Plot & Histogram** | **مخطط الصندوق والرسم البياني**
   - Height data distribution analysis
   - Side-by-side comparison

4. **Scatter Plot** | **المخطط المبعثر**
   - House size vs price relationship
   - Includes trend line and correlation

5. **Line Chart** | **المخطط الخطي**
   - House prices over time (2020-2022)
   - Time series with trend and seasonality

6. **Pairplot** | **المخططات المزدوجة**
   - Relationships between all variable pairs
   - Custom implementation for better control

7. **Descriptive Statistics** | **الإحصائيات الوصفية**
   - Complete statistical summary
   - Data types and missing values analysis

## 🚀 Quick Start | البدء السريع

### Prerequisites | المتطلبات المسبقة

- Python 3.8 or higher
- pip package manager

### Installation | التثبيت

1. **Clone or download the project** | **استنسخ أو حمل المشروع**
   ```bash
   # If using git
   git clone <repository-url>
   cd data-science-platform
   ```

2. **Install dependencies** | **ثبت المتطلبات**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application** | **شغل التطبيق**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser** | **افتح في المتصفح**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in terminal

## 🎯 Usage | الاستخدام

### Navigation | التنقل

- **Home** | **الرئيسية**: Introduction to Data Science and process overview
- **Visualizations** | **التصورات**: Interactive data visualizations with code
- **Upload Images** | **رفع الصور**: Upload and preview images
- **About** | **حول**: Platform information and technologies used

### Language Switching | تبديل اللغة

- Use the language selector in the sidebar
- استخدم منتقي اللغة في الشريط الجانبي
- All content dynamically updates based on selection

## 🛠️ Technologies Used | التقنيات المستخدمة

- **Frontend**: Streamlit with custom CSS
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn, Plotly
- **Machine Learning**: Scikit-learn
- **Image Processing**: Pillow (PIL)
- **Fonts**: Google Fonts (Cairo, Tajawal)

## 📁 Project Structure | هيكل المشروع

```
data-science-platform/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Customization | التخصيص

The platform is designed to be easily customizable:

- **Colors**: Modify the CSS in `app.py` to change the orange theme
- **Visualizations**: Add new visualization functions following the existing pattern
- **Languages**: Extend the `translations` dictionary for additional languages
- **Data**: Replace datasets with your own data sources

## 🔧 Development | التطوير

To add new visualizations:

1. Create a new function following the pattern: `show_your_visualization(language, t)`
2. Add the visualization to the `viz_options` list
3. Add corresponding translations to the `translations` dictionary
4. Include the function call in the visualization selection logic

## 📝 Code Examples | أمثلة الكود

Each visualization includes complete, executable Python code that users can copy and run independently. The code is displayed using Streamlit's `st.code()` function with syntax highlighting.

## 🌐 Browser Compatibility | توافق المتصفحات

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 📞 Support | الدعم

For questions, suggestions, or issues:
- Create an issue in the repository
- Contact: contact@datascience-edu.com

## 📄 License | الرخصة

This project is open source and available under the MIT License.

---

**Happy Learning! | تعلم سعيد!** 🎓📊
