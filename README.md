# 🏨 Hotel Analytics Dashboard

An interactive data analytics dashboard for hotel bookings, developed to provide real-time insights into key performance indicators such as bookings, revenue, average stay duration, hotel ratings, and booking trends. Built using Python and Streamlit, this tool enables users to upload hotel data in Excel format and analyze it visually and interactively.

## 📊 Key Features

- **Dynamic Data Upload**: Supports `.xlsx` file input with drag-and-drop capability.
- **Interactive Filters**:
  - Hotel Rating
  - Area
  - Booking Type
  - Check-in Date Range
  - Days Stayed Range
- **Visual Analytics**:
  - Hotel Rating Distribution
  - Bookings by Hotel Rating
  - Area Performance (Rating vs Average Stay)
  - Booking Type Analysis
  - Check-in Trends (Monthly)
  - Stay Duration Distribution
  - Correlation Matrix (between rating, days stayed, price, and guest count)
- **Export Functionality**: Download filtered datasets as CSV.
- **Date Coverage**: Sample data spans from `2023-01-01` to `2024-12-31`.

## 📈 Metrics Overview

- **Total Bookings**: 725
- **Average Rating**: 3.5 ⭐
- **Average Stay**: 5.4 days
- **Total Revenue**: $1,117 (sample data)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `pip install -r requirements.txt`

### Installation

```bash
git clone https://github.com/hotel-analytics-dashboard.git
cd hotel-analytics-dashboard
pip install -r requirements.txt

hotel-analytics-dashboard/
│
├── app.py                  # Main Streamlit app
├── sample_data.xlsx        # Example hotel booking dataset
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

