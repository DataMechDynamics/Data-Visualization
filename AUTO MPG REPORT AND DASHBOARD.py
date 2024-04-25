import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go

# Use set_page_config at the beginning to define layout
st.set_page_config(layout="wide")

# Function to load data
@st.cache_resource  # Use Streamlit's cache to load data only once
def load_data():
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
    columns = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'Model Year', 'Origin', 'Car Name']
    data = pd.read_csv(url, delim_whitespace=True, names=columns)
    data['Origin'] = data['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
    # Extract manufacturer from the 'Car Name'
    data['Manufacturer'] = data['Car Name'].apply(lambda x: x.split()[0])
    return data

data = load_data()
numeric_columns = data.select_dtypes(include=['float64', 'float32', 'int32', 'int64']).columns
manufacturers = data['Manufacturer'].unique()

# Create tabs
tab1, tab2 = st.tabs(["Dashboard", "Report"])

# Dashboard tab
with tab1:
    st.header("Automobile Data Visualization Dashboard")
    # Sidebar setup for filtering by Manufacturer
    manufacturer_filter = st.sidebar.checkbox("Filter by Manufacturer")
    if manufacturer_filter:
        selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers)
        data = data[data['Manufacturer'] == selected_manufacturer]

# Sidebar setup for filtering by Model Year
    model_year_filter = st.sidebar.checkbox("Filter by Model Year")
    if model_year_filter:
        selected_year = st.sidebar.slider("Select Model Year", int(data['Model Year'].min()), int(data['Model Year'].max()))
        data = data[data['Model Year'] == selected_year]

    # Checkbox widget for displaying data
    checkbox = st.sidebar.checkbox("Reveal data.")
    if checkbox:
        st.dataframe(data)

    # Scatterplot setup
    st.sidebar.subheader("Scatter plot setup")
    select_box1 = st.sidebar.selectbox('X axis', options=numeric_columns)
    st.sidebar.markdown("Y axis is fixed to MPG.")
    color_by_origin_scatter = st.sidebar.checkbox("Color by Origin in Scatter Plot", False)
    add_trendline = st.sidebar.checkbox("Add Trendline", False)

    # Creating scatterplot
    if color_by_origin_scatter:
        fig = px.scatter(data, x=select_box1, y='MPG', color='Origin', trendline="ols" if add_trendline else None,
                         hover_data=['Car Name', 'Cylinders', 'Horsepower'])
    else:
        fig = px.scatter(data, x=select_box1, y='MPG', trendline="ols" if add_trendline else None,
                         hover_data=['Car Name', 'Cylinders', 'Horsepower'])
    st.plotly_chart(fig)

    # Histogram setup
    st.sidebar.subheader("Histogram")
    select_box3 = st.sidebar.selectbox("Feature for Histogram", options=numeric_columns, key='hist')
    histogram_slider = st.sidebar.slider("Number of Bins", min_value=3, max_value=20, value=8)
    overlay_histograms = st.sidebar.checkbox("Overlay Histograms by Origin", True)

    # Creating histogram with Plotly
    if overlay_histograms:
        fig2 = px.histogram(data, x=select_box3, color='Origin', nbins=histogram_slider, barmode='overlay',
                            histnorm='percent', opacity=0.75)
        fig2.update_traces(marker_line_color='black', marker_line_width=1)
    else:
        fig2 = px.histogram(data, x=select_box3, nbins=histogram_slider, histnorm='percent', opacity=0.75)
        fig2.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig2)


