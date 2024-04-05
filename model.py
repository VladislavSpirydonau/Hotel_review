import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import path

# Read the CSV file. During the optimization step, I decided to keep only the necessary columns.
use_cols = ['Hotel_Address', 'Tags', 'Average_Score']
df = pd.read_csv(path.hotel_csv_path, usecols=use_cols)

# Preprocess hotel addresses and create a new column 'Country' to allow the client to choose a destination.
df.Hotel_Address = df.Hotel_Address.str.lower()
df.Hotel_Address = df.Hotel_Address.str.replace('united kingdom','uk')
df['Country'] = df['Hotel_Address'].str.split().str[-1]

# Remove unnecessary symbols.
replace_dict = {"'": '', "[": '', "]": '', ",": ''}
for pattern, replacement in replace_dict.items():
    df['Tags'] = df['Tags'].str.replace(pattern, replacement)
df.Tags = df.Tags.str.lower()

# Initialize the lemmatizer.
lemmatizer = WordNetLemmatizer()

# Tokenize and lemmatize the tags.
df['Tags'] = df['Tags'].apply(lambda x: [lemmatizer.lemmatize(word) for word in word_tokenize(x)])

# Define the final function.
def hotel_choosing(country, expectation, top_n=5):
    # If there country is not in the dataset the script will give back a message
    if country.lower() not in df['Country'].unique():
        print("Unfortunately, we don't currently operate in this location.")
        return
    df_country = df[df['Country'] == country.lower()]
    # Tokenize and lemmatize the description.
    description_tokens = set([lemmatizer.lemmatize(word) for word in word_tokenize(expectation.lower()) if not word in stopwords.words('english')])
    mask = df_country['Tags'].apply(lambda x: bool(set(x) & description_tokens))
    
    # Filter the dataframe using the mask.
    df_description = df_country[mask]
    # If there is no hotel that meet expectation the script will give back a message
    if df_description.empty:
        print("Apologies, we couldn't find a hotel that matches your expectations at the moment.")
        return
    # Filter out duplicate columns.
    df_description = df_description.drop(columns=['Tags', 'Country'])
    df_description = df_description.drop_duplicates()
    # Sort the dataframe based on the Average_Score and get the top_n hotels.
    top_hotels = df_description.nlargest(top_n, 'Average_Score')
    
    return print(top_hotels)