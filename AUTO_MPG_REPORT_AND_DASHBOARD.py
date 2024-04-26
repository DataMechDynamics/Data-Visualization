import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go

st.set_page_config(layout="wide")

#  load data
@st.cache_resource  
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

st.markdown("""
Please select a tab to view:
- **Dashboard Tab**: Explore interactive visualizations of the Auto MPG data.
- **Report Tab**: Read the detailed analysis report.
""")

# Create tabs
tab1, tab2 = st.tabs(["Dashboard", "Report"])
# Dashboard tab
with tab1:
    st.header("Automobile Data Visualization Dashboard")
    st.sidebar.markdown("### Sidebar Controls")
    st.sidebar.markdown("Use the controls below to customize and filter the visualizations in the dashboard:")

    st.sidebar.markdown("<h3 style='color:red;'>VIEW DATA & CORRELATION MATRIX</h3>", unsafe_allow_html=True)
    # Checkbox widget for displaying data
    checkbox = st.sidebar.checkbox("Reveal Data")
    if checkbox:
        st.dataframe(data)

    # Checkbox for displaying correlation matrix
    checkbox_corr = st.sidebar.checkbox("Show Correlation Matrix")
    if checkbox_corr:
        # Calculate correlation matrix
        corr_matrix = data.corr()
        # Create a heatmap using Plotly
        fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    hoverongaps=False,
                    colorscale='Viridis'))
        fig_corr.update_layout(title="Correlation Matrix",
                            xaxis_title="Attributes",
                            yaxis_title="Attributes")
        st.markdown("### Correlation Matrix")
        st.markdown("Explore how different attributes correlate with each other. Hover over the heatmap to see the exact correlation values.")
        st.plotly_chart(fig_corr)

    st.sidebar.markdown("<h3 style='color:red;'>DATA FILTER</h3>", unsafe_allow_html=True)
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

    # Scatterplot setup
    st.sidebar.markdown("<h3 style='color:red;'>SCATTER PLOT SETUP</h3>", unsafe_allow_html=True)
    select_box1 = st.sidebar.selectbox('X axis', options=numeric_columns, index=3)
    select_box_y = st.sidebar.selectbox('Y axis', options=numeric_columns, index=0)

    color_by_origin_scatter = st.sidebar.checkbox("Color by Origin in Scatter Plot", True)
    add_trendline = st.sidebar.checkbox("Add Trendline", False)

    # Creating scatterplot
    st.markdown("### Scatter Plot")
    st.markdown("Interact with the scatter plot by selecting different axes and or toggling trendlines. Use the sidebar to filter data and hover over points for more details. Click the countries in the legend to filter")
    if color_by_origin_scatter:
        fig = px.scatter(data, x=select_box1, y=select_box_y, color='Origin', trendline="ols" if add_trendline else None,
                        hover_data=data.columns)
    else:
        fig = px.scatter(data, x=select_box1, y=select_box_y, trendline="ols" if add_trendline else None,
                     hover_data=data.columns)
    st.plotly_chart(fig)

    # Histogram setup
    st.sidebar.markdown("<h3 style='color:red;'>HISTOGRAM SETUP</h3>", unsafe_allow_html=True)
    select_box3 = st.sidebar.selectbox("Feature for Histogram", options=numeric_columns, key='hist')
    histogram_slider = st.sidebar.slider("Number of Bins", min_value=3, max_value=20, value=8)
    overlay_histograms = st.sidebar.checkbox("Overlay Histograms by Origin", True)

    # Creating histogram with Plotly
    st.markdown("### Histogram")
    st.markdown("Adjust the number of bins with the slider and use the overlay option to compare distributions by Origin. Hover for detailed information.Click the countries in the legend to filter.")
    if overlay_histograms:
        fig2 = px.histogram(data, x=select_box3, color='Origin', nbins=histogram_slider, barmode='overlay',
                            histnorm='percent', opacity=0.75)
        fig2.update_traces(marker_line_color='black', marker_line_width=1)
    else:
        fig2 = px.histogram(data, x=select_box3, nbins=histogram_slider, histnorm='percent', opacity=0.75)
        fig2.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig2)

    # Violin plot setup
    st.sidebar.markdown("<h3 style='color:red;'>VIOLIN PLOT SETUP</h3>", unsafe_allow_html=True)
    select_box4 = st.sidebar.selectbox("Feature for Violin Plot", options=numeric_columns, key='violin')
    violin_color_by_origin = st.sidebar.checkbox("Color by Origin in Violin Plot", True)

    # Creating violin plot with custom hover information
    st.markdown("### Violin Plot")
    st.markdown("The violin plot helps visualize data distribution by Origin. Color-code by Origin and hover over the plot to see details .")
    if violin_color_by_origin:
        fig3 = px.violin(data, y=select_box4, color='Origin', box=True, points="all", hover_data=['Manufacturer', 'Car Name', 'Model Year'])
    else:
        fig3 = px.violin(data, y=select_box4, box=True, points="all", hover_data=['Manufacturer', 'Car Name', 'Model Year'])

    fig3.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig3)


