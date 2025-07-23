import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, date, timedelta
import io
import base64
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
import json
import random
from PIL import Image
import requests

# Configure page with modern Odoo-like styling
st.set_page_config(
    page_title="نظام الإدارة المتكامل | Integrated Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for Odoo-like interface with 3D elements
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        font-family: 'Inter', 'Cairo', sans-serif;
    }
    
    /* Odoo-like Header */
    .odoo-header {
        background: linear-gradient(135deg, #714b67 0%, #5c4b7c 50%, #4a5d7a 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .odoo-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .odoo-header h1 {
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .odoo-header h2 {
        font-size: 1.3em;
        font-weight: 300;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* 3D Cards */
    .odoo-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
    }
    
    .odoo-card:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    /* 3D Metrics */
    .metric-3d {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 
            0 15px 30px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.3);
        margin: 1rem 0;
        position: relative;
        transform-style: preserve-3d;
        transition: all 0.3s ease;
    }
    
    .metric-3d:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(102, 126, 234, 0.6),
            inset 0 1px 0 rgba(255,255,255,0.5);
    }
    
    .metric-3d h3 {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-3d p {
        font-size: 1.1em;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        display: flex;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 0.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .nav-tab {
        flex: 1;
        padding: 1rem 2rem;
        text-align: center;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-weight: 600;
        position: relative;
        overflow: hidden;
    }
    
    .nav-tab:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-3px);
    }
    
    /* 3D Buttons */
    .btn-3d {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 
            0 10px 20px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.3);
        position: relative;
        transform-style: preserve-3d;
    }
    
    .btn-3d:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 30px rgba(102, 126, 234, 0.5),
            inset 0 1px 0 rgba(255,255,255,0.5);
    }
    
    .btn-3d:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Data Tables */
    .data-table-3d {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Success/Error Messages */
    .success-3d {
        background: linear-gradient(145deg, #10b981, #059669);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
        margin: 1rem 0;
    }
    
    .error-3d {
        background: linear-gradient(145deg, #ef4444, #dc2626);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(239, 68, 68, 0.3);
        margin: 1rem 0;
    }
    
    /* Loading Animation */
    .loading-3d {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Arabic Text Support */
    .arabic-text {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .english-text {
        font-family: 'Inter', sans-serif;
        direction: ltr;
        text-align: left;
    }
    
    /* Module Icons */
    .module-icon {
        font-size: 3em;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .odoo-header h1 {
            font-size: 2em;
        }
        
        .nav-tabs {
            flex-direction: column;
        }
        
        .metric-3d h3 {
            font-size: 2em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for all modules
def initialize_odoo_system():
    """Initialize all system modules"""
    
    # Accounting Module
    if 'accounts' not in st.session_state:
        st.session_state.accounts = pd.DataFrame([
            {'رقم الحساب': '1001', 'اسم الحساب': 'النقدية', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد': 500000.0},
            {'رقم الحساب': '1002', 'اسم الحساب': 'البنك', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد': 1000000.0},
            {'رقم الحساب': '1101', 'اسم الحساب': 'العملاء', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد': 250000.0},
            {'رقم الحساب': '1201', 'اسم الحساب': 'المخزون', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد': 300000.0},
            {'رقم الحساب': '2001', 'اسم الحساب': 'الموردين', 'نوع الحساب': 'الخصوم المتداولة', 'الرصيد': 150000.0},
            {'رقم الحساب': '3001', 'اسم الحساب': 'رأس المال', 'نوع الحساب': 'رأس المال', 'الرصيد': 1000000.0},
            {'رقم الحساب': '4001', 'اسم الحساب': 'المبيعات', 'نوع الحساب': 'الإيرادات', 'الرصيد': 800000.0},
            {'رقم الحساب': '5001', 'اسم الحساب': 'تكلفة البضاعة المباعة', 'نوع الحساب': 'المصروفات', 'الرصيد': 400000.0},
        ])
    
    # CRM Module
    if 'customers' not in st.session_state:
        st.session_state.customers = pd.DataFrame([
            {'رقم العميل': 'C001', 'اسم العميل': 'شركة الأمل التجارية', 'الهاتف': '+966501234567', 'البريد': 'info@amal.com', 'الرصيد': 25000.0, 'الحالة': 'نشط'},
            {'رقم العميل': 'C002', 'اسم العميل': 'مؤسسة النجاح', 'الهاتف': '+966507654321', 'البريد': 'contact@najah.com', 'الرصيد': 15000.0, 'الحالة': 'نشط'},
            {'رقم العميل': 'C003', 'اسم العميل': 'شركة التطوير الحديث', 'الهاتف': '+966512345678', 'البريد': 'info@modern.com', 'الرصيد': 35000.0, 'الحالة': 'نشط'},
        ])
    
    # Sales Module
    if 'sales_orders' not in st.session_state:
        st.session_state.sales_orders = pd.DataFrame([
            {'رقم الطلب': 'SO001', 'العميل': 'شركة الأمل التجارية', 'التاريخ': '2024-01-15', 'المبلغ': 50000.0, 'الحالة': 'مؤكد'},
            {'رقم الطلب': 'SO002', 'العميل': 'مؤسسة النجاح', 'التاريخ': '2024-01-16', 'المبلغ': 30000.0, 'الحالة': 'مسودة'},
            {'رقم الطلب': 'SO003', 'العميل': 'شركة التطوير الحديث', 'التاريخ': '2024-01-17', 'المبلغ': 75000.0, 'الحالة': 'مؤكد'},
        ])
    
    # Inventory Module
    if 'products' not in st.session_state:
        st.session_state.products = pd.DataFrame([
            {'كود المنتج': 'P001', 'اسم المنتج': 'لابتوب Dell XPS', 'الفئة': 'إلكترونيات', 'الكمية': 50, 'السعر': 4500.0, 'التكلفة': 3500.0},
            {'كود المنتج': 'P002', 'اسم المنتج': 'طابعة HP LaserJet', 'الفئة': 'إلكترونيات', 'الكمية': 25, 'السعر': 1200.0, 'التكلفة': 900.0},
            {'كود المنتج': 'P003', 'اسم المنتج': 'كرسي مكتبي', 'الفئة': 'أثاث', 'الكمية': 100, 'السعر': 800.0, 'التكلفة': 600.0},
            {'كود المنتج': 'P004', 'اسم المنتج': 'مكتب خشبي', 'الفئة': 'أثاث', 'الكمية': 30, 'السعر': 2500.0, 'التكلفة': 1800.0},
        ])
    
    # HR Module
    if 'employees' not in st.session_state:
        st.session_state.employees = pd.DataFrame([
            {'رقم الموظف': 'E001', 'الاسم': 'أحمد محمد علي', 'القسم': 'المحاسبة', 'المنصب': 'محاسب أول', 'الراتب': 8000.0, 'تاريخ التعيين': '2020-01-15'},
            {'رقم الموظف': 'E002', 'الاسم': 'فاطمة أحمد سعد', 'القسم': 'المبيعات', 'المنصب': 'مدير مبيعات', 'الراتب': 12000.0, 'تاريخ التعيين': '2019-03-10'},
            {'رقم الموظف': 'E003', 'الاسم': 'خالد عبدالله محمد', 'القسم': 'تقنية المعلومات', 'المنصب': 'مطور برمجيات', 'الراتب': 10000.0, 'تاريخ التعيين': '2021-06-01'},
            {'رقم الموظف': 'E004', 'الاسم': 'نورا سعد العتيبي', 'القسم': 'الموارد البشرية', 'المنصب': 'أخصائي موارد بشرية', 'الراتب': 7500.0, 'تاريخ التعيين': '2022-02-20'},
        ])
    
    # Purchase Module
    if 'suppliers' not in st.session_state:
        st.session_state.suppliers = pd.DataFrame([
            {'رقم المورد': 'S001', 'اسم المورد': 'شركة التقنية المتقدمة', 'الهاتف': '+966501111111', 'البريد': 'info@tech.com', 'الرصيد': 45000.0},
            {'رقم المورد': 'S002', 'اسم المورد': 'مؤسسة الأثاث الحديث', 'الهاتف': '+966502222222', 'البريد': 'sales@furniture.com', 'الرصيد': 25000.0},
            {'رقم المورد': 'S003', 'اسم المورد': 'شركة المواد الخام', 'الهاتف': '+966503333333', 'البريد': 'contact@materials.com', 'الرصيد': 35000.0},
        ])

# Language selection
def get_language():
    return st.sidebar.selectbox(
        "🌐 Language / اللغة",
        ["العربية", "English"],
        key="language"
    )

# Translation dictionary
translations = {
    "العربية": {
        "title": "نظام الإدارة المتكامل",
        "subtitle": "حلول أعمال شاملة مع تقنية ثلاثية الأبعاد",
        "dashboard": "🏠 لوحة التحكم",
        "accounting": "💰 المحاسبة",
        "sales": "📈 المبيعات", 
        "crm": "👥 إدارة العملاء",
        "inventory": "📦 المخزون",
        "hr": "👨‍💼 الموارد البشرية",
        "purchase": "🛒 المشتريات",
        "reports": "📊 التقارير"
    },
    "English": {
        "title": "Integrated Management System",
        "subtitle": "Comprehensive Business Solutions with 3D Technology",
        "dashboard": "🏠 Dashboard",
        "accounting": "💰 Accounting",
        "sales": "📈 Sales",
        "crm": "👥 CRM",
        "inventory": "📦 Inventory", 
        "hr": "👨‍💼 Human Resources",
        "purchase": "🛒 Purchase",
        "reports": "📊 Reports"
    }
}

def main():
    # Initialize system
    initialize_odoo_system()
    
    language = get_language()
    t = translations[language]
    
    # Header with 3D effect
    st.markdown(f"""
    <div class="odoo-header">
        <h1>🏢 {t["title"]}</h1>
        <h2>{t["subtitle"]}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("---")
    selected_module = st.sidebar.radio(
        "الوحدات / Modules",
        [
            t["dashboard"], t["accounting"], t["sales"], t["crm"],
            t["inventory"], t["hr"], t["purchase"], t["reports"]
        ]
    )
    
    # Route to modules
    if selected_module == t["dashboard"]:
        show_3d_dashboard(language, t)
    elif selected_module == t["accounting"]:
        show_accounting_module(language, t)
    elif selected_module == t["sales"]:
        show_sales_module(language, t)
    elif selected_module == t["crm"]:
        show_crm_module(language, t)
    elif selected_module == t["inventory"]:
        show_inventory_module(language, t)
    elif selected_module == t["hr"]:
        show_hr_module(language, t)
    elif selected_module == t["purchase"]:
        show_purchase_module(language, t)
    elif selected_module == t["reports"]:
        show_advanced_reports(language, t)

def show_3d_dashboard(language, t):
    """3D Dashboard with high-quality visualizations"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>🏠 {t["dashboard"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Indicators with 3D effects
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_revenue = st.session_state.sales_orders['المبلغ'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <div class="module-icon">💰</div>
            <h3>{total_revenue:,.0f}</h3>
            <p>إجمالي المبيعات<br>Total Sales</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_customers = len(st.session_state.customers)
        st.markdown(f"""
        <div class="metric-3d">
            <div class="module-icon">👥</div>
            <h3>{total_customers}</h3>
            <p>العملاء<br>Customers</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_products = len(st.session_state.products)
        st.markdown(f"""
        <div class="metric-3d">
            <div class="module-icon">📦</div>
            <h3>{total_products}</h3>
            <p>المنتجات<br>Products</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_employees = len(st.session_state.employees)
        st.markdown(f"""
        <div class="metric-3d">
            <div class="module-icon">👨‍💼</div>
            <h3>{total_employees}</h3>
            <p>الموظفين<br>Employees</p>
        </div>
        """, unsafe_allow_html=True)

    # 3D Charts Section
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 التحليلات ثلاثية الأبعاد / 3D Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # 3D Sales Trend
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        sales_data = pd.DataFrame({
            'التاريخ': dates,
            'المبيعات': np.random.normal(15000, 3000, len(dates)),
            'الأرباح': np.random.normal(5000, 1000, len(dates))
        })

        fig = go.Figure()

        # Add 3D surface for sales
        fig.add_trace(go.Scatter3d(
            x=sales_data.index,
            y=sales_data['المبيعات'],
            z=sales_data['الأرباح'],
            mode='markers+lines',
            marker=dict(
                size=8,
                color=sales_data['الأرباح'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="الأرباح")
            ),
            line=dict(color='rgb(102, 126, 234)', width=6),
            name='اتجاه المبيعات'
        ))

        fig.update_layout(
            title='اتجاه المبيعات ثلاثي الأبعاد / 3D Sales Trend',
            scene=dict(
                xaxis_title='الأيام / Days',
                yaxis_title='المبيعات / Sales',
                zaxis_title='الأرباح / Profit',
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)'),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 3D Product Categories
        categories = st.session_state.products['الفئة'].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=categories.index,
            values=categories.values,
            hole=0.4,
            textinfo='label+percent',
            textfont_size=12,
            marker=dict(
                colors=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                line=dict(color='#FFFFFF', width=3)
            )
        )])

        fig.update_layout(
            title='توزيع المنتجات / Product Distribution',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.01
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Advanced 3D Visualization
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("🎯 تحليل الأداء المتقدم / Advanced Performance Analysis")

    # Create complex 3D visualization
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))

    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="الأداء / Performance")
    )])

    fig.update_layout(
        title='خريطة الأداء ثلاثية الأبعاد / 3D Performance Map',
        scene=dict(
            xaxis_title='المحور السيني / X-Axis',
            yaxis_title='المحور الصادي / Y-Axis',
            zaxis_title='الأداء / Performance',
            bgcolor='rgba(0,0,0,0.1)',
            camera=dict(
                eye=dict(x=1.2, y=1.2, z=1.2)
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("⚡ إجراءات سريعة / Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("إضافة عميل جديد", key="add_customer", help="Add new customer"):
            st.success("تم فتح نموذج إضافة عميل جديد")

    with col2:
        if st.button("إنشاء فاتورة", key="create_invoice", help="Create new invoice"):
            st.success("تم فتح نموذج إنشاء فاتورة جديدة")

    with col3:
        if st.button("إضافة منتج", key="add_product", help="Add new product"):
            st.success("تم فتح نموذج إضافة منتج جديد")

    with col4:
        if st.button("تقرير سريع", key="quick_report", help="Generate quick report"):
            st.success("تم إنشاء التقرير السريع")

    st.markdown('</div>', unsafe_allow_html=True)

def show_accounting_module(language, t):
    """Accounting module with advanced features"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>💰 {t["accounting"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Accounting Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة المحاسبة / Accounting Dashboard")

    # Financial metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_assets = st.session_state.accounts[
            st.session_state.accounts['نوع الحساب'].str.contains('أصول', case=False, na=False)
        ]['الرصيد'].sum()

        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_assets:,.0f}</h3>
            <p>إجمالي الأصول<br>Total Assets</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_liabilities = st.session_state.accounts[
            st.session_state.accounts['نوع الحساب'].str.contains('خصوم', case=False, na=False)
        ]['الرصيد'].sum()

        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_liabilities:,.0f}</h3>
            <p>إجمالي الخصوم<br>Total Liabilities</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_equity = st.session_state.accounts[
            st.session_state.accounts['نوع الحساب'].str.contains('رأس المال', case=False, na=False)
        ]['الرصيد'].sum()

        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_equity:,.0f}</h3>
            <p>رأس المال<br>Equity</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        total_revenue = st.session_state.accounts[
            st.session_state.accounts['نوع الحساب'].str.contains('إيرادات', case=False, na=False)
        ]['الرصيد'].sum()

        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_revenue:,.0f}</h3>
            <p>الإيرادات<br>Revenue</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Chart of Accounts
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("🏦 شجرة الحسابات / Chart of Accounts")

    # Display accounts by category
    account_types = st.session_state.accounts['نوع الحساب'].unique()

    for account_type in account_types:
        with st.expander(f"📁 {account_type}", expanded=False):
            type_accounts = st.session_state.accounts[
                st.session_state.accounts['نوع الحساب'] == account_type
            ]

            st.dataframe(
                type_accounts[['رقم الحساب', 'اسم الحساب', 'الرصيد']],
                use_container_width=True,
                column_config={
                    "الرصيد": st.column_config.NumberColumn(format="%.2f ريال")
                }
            )

            total = type_accounts['الرصيد'].sum()
            st.metric(f"إجمالي {account_type}", f"{total:,.2f} ريال")

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new account
    with st.expander("➕ إضافة حساب جديد / Add New Account", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            account_number = st.text_input("رقم الحساب / Account Number")
            account_name = st.text_input("اسم الحساب / Account Name")

        with col2:
            account_type = st.selectbox("نوع الحساب / Account Type", account_types.tolist())
            opening_balance = st.number_input("الرصيد الافتتاحي / Opening Balance", value=0.0)

        if st.button("حفظ الحساب / Save Account", key="save_account"):
            if account_number and account_name:
                new_account = pd.DataFrame({
                    'رقم الحساب': [account_number],
                    'اسم الحساب': [account_name],
                    'نوع الحساب': [account_type],
                    'الرصيد': [opening_balance]
                })

                st.session_state.accounts = pd.concat([
                    st.session_state.accounts, new_account
                ], ignore_index=True)

                st.success("تم إضافة الحساب بنجاح! / Account added successfully!")
                st.rerun()

def show_sales_module(language, t):
    """Sales module with order management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📈 {t["sales"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Sales Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة المبيعات / Sales Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_orders = len(st.session_state.sales_orders)
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_orders}</h3>
            <p>إجمالي الطلبات<br>Total Orders</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        confirmed_orders = len(st.session_state.sales_orders[
            st.session_state.sales_orders['الحالة'] == 'مؤكد'
        ])
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{confirmed_orders}</h3>
            <p>الطلبات المؤكدة<br>Confirmed Orders</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_sales_value = st.session_state.sales_orders['المبلغ'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_sales_value:,.0f}</h3>
            <p>قيمة المبيعات<br>Sales Value</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Sales Orders Table
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("📋 طلبات المبيعات / Sales Orders")

    st.dataframe(
        st.session_state.sales_orders,
        use_container_width=True,
        column_config={
            "المبلغ": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new sales order
    with st.expander("➕ إضافة طلب مبيعات جديد / Add New Sales Order", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            order_number = st.text_input("رقم الطلب / Order Number",
                                       value=f"SO{len(st.session_state.sales_orders) + 1:03d}")
            customer = st.selectbox("العميل / Customer",
                                   st.session_state.customers['اسم العميل'].tolist())
            order_date = st.date_input("تاريخ الطلب / Order Date", value=date.today())

        with col2:
            amount = st.number_input("المبلغ / Amount", value=0.0, step=100.0)
            status = st.selectbox("الحالة / Status", ["مسودة", "مؤكد", "ملغي"])

        if st.button("حفظ الطلب / Save Order", key="save_order"):
            if order_number and customer and amount > 0:
                new_order = pd.DataFrame({
                    'رقم الطلب': [order_number],
                    'العميل': [customer],
                    'التاريخ': [order_date.strftime('%Y-%m-%d')],
                    'المبلغ': [amount],
                    'الحالة': [status]
                })

                st.session_state.sales_orders = pd.concat([
                    st.session_state.sales_orders, new_order
                ], ignore_index=True)

                st.success("تم إضافة الطلب بنجاح! / Order added successfully!")
                st.rerun()

def show_crm_module(language, t):
    """CRM module for customer relationship management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>👥 {t["crm"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # CRM Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة إدارة العملاء / CRM Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_customers = len(st.session_state.customers)
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_customers}</h3>
            <p>إجمالي العملاء<br>Total Customers</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        active_customers = len(st.session_state.customers[
            st.session_state.customers['الحالة'] == 'نشط'
        ])
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{active_customers}</h3>
            <p>العملاء النشطين<br>Active Customers</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_receivables = st.session_state.customers['الرصيد'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_receivables:,.0f}</h3>
            <p>إجمالي المستحقات<br>Total Receivables</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Customer List
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("👥 قائمة العملاء / Customer List")

    st.dataframe(
        st.session_state.customers,
        use_container_width=True,
        column_config={
            "الرصيد": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new customer
    with st.expander("➕ إضافة عميل جديد / Add New Customer", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            customer_id = st.text_input("رقم العميل / Customer ID",
                                      value=f"C{len(st.session_state.customers) + 1:03d}")
            customer_name = st.text_input("اسم العميل / Customer Name")
            phone = st.text_input("الهاتف / Phone")

        with col2:
            email = st.text_input("البريد الإلكتروني / Email")
            balance = st.number_input("الرصيد / Balance", value=0.0)
            status = st.selectbox("الحالة / Status", ["نشط", "غير نشط"])

        if st.button("حفظ العميل / Save Customer", key="save_customer"):
            if customer_id and customer_name:
                new_customer = pd.DataFrame({
                    'رقم العميل': [customer_id],
                    'اسم العميل': [customer_name],
                    'الهاتف': [phone],
                    'البريد': [email],
                    'الرصيد': [balance],
                    'الحالة': [status]
                })

                st.session_state.customers = pd.concat([
                    st.session_state.customers, new_customer
                ], ignore_index=True)

                st.success("تم إضافة العميل بنجاح! / Customer added successfully!")
                st.rerun()

def show_inventory_module(language, t):
    """Inventory management module"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📦 {t["inventory"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Inventory Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة المخزون / Inventory Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_products = len(st.session_state.products)
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_products}</h3>
            <p>إجمالي المنتجات<br>Total Products</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_quantity = st.session_state.products['الكمية'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_quantity}</h3>
            <p>إجمالي الكمية<br>Total Quantity</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        inventory_value = (st.session_state.products['الكمية'] * st.session_state.products['التكلفة']).sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{inventory_value:,.0f}</h3>
            <p>قيمة المخزون<br>Inventory Value</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        low_stock = len(st.session_state.products[st.session_state.products['الكمية'] < 20])
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{low_stock}</h3>
            <p>منتجات قليلة<br>Low Stock Items</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Product List
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("📋 قائمة المنتجات / Product List")

    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox("تصفية حسب الفئة / Filter by Category",
                                     ["الكل"] + st.session_state.products['الفئة'].unique().tolist())
    with col2:
        stock_filter = st.selectbox("تصفية حسب المخزون / Filter by Stock",
                                   ["الكل", "مخزون قليل", "مخزون جيد"])

    # Apply filters
    filtered_products = st.session_state.products.copy()

    if category_filter != "الكل":
        filtered_products = filtered_products[filtered_products['الفئة'] == category_filter]

    if stock_filter == "مخزون قليل":
        filtered_products = filtered_products[filtered_products['الكمية'] < 20]
    elif stock_filter == "مخزون جيد":
        filtered_products = filtered_products[filtered_products['الكمية'] >= 20]

    st.dataframe(
        filtered_products,
        use_container_width=True,
        column_config={
            "السعر": st.column_config.NumberColumn(format="%.2f ريال"),
            "التكلفة": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new product
    with st.expander("➕ إضافة منتج جديد / Add New Product", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            product_code = st.text_input("كود المنتج / Product Code",
                                       value=f"P{len(st.session_state.products) + 1:03d}")
            product_name = st.text_input("اسم المنتج / Product Name")
            category = st.text_input("الفئة / Category")

        with col2:
            quantity = st.number_input("الكمية / Quantity", value=0, step=1)
            price = st.number_input("السعر / Price", value=0.0, step=10.0)
            cost = st.number_input("التكلفة / Cost", value=0.0, step=10.0)

        if st.button("حفظ المنتج / Save Product", key="save_product"):
            if product_code and product_name:
                new_product = pd.DataFrame({
                    'كود المنتج': [product_code],
                    'اسم المنتج': [product_name],
                    'الفئة': [category],
                    'الكمية': [quantity],
                    'السعر': [price],
                    'التكلفة': [cost]
                })

                st.session_state.products = pd.concat([
                    st.session_state.products, new_product
                ], ignore_index=True)

                st.success("تم إضافة المنتج بنجاح! / Product added successfully!")
                st.rerun()

def show_hr_module(language, t):
    """Human Resources module"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>👨‍💼 {t["hr"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # HR Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة الموارد البشرية / HR Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_employees = len(st.session_state.employees)
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_employees}</h3>
            <p>إجمالي الموظفين<br>Total Employees</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_payroll = st.session_state.employees['الراتب'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_payroll:,.0f}</h3>
            <p>إجمالي الرواتب<br>Total Payroll</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_salary = st.session_state.employees['الراتب'].mean()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{avg_salary:,.0f}</h3>
            <p>متوسط الراتب<br>Average Salary</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        departments = st.session_state.employees['القسم'].nunique()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{departments}</h3>
            <p>الأقسام<br>Departments</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Employee List
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("👥 قائمة الموظفين / Employee List")

    # Department filter
    department_filter = st.selectbox("تصفية حسب القسم / Filter by Department",
                                   ["الكل"] + st.session_state.employees['القسم'].unique().tolist())

    filtered_employees = st.session_state.employees.copy()
    if department_filter != "الكل":
        filtered_employees = filtered_employees[filtered_employees['القسم'] == department_filter]

    st.dataframe(
        filtered_employees,
        use_container_width=True,
        column_config={
            "الراتب": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new employee
    with st.expander("➕ إضافة موظف جديد / Add New Employee", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            employee_id = st.text_input("رقم الموظف / Employee ID",
                                      value=f"E{len(st.session_state.employees) + 1:03d}")
            employee_name = st.text_input("الاسم / Name")
            department = st.text_input("القسم / Department")

        with col2:
            position = st.text_input("المنصب / Position")
            salary = st.number_input("الراتب / Salary", value=0.0, step=500.0)
            hire_date = st.date_input("تاريخ التعيين / Hire Date", value=date.today())

        if st.button("حفظ الموظف / Save Employee", key="save_employee"):
            if employee_id and employee_name:
                new_employee = pd.DataFrame({
                    'رقم الموظف': [employee_id],
                    'الاسم': [employee_name],
                    'القسم': [department],
                    'المنصب': [position],
                    'الراتب': [salary],
                    'تاريخ التعيين': [hire_date.strftime('%Y-%m-%d')]
                })

                st.session_state.employees = pd.concat([
                    st.session_state.employees, new_employee
                ], ignore_index=True)

                st.success("تم إضافة الموظف بنجاح! / Employee added successfully!")
                st.rerun()

def show_purchase_module(language, t):
    """Purchase module for supplier management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>🛒 {t["purchase"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Purchase Dashboard
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📊 لوحة المشتريات / Purchase Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_suppliers = len(st.session_state.suppliers)
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_suppliers}</h3>
            <p>إجمالي الموردين<br>Total Suppliers</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_payables = st.session_state.suppliers['الرصيد'].sum()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{total_payables:,.0f}</h3>
            <p>إجمالي المستحقات<br>Total Payables</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_payable = st.session_state.suppliers['الرصيد'].mean()
        st.markdown(f"""
        <div class="metric-3d">
            <h3>{avg_payable:,.0f}</h3>
            <p>متوسط المستحقات<br>Average Payable</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Supplier List
    st.markdown('<div class="data-table-3d">', unsafe_allow_html=True)
    st.subheader("🏪 قائمة الموردين / Supplier List")

    st.dataframe(
        st.session_state.suppliers,
        use_container_width=True,
        column_config={
            "الرصيد": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Add new supplier
    with st.expander("➕ إضافة مورد جديد / Add New Supplier", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            supplier_id = st.text_input("رقم المورد / Supplier ID",
                                      value=f"S{len(st.session_state.suppliers) + 1:03d}")
            supplier_name = st.text_input("اسم المورد / Supplier Name")
            phone = st.text_input("الهاتف / Phone")

        with col2:
            email = st.text_input("البريد الإلكتروني / Email")
            balance = st.number_input("الرصيد / Balance", value=0.0)

        if st.button("حفظ المورد / Save Supplier", key="save_supplier"):
            if supplier_id and supplier_name:
                new_supplier = pd.DataFrame({
                    'رقم المورد': [supplier_id],
                    'اسم المورد': [supplier_name],
                    'الهاتف': [phone],
                    'البريد': [email],
                    'الرصيد': [balance]
                })

                st.session_state.suppliers = pd.concat([
                    st.session_state.suppliers, new_supplier
                ], ignore_index=True)

                st.success("تم إضافة المورد بنجاح! / Supplier added successfully!")
                st.rerun()

def show_advanced_reports(language, t):
    """Advanced reporting module with 3D visualizations"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📊 {t["reports"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Report Selection
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📋 اختيار التقرير / Report Selection")

    report_type = st.selectbox("نوع التقرير / Report Type", [
        "تقرير المبيعات / Sales Report",
        "تقرير المخزون / Inventory Report",
        "تقرير الموارد البشرية / HR Report",
        "التحليل المالي / Financial Analysis",
        "تقرير العملاء / Customer Report"
    ])

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("من تاريخ / From Date", value=date(2024, 1, 1))
    with col2:
        end_date = st.date_input("إلى تاريخ / To Date", value=date.today())

    st.markdown('</div>', unsafe_allow_html=True)

    # Generate Reports
    if st.button("إنشاء التقرير / Generate Report", key="generate_report"):
        if "المبيعات" in report_type or "Sales" in report_type:
            generate_sales_report_3d(language)
        elif "المخزون" in report_type or "Inventory" in report_type:
            generate_inventory_report_3d(language)
        elif "الموارد البشرية" in report_type or "HR" in report_type:
            generate_hr_report_3d(language)
        elif "المالي" in report_type or "Financial" in report_type:
            generate_financial_analysis_3d(language)
        elif "العملاء" in report_type or "Customer" in report_type:
            generate_customer_report_3d(language)

def generate_sales_report_3d(language):
    """Generate 3D sales report"""
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📈 تقرير المبيعات ثلاثي الأبعاد / 3D Sales Report")

    # Create 3D sales visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('اتجاه المبيعات / Sales Trend', 'المبيعات حسب العميل / Sales by Customer',
                       'حالة الطلبات / Order Status', 'الأداء الشهري / Monthly Performance'),
        specs=[[{"type": "scatter3d"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "surface"}]]
    )

    # 3D Sales Trend
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    sales_values = np.random.normal(20000, 5000, 30)
    profits = sales_values * 0.3 + np.random.normal(0, 1000, 30)

    fig.add_trace(
        go.Scatter3d(
            x=list(range(30)),
            y=sales_values,
            z=profits,
            mode='markers+lines',
            marker=dict(size=8, color=profits, colorscale='Viridis'),
            name='اتجاه المبيعات'
        ),
        row=1, col=1
    )

    # Sales by Customer
    customer_sales = st.session_state.sales_orders.groupby('العميل')['المبلغ'].sum()
    fig.add_trace(
        go.Bar(x=customer_sales.index, y=customer_sales.values, name='مبيعات العملاء'),
        row=1, col=2
    )

    # Order Status
    status_counts = st.session_state.sales_orders['الحالة'].value_counts()
    fig.add_trace(
        go.Pie(labels=status_counts.index, values=status_counts.values, name='حالة الطلبات'),
        row=2, col=1
    )

    # Monthly Performance Surface
    x = np.linspace(0, 12, 13)
    y = np.linspace(0, 4, 5)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) * 10000 + 15000

    fig.add_trace(
        go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', name='الأداء الشهري'),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=False, title_text="تقرير المبيعات المتقدم / Advanced Sales Report")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def generate_inventory_report_3d(language):
    """Generate 3D inventory report"""
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("📦 تقرير المخزون ثلاثي الأبعاد / 3D Inventory Report")

    # Create 3D inventory visualization
    fig = go.Figure()

    # 3D Scatter plot for products
    fig.add_trace(go.Scatter3d(
        x=st.session_state.products['الكمية'],
        y=st.session_state.products['السعر'],
        z=st.session_state.products['التكلفة'],
        mode='markers+text',
        marker=dict(
            size=10,
            color=st.session_state.products['الكمية'],
            colorscale='RdYlBu',
            showscale=True,
            colorbar=dict(title="الكمية / Quantity")
        ),
        text=st.session_state.products['اسم المنتج'],
        textposition="top center",
        name='المنتجات'
    ))

    fig.update_layout(
        title='تحليل المخزون ثلاثي الأبعاد / 3D Inventory Analysis',
        scene=dict(
            xaxis_title='الكمية / Quantity',
            yaxis_title='السعر / Price',
            zaxis_title='التكلفة / Cost',
            bgcolor='rgba(0,0,0,0.1)'
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Inventory value by category
    category_value = st.session_state.products.groupby('الفئة').apply(
        lambda x: (x['الكمية'] * x['التكلفة']).sum()
    ).reset_index()
    category_value.columns = ['الفئة', 'القيمة']

    fig2 = px.bar_3d(
        category_value,
        x='الفئة',
        y='القيمة',
        z='القيمة',
        title='قيمة المخزون حسب الفئة / Inventory Value by Category'
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def generate_hr_report_3d(language):
    """Generate 3D HR report"""
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("👨‍💼 تقرير الموارد البشرية ثلاثي الأبعاد / 3D HR Report")

    # Salary distribution by department
    dept_salary = st.session_state.employees.groupby('القسم')['الراتب'].agg(['mean', 'sum', 'count']).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=dept_salary['count'],
        y=dept_salary['mean'],
        z=dept_salary['sum'],
        mode='markers+text',
        marker=dict(
            size=15,
            color=dept_salary['sum'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title="إجمالي الرواتب / Total Salaries")
        ),
        text=dept_salary['القسم'],
        textposition="top center",
        name='الأقسام'
    ))

    fig.update_layout(
        title='تحليل الرواتب ثلاثي الأبعاد / 3D Salary Analysis',
        scene=dict(
            xaxis_title='عدد الموظفين / Employee Count',
            yaxis_title='متوسط الراتب / Average Salary',
            zaxis_title='إجمالي الرواتب / Total Salaries',
            bgcolor='rgba(0,0,0,0.1)'
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def generate_financial_analysis_3d(language):
    """Generate 3D financial analysis"""
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("💰 التحليل المالي ثلاثي الأبعاد / 3D Financial Analysis")

    # Create financial surface plot
    months = np.arange(1, 13)
    categories = ['الإيرادات', 'المصروفات', 'الأرباح']

    # Generate sample financial data
    revenue_data = np.random.normal(100000, 20000, 12)
    expense_data = np.random.normal(70000, 15000, 12)
    profit_data = revenue_data - expense_data

    fig = go.Figure()

    # Add revenue surface
    fig.add_trace(go.Scatter3d(
        x=months,
        y=revenue_data,
        z=[1] * 12,
        mode='lines+markers',
        line=dict(color='green', width=8),
        marker=dict(size=8),
        name='الإيرادات / Revenue'
    ))

    # Add expense surface
    fig.add_trace(go.Scatter3d(
        x=months,
        y=expense_data,
        z=[2] * 12,
        mode='lines+markers',
        line=dict(color='red', width=8),
        marker=dict(size=8),
        name='المصروفات / Expenses'
    ))

    # Add profit surface
    fig.add_trace(go.Scatter3d(
        x=months,
        y=profit_data,
        z=[3] * 12,
        mode='lines+markers',
        line=dict(color='blue', width=8),
        marker=dict(size=8),
        name='الأرباح / Profit'
    ))

    fig.update_layout(
        title='التحليل المالي السنوي / Annual Financial Analysis',
        scene=dict(
            xaxis_title='الشهر / Month',
            yaxis_title='المبلغ / Amount',
            zaxis_title='الفئة / Category',
            bgcolor='rgba(0,0,0,0.1)'
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def generate_customer_report_3d(language):
    """Generate 3D customer report"""
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.subheader("👥 تقرير العملاء ثلاثي الأبعاد / 3D Customer Report")

    # Customer analysis
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=st.session_state.customers.index,
        y=st.session_state.customers['الرصيد'],
        z=[1] * len(st.session_state.customers),
        mode='markers+text',
        marker=dict(
            size=12,
            color=st.session_state.customers['الرصيد'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="الرصيد / Balance")
        ),
        text=st.session_state.customers['اسم العميل'],
        textposition="top center",
        name='العملاء'
    ))

    fig.update_layout(
        title='تحليل أرصدة العملاء / Customer Balance Analysis',
        scene=dict(
            xaxis_title='رقم العميل / Customer Number',
            yaxis_title='الرصيد / Balance',
            zaxis_title='المستوى / Level',
            bgcolor='rgba(0,0,0,0.1)'
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
