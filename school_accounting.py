import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import io
import base64
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
import xlsxwriter
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import json

# Configure page
st.set_page_config(
    page_title="نظام المحاسبة المدرسية | School Accounting System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for school theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Tajawal:wght@300;400;500;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
    }
    
    .stApp {
        font-family: 'Cairo', 'Tajawal', sans-serif;
    }
    
    .arabic-text {
        font-family: 'Cairo', 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .school-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .school-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #3b82f6;
    }
    
    .financial-metric {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .income-amount {
        color: #059669;
        font-weight: bold;
        font-size: 1.5em;
    }
    
    .expense-amount {
        color: #dc2626;
        font-weight: bold;
        font-size: 1.5em;
    }
    
    .balance-amount {
        color: #1e40af;
        font-weight: bold;
        font-size: 1.5em;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        font-family: inherit;
    }
    
    .success-button {
        background: linear-gradient(90deg, #059669, #047857) !important;
    }
    
    .danger-button {
        background: linear-gradient(90deg, #dc2626, #b91c1c) !important;
    }
    
    .data-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .alert-success {
        background: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for school accounting data
def initialize_school_data():
    if 'school_accounts' not in st.session_state:
        # Pre-defined school accounts
        st.session_state.school_accounts = pd.DataFrame([
            {'رقم الحساب': '1001', 'اسم الحساب': 'النقدية', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد الافتتاحي': 100000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 100000.0},
            {'رقم الحساب': '1002', 'اسم الحساب': 'البنك', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد الافتتاحي': 500000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 500000.0},
            {'رقم الحساب': '1101', 'اسم الحساب': 'رسوم مستحقة القبض', 'نوع الحساب': 'الأصول المتداولة', 'الرصيد الافتتاحي': 50000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 50000.0},
            {'رقم الحساب': '1201', 'اسم الحساب': 'أثاث وتجهيزات مدرسية', 'نوع الحساب': 'الأصول الثابتة', 'الرصيد الافتتاحي': 200000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 200000.0},
            {'رقم الحساب': '1202', 'اسم الحساب': 'أجهزة كمبيوتر وتقنية', 'نوع الحساب': 'الأصول الثابتة', 'الرصيد الافتتاحي': 150000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 150000.0},
            {'رقم الحساب': '2001', 'اسم الحساب': 'رواتب مستحقة الدفع', 'نوع الحساب': 'الخصوم المتداولة', 'الرصيد الافتتاحي': 80000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 80000.0},
            {'رقم الحساب': '2002', 'اسم الحساب': 'مصروفات مستحقة الدفع', 'نوع الحساب': 'الخصوم المتداولة', 'الرصيد الافتتاحي': 30000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 30000.0},
            {'رقم الحساب': '3001', 'اسم الحساب': 'رأس المال', 'نوع الحساب': 'رأس المال', 'الرصيد الافتتاحي': 800000.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 800000.0},
            {'رقم الحساب': '4001', 'اسم الحساب': 'رسوم دراسية', 'نوع الحساب': 'الإيرادات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '4002', 'اسم الحساب': 'رسوم أنشطة', 'نوع الحساب': 'الإيرادات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '4003', 'اسم الحساب': 'رسوم نقل', 'نوع الحساب': 'الإيرادات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5001', 'اسم الحساب': 'رواتب المعلمين', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5002', 'اسم الحساب': 'رواتب الإداريين', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5101', 'اسم الحساب': 'مصروفات كهرباء وماء', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5102', 'اسم الحساب': 'مصروفات صيانة', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5103', 'اسم الحساب': 'مصروفات قرطاسية ومواد تعليمية', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0},
            {'رقم الحساب': '5104', 'اسم الحساب': 'مصروفات نقل وانتقالات', 'نوع الحساب': 'المصروفات', 'الرصيد الافتتاحي': 0.0, 'مدين': 0.0, 'دائن': 0.0, 'الرصيد الحالي': 0.0}
        ])

    if 'school_journal_entries' not in st.session_state:
        st.session_state.school_journal_entries = pd.DataFrame(columns=[
            'التاريخ', 'رقم القيد', 'الوصف', 'رقم الحساب', 'اسم الحساب', 'مدين', 'دائن', 'المرجع'
        ])

    if 'school_students' not in st.session_state:
        st.session_state.school_students = pd.DataFrame(columns=[
            'رقم الطالب', 'اسم الطالب', 'الصف', 'الرسوم السنوية', 'المدفوع', 'المتبقي', 'حالة الدفع'
        ])

    if 'school_teachers' not in st.session_state:
        st.session_state.school_teachers = pd.DataFrame(columns=[
            'رقم المعلم', 'اسم المعلم', 'التخصص', 'الراتب الشهري', 'تاريخ التعيين', 'الحالة'
        ])

    if 'school_expenses' not in st.session_state:
        st.session_state.school_expenses = pd.DataFrame(columns=[
            'التاريخ', 'نوع المصروف', 'الوصف', 'المبلغ', 'طريقة الدفع', 'المرجع'
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
        "title": "نظام المحاسبة المدرسية",
        "subtitle": "إدارة مالية شاملة للمؤسسات التعليمية",
        "nav_dashboard": "🏠 لوحة التحكم",
        "nav_accounts": "📊 شجرة الحسابات",
        "nav_journal": "📝 القيود المحاسبية",
        "nav_students": "👥 إدارة الطلاب",
        "nav_teachers": "👨‍🏫 إدارة المعلمين",
        "nav_expenses": "💸 المصروفات",
        "nav_reports": "📈 التقارير",
        "nav_excel": "📋 Excel",
        "nav_settings": "⚙️ الإعدادات"
    },
    "English": {
        "title": "School Accounting System",
        "subtitle": "Comprehensive Financial Management for Educational Institutions",
        "nav_dashboard": "🏠 Dashboard",
        "nav_accounts": "📊 Chart of Accounts",
        "nav_journal": "📝 Journal Entries",
        "nav_students": "👥 Student Management",
        "nav_teachers": "👨‍🏫 Teacher Management",
        "nav_expenses": "💸 Expenses",
        "nav_reports": "📈 Reports",
        "nav_excel": "📋 Excel",
        "nav_settings": "⚙️ Settings"
    }
}

def main():
    # Initialize data
    initialize_school_data()
    
    language = get_language()
    t = translations[language]
    
    # Header
    st.markdown(f"""
    <div class="school-header">
        <h1>🏫 {t["title"]}</h1>
        <h3>{t["subtitle"]}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation / التنقل",
        [
            t["nav_dashboard"], t["nav_accounts"], t["nav_journal"],
            t["nav_students"], t["nav_teachers"], t["nav_expenses"],
            t["nav_reports"], t["nav_excel"], t["nav_settings"]
        ]
    )
    
    # Route to different pages
    if page == t["nav_dashboard"]:
        show_school_dashboard(language, t)
    elif page == t["nav_accounts"]:
        show_school_accounts(language, t)
    elif page == t["nav_journal"]:
        show_school_journal_entries(language, t)
    elif page == t["nav_students"]:
        show_student_management(language, t)
    elif page == t["nav_teachers"]:
        show_teacher_management(language, t)
    elif page == t["nav_expenses"]:
        show_school_expenses(language, t)
    elif page == t["nav_reports"]:
        show_school_reports(language, t)
    elif page == t["nav_excel"]:
        show_excel_functions(language, t)
    elif page == t["nav_settings"]:
        show_school_settings(language, t)

def show_school_dashboard(language, t):
    """School dashboard with key financial metrics"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>🏫 {t["nav_dashboard"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Calculate key metrics
    total_assets = calculate_school_total_by_type("أصول")
    total_liabilities = calculate_school_total_by_type("خصوم")
    total_equity = calculate_school_total_by_type("رأس المال")
    total_revenue = calculate_school_total_by_type("إيرادات")
    total_expenses = calculate_school_total_by_type("مصروفات")
    net_income = total_revenue - total_expenses

    # Key metrics display
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="financial-metric">
            <h4>إجمالي الأصول<br>Total Assets</h4>
            <div class="balance-amount">{total_assets:,.2f} ريال</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="financial-metric">
            <h4>إجمالي الإيرادات<br>Total Revenue</h4>
            <div class="income-amount">{total_revenue:,.2f} ريال</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="financial-metric">
            <h4>إجمالي المصروفات<br>Total Expenses</h4>
            <div class="expense-amount">{total_expenses:,.2f} ريال</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        color_class = "income-amount" if net_income >= 0 else "expense-amount"
        st.markdown(f"""
        <div class="financial-metric">
            <h4>صافي الدخل<br>Net Income</h4>
            <div class="{color_class}">{net_income:,.2f} ريال</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.school_accounts.empty:
            # Revenue vs Expenses chart
            revenue_expense_data = pd.DataFrame({
                'النوع': ['الإيرادات', 'المصروفات'],
                'المبلغ': [total_revenue, total_expenses]
            })

            fig = px.bar(revenue_expense_data, x='النوع', y='المبلغ',
                        title="الإيرادات مقابل المصروفات / Revenue vs Expenses",
                        color='النوع',
                        color_discrete_map={'الإيرادات': '#059669', 'المصروفات': '#dc2626'})
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if not st.session_state.school_students.empty:
            # Student payment status
            payment_status = st.session_state.school_students['حالة الدفع'].value_counts()
            if not payment_status.empty:
                fig = px.pie(values=payment_status.values, names=payment_status.index,
                           title="حالة دفع الرسوم / Fee Payment Status")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد بيانات طلاب لعرضها / No student data to display")

    # Quick actions
    st.markdown('<div class="school-card">', unsafe_allow_html=True)
    st.subheader("إجراءات سريعة / Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("إضافة طالب جديد / Add New Student"):
            st.session_state.quick_action = "add_student"

    with col2:
        if st.button("تسجيل دفع رسوم / Record Fee Payment"):
            st.session_state.quick_action = "record_payment"

    with col3:
        if st.button("إضافة مصروف / Add Expense"):
            st.session_state.quick_action = "add_expense"

    with col4:
        if st.button("إنشاء تقرير / Generate Report"):
            st.session_state.quick_action = "generate_report"

    st.markdown('</div>', unsafe_allow_html=True)

def calculate_school_total_by_type(account_type_filter):
    """Calculate total balance for specific account types"""
    if st.session_state.school_accounts.empty:
        return 0.0

    filtered_accounts = st.session_state.school_accounts[
        st.session_state.school_accounts['نوع الحساب'].str.contains(account_type_filter, case=False, na=False)
    ]
    return filtered_accounts['الرصيد الحالي'].sum()

def show_school_accounts(language, t):
    """School chart of accounts management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📊 {t["nav_accounts"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Display accounts by category
    account_categories = {
        "الأصول المتداولة": "💰",
        "الأصول الثابتة": "🏢",
        "الخصوم المتداولة": "📋",
        "رأس المال": "💎",
        "الإيرادات": "💚",
        "المصروفات": "💸"
    }

    for category, icon in account_categories.items():
        category_accounts = st.session_state.school_accounts[
            st.session_state.school_accounts['نوع الحساب'] == category
        ]

        if not category_accounts.empty:
            st.markdown(f"""
            <div class="school-card">
                <h3>{icon} {category}</h3>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(
                category_accounts[['رقم الحساب', 'اسم الحساب', 'الرصيد الحالي']],
                use_container_width=True,
                column_config={
                    "الرصيد الحالي": st.column_config.NumberColumn(
                        format="%.2f ريال"
                    )
                }
            )

            total = category_accounts['الرصيد الحالي'].sum()
            st.metric(f"إجمالي {category}", f"{total:,.2f} ريال")

    # Add new account form
    with st.expander("➕ إضافة حساب جديد / Add New Account", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            account_number = st.text_input("رقم الحساب / Account Number")
            account_name = st.text_input("اسم الحساب / Account Name")
            account_type = st.selectbox("نوع الحساب / Account Type", list(account_categories.keys()))

        with col2:
            opening_balance = st.number_input("الرصيد الافتتاحي / Opening Balance", value=0.0, step=0.01)

            if st.button("حفظ الحساب / Save Account", key="save_school_account"):
                if account_number and account_name:
                    # Check if account number already exists
                    if account_number in st.session_state.school_accounts['رقم الحساب'].values:
                        st.error("رقم الحساب موجود مسبقاً / Account number already exists")
                    else:
                        new_account = pd.DataFrame({
                            'رقم الحساب': [account_number],
                            'اسم الحساب': [account_name],
                            'نوع الحساب': [account_type],
                            'الرصيد الافتتاحي': [opening_balance],
                            'مدين': [0.0],
                            'دائن': [0.0],
                            'الرصيد الحالي': [opening_balance]
                        })

                        st.session_state.school_accounts = pd.concat([
                            st.session_state.school_accounts, new_account
                        ], ignore_index=True)

                        st.success("تم إضافة الحساب بنجاح! / Account added successfully!")
                        st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

def show_school_journal_entries(language, t):
    """School journal entries with improved validation"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📝 {t["nav_journal"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new journal entry form
    with st.expander("➕ إضافة قيد محاسبي جديد / Add New Journal Entry", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            entry_date = st.date_input("التاريخ / Date", value=date.today())
            entry_number = st.text_input("رقم القيد / Entry Number",
                                       value=f"J{len(st.session_state.school_journal_entries) + 1:03d}")
            description = st.text_area("الوصف / Description")

        with col2:
            if not st.session_state.school_accounts.empty:
                account_options = [f"{row['رقم الحساب']} - {row['اسم الحساب']}"
                                 for _, row in st.session_state.school_accounts.iterrows()]
                selected_account = st.selectbox("الحساب / Account", account_options)

                debit_amount = st.number_input("مبلغ مدين / Debit Amount", value=0.0, step=0.01, min_value=0.0)
                credit_amount = st.number_input("مبلغ دائن / Credit Amount", value=0.0, step=0.01, min_value=0.0)
                reference = st.text_input("المرجع / Reference")

                # Validation and save
                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button("حفظ القيد / Save Entry", key="save_school_journal", type="primary"):
                        # Validation
                        errors = []

                        if not entry_number:
                            errors.append("رقم القيد مطلوب / Entry number required")

                        if not description:
                            errors.append("الوصف مطلوب / Description required")

                        if not selected_account:
                            errors.append("يجب اختيار حساب / Account selection required")

                        if debit_amount == 0 and credit_amount == 0:
                            errors.append("يجب إدخال مبلغ في المدين أو الدائن / Must enter amount in debit or credit")

                        if debit_amount > 0 and credit_amount > 0:
                            errors.append("لا يمكن إدخال مبلغ في المدين والدائن معاً / Cannot enter both debit and credit amounts")

                        if errors:
                            for error in errors:
                                st.error(error)
                        else:
                            # Save the entry
                            account_number = selected_account.split(' - ')[0]
                            account_name = selected_account.split(' - ')[1]

                            new_entry = pd.DataFrame({
                                'التاريخ': [entry_date],
                                'رقم القيد': [entry_number],
                                'الوصف': [description],
                                'رقم الحساب': [account_number],
                                'اسم الحساب': [account_name],
                                'مدين': [debit_amount],
                                'دائن': [credit_amount],
                                'المرجع': [reference]
                            })

                            st.session_state.school_journal_entries = pd.concat([
                                st.session_state.school_journal_entries, new_entry
                            ], ignore_index=True)

                            # Update account balance
                            update_school_account_balance(account_number, debit_amount, credit_amount)

                            st.success("تم حفظ القيد بنجاح! / Entry saved successfully!")
                            st.rerun()

                with col_b:
                    if st.button("مسح النموذج / Clear Form", key="clear_journal_form"):
                        st.rerun()
            else:
                st.warning("يرجى إضافة حسابات أولاً / Please add accounts first")

    # Display journal entries
    if not st.session_state.school_journal_entries.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.subheader("القيود المحاسبية / Journal Entries")

        # Date range filter
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("من تاريخ / From Date", value=date.today().replace(day=1))
        with col2:
            end_date = st.date_input("إلى تاريخ / To Date", value=date.today())
        with col3:
            if st.button("تصفية / Filter"):
                st.rerun()

        # Filter entries by date
        filtered_entries = st.session_state.school_journal_entries.copy()
        filtered_entries['التاريخ'] = pd.to_datetime(filtered_entries['التاريخ'])

        if start_date and end_date:
            filtered_entries = filtered_entries[
                (filtered_entries['التاريخ'].dt.date >= start_date) &
                (filtered_entries['التاريخ'].dt.date <= end_date)
            ]

        # Display entries
        st.dataframe(
            filtered_entries,
            use_container_width=True,
            column_config={
                "مدين": st.column_config.NumberColumn(format="%.2f ريال"),
                "دائن": st.column_config.NumberColumn(format="%.2f ريال")
            }
        )

        # Summary
        total_debit = filtered_entries['مدين'].sum()
        total_credit = filtered_entries['دائن'].sum()
        difference = total_debit - total_credit

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي المدين / Total Debit", f"{total_debit:,.2f} ريال")
        with col2:
            st.metric("إجمالي الدائن / Total Credit", f"{total_credit:,.2f} ريال")
        with col3:
            st.metric("الفرق / Difference", f"{difference:,.2f} ريال")
            if abs(difference) > 0.01:
                st.error("القيود غير متوازنة! / Entries are not balanced!")
            else:
                st.success("القيود متوازنة ✓ / Entries are balanced ✓")

        st.markdown('</div>', unsafe_allow_html=True)

        # Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("تصدير إلى Excel / Export to Excel", key="export_journal_excel"):
                excel_data = create_school_excel_export(filtered_entries, "القيود المحاسبية")
                st.download_button(
                    label="تحميل ملف Excel / Download Excel",
                    data=excel_data,
                    file_name=f"journal_entries_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        with col2:
            if st.button("تصدير إلى PDF / Export to PDF", key="export_journal_pdf"):
                pdf_data = create_school_pdf_export(filtered_entries, "القيود المحاسبية / Journal Entries")
                st.download_button(
                    label="تحميل ملف PDF / Download PDF",
                    data=pdf_data,
                    file_name=f"journal_entries_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("لا توجد قيود محاسبية مضافة بعد / No journal entries added yet")

def update_school_account_balance(account_number, debit_amount, credit_amount):
    """Update school account balance after journal entry"""
    if not st.session_state.school_accounts.empty:
        mask = st.session_state.school_accounts['رقم الحساب'] == account_number
        if mask.any():
            st.session_state.school_accounts.loc[mask, 'مدين'] += debit_amount
            st.session_state.school_accounts.loc[mask, 'دائن'] += credit_amount

            # Calculate new balance based on account type
            account_type = st.session_state.school_accounts.loc[mask, 'نوع الحساب'].iloc[0]
            opening_balance = st.session_state.school_accounts.loc[mask, 'الرصيد الافتتاحي'].iloc[0]
            total_debit = st.session_state.school_accounts.loc[mask, 'مدين'].iloc[0]
            total_credit = st.session_state.school_accounts.loc[mask, 'دائن'].iloc[0]

            # For asset and expense accounts: Debit increases balance
            # For liability, equity, and revenue accounts: Credit increases balance
            if any(x in account_type for x in ['أصول', 'مصروفات']):
                new_balance = opening_balance + total_debit - total_credit
            else:
                new_balance = opening_balance + total_credit - total_debit

            st.session_state.school_accounts.loc[mask, 'الرصيد الحالي'] = new_balance

def show_student_management(language, t):
    """Student management and fee tracking"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>👥 {t["nav_students"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new student form
    with st.expander("➕ إضافة طالب جديد / Add New Student", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            student_id = st.text_input("رقم الطالب / Student ID")
            student_name = st.text_input("اسم الطالب / Student Name")
            grade = st.selectbox("الصف / Grade", [
                "الروضة", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
                "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
                "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط",
                "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي"
            ])

        with col2:
            annual_fees = st.number_input("الرسوم السنوية / Annual Fees", value=0.0, step=100.0)
            paid_amount = st.number_input("المبلغ المدفوع / Paid Amount", value=0.0, step=100.0)

            if st.button("حفظ الطالب / Save Student", key="save_student"):
                if student_id and student_name and annual_fees > 0:
                    # Check if student ID already exists
                    if not st.session_state.school_students.empty and student_id in st.session_state.school_students['رقم الطالب'].values:
                        st.error("رقم الطالب موجود مسبقاً / Student ID already exists")
                    else:
                        remaining = annual_fees - paid_amount
                        payment_status = "مكتمل" if remaining <= 0 else "جزئي" if paid_amount > 0 else "غير مدفوع"

                        new_student = pd.DataFrame({
                            'رقم الطالب': [student_id],
                            'اسم الطالب': [student_name],
                            'الصف': [grade],
                            'الرسوم السنوية': [annual_fees],
                            'المدفوع': [paid_amount],
                            'المتبقي': [remaining],
                            'حالة الدفع': [payment_status]
                        })

                        st.session_state.school_students = pd.concat([
                            st.session_state.school_students, new_student
                        ], ignore_index=True)

                        st.success("تم إضافة الطالب بنجاح! / Student added successfully!")
                        st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display students
    if not st.session_state.school_students.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.subheader("قائمة الطلاب / Student List")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            grade_filter = st.selectbox("تصفية حسب الصف / Filter by Grade",
                                      ["الكل"] + st.session_state.school_students['الصف'].unique().tolist())
        with col2:
            payment_filter = st.selectbox("تصفية حسب حالة الدفع / Filter by Payment Status",
                                        ["الكل"] + st.session_state.school_students['حالة الدفع'].unique().tolist())
        with col3:
            search_student = st.text_input("البحث عن طالب / Search Student")

        # Apply filters
        filtered_students = st.session_state.school_students.copy()

        if grade_filter != "الكل":
            filtered_students = filtered_students[filtered_students['الصف'] == grade_filter]

        if payment_filter != "الكل":
            filtered_students = filtered_students[filtered_students['حالة الدفع'] == payment_filter]

        if search_student:
            filtered_students = filtered_students[
                filtered_students['اسم الطالب'].str.contains(search_student, case=False, na=False) |
                filtered_students['رقم الطالب'].str.contains(search_student, case=False, na=False)
            ]

        # Display students table
        st.dataframe(
            filtered_students,
            use_container_width=True,
            column_config={
                "الرسوم السنوية": st.column_config.NumberColumn(format="%.2f ريال"),
                "المدفوع": st.column_config.NumberColumn(format="%.2f ريال"),
                "المتبقي": st.column_config.NumberColumn(format="%.2f ريال")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary metrics
        total_students = len(filtered_students)
        total_fees = filtered_students['الرسوم السنوية'].sum()
        total_paid = filtered_students['المدفوع'].sum()
        total_remaining = filtered_students['المتبقي'].sum()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("عدد الطلاب / Total Students", total_students)
        with col2:
            st.metric("إجمالي الرسوم / Total Fees", f"{total_fees:,.2f} ريال")
        with col3:
            st.metric("المبلغ المحصل / Collected Amount", f"{total_paid:,.2f} ريال")
        with col4:
            st.metric("المبلغ المتبقي / Remaining Amount", f"{total_remaining:,.2f} ريال")

        # Payment recording
        st.subheader("تسجيل دفع رسوم / Record Fee Payment")

        col1, col2, col3 = st.columns(3)
        with col1:
            if not filtered_students.empty:
                student_options = [f"{row['رقم الطالب']} - {row['اسم الطالب']}"
                                 for _, row in filtered_students.iterrows()]
                selected_student = st.selectbox("اختر الطالب / Select Student", student_options)

        with col2:
            payment_amount = st.number_input("مبلغ الدفع / Payment Amount", value=0.0, step=100.0)

        with col3:
            payment_date = st.date_input("تاريخ الدفع / Payment Date", value=date.today())

            if st.button("تسجيل الدفع / Record Payment", key="record_payment"):
                if selected_student and payment_amount > 0:
                    student_id = selected_student.split(' - ')[0]

                    # Update student payment
                    mask = st.session_state.school_students['رقم الطالب'] == student_id
                    if mask.any():
                        current_paid = st.session_state.school_students.loc[mask, 'المدفوع'].iloc[0]
                        annual_fees = st.session_state.school_students.loc[mask, 'الرسوم السنوية'].iloc[0]

                        new_paid = current_paid + payment_amount
                        new_remaining = annual_fees - new_paid

                        if new_remaining <= 0:
                            payment_status = "مكتمل"
                        elif new_paid > 0:
                            payment_status = "جزئي"
                        else:
                            payment_status = "غير مدفوع"

                        st.session_state.school_students.loc[mask, 'المدفوع'] = new_paid
                        st.session_state.school_students.loc[mask, 'المتبقي'] = new_remaining
                        st.session_state.school_students.loc[mask, 'حالة الدفع'] = payment_status

                        # Create journal entry for the payment
                        entry_number = f"FEE{len(st.session_state.school_journal_entries) + 1:03d}"
                        student_name = selected_student.split(' - ')[1]

                        # Debit Cash/Bank, Credit Fee Revenue
                        cash_entry = pd.DataFrame({
                            'التاريخ': [payment_date],
                            'رقم القيد': [entry_number],
                            'الوصف': [f"دفع رسوم الطالب {student_name}"],
                            'رقم الحساب': ['1001'],
                            'اسم الحساب': ['النقدية'],
                            'مدين': [payment_amount],
                            'دائن': [0.0],
                            'المرجع': [f"رسوم طالب {student_id}"]
                        })

                        fee_entry = pd.DataFrame({
                            'التاريخ': [payment_date],
                            'رقم القيد': [entry_number],
                            'الوصف': [f"دفع رسوم الطالب {student_name}"],
                            'رقم الحساب': ['4001'],
                            'اسم الحساب': ['رسوم دراسية'],
                            'مدين': [0.0],
                            'دائن': [payment_amount],
                            'المرجع': [f"رسوم طالب {student_id}"]
                        })

                        st.session_state.school_journal_entries = pd.concat([
                            st.session_state.school_journal_entries, cash_entry, fee_entry
                        ], ignore_index=True)

                        # Update account balances
                        update_school_account_balance('1001', payment_amount, 0.0)
                        update_school_account_balance('4001', 0.0, payment_amount)

                        st.success(f"تم تسجيل دفع {payment_amount:,.2f} ريال للطالب {student_name}")
                        st.rerun()
                else:
                    st.error("يرجى اختيار طالب وإدخال مبلغ صحيح / Please select student and enter valid amount")
    else:
        st.info("لا يوجد طلاب مسجلون بعد / No students registered yet")

def show_teacher_management(language, t):
    """Teacher management and salary tracking"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>👨‍🏫 {t["nav_teachers"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new teacher form
    with st.expander("➕ إضافة معلم جديد / Add New Teacher", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            teacher_id = st.text_input("رقم المعلم / Teacher ID")
            teacher_name = st.text_input("اسم المعلم / Teacher Name")
            specialization = st.selectbox("التخصص / Specialization", [
                "اللغة العربية", "اللغة الإنجليزية", "الرياضيات", "العلوم",
                "الفيزياء", "الكيمياء", "الأحياء", "التاريخ", "الجغرافيا",
                "التربية الإسلامية", "التربية البدنية", "الحاسوب", "الفنون"
            ])

        with col2:
            monthly_salary = st.number_input("الراتب الشهري / Monthly Salary", value=0.0, step=500.0)
            hire_date = st.date_input("تاريخ التعيين / Hire Date", value=date.today())
            status = st.selectbox("الحالة / Status", ["نشط", "إجازة", "متقاعد"])

            if st.button("حفظ المعلم / Save Teacher", key="save_teacher"):
                if teacher_id and teacher_name and monthly_salary > 0:
                    # Check if teacher ID already exists
                    if not st.session_state.school_teachers.empty and teacher_id in st.session_state.school_teachers['رقم المعلم'].values:
                        st.error("رقم المعلم موجود مسبقاً / Teacher ID already exists")
                    else:
                        new_teacher = pd.DataFrame({
                            'رقم المعلم': [teacher_id],
                            'اسم المعلم': [teacher_name],
                            'التخصص': [specialization],
                            'الراتب الشهري': [monthly_salary],
                            'تاريخ التعيين': [hire_date],
                            'الحالة': [status]
                        })

                        st.session_state.school_teachers = pd.concat([
                            st.session_state.school_teachers, new_teacher
                        ], ignore_index=True)

                        st.success("تم إضافة المعلم بنجاح! / Teacher added successfully!")
                        st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display teachers
    if not st.session_state.school_teachers.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.subheader("قائمة المعلمين / Teacher List")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            specialization_filter = st.selectbox("تصفية حسب التخصص / Filter by Specialization",
                                               ["الكل"] + st.session_state.school_teachers['التخصص'].unique().tolist())
        with col2:
            status_filter = st.selectbox("تصفية حسب الحالة / Filter by Status",
                                       ["الكل"] + st.session_state.school_teachers['الحالة'].unique().tolist())
        with col3:
            search_teacher = st.text_input("البحث عن معلم / Search Teacher")

        # Apply filters
        filtered_teachers = st.session_state.school_teachers.copy()

        if specialization_filter != "الكل":
            filtered_teachers = filtered_teachers[filtered_teachers['التخصص'] == specialization_filter]

        if status_filter != "الكل":
            filtered_teachers = filtered_teachers[filtered_teachers['الحالة'] == status_filter]

        if search_teacher:
            filtered_teachers = filtered_teachers[
                filtered_teachers['اسم المعلم'].str.contains(search_teacher, case=False, na=False) |
                filtered_teachers['رقم المعلم'].str.contains(search_teacher, case=False, na=False)
            ]

        # Display teachers table
        st.dataframe(
            filtered_teachers,
            use_container_width=True,
            column_config={
                "الراتب الشهري": st.column_config.NumberColumn(format="%.2f ريال")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary metrics
        total_teachers = len(filtered_teachers)
        total_salaries = filtered_teachers['الراتب الشهري'].sum()
        avg_salary = filtered_teachers['الراتب الشهري'].mean() if total_teachers > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("عدد المعلمين / Total Teachers", total_teachers)
        with col2:
            st.metric("إجمالي الرواتب الشهرية / Total Monthly Salaries", f"{total_salaries:,.2f} ريال")
        with col3:
            st.metric("متوسط الراتب / Average Salary", f"{avg_salary:,.2f} ريال")

        # Salary payment
        st.subheader("دفع الرواتب / Salary Payment")

        col1, col2, col3 = st.columns(3)
        with col1:
            if not filtered_teachers.empty:
                teacher_options = [f"{row['رقم المعلم']} - {row['اسم المعلم']}"
                                 for _, row in filtered_teachers.iterrows()]
                selected_teacher = st.selectbox("اختر المعلم / Select Teacher", teacher_options)

        with col2:
            payment_month = st.selectbox("الشهر / Month", [
                "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
            ])

        with col3:
            payment_date = st.date_input("تاريخ الدفع / Payment Date", value=date.today(), key="salary_date")

            if st.button("دفع الراتب / Pay Salary", key="pay_salary"):
                if selected_teacher:
                    teacher_id = selected_teacher.split(' - ')[0]
                    teacher_name = selected_teacher.split(' - ')[1]

                    # Get teacher salary
                    mask = st.session_state.school_teachers['رقم المعلم'] == teacher_id
                    if mask.any():
                        salary_amount = st.session_state.school_teachers.loc[mask, 'الراتب الشهري'].iloc[0]

                        # Create journal entry for salary payment
                        entry_number = f"SAL{len(st.session_state.school_journal_entries) + 1:03d}"

                        # Debit Salary Expense, Credit Cash
                        salary_expense_entry = pd.DataFrame({
                            'التاريخ': [payment_date],
                            'رقم القيد': [entry_number],
                            'الوصف': [f"راتب {teacher_name} - {payment_month}"],
                            'رقم الحساب': ['5001'],
                            'اسم الحساب': ['رواتب المعلمين'],
                            'مدين': [salary_amount],
                            'دائن': [0.0],
                            'المرجع': [f"راتب {teacher_id} - {payment_month}"]
                        })

                        cash_entry = pd.DataFrame({
                            'التاريخ': [payment_date],
                            'رقم القيد': [entry_number],
                            'الوصف': [f"راتب {teacher_name} - {payment_month}"],
                            'رقم الحساب': ['1001'],
                            'اسم الحساب': ['النقدية'],
                            'مدين': [0.0],
                            'دائن': [salary_amount],
                            'المرجع': [f"راتب {teacher_id} - {payment_month}"]
                        })

                        st.session_state.school_journal_entries = pd.concat([
                            st.session_state.school_journal_entries, salary_expense_entry, cash_entry
                        ], ignore_index=True)

                        # Update account balances
                        update_school_account_balance('5001', salary_amount, 0.0)
                        update_school_account_balance('1001', 0.0, salary_amount)

                        st.success(f"تم دفع راتب {salary_amount:,.2f} ريال للمعلم {teacher_name} عن شهر {payment_month}")
                        st.rerun()
                else:
                    st.error("يرجى اختيار معلم / Please select a teacher")
    else:
        st.info("لا يوجد معلمون مسجلون بعد / No teachers registered yet")

def create_school_excel_export(dataframe, sheet_name):
    """Create Excel file from dataframe with proper formatting"""
    output = io.BytesIO()

    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Style the header
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="1e40af", end_color="1e40af", fill_type="solid")

            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)
        return output.getvalue()

    except Exception as e:
        st.error(f"خطأ في إنشاء ملف Excel: {str(e)}")
        return None

def create_school_pdf_export(dataframe, title):
    """Create PDF file from dataframe with proper formatting"""
    output = io.BytesIO()

    try:
        # Create PDF document
        doc = SimpleDocTemplate(output, pagesize=A4)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )

        # Add title
        title_para = Paragraph(title, title_style)
        elements.append(title_para)
        elements.append(Spacer(1, 12))

        # Convert dataframe to table data
        data = [dataframe.columns.tolist()]  # Header
        for _, row in dataframe.iterrows():
            data.append([str(cell) for cell in row])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        st.error(f"خطأ في إنشاء ملف PDF: {str(e)}")
        return None

def show_school_expenses(language, t):
    """School expense management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>💸 {t["nav_expenses"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # School-specific expense categories
    school_expense_categories = [
        "مصروفات كهرباء وماء", "مصروفات صيانة", "مصروفات قرطاسية ومواد تعليمية",
        "مصروفات نقل وانتقالات", "مصروفات أمن ونظافة", "مصروفات اتصالات وإنترنت",
        "مصروفات تدريب المعلمين", "مصروفات أنشطة طلابية", "مصروفات إدارية أخرى"
    ]

    payment_methods = ["نقداً", "شيك", "تحويل بنكي", "بطاقة ائتمان"]

    # Add new expense form
    with st.expander("➕ إضافة مصروف جديد / Add New Expense", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("التاريخ / Date", value=date.today())
            expense_type = st.selectbox("نوع المصروف / Expense Type", school_expense_categories)
            description = st.text_area("الوصف / Description")

        with col2:
            amount = st.number_input("المبلغ / Amount", value=0.0, step=10.0)
            payment_method = st.selectbox("طريقة الدفع / Payment Method", payment_methods)
            reference = st.text_input("المرجع / Reference")

            if st.button("حفظ المصروف / Save Expense", key="save_school_expense"):
                if description and amount > 0:
                    new_expense = pd.DataFrame({
                        'التاريخ': [expense_date],
                        'نوع المصروف': [expense_type],
                        'الوصف': [description],
                        'المبلغ': [amount],
                        'طريقة الدفع': [payment_method],
                        'المرجع': [reference]
                    })

                    st.session_state.school_expenses = pd.concat([
                        st.session_state.school_expenses, new_expense
                    ], ignore_index=True)

                    # Create journal entry for the expense
                    entry_number = f"EXP{len(st.session_state.school_journal_entries) + 1:03d}"

                    # Find appropriate expense account
                    expense_account = '5102'  # Default to maintenance expenses
                    expense_account_name = 'مصروفات صيانة'

                    if 'كهرباء' in expense_type or 'ماء' in expense_type:
                        expense_account = '5101'
                        expense_account_name = 'مصروفات كهرباء وماء'
                    elif 'قرطاسية' in expense_type or 'تعليمية' in expense_type:
                        expense_account = '5103'
                        expense_account_name = 'مصروفات قرطاسية ومواد تعليمية'
                    elif 'نقل' in expense_type:
                        expense_account = '5104'
                        expense_account_name = 'مصروفات نقل وانتقالات'

                    # Debit Expense, Credit Cash
                    expense_entry = pd.DataFrame({
                        'التاريخ': [expense_date],
                        'رقم القيد': [entry_number],
                        'الوصف': [description],
                        'رقم الحساب': [expense_account],
                        'اسم الحساب': [expense_account_name],
                        'مدين': [amount],
                        'دائن': [0.0],
                        'المرجع': [reference]
                    })

                    cash_entry = pd.DataFrame({
                        'التاريخ': [expense_date],
                        'رقم القيد': [entry_number],
                        'الوصف': [description],
                        'رقم الحساب': ['1001'],
                        'اسم الحساب': ['النقدية'],
                        'مدين': [0.0],
                        'دائن': [amount],
                        'المرجع': [reference]
                    })

                    st.session_state.school_journal_entries = pd.concat([
                        st.session_state.school_journal_entries, expense_entry, cash_entry
                    ], ignore_index=True)

                    # Update account balances
                    update_school_account_balance(expense_account, amount, 0.0)
                    update_school_account_balance('1001', 0.0, amount)

                    st.success("تم حفظ المصروف بنجاح! / Expense saved successfully!")
                    st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display expenses
    if not st.session_state.school_expenses.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.subheader("المصروفات المدرسية / School Expenses")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox("تصفية حسب النوع / Filter by Type",
                                     ["الكل"] + school_expense_categories)
        with col2:
            payment_filter = st.selectbox("تصفية حسب طريقة الدفع / Filter by Payment Method",
                                        ["الكل"] + payment_methods)

        # Apply filters
        filtered_expenses = st.session_state.school_expenses.copy()

        if type_filter != "الكل":
            filtered_expenses = filtered_expenses[filtered_expenses['نوع المصروف'] == type_filter]

        if payment_filter != "الكل":
            filtered_expenses = filtered_expenses[filtered_expenses['طريقة الدفع'] == payment_filter]

        # Display expenses table
        st.dataframe(
            filtered_expenses,
            use_container_width=True,
            column_config={
                "المبلغ": st.column_config.NumberColumn(format="%.2f ريال")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary and charts
        col1, col2 = st.columns(2)

        with col1:
            total_expenses = filtered_expenses['المبلغ'].sum()
            avg_expense = filtered_expenses['المبلغ'].mean() if len(filtered_expenses) > 0 else 0
            expense_count = len(filtered_expenses)

            st.metric("إجمالي المصروفات / Total Expenses", f"{total_expenses:,.2f} ريال")
            st.metric("متوسط المصروف / Average Expense", f"{avg_expense:,.2f} ريال")
            st.metric("عدد المصروفات / Number of Expenses", expense_count)

        with col2:
            # Expense by category chart
            if not filtered_expenses.empty:
                category_summary = filtered_expenses.groupby('نوع المصروف')['المبلغ'].sum().reset_index()
                fig = px.pie(category_summary, values='المبلغ', names='نوع المصروف',
                           title="المصروفات حسب النوع / Expenses by Category")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد مصروفات مضافة بعد / No expenses added yet")

def show_school_reports(language, t):
    """School-specific financial reports"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📈 {t["nav_reports"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Report selection
    report_types = [
        "ميزان المراجعة / Trial Balance",
        "تقرير الرسوم المدرسية / School Fees Report",
        "تقرير الرواتب / Salary Report",
        "تقرير المصروفات / Expenses Report",
        "قائمة الدخل / Income Statement",
        "الميزانية العمومية / Balance Sheet"
    ]

    selected_report = st.selectbox("نوع التقرير / Report Type", report_types)

    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("من تاريخ / From Date", value=date(date.today().year, 1, 1))
    with col2:
        end_date = st.date_input("إلى تاريخ / To Date", value=date.today())

    if st.button("إنشاء التقرير / Generate Report", type="primary"):
        if "ميزان المراجعة" in selected_report:
            generate_school_trial_balance(language, start_date, end_date)
        elif "الرسوم المدرسية" in selected_report:
            generate_school_fees_report(language, start_date, end_date)
        elif "الرواتب" in selected_report:
            generate_salary_report(language, start_date, end_date)
        elif "المصروفات" in selected_report:
            generate_expenses_report(language, start_date, end_date)
        elif "قائمة الدخل" in selected_report:
            generate_school_income_statement(language, start_date, end_date)
        elif "الميزانية العمومية" in selected_report:
            generate_school_balance_sheet(language, start_date, end_date)

def generate_school_trial_balance(language, start_date, end_date):
    """Generate school trial balance"""
    if st.session_state.school_accounts.empty:
        st.warning("لا توجد حسابات لإنشاء التقرير / No accounts available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("ميزان المراجعة المدرسي / School Trial Balance")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # Prepare trial balance data
    trial_balance = st.session_state.school_accounts.copy()
    trial_balance = trial_balance[['رقم الحساب', 'اسم الحساب', 'نوع الحساب', 'مدين', 'دائن', 'الرصيد الحالي']]

    # Display trial balance
    st.dataframe(
        trial_balance,
        use_container_width=True,
        column_config={
            "مدين": st.column_config.NumberColumn(format="%.2f ريال"),
            "دائن": st.column_config.NumberColumn(format="%.2f ريال"),
            "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    # Totals
    total_debit = trial_balance['مدين'].sum()
    total_credit = trial_balance['دائن'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي المدين / Total Debit", f"{total_debit:,.2f} ريال")
    with col2:
        st.metric("إجمالي الدائن / Total Credit", f"{total_credit:,.2f} ريال")
    with col3:
        difference = total_debit - total_credit
        st.metric("الفرق / Difference", f"{difference:,.2f} ريال")
        if abs(difference) > 0.01:
            st.error("الميزان غير متوازن! / Trial balance is not balanced!")
        else:
            st.success("الميزان متوازن ✓ / Trial balance is balanced ✓")

    st.markdown('</div>', unsafe_allow_html=True)

    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("تصدير Excel / Export Excel", key="export_trial_balance_excel"):
            excel_data = create_school_excel_export(trial_balance, "ميزان المراجعة")
            if excel_data:
                st.download_button(
                    "تحميل Excel / Download Excel",
                    data=excel_data,
                    file_name=f"school_trial_balance_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    with col2:
        if st.button("تصدير PDF / Export PDF", key="export_trial_balance_pdf"):
            pdf_data = create_school_pdf_export(trial_balance, "ميزان المراجعة المدرسي / School Trial Balance")
            if pdf_data:
                st.download_button(
                    "تحميل PDF / Download PDF",
                    data=pdf_data,
                    file_name=f"school_trial_balance_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

def generate_school_fees_report(language, start_date, end_date):
    """Generate school fees collection report"""
    if st.session_state.school_students.empty:
        st.warning("لا توجد بيانات طلاب لإنشاء التقرير / No student data available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("تقرير الرسوم المدرسية / School Fees Report")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # Fees summary by grade
    fees_by_grade = st.session_state.school_students.groupby('الصف').agg({
        'الرسوم السنوية': 'sum',
        'المدفوع': 'sum',
        'المتبقي': 'sum'
    }).reset_index()

    fees_by_grade['نسبة التحصيل'] = (fees_by_grade['المدفوع'] / fees_by_grade['الرسوم السنوية'] * 100).round(2)

    st.dataframe(
        fees_by_grade,
        use_container_width=True,
        column_config={
            "الرسوم السنوية": st.column_config.NumberColumn(format="%.2f ريال"),
            "المدفوع": st.column_config.NumberColumn(format="%.2f ريال"),
            "المتبقي": st.column_config.NumberColumn(format="%.2f ريال"),
            "نسبة التحصيل": st.column_config.NumberColumn(format="%.2f%%")
        }
    )

    # Overall summary
    total_fees = st.session_state.school_students['الرسوم السنوية'].sum()
    total_collected = st.session_state.school_students['المدفوع'].sum()
    total_remaining = st.session_state.school_students['المتبقي'].sum()
    collection_rate = (total_collected / total_fees * 100) if total_fees > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي الرسوم / Total Fees", f"{total_fees:,.2f} ريال")
    with col2:
        st.metric("المحصل / Collected", f"{total_collected:,.2f} ريال")
    with col3:
        st.metric("المتبقي / Remaining", f"{total_remaining:,.2f} ريال")
    with col4:
        st.metric("نسبة التحصيل / Collection Rate", f"{collection_rate:.1f}%")

    st.markdown('</div>', unsafe_allow_html=True)

    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("تصدير Excel / Export Excel", key="export_fees_excel"):
            excel_data = create_school_excel_export(fees_by_grade, "تقرير الرسوم")
            if excel_data:
                st.download_button(
                    "تحميل Excel / Download Excel",
                    data=excel_data,
                    file_name=f"school_fees_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def generate_salary_report(language, start_date, end_date):
    """Generate salary report"""
    if st.session_state.school_teachers.empty:
        st.warning("لا توجد بيانات معلمين لإنشاء التقرير / No teacher data available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("تقرير الرواتب / Salary Report")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # Salary summary by specialization
    salary_by_spec = st.session_state.school_teachers.groupby('التخصص').agg({
        'الراتب الشهري': ['count', 'sum', 'mean']
    }).round(2)

    salary_by_spec.columns = ['عدد المعلمين', 'إجمالي الرواتب', 'متوسط الراتب']
    salary_by_spec = salary_by_spec.reset_index()

    st.dataframe(
        salary_by_spec,
        use_container_width=True,
        column_config={
            "إجمالي الرواتب": st.column_config.NumberColumn(format="%.2f ريال"),
            "متوسط الراتب": st.column_config.NumberColumn(format="%.2f ريال")
        }
    )

    # Overall summary
    total_teachers = len(st.session_state.school_teachers)
    total_monthly_salaries = st.session_state.school_teachers['الراتب الشهري'].sum()
    avg_salary = st.session_state.school_teachers['الراتب الشهري'].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("عدد المعلمين / Total Teachers", total_teachers)
    with col2:
        st.metric("إجمالي الرواتب الشهرية / Total Monthly Salaries", f"{total_monthly_salaries:,.2f} ريال")
    with col3:
        st.metric("متوسط الراتب / Average Salary", f"{avg_salary:,.2f} ريال")

    st.markdown('</div>', unsafe_allow_html=True)

def show_excel_functions(language, t):
    """Excel functions for school accounting"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📋 {t["nav_excel"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Excel calculator
    st.subheader("حاسبة Excel المدرسية / School Excel Calculator")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### العمليات الحسابية / Mathematical Operations")

        num1 = st.number_input("الرقم الأول / First Number", value=0.0, key="calc_num1")
        operation = st.selectbox("العملية / Operation", [
            "جمع / Add (+)", "طرح / Subtract (-)",
            "ضرب / Multiply (×)", "قسمة / Divide (÷)"
        ])
        num2 = st.number_input("الرقم الثاني / Second Number", value=0.0, key="calc_num2")

        if st.button("احسب / Calculate", key="basic_calc"):
            try:
                if "جمع" in operation or "Add" in operation:
                    result = num1 + num2
                    st.success(f"النتيجة / Result: {result:,.2f}")
                elif "طرح" in operation or "Subtract" in operation:
                    result = num1 - num2
                    st.success(f"النتيجة / Result: {result:,.2f}")
                elif "ضرب" in operation or "Multiply" in operation:
                    result = num1 * num2
                    st.success(f"النتيجة / Result: {result:,.2f}")
                elif "قسمة" in operation or "Divide" in operation:
                    if num2 != 0:
                        result = num1 / num2
                        st.success(f"النتيجة / Result: {result:,.2f}")
                    else:
                        st.error("لا يمكن القسمة على صفر / Cannot divide by zero")
            except Exception as e:
                st.error(f"خطأ في الحساب / Calculation error: {str(e)}")

    with col2:
        st.write("### الدوال الإحصائية / Statistical Functions")

        data_input = st.text_area(
            "أدخل الأرقام (رقم في كل سطر) / Enter numbers (one per line)",
            placeholder="1000\n2000\n3000\n4000",
            key="stats_input"
        )

        if st.button("احسب الدوال / Calculate Functions", key="stats_calc"):
            try:
                if data_input.strip():
                    numbers = [float(x.strip()) for x in data_input.split('\n') if x.strip()]

                    if numbers:
                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.metric("المجموع / SUM", f"{sum(numbers):,.2f}")
                            st.metric("المتوسط / AVERAGE", f"{np.mean(numbers):,.2f}")
                            st.metric("العدد / COUNT", len(numbers))

                        with col_b:
                            st.metric("الحد الأقصى / MAX", f"{max(numbers):,.2f}")
                            st.metric("الحد الأدنى / MIN", f"{min(numbers):,.2f}")
                            st.metric("الانحراف المعياري / STDEV", f"{np.std(numbers):,.2f}")
                    else:
                        st.warning("لم يتم إدخال أرقام صحيحة / No valid numbers entered")
                else:
                    st.warning("يرجى إدخال بعض الأرقام / Please enter some numbers")
            except ValueError:
                st.error("يرجى إدخال أرقام صحيحة فقط / Please enter valid numbers only")
            except Exception as e:
                st.error(f"خطأ في الحساب / Calculation error: {str(e)}")

    # School-specific calculations
    st.markdown("---")
    st.subheader("حسابات مدرسية متخصصة / Specialized School Calculations")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("#### حساب نسبة التحصيل / Collection Rate Calculator")
        total_fees = st.number_input("إجمالي الرسوم / Total Fees", value=0.0, step=1000.0, key="total_fees_calc")
        collected_fees = st.number_input("الرسوم المحصلة / Collected Fees", value=0.0, step=1000.0, key="collected_fees_calc")

        if st.button("احسب النسبة / Calculate Rate", key="collection_rate_calc"):
            if total_fees > 0:
                rate = (collected_fees / total_fees) * 100
                remaining = total_fees - collected_fees
                st.success(f"نسبة التحصيل: {rate:.2f}%")
                st.info(f"المبلغ المتبقي: {remaining:,.2f} ريال")
            else:
                st.error("يرجى إدخال إجمالي الرسوم / Please enter total fees")

    with col2:
        st.write("#### حساب متوسط الراتب / Average Salary Calculator")
        salaries_input = st.text_area(
            "أدخل الرواتب / Enter Salaries",
            placeholder="5000\n6000\n7000",
            key="salaries_input"
        )

        if st.button("احسب المتوسط / Calculate Average", key="avg_salary_calc"):
            try:
                if salaries_input.strip():
                    salaries = [float(x.strip()) for x in salaries_input.split('\n') if x.strip()]
                    if salaries:
                        avg_salary = np.mean(salaries)
                        total_salary = sum(salaries)
                        st.success(f"متوسط الراتب: {avg_salary:,.2f} ريال")
                        st.info(f"إجمالي الرواتب: {total_salary:,.2f} ريال")
                        st.info(f"عدد المعلمين: {len(salaries)}")
                    else:
                        st.warning("لم يتم إدخال رواتب صحيحة / No valid salaries entered")
            except ValueError:
                st.error("يرجى إدخال أرقام صحيحة / Please enter valid numbers")

    with col3:
        st.write("#### حساب تكلفة الطالب / Cost Per Student Calculator")
        total_expenses = st.number_input("إجمالي المصروفات / Total Expenses", value=0.0, step=1000.0, key="total_exp_calc")
        num_students = st.number_input("عدد الطلاب / Number of Students", value=0, step=1, key="num_students_calc")

        if st.button("احسب التكلفة / Calculate Cost", key="cost_per_student_calc"):
            if num_students > 0:
                cost_per_student = total_expenses / num_students
                st.success(f"تكلفة الطالب الواحد: {cost_per_student:,.2f} ريال")
            else:
                st.error("يرجى إدخال عدد الطلاب / Please enter number of students")

    # Export templates
    st.markdown("---")
    st.subheader("قوالب Excel المدرسية / School Excel Templates")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("قالب بيانات الطلاب / Student Data Template", key="student_template"):
            template_data = pd.DataFrame({
                'رقم الطالب': ['S001', 'S002', 'S003'],
                'اسم الطالب': ['أحمد محمد', 'فاطمة علي', 'خالد سعد'],
                'الصف': ['الأول الابتدائي', 'الثاني الابتدائي', 'الثالث الابتدائي'],
                'الرسوم السنوية': [5000, 5000, 5500],
                'المدفوع': [2500, 5000, 0],
                'المتبقي': [2500, 0, 5500],
                'حالة الدفع': ['جزئي', 'مكتمل', 'غير مدفوع']
            })

            excel_data = create_school_excel_export(template_data, "قالب الطلاب")
            if excel_data:
                st.download_button(
                    "تحميل قالب الطلاب / Download Student Template",
                    data=excel_data,
                    file_name="student_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    with col2:
        if st.button("قالب بيانات المعلمين / Teacher Data Template", key="teacher_template"):
            template_data = pd.DataFrame({
                'رقم المعلم': ['T001', 'T002', 'T003'],
                'اسم المعلم': ['محمد أحمد', 'سارة محمد', 'عبدالله علي'],
                'التخصص': ['الرياضيات', 'اللغة العربية', 'العلوم'],
                'الراتب الشهري': [8000, 7500, 8500],
                'تاريخ التعيين': ['2020-01-01', '2019-09-01', '2021-02-01'],
                'الحالة': ['نشط', 'نشط', 'نشط']
            })

            excel_data = create_school_excel_export(template_data, "قالب المعلمين")
            if excel_data:
                st.download_button(
                    "تحميل قالب المعلمين / Download Teacher Template",
                    data=excel_data,
                    file_name="teacher_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    with col3:
        if st.button("قالب المصروفات / Expenses Template", key="expenses_template"):
            template_data = pd.DataFrame({
                'التاريخ': ['2024-01-01', '2024-01-02', '2024-01-03'],
                'نوع المصروف': ['مصروفات كهرباء وماء', 'مصروفات صيانة', 'مصروفات قرطاسية ومواد تعليمية'],
                'الوصف': ['فاتورة كهرباء يناير', 'صيانة أجهزة الكمبيوتر', 'شراء أوراق وأقلام'],
                'المبلغ': [2500, 1500, 800],
                'طريقة الدفع': ['تحويل بنكي', 'نقداً', 'شيك'],
                'المرجع': ['فاتورة 001', 'إيصال 002', 'فاتورة 003']
            })

            excel_data = create_school_excel_export(template_data, "قالب المصروفات")
            if excel_data:
                st.download_button(
                    "تحميل قالب المصروفات / Download Expenses Template",
                    data=excel_data,
                    file_name="expenses_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def show_school_settings(language, t):
    """School settings and configuration"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>⚙️ {t["nav_settings"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # School information
    st.subheader("معلومات المدرسة / School Information")

    col1, col2 = st.columns(2)

    with col1:
        school_name = st.text_input("اسم المدرسة / School Name", value="مدرسة المستقبل الأهلية")
        school_address = st.text_area("العنوان / Address", value="الرياض، المملكة العربية السعودية")
        school_phone = st.text_input("الهاتف / Phone", value="+966-11-XXX-XXXX")

    with col2:
        school_email = st.text_input("البريد الإلكتروني / Email", value="info@future-school.edu.sa")
        license_number = st.text_input("رقم الترخيص / License Number", value="EDU-2024-001")
        academic_year = st.text_input("العام الدراسي / Academic Year", value="1445-1446 هـ")

    if st.button("حفظ معلومات المدرسة / Save School Information"):
        st.success("تم حفظ معلومات المدرسة بنجاح! / School information saved successfully!")

    # System settings
    st.markdown("---")
    st.subheader("إعدادات النظام / System Settings")

    col1, col2 = st.columns(2)

    with col1:
        currency = st.selectbox("العملة / Currency", ["ريال سعودي / SAR", "دولار أمريكي / USD", "يورو / EUR"])
        decimal_places = st.selectbox("عدد الخانات العشرية / Decimal Places", [0, 1, 2, 3])

    with col2:
        auto_backup = st.checkbox("النسخ الاحتياطي التلقائي / Auto Backup", value=True)
        email_notifications = st.checkbox("إشعارات البريد الإلكتروني / Email Notifications")

    # Data management
    st.markdown("---")
    st.subheader("إدارة البيانات / Data Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("نسخ احتياطي شامل / Full Backup", type="primary"):
            backup_data = create_school_full_backup()
            if backup_data:
                st.download_button(
                    "تحميل النسخة الاحتياطية / Download Backup",
                    data=backup_data,
                    file_name=f"school_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    with col2:
        uploaded_backup = st.file_uploader("استعادة من نسخة احتياطية / Restore from Backup", type=['xlsx'])
        if uploaded_backup is not None:
            if st.button("استعادة البيانات / Restore Data"):
                success = restore_school_backup(uploaded_backup)
                if success:
                    st.success("تم استعادة البيانات بنجاح! / Data restored successfully!")
                    st.rerun()
                else:
                    st.error("فشل في استعادة البيانات / Failed to restore data")

    with col3:
        if st.button("مسح جميع البيانات / Clear All Data", type="secondary"):
            if st.checkbox("أؤكد مسح جميع البيانات / I confirm clearing all data"):
                clear_school_data()
                st.success("تم مسح جميع البيانات / All data cleared")
                st.rerun()

def create_school_full_backup():
    """Create full school system backup"""
    try:
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.school_accounts.to_excel(writer, sheet_name='الحسابات', index=False)
            st.session_state.school_journal_entries.to_excel(writer, sheet_name='القيود المحاسبية', index=False)
            st.session_state.school_students.to_excel(writer, sheet_name='الطلاب', index=False)
            st.session_state.school_teachers.to_excel(writer, sheet_name='المعلمين', index=False)
            st.session_state.school_expenses.to_excel(writer, sheet_name='المصروفات', index=False)

        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"خطأ في إنشاء النسخة الاحتياطية: {str(e)}")
        return None

def restore_school_backup(backup_file):
    """Restore school data from backup file"""
    try:
        sheets = pd.read_excel(backup_file, sheet_name=None)

        if 'الحسابات' in sheets:
            st.session_state.school_accounts = sheets['الحسابات']

        if 'القيود المحاسبية' in sheets:
            st.session_state.school_journal_entries = sheets['القيود المحاسبية']

        if 'الطلاب' in sheets:
            st.session_state.school_students = sheets['الطلاب']

        if 'المعلمين' in sheets:
            st.session_state.school_teachers = sheets['المعلمين']

        if 'المصروفات' in sheets:
            st.session_state.school_expenses = sheets['المصروفات']

        return True
    except Exception as e:
        st.error(f"خطأ في استعادة البيانات: {str(e)}")
        return False

def clear_school_data():
    """Clear all school system data"""
    initialize_school_data()

if __name__ == "__main__":
    main()
