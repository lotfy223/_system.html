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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

# Configure page
st.set_page_config(
    page_title="نظام المحاسبة الشامل | Complete Accounting System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Arabic support and professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&family=Tajawal:wght@300;400;500;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
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
    
    .accounting-header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .account-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    .financial-metric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    
    .debit-amount {
        color: #e74c3c;
        font-weight: bold;
    }
    
    .credit-amount {
        color: #27ae60;
        font-weight: bold;
    }
    
    .balance-positive {
        color: #27ae60;
        font-weight: bold;
    }
    
    .balance-negative {
        color: #e74c3c;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    
    .excel-button {
        background: linear-gradient(90deg, #27ae60, #229954) !important;
    }
    
    .pdf-button {
        background: linear-gradient(90deg, #e74c3c, #c0392b) !important;
    }
    
    .data-table {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for accounting data
if 'accounts' not in st.session_state:
    st.session_state.accounts = pd.DataFrame(columns=[
        'رقم الحساب', 'اسم الحساب', 'نوع الحساب', 'الرصيد الافتتاحي', 'مدين', 'دائن', 'الرصيد الحالي'
    ])

if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = pd.DataFrame(columns=[
        'التاريخ', 'رقم القيد', 'الوصف', 'رقم الحساب', 'اسم الحساب', 'مدين', 'دائن', 'المرجع'
    ])

if 'invoices' not in st.session_state:
    st.session_state.invoices = pd.DataFrame(columns=[
        'رقم الفاتورة', 'التاريخ', 'العميل', 'الوصف', 'الكمية', 'السعر', 'الإجمالي', 'الحالة'
    ])

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=[
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
        "title": "نظام المحاسبة الشامل",
        "subtitle": "إدارة مالية متكاملة مع دعم Excel",
        "nav_dashboard": "🏠 لوحة التحكم",
        "nav_accounts": "📊 شجرة الحسابات",
        "nav_journal": "📝 القيود المحاسبية",
        "nav_invoices": "🧾 الفواتير",
        "nav_expenses": "💸 المصروفات",
        "nav_reports": "📈 التقارير",
        "nav_excel": "📋 Excel",
        "nav_settings": "⚙️ الإعدادات",
        "add_account": "إضافة حساب جديد",
        "account_number": "رقم الحساب",
        "account_name": "اسم الحساب",
        "account_type": "نوع الحساب",
        "opening_balance": "الرصيد الافتتاحي",
        "current_balance": "الرصيد الحالي",
        "debit": "مدين",
        "credit": "دائن",
        "total": "الإجمالي",
        "date": "التاريخ",
        "description": "الوصف",
        "amount": "المبلغ",
        "reference": "المرجع",
        "save": "حفظ",
        "export_excel": "تصدير Excel",
        "export_pdf": "تصدير PDF",
        "import_excel": "استيراد Excel",
        "trial_balance": "ميزان المراجعة",
        "income_statement": "قائمة الدخل",
        "balance_sheet": "الميزانية العمومية",
        "cash_flow": "قائمة التدفق النقدي"
    },
    "English": {
        "title": "Complete Accounting System",
        "subtitle": "Integrated Financial Management with Excel Support",
        "nav_dashboard": "🏠 Dashboard",
        "nav_accounts": "📊 Chart of Accounts",
        "nav_journal": "📝 Journal Entries",
        "nav_invoices": "🧾 Invoices",
        "nav_expenses": "💸 Expenses",
        "nav_reports": "📈 Reports",
        "nav_excel": "📋 Excel",
        "nav_settings": "⚙️ Settings",
        "add_account": "Add New Account",
        "account_number": "Account Number",
        "account_name": "Account Name",
        "account_type": "Account Type",
        "opening_balance": "Opening Balance",
        "current_balance": "Current Balance",
        "debit": "Debit",
        "credit": "Credit",
        "total": "Total",
        "date": "Date",
        "description": "Description",
        "amount": "Amount",
        "reference": "Reference",
        "save": "Save",
        "export_excel": "Export Excel",
        "export_pdf": "Export PDF",
        "import_excel": "Import Excel",
        "trial_balance": "Trial Balance",
        "income_statement": "Income Statement",
        "balance_sheet": "Balance Sheet",
        "cash_flow": "Cash Flow Statement"
    }
}

# Account types in both languages
account_types = {
    "العربية": [
        "الأصول المتداولة", "الأصول الثابتة", "الخصوم المتداولة", 
        "الخصوم طويلة الأجل", "رأس المال", "الإيرادات", "المصروفات"
    ],
    "English": [
        "Current Assets", "Fixed Assets", "Current Liabilities",
        "Long-term Liabilities", "Equity", "Revenue", "Expenses"
    ]
}

def main():
    language = get_language()
    t = translations[language]
    
    # Header
    st.markdown(f"""
    <div class="accounting-header">
        <h1>{t["title"]}</h1>
        <h3>{t["subtitle"]}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation / التنقل",
        [
            t["nav_dashboard"], t["nav_accounts"], t["nav_journal"],
            t["nav_invoices"], t["nav_expenses"], t["nav_reports"],
            t["nav_excel"], t["nav_settings"]
        ]
    )
    
    # Route to different pages
    if page == t["nav_dashboard"]:
        show_dashboard(language, t)
    elif page == t["nav_accounts"]:
        show_accounts(language, t)
    elif page == t["nav_journal"]:
        show_journal_entries(language, t)
    elif page == t["nav_invoices"]:
        show_invoices(language, t)
    elif page == t["nav_expenses"]:
        show_expenses(language, t)
    elif page == t["nav_reports"]:
        show_reports(language, t)
    elif page == t["nav_excel"]:
        show_excel_functions(language, t)
    elif page == t["nav_settings"]:
        show_settings(language, t)

def show_dashboard(language, t):
    """Dashboard with key financial metrics and charts"""
    text_class = "arabic-text" if language == "العربية" else "english-text"
    
    st.markdown(f"""
    <div class="{text_class}">
        <h2>📊 {t["nav_dashboard"]}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_assets = calculate_total_by_type("أصول" if language == "العربية" else "Assets")
        st.markdown(f"""
        <div class="financial-metric">
            <h4>إجمالي الأصول<br>Total Assets</h4>
            <h2 class="balance-positive">{total_assets:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_liabilities = calculate_total_by_type("خصوم" if language == "العربية" else "Liabilities")
        st.markdown(f"""
        <div class="financial-metric">
            <h4>إجمالي الخصوم<br>Total Liabilities</h4>
            <h2 class="balance-negative">{total_liabilities:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_equity = calculate_total_by_type("رأس المال" if language == "العربية" else "Equity")
        st.markdown(f"""
        <div class="financial-metric">
            <h4>رأس المال<br>Equity</h4>
            <h2 class="balance-positive">{total_equity:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        net_income = calculate_net_income()
        color_class = "balance-positive" if net_income >= 0 else "balance-negative"
        st.markdown(f"""
        <div class="financial-metric">
            <h4>صافي الدخل<br>Net Income</h4>
            <h2 class="{color_class}">{net_income:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.accounts.empty:
            # Account types pie chart
            account_summary = st.session_state.accounts.groupby('نوع الحساب')['الرصيد الحالي'].sum().reset_index()
            fig = px.pie(account_summary, values='الرصيد الحالي', names='نوع الحساب',
                        title="توزيع الحسابات حسب النوع / Account Distribution by Type")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not st.session_state.journal_entries.empty:
            # Monthly transactions chart
            monthly_data = prepare_monthly_data()
            if not monthly_data.empty:
                fig = px.bar(monthly_data, x='الشهر', y=['مدين', 'دائن'],
                           title="المعاملات الشهرية / Monthly Transactions",
                           barmode='group')
                st.plotly_chart(fig, use_container_width=True)

def calculate_total_by_type(account_type_filter):
    """Calculate total balance for specific account types"""
    if st.session_state.accounts.empty:
        return 0.0

    filtered_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains(account_type_filter, case=False, na=False)
    ]
    return filtered_accounts['الرصيد الحالي'].sum()

def calculate_net_income():
    """Calculate net income (Revenue - Expenses)"""
    if st.session_state.accounts.empty:
        return 0.0

    revenue = calculate_total_by_type("إيرادات" if get_language() == "العربية" else "Revenue")
    expenses = calculate_total_by_type("مصروفات" if get_language() == "العربية" else "Expenses")
    return revenue - expenses

def prepare_monthly_data():
    """Prepare monthly transaction data for charts"""
    if st.session_state.journal_entries.empty:
        return pd.DataFrame()

    # Convert date column and extract month
    df = st.session_state.journal_entries.copy()
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    df['الشهر'] = df['التاريخ'].dt.strftime('%Y-%m')

    # Group by month and sum debits/credits
    monthly_summary = df.groupby('الشهر').agg({
        'مدين': 'sum',
        'دائن': 'sum'
    }).reset_index()

    return monthly_summary

def show_accounts(language, t):
    """Chart of Accounts management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📊 {t["nav_accounts"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new account form
    with st.expander(f"➕ {t['add_account']}", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            account_number = st.text_input(t["account_number"])
            account_name = st.text_input(t["account_name"])
            account_type = st.selectbox(t["account_type"], account_types[language])

        with col2:
            opening_balance = st.number_input(t["opening_balance"], value=0.0, step=0.01)

            if st.button(t["save"], key="save_account"):
                if account_number and account_name:
                    new_account = pd.DataFrame({
                        'رقم الحساب': [account_number],
                        'اسم الحساب': [account_name],
                        'نوع الحساب': [account_type],
                        'الرصيد الافتتاحي': [opening_balance],
                        'مدين': [0.0],
                        'دائن': [0.0],
                        'الرصيد الحالي': [opening_balance]
                    })

                    st.session_state.accounts = pd.concat([st.session_state.accounts, new_account], ignore_index=True)
                    st.success("تم إضافة الحساب بنجاح! / Account added successfully!")
                    st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display accounts table
    if not st.session_state.accounts.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)

        # Add search and filter
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 البحث / Search")
        with col2:
            filter_type = st.selectbox("تصفية حسب النوع / Filter by Type",
                                     ["الكل / All"] + account_types[language])

        # Apply filters
        filtered_df = st.session_state.accounts.copy()

        if search_term:
            filtered_df = filtered_df[
                filtered_df['اسم الحساب'].str.contains(search_term, case=False, na=False) |
                filtered_df['رقم الحساب'].str.contains(search_term, case=False, na=False)
            ]

        if filter_type != "الكل / All":
            filtered_df = filtered_df[filtered_df['نوع الحساب'] == filter_type]

        # Display table with formatting
        st.dataframe(
            filtered_df,
            use_container_width=True,
            column_config={
                "الرصيد الافتتاحي": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "مدين": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "دائن": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "الرصيد الحالي": st.column_config.NumberColumn(
                    format="%.2f"
                )
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Export buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📊 {t['export_excel']}", key="export_accounts_excel"):
                excel_data = create_excel_export(filtered_df, "شجرة الحسابات")
                st.download_button(
                    label="تحميل ملف Excel / Download Excel",
                    data=excel_data,
                    file_name=f"chart_of_accounts_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        with col2:
            if st.button(f"📄 {t['export_pdf']}", key="export_accounts_pdf"):
                pdf_data = create_pdf_export(filtered_df, "شجرة الحسابات / Chart of Accounts")
                st.download_button(
                    label="تحميل ملف PDF / Download PDF",
                    data=pdf_data,
                    file_name=f"chart_of_accounts_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

        with col3:
            uploaded_file = st.file_uploader(f"📤 {t['import_excel']}", type=['xlsx', 'xls'])
            if uploaded_file is not None:
                try:
                    imported_df = pd.read_excel(uploaded_file)
                    # Validate and import data
                    if validate_accounts_import(imported_df):
                        st.session_state.accounts = imported_df
                        st.success("تم استيراد البيانات بنجاح! / Data imported successfully!")
                        st.rerun()
                    else:
                        st.error("تنسيق الملف غير صحيح / Invalid file format")
                except Exception as e:
                    st.error(f"خطأ في استيراد الملف / Import error: {str(e)}")
    else:
        st.info("لا توجد حسابات مضافة بعد / No accounts added yet")

def show_journal_entries(language, t):
    """Journal entries management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📝 {t["nav_journal"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new journal entry form
    with st.expander("➕ إضافة قيد محاسبي جديد / Add New Journal Entry", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            entry_date = st.date_input("التاريخ / Date", value=date.today())
            entry_number = st.text_input("رقم القيد / Entry Number")
            description = st.text_area("الوصف / Description")

        with col2:
            if not st.session_state.accounts.empty:
                account_options = [f"{row['رقم الحساب']} - {row['اسم الحساب']}"
                                 for _, row in st.session_state.accounts.iterrows()]
                selected_account = st.selectbox("الحساب / Account", account_options)

                debit_amount = st.number_input("مبلغ مدين / Debit Amount", value=0.0, step=0.01)
                credit_amount = st.number_input("مبلغ دائن / Credit Amount", value=0.0, step=0.01)
                reference = st.text_input("المرجع / Reference")

                if st.button("حفظ القيد / Save Entry", key="save_journal"):
                    if entry_number and description and selected_account and (debit_amount > 0 or credit_amount > 0):
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

                        st.session_state.journal_entries = pd.concat([st.session_state.journal_entries, new_entry], ignore_index=True)

                        # Update account balances
                        update_account_balance(account_number, debit_amount, credit_amount)

                        st.success("تم حفظ القيد بنجاح! / Entry saved successfully!")
                        st.rerun()
                    else:
                        st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")
            else:
                st.warning("يرجى إضافة حسابات أولاً / Please add accounts first")

    # Display journal entries
    if not st.session_state.journal_entries.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)

        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("من تاريخ / From Date")
        with col2:
            end_date = st.date_input("إلى تاريخ / To Date", value=date.today())

        # Filter entries by date
        filtered_entries = st.session_state.journal_entries.copy()
        filtered_entries['التاريخ'] = pd.to_datetime(filtered_entries['التاريخ'])

        if start_date and end_date:
            filtered_entries = filtered_entries[
                (filtered_entries['التاريخ'].dt.date >= start_date) &
                (filtered_entries['التاريخ'].dt.date <= end_date)
            ]

        # Display entries with formatting
        st.dataframe(
            filtered_entries,
            use_container_width=True,
            column_config={
                "مدين": st.column_config.NumberColumn(format="%.2f"),
                "دائن": st.column_config.NumberColumn(format="%.2f")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary
        total_debit = filtered_entries['مدين'].sum()
        total_credit = filtered_entries['دائن'].sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي المدين / Total Debit", f"{total_debit:,.2f}")
        with col2:
            st.metric("إجمالي الدائن / Total Credit", f"{total_credit:,.2f}")
        with col3:
            difference = total_debit - total_credit
            st.metric("الفرق / Difference", f"{difference:,.2f}")
            if abs(difference) > 0.01:
                st.warning("القيود غير متوازنة! / Entries are not balanced!")
    else:
        st.info("لا توجد قيود محاسبية مضافة بعد / No journal entries added yet")

def update_account_balance(account_number, debit_amount, credit_amount):
    """Update account balance after journal entry"""
    if not st.session_state.accounts.empty:
        mask = st.session_state.accounts['رقم الحساب'] == account_number
        if mask.any():
            st.session_state.accounts.loc[mask, 'مدين'] += debit_amount
            st.session_state.accounts.loc[mask, 'دائن'] += credit_amount

            # Calculate new balance based on account type
            account_type = st.session_state.accounts.loc[mask, 'نوع الحساب'].iloc[0]
            opening_balance = st.session_state.accounts.loc[mask, 'الرصيد الافتتاحي'].iloc[0]
            total_debit = st.session_state.accounts.loc[mask, 'مدين'].iloc[0]
            total_credit = st.session_state.accounts.loc[mask, 'دائن'].iloc[0]

            # For asset and expense accounts: Debit increases balance
            # For liability, equity, and revenue accounts: Credit increases balance
            if any(x in account_type for x in ['أصول', 'مصروفات', 'Assets', 'Expenses']):
                new_balance = opening_balance + total_debit - total_credit
            else:
                new_balance = opening_balance + total_credit - total_debit

            st.session_state.accounts.loc[mask, 'الرصيد الحالي'] = new_balance

def show_invoices(language, t):
    """Invoice management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>🧾 {t["nav_invoices"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Add new invoice form
    with st.expander("➕ إضافة فاتورة جديدة / Add New Invoice", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            invoice_number = st.text_input("رقم الفاتورة / Invoice Number")
            invoice_date = st.date_input("تاريخ الفاتورة / Invoice Date", value=date.today())
            customer = st.text_input("العميل / Customer")
            description = st.text_area("وصف الخدمة/المنتج / Description")

        with col2:
            quantity = st.number_input("الكمية / Quantity", value=1.0, step=0.01)
            unit_price = st.number_input("السعر للوحدة / Unit Price", value=0.0, step=0.01)
            total_amount = quantity * unit_price
            st.metric("الإجمالي / Total", f"{total_amount:,.2f}")

            status = st.selectbox("الحالة / Status",
                                ["مسودة / Draft", "مرسلة / Sent", "مدفوعة / Paid", "ملغاة / Cancelled"])

            if st.button("حفظ الفاتورة / Save Invoice", key="save_invoice"):
                if invoice_number and customer and description and total_amount > 0:
                    new_invoice = pd.DataFrame({
                        'رقم الفاتورة': [invoice_number],
                        'التاريخ': [invoice_date],
                        'العميل': [customer],
                        'الوصف': [description],
                        'الكمية': [quantity],
                        'السعر': [unit_price],
                        'الإجمالي': [total_amount],
                        'الحالة': [status]
                    })

                    st.session_state.invoices = pd.concat([st.session_state.invoices, new_invoice], ignore_index=True)
                    st.success("تم حفظ الفاتورة بنجاح! / Invoice saved successfully!")
                    st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display invoices
    if not st.session_state.invoices.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("تصفية حسب الحالة / Filter by Status",
                                       ["الكل / All"] + ["مسودة / Draft", "مرسلة / Sent", "مدفوعة / Paid", "ملغاة / Cancelled"])
        with col2:
            customer_filter = st.text_input("تصفية حسب العميل / Filter by Customer")
        with col3:
            date_filter = st.date_input("تصفية حسب التاريخ / Filter by Date")

        # Apply filters
        filtered_invoices = st.session_state.invoices.copy()

        if status_filter != "الكل / All":
            filtered_invoices = filtered_invoices[filtered_invoices['الحالة'] == status_filter]

        if customer_filter:
            filtered_invoices = filtered_invoices[
                filtered_invoices['العميل'].str.contains(customer_filter, case=False, na=False)
            ]

        # Display invoices table
        st.dataframe(
            filtered_invoices,
            use_container_width=True,
            column_config={
                "الكمية": st.column_config.NumberColumn(format="%.2f"),
                "السعر": st.column_config.NumberColumn(format="%.2f"),
                "الإجمالي": st.column_config.NumberColumn(format="%.2f")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary metrics
        total_invoices = len(filtered_invoices)
        total_amount = filtered_invoices['الإجمالي'].sum()
        paid_amount = filtered_invoices[filtered_invoices['الحالة'] == 'مدفوعة / Paid']['الإجمالي'].sum()
        pending_amount = total_amount - paid_amount

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("عدد الفواتير / Total Invoices", total_invoices)
        with col2:
            st.metric("إجمالي المبلغ / Total Amount", f"{total_amount:,.2f}")
        with col3:
            st.metric("المبلغ المدفوع / Paid Amount", f"{paid_amount:,.2f}")
        with col4:
            st.metric("المبلغ المعلق / Pending Amount", f"{pending_amount:,.2f}")
    else:
        st.info("لا توجد فواتير مضافة بعد / No invoices added yet")

def show_expenses(language, t):
    """Expense management"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>💸 {t["nav_expenses"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Expense categories
    expense_categories = [
        "مصروفات إدارية / Administrative", "مصروفات تشغيلية / Operational",
        "مصروفات تسويقية / Marketing", "مصروفات سفر / Travel",
        "مصروفات مكتبية / Office", "أخرى / Other"
    ]

    payment_methods = [
        "نقداً / Cash", "شيك / Check", "تحويل بنكي / Bank Transfer",
        "بطاقة ائتمان / Credit Card", "أخرى / Other"
    ]

    # Add new expense form
    with st.expander("➕ إضافة مصروف جديد / Add New Expense", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("التاريخ / Date", value=date.today())
            expense_type = st.selectbox("نوع المصروف / Expense Type", expense_categories)
            description = st.text_area("الوصف / Description")

        with col2:
            amount = st.number_input("المبلغ / Amount", value=0.0, step=0.01)
            payment_method = st.selectbox("طريقة الدفع / Payment Method", payment_methods)
            reference = st.text_input("المرجع / Reference")

            if st.button("حفظ المصروف / Save Expense", key="save_expense"):
                if description and amount > 0:
                    new_expense = pd.DataFrame({
                        'التاريخ': [expense_date],
                        'نوع المصروف': [expense_type],
                        'الوصف': [description],
                        'المبلغ': [amount],
                        'طريقة الدفع': [payment_method],
                        'المرجع': [reference]
                    })

                    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
                    st.success("تم حفظ المصروف بنجاح! / Expense saved successfully!")
                    st.rerun()
                else:
                    st.error("يرجى ملء جميع الحقول المطلوبة / Please fill all required fields")

    # Display expenses
    if not st.session_state.expenses.empty:
        st.markdown('<div class="data-table">', unsafe_allow_html=True)

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox("تصفية حسب النوع / Filter by Type",
                                     ["الكل / All"] + expense_categories)
        with col2:
            payment_filter = st.selectbox("تصفية حسب طريقة الدفع / Filter by Payment Method",
                                        ["الكل / All"] + payment_methods)

        # Apply filters
        filtered_expenses = st.session_state.expenses.copy()

        if type_filter != "الكل / All":
            filtered_expenses = filtered_expenses[filtered_expenses['نوع المصروف'] == type_filter]

        if payment_filter != "الكل / All":
            filtered_expenses = filtered_expenses[filtered_expenses['طريقة الدفع'] == payment_filter]

        # Display expenses table
        st.dataframe(
            filtered_expenses,
            use_container_width=True,
            column_config={
                "المبلغ": st.column_config.NumberColumn(format="%.2f")
            }
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Summary and charts
        col1, col2 = st.columns(2)

        with col1:
            total_expenses = filtered_expenses['المبلغ'].sum()
            avg_expense = filtered_expenses['المبلغ'].mean()
            expense_count = len(filtered_expenses)

            st.metric("إجمالي المصروفات / Total Expenses", f"{total_expenses:,.2f}")
            st.metric("متوسط المصروف / Average Expense", f"{avg_expense:,.2f}")
            st.metric("عدد المصروفات / Number of Expenses", expense_count)

        with col2:
            # Expense by category chart
            category_summary = filtered_expenses.groupby('نوع المصروف')['المبلغ'].sum().reset_index()
            if not category_summary.empty:
                fig = px.pie(category_summary, values='المبلغ', names='نوع المصروف',
                           title="المصروفات حسب النوع / Expenses by Category")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد مصروفات مضافة بعد / No expenses added yet")

def show_reports(language, t):
    """Financial reports generation"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📈 {t["nav_reports"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Report selection
    report_type = st.selectbox(
        "نوع التقرير / Report Type",
        [
            t["trial_balance"],
            t["income_statement"],
            t["balance_sheet"],
            t["cash_flow"]
        ]
    )

    # Date range for reports
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("من تاريخ / From Date", value=date(date.today().year, 1, 1))
    with col2:
        end_date = st.date_input("إلى تاريخ / To Date", value=date.today())

    if st.button("إنشاء التقرير / Generate Report"):
        if report_type == t["trial_balance"]:
            generate_trial_balance(language, start_date, end_date)
        elif report_type == t["income_statement"]:
            generate_income_statement(language, start_date, end_date)
        elif report_type == t["balance_sheet"]:
            generate_balance_sheet(language, start_date, end_date)
        elif report_type == t["cash_flow"]:
            generate_cash_flow_statement(language, start_date, end_date)

def generate_trial_balance(language, start_date, end_date):
    """Generate trial balance report"""
    if st.session_state.accounts.empty:
        st.warning("لا توجد حسابات لإنشاء التقرير / No accounts available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("ميزان المراجعة / Trial Balance")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # Prepare trial balance data
    trial_balance = st.session_state.accounts.copy()
    trial_balance = trial_balance[['رقم الحساب', 'اسم الحساب', 'نوع الحساب', 'مدين', 'دائن', 'الرصيد الحالي']]

    # Display trial balance
    st.dataframe(
        trial_balance,
        use_container_width=True,
        column_config={
            "مدين": st.column_config.NumberColumn(format="%.2f"),
            "دائن": st.column_config.NumberColumn(format="%.2f"),
            "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
        }
    )

    # Totals
    total_debit = trial_balance['مدين'].sum()
    total_credit = trial_balance['دائن'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي المدين / Total Debit", f"{total_debit:,.2f}")
    with col2:
        st.metric("إجمالي الدائن / Total Credit", f"{total_credit:,.2f}")
    with col3:
        difference = total_debit - total_credit
        st.metric("الفرق / Difference", f"{difference:,.2f}")
        if abs(difference) > 0.01:
            st.error("الميزان غير متوازن! / Trial balance is not balanced!")
        else:
            st.success("الميزان متوازن ✓ / Trial balance is balanced ✓")

    st.markdown('</div>', unsafe_allow_html=True)

    # Export options
    col1, col2 = st.columns(2)
    with col1:
        excel_data = create_excel_export(trial_balance, "ميزان المراجعة")
        st.download_button(
            "تصدير Excel / Export Excel",
            data=excel_data,
            file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        pdf_data = create_pdf_export(trial_balance, "ميزان المراجعة / Trial Balance")
        st.download_button(
            "تصدير PDF / Export PDF",
            data=pdf_data,
            file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

def generate_income_statement(language, start_date, end_date):
    """Generate income statement"""
    if st.session_state.accounts.empty:
        st.warning("لا توجد حسابات لإنشاء التقرير / No accounts available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("قائمة الدخل / Income Statement")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # Filter revenue and expense accounts
    revenue_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains('إيرادات|Revenue', case=False, na=False)
    ]
    expense_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains('مصروفات|Expenses', case=False, na=False)
    ]

    # Revenue section
    st.write("### الإيرادات / Revenues")
    if not revenue_accounts.empty:
        st.dataframe(
            revenue_accounts[['اسم الحساب', 'الرصيد الحالي']],
            use_container_width=True,
            column_config={
                "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
            }
        )
        total_revenue = revenue_accounts['الرصيد الحالي'].sum()
    else:
        total_revenue = 0
        st.info("لا توجد حسابات إيرادات / No revenue accounts")

    # Expense section
    st.write("### المصروفات / Expenses")
    if not expense_accounts.empty:
        st.dataframe(
            expense_accounts[['اسم الحساب', 'الرصيد الحالي']],
            use_container_width=True,
            column_config={
                "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
            }
        )
        total_expenses = expense_accounts['الرصيد الحالي'].sum()
    else:
        total_expenses = 0
        st.info("لا توجد حسابات مصروفات / No expense accounts")

    # Net income calculation
    net_income = total_revenue - total_expenses

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي الإيرادات / Total Revenue", f"{total_revenue:,.2f}")
    with col2:
        st.metric("إجمالي المصروفات / Total Expenses", f"{total_expenses:,.2f}")
    with col3:
        color = "normal" if net_income >= 0 else "inverse"
        st.metric("صافي الدخل / Net Income", f"{net_income:,.2f}")
        if net_income >= 0:
            st.success("ربح / Profit ✓")
        else:
            st.error("خسارة / Loss ⚠️")

    st.markdown('</div>', unsafe_allow_html=True)

def show_excel_functions(language, t):
    """Excel-like functions and calculations"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>📋 {t["nav_excel"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Excel calculator
    st.subheader("حاسبة Excel / Excel Calculator")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### العمليات الأساسية / Basic Operations")

        num1 = st.number_input("الرقم الأول / First Number", value=0.0)
        operation = st.selectbox("العملية / Operation", [
            "جمع / Add (+)", "طرح / Subtract (-)",
            "ضرب / Multiply (×)", "قسمة / Divide (÷)"
        ])
        num2 = st.number_input("الرقم الثاني / Second Number", value=0.0)

        if st.button("احسب / Calculate"):
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

    with col2:
        st.write("### الدوال المحاسبية / Accounting Functions")

        # Data input for calculations
        data_input = st.text_area(
            "أدخل الأرقام (رقم في كل سطر) / Enter numbers (one per line)",
            placeholder="100\n200\n300\n400"
        )

        if data_input:
            try:
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

                    # Advanced calculations
                    st.write("### حسابات متقدمة / Advanced Calculations")

                    # Percentage calculations
                    if len(numbers) >= 2:
                        percentage_change = ((numbers[-1] - numbers[0]) / numbers[0]) * 100
                        st.metric("نسبة التغيير / Percentage Change", f"{percentage_change:,.2f}%")

                    # Compound growth rate
                    if len(numbers) >= 2:
                        periods = len(numbers) - 1
                        cagr = (((numbers[-1] / numbers[0]) ** (1/periods)) - 1) * 100
                        st.metric("معدل النمو المركب / CAGR", f"{cagr:,.2f}%")

            except ValueError:
                st.error("يرجى إدخال أرقام صحيحة فقط / Please enter valid numbers only")

    # Excel import/export section
    st.markdown("---")
    st.subheader("استيراد/تصدير Excel / Excel Import/Export")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### تصدير البيانات / Export Data")
        export_type = st.selectbox("نوع البيانات / Data Type", [
            "الحسابات / Accounts", "القيود / Journal Entries",
            "الفواتير / Invoices", "المصروفات / Expenses"
        ])

        if st.button("تصدير إلى Excel / Export to Excel"):
            if "الحسابات" in export_type or "Accounts" in export_type:
                data = st.session_state.accounts
                filename = "accounts"
            elif "القيود" in export_type or "Journal" in export_type:
                data = st.session_state.journal_entries
                filename = "journal_entries"
            elif "الفواتير" in export_type or "Invoices" in export_type:
                data = st.session_state.invoices
                filename = "invoices"
            else:
                data = st.session_state.expenses
                filename = "expenses"

            if not data.empty:
                excel_data = create_excel_export(data, export_type)
                st.download_button(
                    "تحميل الملف / Download File",
                    data=excel_data,
                    file_name=f"{filename}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("لا توجد بيانات للتصدير / No data to export")

    with col2:
        st.write("### استيراد البيانات / Import Data")
        uploaded_file = st.file_uploader("اختر ملف Excel / Choose Excel File", type=['xlsx', 'xls'])

        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.write("معاينة البيانات / Data Preview:")
                st.dataframe(df.head())

                import_type = st.selectbox("نوع الاستيراد / Import Type", [
                    "الحسابات / Accounts", "القيود / Journal Entries",
                    "الفواتير / Invoices", "المصروفات / Expenses"
                ])

                if st.button("استيراد البيانات / Import Data"):
                    # Validate and import based on type
                    success = import_excel_data(df, import_type)
                    if success:
                        st.success("تم الاستيراد بنجاح! / Import successful!")
                        st.rerun()
                    else:
                        st.error("فشل في الاستيراد - تحقق من تنسيق الملف / Import failed - check file format")

            except Exception as e:
                st.error(f"خطأ في قراءة الملف / Error reading file: {str(e)}")

    with col3:
        st.write("### قوالب Excel / Excel Templates")
        st.write("تحميل قوالب جاهزة / Download ready templates:")

        templates = {
            "قالب الحسابات / Accounts Template": create_accounts_template(),
            "قالب القيود / Journal Template": create_journal_template(),
            "قالب الفواتير / Invoices Template": create_invoices_template(),
            "قالب المصروفات / Expenses Template": create_expenses_template()
        }

        for template_name, template_data in templates.items():
            st.download_button(
                template_name,
                data=template_data,
                file_name=f"{template_name.split('/')[0].replace(' ', '_').lower()}_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def create_excel_export(dataframe, sheet_name):
    """Create Excel file from dataframe"""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Style the header
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")

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

def create_pdf_export(dataframe, title):
    """Create PDF file from dataframe"""
    output = io.BytesIO()

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
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)
    output.seek(0)
    return output.getvalue()

def validate_accounts_import(dataframe):
    """Validate imported accounts data"""
    required_columns = ['رقم الحساب', 'اسم الحساب', 'نوع الحساب', 'الرصيد الافتتاحي']
    return all(col in dataframe.columns for col in required_columns)

def import_excel_data(dataframe, import_type):
    """Import Excel data into the system"""
    try:
        if "الحسابات" in import_type or "Accounts" in import_type:
            if validate_accounts_import(dataframe):
                # Add missing columns if needed
                for col in ['مدين', 'دائن', 'الرصيد الحالي']:
                    if col not in dataframe.columns:
                        dataframe[col] = 0.0

                dataframe['الرصيد الحالي'] = dataframe['الرصيد الافتتاحي']
                st.session_state.accounts = dataframe
                return True

        elif "القيود" in import_type or "Journal" in import_type:
            required_cols = ['التاريخ', 'رقم القيد', 'الوصف', 'رقم الحساب', 'اسم الحساب', 'مدين', 'دائن']
            if all(col in dataframe.columns for col in required_cols):
                st.session_state.journal_entries = dataframe
                return True

        elif "الفواتير" in import_type or "Invoices" in import_type:
            required_cols = ['رقم الفاتورة', 'التاريخ', 'العميل', 'الوصف', 'الكمية', 'السعر', 'الإجمالي']
            if all(col in dataframe.columns for col in required_cols):
                st.session_state.invoices = dataframe
                return True

        elif "المصروفات" in import_type or "Expenses" in import_type:
            required_cols = ['التاريخ', 'نوع المصروف', 'الوصف', 'المبلغ', 'طريقة الدفع']
            if all(col in dataframe.columns for col in required_cols):
                st.session_state.expenses = dataframe
                return True

        return False
    except Exception:
        return False

def create_accounts_template():
    """Create accounts template Excel file"""
    template_data = pd.DataFrame({
        'رقم الحساب': ['1001', '1002', '2001', '3001', '4001', '5001'],
        'اسم الحساب': ['النقدية', 'البنك', 'حسابات دائنة', 'رأس المال', 'إيرادات المبيعات', 'مصروفات إدارية'],
        'نوع الحساب': ['الأصول المتداولة', 'الأصول المتداولة', 'الخصوم المتداولة', 'رأس المال', 'الإيرادات', 'المصروفات'],
        'الرصيد الافتتاحي': [10000, 50000, 5000, 100000, 0, 0]
    })

    return create_excel_export(template_data, "قالب الحسابات")

def create_journal_template():
    """Create journal entries template Excel file"""
    template_data = pd.DataFrame({
        'التاريخ': ['2024-01-01', '2024-01-02'],
        'رقم القيد': ['J001', 'J002'],
        'الوصف': ['قيد افتتاحي', 'مبيعات نقدية'],
        'رقم الحساب': ['1001', '4001'],
        'اسم الحساب': ['النقدية', 'إيرادات المبيعات'],
        'مدين': [10000, 0],
        'دائن': [0, 10000],
        'المرجع': ['افتتاحي', 'فاتورة 001']
    })

    return create_excel_export(template_data, "قالب القيود")

def create_invoices_template():
    """Create invoices template Excel file"""
    template_data = pd.DataFrame({
        'رقم الفاتورة': ['INV001', 'INV002'],
        'التاريخ': ['2024-01-01', '2024-01-02'],
        'العميل': ['عميل أ', 'عميل ب'],
        'الوصف': ['خدمة استشارية', 'منتج أ'],
        'الكمية': [1, 2],
        'السعر': [1000, 500],
        'الإجمالي': [1000, 1000],
        'الحالة': ['مرسلة / Sent', 'مدفوعة / Paid']
    })

    return create_excel_export(template_data, "قالب الفواتير")

def create_expenses_template():
    """Create expenses template Excel file"""
    template_data = pd.DataFrame({
        'التاريخ': ['2024-01-01', '2024-01-02'],
        'نوع المصروف': ['مصروفات إدارية / Administrative', 'مصروفات تشغيلية / Operational'],
        'الوصف': ['إيجار المكتب', 'فواتير كهرباء'],
        'المبلغ': [5000, 1000],
        'طريقة الدفع': ['تحويل بنكي / Bank Transfer', 'نقداً / Cash'],
        'المرجع': ['عقد إيجار', 'فاتورة كهرباء']
    })

    return create_excel_export(template_data, "قالب المصروفات")

def generate_balance_sheet(language, start_date, end_date):
    """Generate balance sheet report"""
    if st.session_state.accounts.empty:
        st.warning("لا توجد حسابات لإنشاء التقرير / No accounts available for report")
        return

    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("الميزانية العمومية / Balance Sheet")
    st.write(f"كما في {end_date} / As of {end_date}")

    # Assets
    asset_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains('أصول|Assets', case=False, na=False)
    ]

    # Liabilities
    liability_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains('خصوم|Liabilities', case=False, na=False)
    ]

    # Equity
    equity_accounts = st.session_state.accounts[
        st.session_state.accounts['نوع الحساب'].str.contains('رأس المال|Equity', case=False, na=False)
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.write("### الأصول / Assets")
        if not asset_accounts.empty:
            st.dataframe(
                asset_accounts[['اسم الحساب', 'الرصيد الحالي']],
                use_container_width=True,
                column_config={
                    "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
                }
            )
            total_assets = asset_accounts['الرصيد الحالي'].sum()
            st.metric("إجمالي الأصول / Total Assets", f"{total_assets:,.2f}")
        else:
            total_assets = 0
            st.info("لا توجد حسابات أصول / No asset accounts")

    with col2:
        st.write("### الخصوم ورأس المال / Liabilities & Equity")

        if not liability_accounts.empty:
            st.write("#### الخصوم / Liabilities")
            st.dataframe(
                liability_accounts[['اسم الحساب', 'الرصيد الحالي']],
                use_container_width=True,
                column_config={
                    "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
                }
            )
            total_liabilities = liability_accounts['الرصيد الحالي'].sum()
        else:
            total_liabilities = 0

        if not equity_accounts.empty:
            st.write("#### رأس المال / Equity")
            st.dataframe(
                equity_accounts[['اسم الحساب', 'الرصيد الحالي']],
                use_container_width=True,
                column_config={
                    "الرصيد الحالي": st.column_config.NumberColumn(format="%.2f")
                }
            )
            total_equity = equity_accounts['الرصيد الحالي'].sum()
        else:
            total_equity = 0

        total_liab_equity = total_liabilities + total_equity

        st.metric("إجمالي الخصوم / Total Liabilities", f"{total_liabilities:,.2f}")
        st.metric("إجمالي رأس المال / Total Equity", f"{total_equity:,.2f}")
        st.metric("إجمالي الخصوم ورأس المال / Total Liab. & Equity", f"{total_liab_equity:,.2f}")

    # Balance check
    st.markdown("---")
    balance_difference = total_assets - total_liab_equity

    if abs(balance_difference) < 0.01:
        st.success("الميزانية متوازنة ✓ / Balance Sheet is balanced ✓")
    else:
        st.error(f"الميزانية غير متوازنة! الفرق: {balance_difference:,.2f} / Balance Sheet is not balanced! Difference: {balance_difference:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

def generate_cash_flow_statement(language, start_date, end_date):
    """Generate cash flow statement"""
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.subheader("قائمة التدفق النقدي / Cash Flow Statement")
    st.write(f"من {start_date} إلى {end_date} / From {start_date} to {end_date}")

    # This is a simplified cash flow statement
    # In a real system, you would track cash movements more precisely

    if not st.session_state.journal_entries.empty:
        # Filter cash-related entries
        cash_entries = st.session_state.journal_entries[
            st.session_state.journal_entries['اسم الحساب'].str.contains('نقد|cash|بنك|bank', case=False, na=False)
        ]

        if not cash_entries.empty:
            # Operating activities (simplified)
            operating_inflows = cash_entries[cash_entries['دائن'] > 0]['دائن'].sum()
            operating_outflows = cash_entries[cash_entries['مدين'] > 0]['مدين'].sum()
            net_operating = operating_inflows - operating_outflows

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("### الأنشطة التشغيلية / Operating Activities")
                st.metric("التدفقات الداخلة / Cash Inflows", f"{operating_inflows:,.2f}")
                st.metric("التدفقات الخارجة / Cash Outflows", f"{operating_outflows:,.2f}")
                st.metric("صافي التدفق التشغيلي / Net Operating Cash Flow", f"{net_operating:,.2f}")

            with col2:
                st.write("### الأنشطة الاستثمارية / Investing Activities")
                st.info("لا توجد بيانات / No data available")

            with col3:
                st.write("### الأنشطة التمويلية / Financing Activities")
                st.info("لا توجد بيانات / No data available")

            st.markdown("---")
            st.metric("صافي التغير في النقدية / Net Change in Cash", f"{net_operating:,.2f}")
        else:
            st.info("لا توجد معاملات نقدية / No cash transactions found")
    else:
        st.info("لا توجد قيود محاسبية / No journal entries available")

    st.markdown('</div>', unsafe_allow_html=True)

def show_settings(language, t):
    """System settings and configuration"""
    text_class = "arabic-text" if language == "العربية" else "english-text"

    st.markdown(f"""
    <div class="{text_class}">
        <h2>⚙️ {t["nav_settings"]}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Company information
    st.subheader("معلومات الشركة / Company Information")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("اسم الشركة / Company Name", value="شركة المحاسبة المتقدمة")
        company_address = st.text_area("العنوان / Address")
        company_phone = st.text_input("الهاتف / Phone")

    with col2:
        company_email = st.text_input("البريد الإلكتروني / Email")
        tax_number = st.text_input("الرقم الضريبي / Tax Number")
        currency = st.selectbox("العملة / Currency", ["ريال سعودي / SAR", "دولار أمريكي / USD", "يورو / EUR"])

    # System settings
    st.subheader("إعدادات النظام / System Settings")

    col1, col2 = st.columns(2)

    with col1:
        fiscal_year_start = st.date_input("بداية السنة المالية / Fiscal Year Start", value=date(date.today().year, 1, 1))
        decimal_places = st.selectbox("عدد الخانات العشرية / Decimal Places", [0, 1, 2, 3, 4])

    with col2:
        auto_backup = st.checkbox("النسخ الاحتياطي التلقائي / Auto Backup")
        email_notifications = st.checkbox("إشعارات البريد الإلكتروني / Email Notifications")

    # Data management
    st.subheader("إدارة البيانات / Data Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("نسخ احتياطي للبيانات / Backup Data"):
            backup_data = create_full_backup()
            st.download_button(
                "تحميل النسخة الاحتياطية / Download Backup",
                data=backup_data,
                file_name=f"accounting_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        uploaded_backup = st.file_uploader("استعادة من نسخة احتياطية / Restore from Backup", type=['xlsx'])
        if uploaded_backup is not None:
            if st.button("استعادة البيانات / Restore Data"):
                success = restore_from_backup(uploaded_backup)
                if success:
                    st.success("تم استعادة البيانات بنجاح! / Data restored successfully!")
                    st.rerun()
                else:
                    st.error("فشل في استعادة البيانات / Failed to restore data")

    with col3:
        if st.button("مسح جميع البيانات / Clear All Data", type="secondary"):
            if st.checkbox("أؤكد مسح جميع البيانات / I confirm clearing all data"):
                clear_all_data()
                st.success("تم مسح جميع البيانات / All data cleared")
                st.rerun()

def create_full_backup():
    """Create full system backup"""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.accounts.to_excel(writer, sheet_name='الحسابات', index=False)
        st.session_state.journal_entries.to_excel(writer, sheet_name='القيود المحاسبية', index=False)
        st.session_state.invoices.to_excel(writer, sheet_name='الفواتير', index=False)
        st.session_state.expenses.to_excel(writer, sheet_name='المصروفات', index=False)

    output.seek(0)
    return output.getvalue()

def restore_from_backup(backup_file):
    """Restore data from backup file"""
    try:
        # Read all sheets
        sheets = pd.read_excel(backup_file, sheet_name=None)

        if 'الحسابات' in sheets:
            st.session_state.accounts = sheets['الحسابات']

        if 'القيود المحاسبية' in sheets:
            st.session_state.journal_entries = sheets['القيود المحاسبية']

        if 'الفواتير' in sheets:
            st.session_state.invoices = sheets['الفواتير']

        if 'المصروفات' in sheets:
            st.session_state.expenses = sheets['المصروفات']

        return True
    except Exception:
        return False

def clear_all_data():
    """Clear all system data"""
    st.session_state.accounts = pd.DataFrame(columns=[
        'رقم الحساب', 'اسم الحساب', 'نوع الحساب', 'الرصيد الافتتاحي', 'مدين', 'دائن', 'الرصيد الحالي'
    ])
    st.session_state.journal_entries = pd.DataFrame(columns=[
        'التاريخ', 'رقم القيد', 'الوصف', 'رقم الحساب', 'اسم الحساب', 'مدين', 'دائن', 'المرجع'
    ])
    st.session_state.invoices = pd.DataFrame(columns=[
        'رقم الفاتورة', 'التاريخ', 'العميل', 'الوصف', 'الكمية', 'السعر', 'الإجمالي', 'الحالة'
    ])
    st.session_state.expenses = pd.DataFrame(columns=[
        'التاريخ', 'نوع المصروف', 'الوصف', 'المبلغ', 'طريقة الدفع', 'المرجع'
    ])

if __name__ == "__main__":
    main()
