# To deploy this app use the 'streamlit run <script_name>' command in shell

import streamlit as st
import pandas as pd
import altair as alt

color_scale = alt.Scale(domain=['Emerica', 'Vans', 'Nike SB', 'Last Resort'], range=['#022ec9', '#03a9f4', '#4fc3f7', '#bff4ff'])
brands_to_keep = ['Emerica', 'Vans', 'Nike SB', 'Last Resort']

data = pd.read_csv("shoes_db.csv")
data['dt'] = pd.to_datetime(data['dt'])

model_data = pd.read_csv("shoes_models_data.csv")
model_data['dt'] = pd.to_datetime(model_data['dt'])

filtered_df = data[data['brand_name'].isin(brands_to_keep)]
filtered_model_data = model_data[model_data['brand'].isin(brands_to_keep)].groupby(['brand', 'models', 'source'])['average_daily_price'].mean().reset_index() 


brands_df = filtered_df.groupby(['brand_name'])['average_daily_price'].mean().round(2).reset_index()  
brands_df_date =  data[data['brand_name'].isin(brands_to_keep)].groupby(['brand_name', 'dt'])['average_daily_price'].mean().round(2).reset_index() 

# Box & Whisker Data
site_min_df = data.groupby(['source'])['average_daily_price'].min().round(2).reset_index()
site_max_df = data.groupby(['source'])['average_daily_price'].max().round(2).reset_index()
site_avg_df = data.groupby(['source'])['average_daily_price'].mean().round(2).reset_index()
site_merge = pd.merge(site_min_df, site_max_df, on='source', suffixes=('min', 'max'))
site_merge = pd.merge(site_merge, site_avg_df, on='source')
site_merge = site_merge.rename(columns={ 'average_daily_pricemin' : 'min', 'average_daily_pricemax' : 'max', 'average_daily_price' : 'avg' } )



#############################################################

