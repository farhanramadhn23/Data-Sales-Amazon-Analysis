import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset with caching to optimize performance
@st.cache_data
def load_data():
    return pd.read_csv('dashboard/cleaned_amazon.csv')

# Load data
data = load_data()

# Convert discount percentage to numeric
data['discount_percentage'] = data['discount_percentage'].str.rstrip('%').astype('float')

# Title of the dashboard
st.title('Amazon Product Analysis Dashboard')

# Sidebar filters
st.sidebar.header("Filters")

# Filter by rating with a slider
rating_filter = st.sidebar.slider('Rating', 0.0, 5.0, (3.0, 5.0))
data_filtered = data[(data['rating'] >= rating_filter[0]) & (data['rating'] <= rating_filter[1])]

# Filter by category with a multiselect dropdown
category_filter = st.sidebar.multiselect(
    'Category', 
    options=data['category'].unique(), 
    default=data['category'].unique()
)
# Apply category filter
if category_filter:
    data_filtered = data_filtered[data_filtered['category'].isin(category_filter)]

# Display the number of filtered products
st.write(f"Showing {len(data_filtered)} products based on your filters")
st.dataframe(data_filtered)

# Plot: Comparison of Actual Price vs Discounted Price
st.subheader('Comparison of Actual Price vs Discounted Price')

# Applying log scale for better visualization if price values vary widely
fig, ax = plt.subplots(figsize=(10,6))

# Limit the number of categories to show, e.g., top 10 most common
top_categories = data_filtered['category'].value_counts().index[:10]
data_top_categories = data_filtered[data_filtered['category'].isin(top_categories)]

# Scatter plot with limited categories, adding transparency and moving legend
sns.scatterplot(
    x=data_top_categories['actual_price'], 
    y=data_top_categories['discounted_price'], 
    hue=data_top_categories['category'], 
    ax=ax,
    alpha=0.6  # Adding transparency
)

# Use a log scale if prices are very dispersed
ax.set(xscale="log", yscale="log")

# Improving the layout of the plot
ax.set_title('Actual Price vs Discounted Price', fontsize=15)
ax.set_xlabel('Actual Price', fontsize=12)
ax.set_ylabel('Discounted Price', fontsize=12)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
st.pyplot(fig)


# Plot: Distribution of Ratings
st.subheader('Distribution of Ratings')
fig, ax = plt.subplots(figsize=(10,6))
sns.histplot(data_filtered['rating'], bins=20, kde=True, color='green')
ax.set_title('Distribution of Product Ratings')
ax.set_xlabel('Rating')
st.pyplot(fig)

# Plot: Discount Percentage vs Rating
st.subheader('Discount Percentage vs Rating')

# Limit the categories to the top 10 most common ones
top_categories = data_filtered['category'].value_counts().index[:10]
data_top_categories = data_filtered[data_filtered['category'].isin(top_categories)]

fig, ax = plt.subplots(figsize=(10,6))

# Scatter plot with transparency and limited categories
sns.scatterplot(
    x=data_top_categories['discount_percentage'], 
    y=data_top_categories['rating'], 
    hue=data_top_categories['category'], 
    ax=ax,
    alpha=0.6  # Add transparency
)

# Set plot title and labels
ax.set_title('Discount Percentage vs Rating', fontsize=15)
ax.set_xlabel('Discount Percentage', fontsize=12)
ax.set_ylabel('Rating', fontsize=12)

# Move legend outside the plot
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
st.pyplot(fig)


# Plot: Top Product Categories by Count
st.subheader('Top Product Categories')
top_categories = data_filtered['category'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, palette='coolwarm')
ax.set_title('Top 10 Product Categories by Count')
ax.set_xlabel('Number of Products')
ax.set_ylabel('Category')
st.pyplot(fig)
