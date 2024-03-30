import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import path

# Read CSV file 
df = pd.read_csv(path.hotel_csv_path)
# Preprocessing hotel addresses and creating a new column country for adding posibility to client to chose destination
df.Hotel_Address = df.Hotel_Address.str.lower()
df.Hotel_Address = df.Hotel_Address.str.replace('united kingdom','uk')
df['Country'] = df['Hotel_Address'].apply(lambda x: x.split()[-1] if len(x.split()) > 1 else x)
# Here I remove unnescesary columns
df1 = df.drop(columns=['Unnamed: 0', 'Additional_Number_of_Scoring', 'Review_Date','Reviewer_Nationality','days_since_review', 'lat','lng','Review_Total_Negative_Word_Counts','Review_Total_Positive_Word_Counts','Total_Number_of_Reviews_Reviewer_Has_Given','Reviewer_Score','Total_Number_of_Reviews', 'Negative_Review','Positive_Review'])
# Replace unnescesary columns
replace_dict = {"'": '', "[": '', "]": '', ",": ''}
for pattern, replacement in replace_dict.items():
    df1['Tags'] = df1['Tags'].str.replace(pattern, replacement)
df1.Tags = df1.Tags.str.lower()

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Tokenize and lemmatize the tags
df1['Tags'] = df1['Tags'].apply(lambda x: [lemmatizer.lemmatize(word) for word in word_tokenize(x)])

# defining final function
def hotel_chosing(country, expectation, top_n=5):
    df_country = df1[df1['Country'] == country.lower()]
    
    # Tokenize and lemmatize the description
    description_tokens = [lemmatizer.lemmatize(word) for word in word_tokenize(expectation) if not word in stopwords.words('english')]
    
    # Create a mask for rows where the Tags column contains any of the words in the description
    mask = df_country['Tags'].apply(lambda x: any(word in x for word in description_tokens))
    
    # Filter the dataframe using the mask
    df_description = df_country[mask]
    #filtering duplicate columns
    df_description.drop(columns=['Tags', 'Country'], inplace=True)
    df_description.drop_duplicates(inplace=True)
    # Sort the dataframe based on the Average_Score and get the top_n hotels
    top_hotels = df_description.sort_values('Average_Score', ascending=False).head(top_n)
    
    return print(top_hotels)