# Report tab
# Report tab with Plotly visualizations
with tab2:
    st.header("Automobile Data Analysis Report")
    st.markdown("""
        ## 1.0 Introduction
        Understanding the factors that influence fuel efficiency in automobiles is crucial for advancing automotive technology, allowing for reduced emissions and operational costs.
        This report aims to analyze the Auto MPG dataset, a collection of vehicle data from the 1970s to the 1980s. 
        By exploring attributes such as miles per gallon (MPG), cylinder count, and horsepower, this project aims to uncover historical trends in car efficiency and apply modern visualization techniques to reveal insights that can inform current and future challenges in automotive design. 
        This dataset allows for an in-depth exploration of the complex links between car design features and their fuel efficiencies. 
        Analyzing this data set via visual exploration will allow for a straightforward understanding of how vehicle attributes influence overall energy consumption.
        
        ## 2.0 Data Description
        ### 2.1 Source
        For this project, the Auto MPG dataset will be utilized. The data set was originally compiled for the analysis of fuel efficiency in cars in the 1970s to 1980s.
         "The data concerns city-cycle fuel consumption in miles per gallon, to be predicted in terms of 3 multivalued discrete and 5 continuous attributes." (Quinlan, 1993). 
        Sourced from UCI Machine Learning Repository.

        ### 2.2 Key Attributes
        The dataset comprises several important attributes for analyzing vehicle performance and fuel efficiency:
        - **MPG (Miles Per Gallon):** A continuous variable representing fuel efficiency, measured in miles per gallon (MPG).
        - **Cylinders:** The number of cylinders in the vehicle’s engine, a discrete variable.
        - **Displacement:** The total volume of all the engine's cylinders, measured in cubic inches (cu in), a continuous variable indicating engine size.
        - **Horsepower:** Engine power output, measured in horsepower (hp), a continuous variable that can significantly impact fuel consumption.
        - **Weight:** The total weight of the vehicle in pounds (lbs), a continuous variable that influences fuel efficiency.
        - **Acceleration:** Time taken to accelerate from 0 to 60 mph, measured in seconds (sec), a continuous variable providing insight into vehicle dynamics.
        - **Model Year:** The year of manufacture of the vehicle model, an ordinal variable that can show trends over time.
        - **Origin:** A categorical variable indicating the region where the vehicle was manufactured, which may relate to differences in manufacturing standards and technology.
        - **Car Name:** The make and model of the car, a nominal variable used for detailed identification.

        ### 2.3 Appropriateness of the Dataset
        This dataset is particularly suitable for this project because it offers a manageable size and scope. 
        It contains enough data points to allow for statistical analysis  while remaining sufficently small to not require specialized hardware or algorithmic approaches to analyze. 
        The diversity of attributes—from technical specifications like horsepower and cylinders to more general information like model year and origin—provides oprotunity for exploring the impact of various factors on fuel efficiency. 
        his makes it an ideal choice for visualizing trends and drawing actionable insights from historical data.
        ### 2.4 Existing Relevant Visualizations and Critique
        #### Scatter Plots (MPG vs. Weight/Horsepower)
        - **Strengths:** Demonstrates the inverse relationship between weight or horsepower and MPG.
        - **Critiques:** Lack of color coding for Origin  limits the depth of analysis.
        #### Box Plots (MPG by Cylinders/Origin)
        - **Strengths:** Effectively compares MPG distribution across different Cylinder and Origin categories.
        - **Critiques:** Lack of individual data point overlay obscures specific distribution characteristics.
        #### Line Charts (Yearly MPG Trends)
        - **Strengths:** Suitable for observing MPG changes over Model Years.
        - **Critiques:** Lack of analysys of different models or origin.
        #### Histograms (Distribution of MPG/Weight)
        - **Strengths:** Provides a clear view of distribution shape for MPG and weight.
        - **Critiques:** May not effectively handle skewed or multimodal distributions.
        
        ### 3.0 Data Exploration Through Visualization
    """)

    # Histogram of MPG
    st.subheader("Distribution of Miles Per Gallon (MPG)")
    st.markdown("""
    In this visual, distribution of fuel efficiency across all vehicles in the dataset is explored. 
    Fuel efficiency, measured in miles per gallon (MPG), is a critical metric for assessing the performance and environmental impact of vehicles. 
    The histogram below provides a visual representation of how MPG values are distributed, helping us identify common efficiencies and outliers within the dataset.
    **Chart Interaction** by hovering over the bars to see the exact count of vehicles for each MPG range, which can help identify the most common fuel efficiency figures in the dataset. This interaction enhances your ability to spot and analyze trends in vehicle efficiency.
    """)
    fig_mpg = px.histogram(data, x='MPG', nbins=30, title="MPG Distribution",
                           labels={'MPG': 'Miles Per Gallon'}, color_discrete_sequence=['indianred'])
    st.plotly_chart(fig_mpg)

    st.subheader("Box Plot of MPG by Origin")
    st.markdown("""
    This box plot provides a comparative look at the MPG distributions based on the vehicles' manufacturing origin. 
    It highlights the median, quartiles, and potential outliers for MPG within each region. 
    This visualization is valuable for understanding how geographical differences in automotive design and regulation impact fuel efficiency.
    **Chart Interaction** by hovering over each box to view the median, quartiles, and outliers. 
    This interaction allows you to understand the range of MPG within each region quickly and can help pinpoint anomalies or exceptional cases in fuel efficiency. Deselecting origin countries can aid attaining more fucused view of each origin.
    """)

    # Box Plot of MPG by Origin
    fig_mpg_origin = px.box(data, x='Origin', y='MPG', color='Origin',
                            title="MPG by Vehicle Origin",
                            labels={'MPG': 'Miles Per Gallon', 'Origin': 'Vehicle Origin'})
    st.plotly_chart(fig_mpg_origin)
    st.subheader("Correlation Heatmap")
    st.markdown("""
    Below is a heatmap depicting the correlation coefficients between various attributes of the vehicles, such as MPG, weight, horsepower, and engine size. 
    A darker color indicates a stronger relationship. This matrix helps us quickly identify which factors have the most influence on MPG, guiding further analysis on optimizing vehicle performance for better fuel efficiency.
    **Heatmap Interaction** by hovering over each cell to see the exact correlation value between any two attributes. 
    This direct interaction enhances your understanding of how different vehicle characteristics are interrelated and can drive deeper analysis into factors influencing fuel efficiency.
    """)

    # Correlation Heatmap
    corr_data = data.select_dtypes(include=['float64', 'int32']).corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
                   z=corr_data,
                   x=corr_data.columns,
                   y=corr_data.columns,
                   hoverongaps=False,
                   colorscale='Viridis'))
    fig_heatmap.update_layout(title="Correlation Matrix", xaxis_title="Attributes", yaxis_title="Attributes")
    st.plotly_chart(fig_heatmap)

    st.markdown("""
        ## 4.0 key Correlations
    - **MPG and Engine Size:**
    - Negative correlation between MPG and 'Cylinders', 'Displacement', suggesting cars with larger engines tend to be less fuel-efficient.
    - **MPG and Weight:**
    - Strong negative correlation between MPG and 'Weight', indicating heavier cars usually have lower fuel economy.
    - **Model Year and Efficiency:**
    - Positive correlation between 'Model Year' and MPG, suggesting newer car models are more likely to be more fuel-efficient.
    - **Origin and Efficiency:**
    - 'Origin' shows a positive correlation with MPG, Sugesting diffrences in MPG based on wher the car was manufactured.
    **Origin and Efficiency:**
    - **Acceleration and Efficiency:**
    - Negative correlation between 'Acceleration' and 'MPG' suggests that vehicles with slower acceleration tend to be more fuel-efficient. 
    """)