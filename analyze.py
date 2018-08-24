#导入所需要的包
import time
import math
import os
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

# Flags on what to analyze
block0 = 0  # Explore the distribution of occupations who responded 探讨有回应的职业的分布
block1 = 0  # Explore the distribution of ratings for different occupations 探究不同职业的评分分布
block2 = 0  # Explore the average rating for a genre for all occupations 探索所有职业类型的平均评级
block3 = 1  # Explore average rating for a genre for each gender  探索每种性别类型的平均评级


# Pandas dataframes for the three .dat files  为三个dat文件创建数据框
if not os.path.isfile( "MergedDataset.csv" ):
    print ("Loading movies.dat ...")
    dfMovies = pd.read_table("movies.dat", 
                             sep='::', 
                             engine="python", 
                             header=None
                             )
    dfMovies.columns = ['MovieID', 'Title', 'Genres']   #movies数据列名

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
    dfUsers.columns = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'] #用户数据列表

    # Merge dataframes
    print ("Merging dataframes ...")
    dfMerged = pd.merge(dfRatings, dfUsers, how = 'outer') #how用于指定链接方式，指定为外连接
    dfFinal  = pd.merge(dfMerged, dfMovies, how = 'outer') #传出数组
    del dfMerged  #进行内存的释放

    dfFinal.to_csv("MergedDataset.csv")   #对合并的数据进行保存为MergedDataset.csv
else:                                       #如果存在的话直接对MergedDataset.csv表进行输出
    print ("Loading MergedDataset.csv ...")
    dfFinal = pd.read_csv("MergedDataset.csv",
                          engine="python"
                          )

# Dictionary that maps occupation code to occupation 将职业代码映射到职业的字典
occupations = {}
occupations[0]  = "Other"
occupations[1]  = "Academic/educator"
occupations[2]  = "Artist"
occupations[3]  = "Clerical/admin"
occupations[4]  = "College/grad student"
occupations[5]  = "Customer service"
occupations[6]  = "Doctor/health care"
occupations[7]  = "Executive/managerial"
occupations[8]  = "Farmer"
occupations[9]  = "Homemaker"
occupations[10] = "K-12 student"
occupations[11] = "Lawyer"
occupations[12] = "Programmer"
occupations[13] = "Retired"
occupations[14] = "Sales/marketing"
occupations[15] = "Scientist"
occupations[16] = "Self-employed"
occupations[17] = "Technician/engineer"
occupations[18] = "Tradesman/craftsman"
occupations[19] = "Unemployed"
occupations[20] = "Writer"

# Dictionary that maps age code to age group  将年龄代码映射到年龄的字典
ageGroup = {}
ageGroup[1]  = "Under 18"
ageGroup[18] = "18-24"
ageGroup[25] = "25-34"
ageGroup[35] = "35-44"
ageGroup[45] = "45-49"
ageGroup[50] = "50-55"
ageGroup[56] = "56+"

# List containing all possible genres in the dataset  包含数据集中所有可能的类型的列表
genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children\'s",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"]

# Explore the distribution of occupations who responded ######################################### 探讨有回应的职业的分布
if block0:
    dfUsers = pd.read_table("users.dat",
                            sep='::',
                            engine="python",
                            header=None
                            )
    dfUsers.columns = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']

    occupation_list = dfUsers["Occupation"].tolist()  # 将Occupation转化为列表
    bin_boundaries = [i+0.5 for i in range(-1,21)]

    fig = plt.hist(occupation_list, bins=bin_boundaries) 
    ax = plt.subplot(111)

    # x axis
    ax.set_xlabel("Occupation")
    ax.set_xlim(-1,21)
    x =  [i for i in range(0,21)]
    xl = [occupations[i] for i in range(0,21)]
    plt.xticks(x, xl, rotation='vertical')
    plt.tick_params(axis='x', which='major', labelsize=9)
    plt.gcf().subplots_adjust(bottom=0.35)

    # y axis
    ax.set_ylabel("Count")

    # save plot
    plt.savefig('plots/OccupationDist.pdf')
    plt.close()

    del dfUsers
#ENDIF

# Explore the distribution of ratings for different occupations ################################# 探究不同职业的评分分布
if block1:
    bin_boundaries = [i+0.5 for i in range(-1,6)]
    for occ in occupations:
        occupation_ratings = dfFinal.loc[dfFinal["Occupation"] == occ, "Rating"].tolist()
        fig = plt.hist(occupation_ratings, bins=bin_boundaries), 
        ax = plt.subplot(111)

        # x axis
        ax.set_xlabel("Rating")
        ax.set_xlim(0,6)
        # y axis
        ax.set_ylabel("Count")
        # title
        name = occupations[occ] + " Distribution of Ratings"
        plt.title(name)
        # save plot
        name = 'plots/OccupationDistnOfRatings/%sRatings.pdf' % (occupations[occ].replace("/", "_"))
        name = name.replace(" ", "")
        print (name + " created!")
        plt.savefig(name)
        plt.close()
    #ENDFOR
#ENDIF