def app():
    '''main body of streamlit app'''
      
    st.set_page_config(layout='wide')

    ####################
    ### Core Visuals ###
    ####################

    line_chart = alt.Chart(brands_df_date, title='Daily Price').mark_line().encode(
        x=alt.X('dt', title= ' ', axis= alt.Axis(tickCount=5, format='%b %d')),
        y=alt.Y('average_daily_price', title= ' ', scale=alt.Scale(domain=[ min(brands_df_date['average_daily_price'])-30, max(brands_df_date['average_daily_price'])+30])), 
        color=alt.Color('brand_name', scale=color_scale, legend=None)
    ).properties(width=1350, height=400)    
   
    line_chart = line_chart.configure_title(fontSize=24, offset=5, orient='top', anchor='middle')
    
    
    # Brand Specific Bar Charts
    emerica_bar_chart = alt.Chart(filtered_model_data[filtered_model_data['brand']=='Emerica'].nlargest(10, 'average_daily_price')).mark_bar().encode(
        x=alt.X('average_daily_price', title=''),
        y=alt.Y('models', title=None, sort='-x', axis=alt.Axis(labelAlign='left', labelPadding=125)),
        color=alt.Color('brand', scale=color_scale, legend=None)
    ).configure_axis(grid=False).properties(width=300, height=200) 


    vans_bar_chart = alt.Chart(filtered_model_data[filtered_model_data['brand']=='Vans'].nlargest(10, 'average_daily_price')).mark_bar().encode(
        x=alt.X('average_daily_price', title=''),
        y=alt.Y('models', title=None, sort='-x', axis=alt.Axis(labelAlign='left', labelPadding=125)),
        color=alt.Color('brand', scale=color_scale, legend=None)
    ).configure_axis(grid=False).properties(width=300, height=200)


    nike_bar_chart = alt.Chart(filtered_model_data[filtered_model_data['brand']=='Nike SB'].nlargest(10, 'average_daily_price')).mark_bar().encode(
        x=alt.X('average_daily_price', title=''),
        y=alt.Y('models', title=None, sort='-x', axis=alt.Axis(labelAlign='left', labelPadding=125)),
        color=alt.Color('brand', scale=color_scale, legend=None)
    ).configure_axis(grid=False).properties(width=300, height=200)

 
    last_resort_bar_chart = alt.Chart(filtered_model_data[filtered_model_data['brand']=='Last Resort'].nlargest(10, 'average_daily_price')).mark_bar().encode(
        x=alt.X('average_daily_price', title=''),
        y=alt.Y('models', title=None, sort='-x', axis=alt.Axis(labelAlign='left', labelPadding=125)),
        color=alt.Color('brand', scale=color_scale, legend=None)
    ).configure_axis(grid=False).properties(width=300, height=200)
    
    
    # Crude Box & Whisker to compare summary stats
    box_chart = alt.Chart(site_merge, title='Min Max & Avg by Store').mark_bar(size=20, color='#bff4ff').encode(
        x=alt.X('source:N', axis=alt.Axis(labelAngle=0, title=None)),
        y=alt.Y('min:Q', axis=alt.Axis(title=None)),
        y2='max:Q'
    ).properties(width=600, height=375) + alt.Chart(site_merge).mark_point(color='red', size=500, opacity=1, filled=True, shape='square').encode(
            x='source:N',
            y='avg:Q'
        )
   
    box_chart = box_chart.configure_title(fontSize=20, offset=10, orient='top', anchor='middle')

    # CSS Styling Template for Avg Cards
    st.markdown(
        """
        <div>
        <style>
        .metric-card {
            display: flex;
            justify-content: center;
            padding: .5px;
            border-radius: 5px;
            margin-bottom: 20px;
            width: 200px;
        }
        .metric-label {
            text-align: center;
            font-size: 18px; 
            margin-bottom: 1px; 
        }
        .metric-value {
            text-align: center;
            font-size: 18px; 
            margin-top: 1px; 
        }
        .metric-card-1 {
            border: 5px solid #022ec9;
            margin: auto; 
            border-radius: 4px;
            height: 40px;
            width: 100px;
        }
        .metric-card-2 {
            border: 5px solid #03a9f4; 
            margin: auto;
            border-radius: 4px;
            height: 40px;
            width: 100px;
        }
        .metric-card-3 {
            border: 5px solid #4fc3f7;
            margin: auto;
            border-radius: 4px;
            height: 40px;
            width: 100px;
        }
        .metric-card-4 {
            border: 5px solid #bff4ff;
            margin: auto;
            border-radius: 4px;
            height: 40px;
            width: 100px;
        }
        </style>
        </div>
        """,
        unsafe_allow_html=True
    )


    # CSS Styling for Custom Title
    st.markdown(
    """
    <div style='background-color: #252d3d ; padding: 10px; border-radius: 5px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>
            Footwear Retail Trends 10/23
        </h1>
    </div>
    """,
    unsafe_allow_html=True
    )
    
    st.markdown('')
    st.markdown('')

    
    # Avg Price by Brand Cards
    st.subheader('Average Price by Brand', divider='grey')
    card1, card2, card3, card4 = st.columns([1, 1, 1, 1])

    with card1:
        st.markdown(  
            '<p class="metric-label">Emerica</p>'
            '<div class="metric-card-1">'
            '<p class="metric-value">${:.2f}</p>'
            '</div>'.format(brands_df[brands_df['brand_name'] == 'Emerica']['average_daily_price'].iloc[0]),
            unsafe_allow_html=True
        )

    with card2:
        st.markdown(
            '<p class="metric-label">Vans</p>'
            '<div class="metric-card-2">'
            '<p class="metric-value">${:.2f}</p>'
            '</div>'.format(brands_df[brands_df['brand_name'] == 'Vans']['average_daily_price'].iloc[0]), 
        unsafe_allow_html=True
    )
    
    with card3:
        st.markdown(
            '<p class="metric-label">Nike SB</p>'
            '<div class="metric-card-3">'
            '<p class="metric-value">${:.2f}</p>'
            '</div>'.format(brands_df[brands_df['brand_name'] == 'Nike SB']['average_daily_price'].iloc[0]), 
            unsafe_allow_html=True
        )

    with card4:
        st.markdown(
            '<p class="metric-label">Last Resort</p>'
            '<div class="metric-card-4">'
            '<p class="metric-value">${:.2f}</p>'
            '</div>'.format(brands_df[brands_df['brand_name'] == 'Last Resort']['average_daily_price'].iloc[0]),
            unsafe_allow_html=True 
        )
    
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    
    #################################
    ### Main Visual Canvas Layout ### 
    #################################

    test1, test2 = st.columns([1.5, 5])
    
    with test1:
        st.subheader('Model Prices', divider='grey')
        st.altair_chart(emerica_bar_chart)
        st.altair_chart(vans_bar_chart)
        st.altair_chart(nike_bar_chart)
        st.altair_chart(last_resort_bar_chart)

    with test2:
        st.subheader('Brand Price Trends', divider='grey')
        st.altair_chart(line_chart, use_container_width=True)
        st.subheader('Summary Stats & Data', divider='grey')
        sub1, sub2, sub3 = st.columns([1.5,.2, 4])
        sub1.altair_chart(box_chart, use_container_width=True)
        sub2.markdown('')
        sub3.dataframe(model_data, width=1700, height=375)   

    ###########################
    ## Invoke App on Execute ##
    ###########################


app()

