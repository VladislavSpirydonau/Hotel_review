import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import path

# Read CSV file, and on the optimization step i decieded to leave only nescesary columns

use_cols = ['Hotel_Address', 'Tags', 'Average_Score']
df = pd.read_csv(path.hotel_csv_path, usecols=use_cols)
# Preprocessing hotel addresses and creating a new column country for adding posibility to client to chose destination
df.Hotel_Address = df.Hotel_Address.str.lower()
df.Hotel_Address = df.Hotel_Address.str.replace('united kingdom','uk')
df['Country'] = df['Hotel_Address'].str.split().str[-1]

# Repmoove unnescesary symbols
replace_dict = {"'": '', "[": '', "]": '', ",": ''}
for pattern, replacement in replace_dict.items():
    df['Tags'] = df['Tags'].str.replace(pattern, replacement)
df.Tags = df.Tags.str.lower()

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Tokenize and lemmatize the tags
df['Tags'] = df['Tags'].apply(lambda x: [lemmatizer.lemmatize(word) for word in word_tokenize(x)])

# defining final function
def hotel_chosing(country, expectation, top_n=5):
    df_country = df[df['Country'] == country.lower()]
    
    # Tokenize and lemmatize the description
    description_tokens = set([lemmatizer.lemmatize(word) for word in word_tokenize(expectation) if not word in stopwords.words('english')])
    mask = df_country['Tags'].apply(lambda x: bool(set(x) & description_tokens))
    
    # Filter the dataframe using the mask
    df_description = df_country[mask]
    #filtering duplicate columns
    df_description = df_description.drop(columns=['Tags', 'Country'])
    df_description = df_description.drop_duplicates()
    # Sort the dataframe based on the Average_Score and get the top_n hotels
    top_hotels = df_description.nlargest(top_n, 'Average_Score')
    
    return print(top_hotels)