# Explore the average rating for a genre for all occupations/ages ################################# 探索所有职业/年龄类型的平均评级
if block2:

    for gen in genres:

        # Occupation
        x =  [i for i in range(0,len(occupations))]
        xl = [occupations[i] for i in range(0,len(occupations))]
        y  = []
        ye = []
        for occ in occupations:
            occupation_ratings = dfFinal.loc[ (dfFinal["Occupation"] == occ) & (dfFinal["Genres"].str.contains(gen)), "Rating"].tolist()
            occupation_ratings = np.array(occupation_ratings)
            ave_rating = np.average( occupation_ratings )
            std_rating = np.std( occupation_ratings )
            y.append(ave_rating)
            ye.append(std_rating)
            #print "Average Rating = " + str(ave_rating)
        #ENDFOR

        fig = plt.bar(x, y, 1, yerr = ye),
        ax = plt.subplot(111)

        # x axis
        ax.set_xlabel("Occupation")
        ax.set_xlim(-1,len(occupations))
        plt.xticks(x, xl, rotation='vertical')
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.gcf().subplots_adjust(bottom=0.35)

        # y axis
        ax.set_ylabel("Average Rating")
        ax.set_ylim(0,5)

        # title
        name = gen + " Genre: Average Rating Per Occupation"
        plt.title(name)

        # save plot
        name = 'plots/GenreAveRatingVSOccupation/Genre%s_AveRating_VS_occupation.pdf' % gen.replace("\'", "")
        name = name.replace(" ", "")
        print (name + " created!")
        plt.savefig(name)
        plt.close()

        # Age group
        x =  [i for i in range(0,len(ageGroup))]
        xl = [ageGroup[i] for i in sorted(ageGroup.keys())]
        y  = []
        ye = []
        for age in ageGroup:
            age_ratings = dfFinal.loc[ (dfFinal["Age"] == age) & (dfFinal["Genres"].str.contains(gen)), "Rating"].tolist()
            age_ratings = np.array( age_ratings )
            ave_rating = np.average( age_ratings )
            std_rating = np.std( age_ratings )
            y.append(ave_rating)
            ye.append(std_rating)
        #ENDFOR

        fig = plt.bar(x, y, 1, yerr = ye),
        ax = plt.subplot(111)

        # x axis
        ax.set_xlabel("Age Group")
        ax.set_xlim(-1,len(ageGroup))
        plt.xticks(x, xl)#, rotation='vertical')
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.gcf().subplots_adjust(bottom=0.15)

        # y axis
        ax.set_ylabel("Average Rating")
        ax.set_ylim(0,5)

        # title
        name = gen + " Genre: Average Rating Per Age Group"
        plt.title(name)

        # save plot
        name = 'plots/GenreAveRatingVSAge/Genre%s_AveRating_VS_Age.pdf' % gen.replace("\'", "")
        name = name.replace(" ", "")
        print (name + " created!")
        plt.savefig(name)
        plt.close()

    #ENDFOR
#ENDIF

# Explore average rating for a genre for each gender ################################# 探测性别对评分的影响
if block3:

    x   =  [i for i in range(0, len(genres))]
    xM  =  [i-0.2 for i in range(0, len(genres))]
    xF  =  [i+0.2 for i in range(0, len(genres))]
    xl  = []
    yM  = []
    yMe = []
    yF  = []
    yFe = []

    for gen in genres:
        xl.append(gen)
        male_ratings = dfFinal.loc[ (dfFinal["Gender"] == "M") & (dfFinal["Genres"].str.contains(gen)), "Rating" ].tolist()
        female_ratings = dfFinal.loc[ (dfFinal["Gender"] == "F") & (dfFinal["Genres"].str.contains(gen)), "Rating" ].tolist()

        male_ratings = np.array( male_ratings )
        ave_male_rating = np.average( male_ratings )
        std_male_rating = np.std( male_ratings )
        yM.append( ave_male_rating )
        yMe.append( std_male_rating )

        female_ratings = np.array( female_ratings )
        ave_female_rating = np.average( female_ratings )
        std_female_rating = np.std( female_ratings )
        yF.append( ave_female_rating )
        yFe.append( std_female_rating )
    #ENDFOR

    #fig = plt.bar(x, y, 0.5, yerr = ye),
    ax = plt.subplot(111)
    male_bar   = ax.bar(xM, yM, width=0.4, color='b', align='center')
    female_bar = ax.bar(xF, yF, width=0.4, color='r', align='center')
    ax.legend( (male_bar, female_bar), ('Male', 'Female') )

    # x axis
    ax.set_xlabel("Genre")
    ax.set_xlim(-1,len(genres))
    plt.xticks(x, xl, rotation='vertical')
    plt.tick_params(axis='x', which='major', labelsize=9)
    plt.gcf().subplots_adjust(bottom=0.25)

    # y axis
    ax.set_ylabel("Average Rating")
    ax.set_ylim(0,5)

    # title
    name = "Average Genre Rating Per Gender"
    plt.title(name)

    # save plot
    name = 'plots/GenreAveRatingVSGender/Genre%s_AveRating_VS_Gender.pdf' % gen.replace("\'", "")
    name = name.replace(" ", "")
    print (name + " created!")
    plt.savefig(name)
    plt.close()
#经过对数据的探测我们可以得出性别，年龄，职业等与影片评论的关系，以便我们可以进行下一步的分析。


