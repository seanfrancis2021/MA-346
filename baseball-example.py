import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Visualizing Baseball Salaries')
st.write('''A description of the dashboard as well as input constraints are located in the sidebar.''')
st.sidebar.markdown('''This is a small interactive dashboard that does a simple visualization of Major League Baseball players' salary trends, using a dataset we've seen in previous weeks of this course.''')

first_year, last_year = st.sidebar.slider('Select year range to focus on:', 1991, 2017, (1991, 2017), 1)
position = st.sidebar.selectbox("What position would you like to focus on?", ('OF', '1B', 'P', 'DH', '3B', '2B', 'C', 'SS'))

# The @st.cache code tells Streamlit that the function immediately after it should be run only once, the first time the dashboard is launched, and any later attempt to call to the same function can just use the previously-loaded value, without actually re-running the function at all. Makes things go by quicker!
@st.cache
def load_salary_data():
    return pd.read_csv('baseball-salaries-simplified.csv')

df = load_salary_data()

st.write('The first five rows of the ORIGINAL dataset displayed using st.write(df.head()):')
st.write(df.head())

# Filter the dataset
st.write('Use the input controls in the sidebar to filter the dataset. Below you will see the first five rows of the FILTERED dataset.')
year_limits = (df.year >= first_year) & (df.year <= last_year)
position_limits = df.pos == position
focus = df[year_limits & position_limits]
st.write(focus.head())

# Create a table of percentiles
st.write('''We're interested in seeing trends in the entire dataset.  There are so many data points that if we plotted them all, the graph would be quite busy.  So we'll plot the various percentiles of the data over time instead.  To do so, we must first compute what those percentiles are.''')

# Which years do we care about?
years = range(first_year, last_year)

# We'll store the results in a new DataFrame.
df_pcts = pd.DataFrame({"year":years})

# How to compute a percentile in a given year:
def percentile_in_year(year, percent):
    return focus[focus.year == year].salary.quantile( percent/100 )

# Fill the DataFrame using that function.
for percent in range( 0, 110, 10 ):
    df_pcts[percent] = [ percentile_in_year(year, percent) for year in years ]

# Make years the index.
df_pcts.index = df_pcts.year
del df_pcts['year']

# Change units to millions of dollars.
df_pcts /= 1000000

# See resulting dataframe.
st.write(df_pcts)

# Plot the data
st.write('Now we can view the trends in the salary distribution over time by plotting.')

df_pcts.plot(legend='upper left')
plt.gcf().set_size_inches(8,10)
plt.title(f'Salaries for {position} only, {len(focus)} players', fontsize=20)
plt.xticks(df_pcts.index, rotation=90)
plt.ylabel('Salary percentiles in $1M', fontsize=14)
plt.xlabel('Year')
st.pyplot()

# Investigate Extreme Values
st.write('''Makes you wonder who created the spikes on the graph...Let's find out!''')

st.write(focus.nlargest(10, 'salary' ).reset_index( drop=True))

