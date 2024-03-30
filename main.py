# Importing the recommendation system
import model

# After importing, you can run this as many times as you need
while True:
    country = input('Please choose a country for your destination: Netherlands, UK, France, Spain, Italy, Austria \n')
    expectation = input('Please describe what you expect from your trip: \n')
    model.hotel_choosing(country, expectation)