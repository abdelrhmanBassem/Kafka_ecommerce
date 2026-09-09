import streamlit as st

# ضبط الصفحة لتكون بعرض الشاشة بالكامل
st.set_page_config(page_title="Events Dashboard", layout="wide")
st.title("🛒 E-Commerce Real-Time Events Funnel")

# الاتصال بـ Snowflake
conn = st.connection("snowflake")

# استعلام جميع الأعمدة مباشرة من الـ View
query = """
    SELECT *
    FROM KAFKA_DB.STREAMING.GOLD_TRANSFORMATION_TASK2
    ORDER BY EVENT_DATE DESC;
"""

df = conn.query(query)

if not df.empty:
    # توحيد أسماء الأعمدة لتجنب أي مشاكل في حالة الأحرف
    df.columns = [c.upper() for c in df.columns]

    # جلب أسماء الأعمدة المتاحة لتفادي أي خطأ إملائي سابق (مثل purschase)
    col_page = next((c for c in df.columns if "PAGE" in c), None)
    col_cart = next((c for c in df.columns if "CART" in c), None)
    col_pur = next((c for c in df.columns if "PUR" in c), None)

    # 1. عرض بطاقات الإجماليات (Metrics)
    col1, col2, col3 = st.columns(3)
    if col_page:
        col1.metric("Total Page Views", f"{df[col_page].sum():,}")
    if col_cart:
        col2.metric("Total Added to Cart", f"{df[col_cart].sum():,}")
    if col_pur:
        col3.metric("Total Purchases", f"{df[col_pur].sum():,}")

    st.divider()

    # 2. رسم بياني لتوزيع الأحداث عبر الأيام
    st.subheader("📊 Events Distribution by Date")
    if "EVENT_DATE" in df.columns:
        chart_data = df.set_index("EVENT_DATE")
        st.bar_chart(chart_data)

    # 3. عرض جدول البيانات المجمعة
    st.subheader("📋 Aggregated Data Table")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No data available yet in the View. Make sure your Kafka consumer is running and inserting events!")
