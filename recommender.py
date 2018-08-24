import time
import math
import os
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

# Pandas dataframes for the three .dat files
print ("Loading movies.dat ...")
dfMovies = pd.read_table("movies.dat",
                         sep='::',
                         engine="python",
                         header=None
                         )
dfMovies.columns = ['MovieID', 'Title', 'Genres']

print ("Loading ratings.dat ...")
dfRatings = pd.read_table("ratings.dat",
                          sep='::',
                          engine="python",
                          header=None
                          )
dfRatings.columns = ['UserID', 'MovieID', 'Rating', 'Timestamp']

print ("Loading users.dat ...")
dfUsers = pd.read_table("users.dat",
                        sep='::',
                        engine="python",
                        header=None
                        )
dfUsers.columns = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']

# Merge dataframes
print ("Merging dataframes ...")
dfMerged = pd.merge(dfRatings, dfUsers, how = 'outer')
dfFinal  = pd.merge(dfMerged, dfMovies, how = 'outer')
del dfMerged

# Get information about the user 
# Occupation
print ("\n\nPlease enter a code for your occupation")
print ("Use \'1\'  for Academic/educator")
print ("Use \'2\'  for Artist")
print ("Use \'3\'  for Clerical/admin")
print ("Use \'4\'  for College/grad student")
print ("Use \'5\'  for Customer service")
print ("Use \'6\'  for Doctor/health care")
print ("Use \'7\'  for Executive/managerial")
print ("Use \'8\'  for Farmer")
print ("Use \'9\'  for Homemaker")
print ("Use \'10\' for K-12 student")
print ("Use \'11\' for Lawyer")
print ("Use \'12\' for Programmer")
print ("Use \'13\' for Retired")
print ("Use \'14\' for Sales/marketing")
print ("Use \'15\' for Scientist")
print ("Use \'16\' for Self-employed")
print ("Use \'17\' for Technician/engineer")
print ("Use \'18\' for Tradesman/craftsman")
print ("Use \'19\' for Unemployed")
print ("Use \'20\' for Writer")
print ("Use \'0\'  for Other")
occupation = int( input('Enter your occupation here: ') ) #3.0以后的版本使用input()替换了raw_input()
if occupation not in range(0, 21):
    occupation = 0

# Age group
age = int( input("\n\nPlease enter your age (if you prefer not to answer, please enter \'-1\': ") )
ageGroup = -1
if age >= 0 and age < 18:
    ageGroup = 1
elif age > 17 and age <= 24:
    ageGroup = 18
elif age > 24 and age <= 34:
    ageGroup = 25
elif age > 34 and age <= 44:
    ageGroup = 35
elif age > 44 and age <= 49:
    ageGroup = 45
elif age > 49 and age <= 55:
    ageGroup = 50
elif age > 55:
    ageGroup = 56

# Gender
print ("\n\nWhat is your gender?")
print ("Use \'M\' for Male")
print ("Use \'F\' for Female")
print ("Use \'NA\' if you prefer not to answer")
gender = str( input("Enter your gender here: ") )
if gender != "M" and gender != "F":
    gender = "NA"

# Zip code
print ("\n\nWhat is your zip code?")
print ("Use the form 00000")
print ("If you prefer not to answer, please enter \'-1\'")
zipCode = int( input("Enter your zip code here: ") )
zl = dfUsers.loc[:, "Zip-code" ]
if len(str(zipCode)) != 5 or zipCode not in zl:
    zipCode = -1
del zl

# Get Movie Information
movieFound = True
genre = ""
movie = str( input("\n\nWhat is the movie in which you're interested (spelling counts): ") )
ml = dfMovies.loc[ dfMovies["Title"].str.contains(movie, case = False), "Title" ].tolist()
if len(ml) == 0:
    movieFound = False
    print ("\n\nMovie not found in our database... What is the genre for the movie? Here are the genres we have in our database:")
    print ("Action")
    print ("Adventure")
    print ("Animation")
    print ("Childrens")
    print ("Comedy")
    print ("Crime")
    print ("Documentary")
    print ("Drama")
    print ("Fantasy")
    print ("Film-Noir")
    print ("Horror")
    print ("Musical")
    print ("Mystery")
    print ("Romance")
    print ("Sci-Fi")
    print ("Thriller")
    print ("War")
    print ("Western")
    genre = str( input("Please provide a genre for the movie of interest: ") )
    if genre == "Childrens":
        genre = "Children\'s"
del ml

############################# TODO #############################
# * Based on all flags/entered information build a function, or 
#   many functions, that return(s) the agerage rating of the 
#   movie/genre + standard deviation for that demographic
