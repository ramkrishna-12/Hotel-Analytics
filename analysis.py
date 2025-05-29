import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# Set page configuration
st.set_page_config(
    page_title="Hotel Analytics Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and process data
@st.cache_data
def load_data(file):
    """Load data from Excel file"""
    try:
        df = pd.read_excel(r"C:\Users\Rupam\Desktop\ana\Version 2 Analytics Test_ Ramkrishna R. Barman.xlsx")
        # Convert check_in to datetime if it's not already
        if 'check_in' in df.columns:
            df['check_in'] = pd.to_datetime(df['check_in'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to create sample data if no file is uploaded
def create_sample_data():
    """Create sample hotel booking data"""
    np.random.seed(42)
    n_records = 1000
    
    areas = ['Downtown', 'Airport', 'Beach', 'Mountains', 'Suburbs', 'City Center']
    booking_types = ['Online', 'Phone', 'Walk-in', 'Travel Agent', 'Corporate']
    
    data = {
        'hotel_id': range(1, n_records + 1),
        'hotel_rating': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.05, 0.1, 0.3, 0.4, 0.15]),
        'area': np.random.choice(areas, n_records),
        'booking_type': np.random.choice(booking_types, n_records),
        'total_days_stayed': np.random.randint(1, 15, n_records),
        'check_in': pd.date_range(start='2023-01-01', end='2024-12-31', periods=n_records),
        'price_per_night': np.random.randint(50, 500, n_records),
        'guest_count': np.random.randint(1, 6, n_records)
    }
    
    df = pd.DataFrame(data)
    df['total_revenue'] = df['price_per_night'] * df['total_days_stayed']
    return df

# Main dashboard function
def main():
    st.markdown('<h1 class="main-header">🏨 Hotel Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for file upload and filters
    st.sidebar.header("📊 Data & Filters")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File", 
        type=['xlsx', 'xls'],
        help="Upload your hotel booking data in Excel format"
    )
    
    # Load data
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is None:
            return
        st.sidebar.success("✅ File uploaded successfully!")
    else:
        st.sidebar.info("Using sample data. Upload your Excel file to analyze your own data.")
        df = create_sample_data()
    
    # Display data info
    st.sidebar.markdown("### 📋 Data Overview")
    st.sidebar.info(f"Total Records: {len(df)}")
    st.sidebar.info(f"Date Range: {df['check_in'].min().strftime('%Y-%m-%d')} to {df['check_in'].max().strftime('%Y-%m-%d')}")
    
    # Filters
    st.sidebar.markdown("### 🔍 Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Check-in Date Range",
        value=(df['check_in'].min().date(), df['check_in'].max().date()),
        min_value=df['check_in'].min().date(),
        max_value=df['check_in'].max().date()
    )
    
    # Rating filter
    rating_filter = st.sidebar.multiselect(
        "Hotel Rating",
        options=sorted(df['hotel_rating'].unique()),
        default=sorted(df['hotel_rating'].unique())
    )
    
    # Area filter
    area_filter = st.sidebar.multiselect(
        "Area",
        options=sorted(df['area'].unique()),
        default=sorted(df['area'].unique())
    )
    
    # Booking type filter
    booking_type_filter = st.sidebar.multiselect(
        "Booking Type",
        options=sorted(df['booking_type'].unique()),
        default=sorted(df['booking_type'].unique())
    )
    
    # Days stayed filter
    days_range = st.sidebar.slider(
        "Days Stayed Range",
        min_value=int(df['total_days_stayed'].min()),
        max_value=int(df['total_days_stayed'].max()),
        value=(int(df['total_days_stayed'].min()), int(df['total_days_stayed'].max()))
    )
    
    # Apply filters
    filtered_df = df[
        (df['check_in'].dt.date >= date_range[0]) &
        (df['check_in'].dt.date <= date_range[1]) &
        (df['hotel_rating'].isin(rating_filter)) &
        (df['area'].isin(area_filter)) &
        (df['booking_type'].isin(booking_type_filter)) &
        (df['total_days_stayed'] >= days_range[0]) &
        (df['total_days_stayed'] <= days_range[1])
    ]
    
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters. Please adjust your filters.")
        return
    
    # Key Metrics
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Bookings",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df) + len(filtered_df):.0f} vs Total"
        )
    
    with col2:
        avg_rating = filtered_df['hotel_rating'].mean()
        st.metric(
            label="Average Rating",
            value=f"{avg_rating:.1f}⭐",
            delta=f"{avg_rating - df['hotel_rating'].mean():.1f}"
        )
    
    with col3:
        avg_stay = filtered_df['total_days_stayed'].mean()
        st.metric(
            label="Average Stay (days)",
            value=f"{avg_stay:.1f}",
            delta=f"{avg_stay - df['total_days_stayed'].mean():.1f}"
        )
    
    with col4:
        if 'total_revenue' in filtered_df.columns:
            total_revenue = filtered_df['total_revenue'].sum()
            st.metric(
                label="Total Revenue",
                value=f"${total_revenue:,.0f}",
                delta=f"${total_revenue - df['total_revenue'].sum() + total_revenue:.0f}"
            )
    
    with col5:
        occupancy_rate = len(filtered_df) / len(df) * 100
        st.metric(
            label="Data Coverage",
            value=f"{occupancy_rate:.1f}%",
            delta=f"{occupancy_rate - 100:.1f}%"
        )
    
    # Charts
    st.markdown("## 📊 Analytics")
    
    # Row 1: Rating Distribution and Area Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Hotel Rating Distribution")
        rating_counts = filtered_df['hotel_rating'].value_counts().sort_index()
        
        fig_rating = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': 'Hotel Rating', 'y': 'Number of Bookings'},
            title="Bookings by Hotel Rating",
            color=rating_counts.values,
            color_continuous_scale='viridis'
        )
        fig_rating.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_rating, use_container_width=True)
    
    with col2:
        st.markdown("### Performance by Area")
        area_stats = filtered_df.groupby('area').agg({
            'hotel_rating': 'mean',
            'total_days_stayed': 'mean',
            'hotel_id': 'count'
        }).round(2)
        area_stats.columns = ['Avg Rating', 'Avg Stay Days', 'Bookings']
        
        fig_area = px.scatter(
            area_stats,
            x='Avg Rating',
            y='Avg Stay Days',
            size='Bookings',
            hover_name=area_stats.index,
            title="Area Performance (Rating vs Stay Duration)",
            labels={'Avg Rating': 'Average Rating', 'Avg Stay Days': 'Average Stay (days)'}
        )
        fig_area.update_layout(height=400)
        st.plotly_chart(fig_area, use_container_width=True)
    
    # Row 2: Booking Type Analysis and Time Series
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Booking Type Analysis")
        booking_type_data = filtered_df.groupby('booking_type').agg({
            'hotel_id': 'count',
            'total_days_stayed': 'mean',
            'hotel_rating': 'mean'
        }).round(2)
        
        fig_booking = px.pie(
            values=booking_type_data['hotel_id'],
            names=booking_type_data.index,
            title="Booking Distribution by Type"
        )
        fig_booking.update_layout(height=400)
        st.plotly_chart(fig_booking, use_container_width=True)
    
    with col2:
        st.markdown("### Check-in Trends Over Time")
        # Resample by month for better visualization
        time_series = filtered_df.set_index('check_in').resample('M').size()
        
        fig_time = px.line(
            x=time_series.index,
            y=time_series.values,
            title="Monthly Check-in Trends",
            labels={'x': 'Month', 'y': 'Number of Check-ins'}
        )
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Row 3: Stay Duration Analysis
    st.markdown("### Stay Duration Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram of stay duration
        fig_duration = px.histogram(
            filtered_df,
            x='total_days_stayed',
            nbins=20,
            title="Distribution of Stay Duration",
            labels={'total_days_stayed': 'Days Stayed', 'count': 'Frequency'}
        )
        fig_duration.update_layout(height=400)
        st.plotly_chart(fig_duration, use_container_width=True)
    
    with col2:
        # Box plot of stay duration by rating
        fig_box = px.box(
            filtered_df,
            x='hotel_rating',
            y='total_days_stayed',
            title="Stay Duration by Hotel Rating",
            labels={'hotel_rating': 'Hotel Rating', 'total_days_stayed': 'Days Stayed'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Correlation Heatmap
    st.markdown("### Correlation Analysis")
    numeric_cols = ['hotel_rating', 'total_days_stayed']
    if 'price_per_night' in filtered_df.columns:
        numeric_cols.append('price_per_night')
    if 'guest_count' in filtered_df.columns:
        numeric_cols.append('guest_count')
    
    if len(numeric_cols) > 1:
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            title="Correlation Matrix",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Data Table
    st.markdown("## 📋 Filtered Data")
    
    # Display options
    col1, col2 = st.columns([1, 3])
    with col1:
        show_records = st.selectbox("Records to show:", [10, 25, 50, 100, "All"])
    
    if show_records == "All":
        display_df = filtered_df
    else:
        display_df = filtered_df.head(show_records)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"hotel_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Note:** This dashboard provides interactive analysis of hotel booking data. "
        "Use the filters in the sidebar to explore different aspects of your data."
    )

if __name__ == "__main__":
    main()