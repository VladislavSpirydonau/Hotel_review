import os

# Using relative path unfortinatly csv file is to big to post it on github but it is enough to place it into the rep
csv_filename = "Accommodation_Reviews.csv"
hotel_csv_path = os.path.join(os.path.dirname(__file__), csv_filename)