# Report tab

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

    st.markdown("""
                
    ## 5.0 Design Implementation 

    ### 5.1 Importance of Interactive Analysis

    The ability to interact dynamically with data is indispensable in the field of automotive engineering, where data-driven decisions are essential for optimizing vehicle performance and efficiency.
    The complexity of vehicle design demands more than static data presentation; engineers require tools that allow them to manipulate and explore data independently. 
    An interactive dashboard was created to encourage engineers to interact closely with the data and provide them with a practical analytical tool that is customized to meet their unique requirements. 
    This dashboard caters to this need by facilitating a hands-on approach to data analysis, enabling engineers to test hypotheses, modify variables, and observe the outcomes in real time, thus accelerating the design and decision-making processes.
     Self-service BI tools are transforming the way industries operate, granting professionals the ability to perform complex analyses without specialized data science expertise. 
    For automotive engineers, this translates to an unparalleled capacity to adjust, analyze, and visualize vehicle features and performance metrics on their terms, developing a deeper understanding.

    ### 5.2 Benefits of Dashboard Versatility

    - **Customization of Data Views**: Engineers can personalize the dashboard to highlight the data most relevant to their current project or inquiry.
    - **Scenario Simulation**: The tool allows for the adjustment of vehicle parameters to simulate different configurations and instantly evaluate their impact on fuel efficiency.
    - **Comparative Data Analysis**: It facilitates easy comparison of vehicle data across different model years, manufacturers, or manufacturing origins, aiding in trend analysis and benchmarking.
    - **Advanced Data Visualization**: With built-in visualization capabilities, engineers can effortlessly identify patterns, trends, and correlations, making the data accessible and understandable.
                
    ## 6.0 Evaluation
    User feedback is essential to the development of the Visualization Dashboard as it guides improvements and helps evaluate efficacy. 
    The purpose of this evaluation section is to consider the dashboard's usefulness, functionality, and significance of its data visualizations by combining the responses obtained from a structured user survey.
    The feedback provided is crucial in guiding future developments and ensuring that the dashboard adapts to the changing needs of its users. 
    ### 6.1 Evaluation Approach
    The evaluation approach was tailored to gather actionable feedback from a select group of five users, comprising data scientists and engineers. 
    These participants were chosen for their relevant expertise and were asked to interact with the dashboard and provide feedback through a structured survey. 
    The group included individuals with a range of experience from novices to experts in data analysis and automotive engineering, ensuring a focused perspective on the dashboard’s technical accessibility and usability.
    The survey consisted of both quantitative and open-ended questions that covered various aspects of the dashboard, such as ease of use, informational value, and visual appeal. 
    Responses were collected that provided insights into how users engage with the dashboard. Key findings highlighted the intuitive nature of interactive elements and the clarity of visual data presentations. 
    However, it also became apparent that there was a need for improved navigational aids for less tech-savvy users and enhancements to mobile device accessibility.
    ### 6.2 Synthesis of Findings
    Survey results revealed that the dashboard’s interactive filters and dynamic visualizations were highly effective in engaging users and facilitating understanding of the relationships within the dataset. 
    It was noted that users appreciated the ability to manipulate data visualizations directly to uncover new insights. 
    While the evaluation highlighted the overall effectiveness of the dashboard, it also provided insights into areas for subtle improvements, particularly in enhancing usability for new users. 
    The need for slight adjustments in the design elements was noted, with a focus on incrementally simplifying the user interface to enhance the learning curve in future iterations.
    Participants provided specific suggestions for enhancing the dashboard’s functionality, including the addition of a tutorial for new users, the incorporation of more granular data filters, and the enhancement of the mobile user experience to increase accessibility. 
    Additionally, there was a suggestion to expand the dataset to include more recent automotive trends, which several participants noted would significantly enhance the dashboard’s utility. 
                
    ## 7.0 Conclusion

    The exploration of the Auto MPG dataset through this interactive dashboard has provided key insights into the factors influencing fuel efficiency in automobiles manufactured during the 1970s and 1980s. The analysis highlights several critical aspects:

    1. **Engine Efficiency Trends**: There is a clear negative correlation between engine size (cylinders and displacement) and fuel efficiency (MPG), indicating that larger engines generally consume more fuel. This trend underscores the importance of advancements in engine technology that can enhance efficiency without increasing size, as well as focusing efforts on the ongoing trend of down-cylindering.

    2. **Impact of Vehicle Weight on MPG**: The data shows a strong inverse relationship between vehicle weight and MPG, suggesting that lighter vehicles tend to be more fuel-efficient. This finding supports ongoing efforts in the automotive industry to reduce vehicle weight to improve fuel economy.

    3. **Regional Manufacturing Differences**: Vehicles from different regions exhibit distinct characteristics in terms of MPG, which can be attributed to varying engineering practices and regulatory standards across the globe. Japanese cars, for example, consistently show higher fuel efficiency compared to their American and European counterparts within the dataset. This can be attributed to their efforts to manufacture smaller, less powerful commuter vehicles which are more suited to their infrastructure.

    4. **Temporal Improvements**: The analysis also reveals a positive trend in MPG over the model years covered in the dataset, reflecting technological improvements as well as adherence to ever-increasing emissions legislation.

    The use of an interactive dashboard for this analysis not only facilitated a deeper understanding of these dynamics but also provided a dynamic tool for users to explore data relationships independently. The ability to filter, customize, and interact with the data in real-time enhances engagement and enables a personalized analysis experience.

    ### 7.1 Implications and Utility

    The insights derived from this study are particularly valuable for stakeholders in the automotive industry, including engineers, designers, and policymakers.
    Understanding historical trends and the impact of different vehicle attributes on fuel efficiency can inform future vehicle design and regulatory approaches to meet environmental and economic goals.
    Moreover, this project exemplifies the power of modern data visualization tools in making complex data accessible and understandable for a broad audience. 
    It highlights the importance of interactivity in data analysis, which can significantly enrich the analytical process by allowing users to view data from multiple perspectives, draw more nuanced conclusions, and present them with the opportunity of potentially discovering previously unseen insights.In conclusion, this dashboard serves as a robust model for effective data exploration and decision support, providing both detailed insights and a flexible, user-friendly interface to navigate complex datasets. 
    This approach can be extended to other datasets and sectors, promoting a more data-informed approach across various fields.

    ## 8.0 Further Work

    To enhance the insights from the Auto MPG dataset and increase the dashboard's utility, future work could include integrating additional data from newer vehicle models to extend the analysis across decades and better understand trends in automotive technology. 
    Developing advanced analytical features, such as predictive models within the dashboard, would allow users to simulate changes in vehicle design and their impact on fuel efficiency. 
    Enhancing user customization options, improving mobile accessibility, and incorporating collaborative tools could significantly improve the user experience. 
    Moreover, adding educational resources and interactive tutorials could help users more effectively navigate and utilize the dashboard, making complex data more accessible and understandable. 
    These enhancements would not only refine the dashboard's functionality but also broaden its applicability to a wider range of users and use cases, fostering a deeper engagement with the data.
                    
     """)
