
# Auto MPG Data Visualization Dashboard
access the deployed dashboard through the following link:
- [View Dashboard](https://daherdatavisualisation.streamlit.app/)

## Project Overview
This project presents an interactive dashboard built with Streamlit, showcasing visualizations of the Auto MPG dataset. The dashboard aims to analyze vehicle data from the 1970s to the 1980s to uncover historical trends in car efficiency and explore how various vehicle attributes influence fuel efficiency.

## Dataset
The dataset used in this project, known as the Auto MPG dataset, is sourced from the UCI Machine Learning Repository. It includes attributes such as miles per gallon (MPG), cylinders, displacement, horsepower, weight, acceleration, model year, origin, and car names. These attributes help analyze trends and patterns in fuel efficiency based on vehicle characteristics from the given era.

## Features
The dashboard includes the following features:
- **Data Filters**: Allows users to filter data by manufacturer and model year.
- **Correlation Matrix**: Visualizes correlations between different vehicle attributes.
- **Scatter Plots**: Helps explore relationships between variables with options to color by origin and add trend lines.
- **Histograms**: Shows the distribution of selected variables, with options to overlay histograms by vehicle origin.
- **Violin Plots**: Provides insights into the distribution of variables, segmented by origin with detailed hoverable data points.

## Installation
To run this project locally, you will need Python and Streamlit installed. Follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DataMechDynamics/Data-Visualization
   cd auto-mpg-dashboard
   ```

2. **Install Requirements**
   Make sure Python is installed on your system. Then install Streamlit using pip:
   ```bash
   pip install streamlit
   ```

3. **Launch the Dashboard**
   Run the following command to start the Streamlit server and view the dashboard:
   ```bash
   streamlit run app.py
   ```

## Accessing the Dashboard
Once the Streamlit server is running, you can view the dashboard by navigating to `http://localhost:8501` in your web browser.  

The dashboard is divided into two main tabs:
- **Dashboard Tab**: For interactive data visualizations.
- **Report Tab**: Contains a detailed report on data analysis and findings.


