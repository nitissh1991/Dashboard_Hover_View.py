import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title('Dynamic Data Plotter')

excel_file = st.file_uploader("Upload your data file", type=['xlsx'])
if excel_file:
    df_data = pd.read_excel(excel_file, sheet_name='Sheet1', skiprows=3)
    x_column_name = st.selectbox('Select X-axis', df_data.columns)

    # Primary Y-axis
    y_column_name = st.selectbox('Select primary Y-axis', df_data.columns)
    y_color = st.color_picker('Pick a color for primary Y-axis', '#00f900')
    y_min = st.number_input('Min value for primary Y-axis', value=float(df_data[y_column_name].min()))
    y_max = st.number_input('Max value for primary Y-axis', value=float(df_data[y_column_name].max()))
    y_increment = st.number_input('Increment for primary Y-axis', value=1.0)

    # Secondary Y-axis
    y2_column_name = st.selectbox('Select secondary Y-axis (optional)', ['None'] + list(df_data.columns))
    if y2_column_name != 'None':
        y2_color = st.color_picker('Pick a color for secondary Y-axis', '#f90000')
        y2_min = st.number_input('Min value for secondary Y-axis', value=float(df_data[y2_column_name].min()) if y2_column_name != 'None' else 0)
        y2_max = st.number_input('Max value for secondary Y-axis', value=float(df_data[y2_column_name].max()) if y2_column_name != 'None' else 1)
        y2_increment = st.number_input('Increment for secondary Y-axis', value=1.0)

    # X-axis settings
    x_min = st.number_input('Min value for X-axis', value=float(df_data[x_column_name].min()), key='x_min')
    x_max = st.number_input('Max value for X-axis', value=float(df_data[x_column_name].max()), key='x_max')
    x_increment = st.number_input('Increment for X-axis', value=1.0, key='x_increment')

    if st.button('Plot Graph'):
        # Filtering the DataFrame based on the user inputs
        filtered_data = df_data[(df_data[x_column_name] >= x_min) & (df_data[x_column_name] <= x_max)]

        # Plotting with Plotly
        fig = go.Figure()

        # Primary Y-axis plot
        fig.add_trace(go.Scatter(x=filtered_data[x_column_name], y=filtered_data[y_column_name],
                                 mode='lines', name=y_column_name, line=dict(color=y_color)))

        # Secondary Y-axis plot
        if y2_column_name != 'None':
            fig.add_trace(go.Scatter(x=filtered_data[x_column_name], y=filtered_data[y2_column_name],
                                     mode='lines', name=y2_column_name, line=dict(color=y2_color),
                                     yaxis='y2'))

        # Layout settings for primary Y-axis
        fig.update_layout(
            xaxis_title=x_column_name,
            yaxis_title=y_column_name,
            xaxis=dict(range=[x_min, x_max], dtick=x_increment),
            yaxis=dict(range=[y_min, y_max], dtick=y_increment),
            title=f'{y_column_name} vs {x_column_name}'
        )

        # Layout settings for secondary Y-axis
        if y2_column_name != 'None':
            fig.update_layout(
                yaxis2=dict(title=y2_column_name, overlaying='y', side='right', range=[y2_min, y2_max], dtick=y2_increment),
                legend=dict(x=0.5, xanchor='center', y=-0.2, orientation='h')
            )

        st.plotly_chart(fig, use_container_width=True)
