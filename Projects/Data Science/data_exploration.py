#Load all libraries needed
import numpy as np
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from sklearn.preprocessing import OneHotEncoder



#Load dataset into df
df = pd.read_csv('recruitmentdataset-2022-1.3.csv')

#We are group 1 so Company A -> Cut out all data not company A

"""Explore the data"""

# one hot encoding to convert 'ind-degree' to numerical data
ohe = OneHotEncoder()
transformed = ohe.fit_transform(df[['ind-degree']])
# and add three new columns to the dataset
df[ohe.categories_[0]] = transformed.toarray()
# one hot encoding to convert 'gender' to numerical data
transformed = ohe.fit_transform(df[['gender']])
# and add three new columns to the dataset
df[ohe.categories_[0]] = transformed.toarray()
# one hot encoding to convert 'nationality' to numerical data
transformed = ohe.fit_transform(df[['nationality']])
# and add three new columns to the dataset
df[ohe.categories_[0]] = transformed.toarray()
# one hot encoding to convert 'sport' to numerical data
transformed = ohe.fit_transform(df[['sport']])
# and add seven new columns to the dataset
df[ohe.categories_[0]] = transformed.toarray()




# Make a copy from the original dataset as to not overwrite data
df_new = df.copy()
# Turn the 'decision' column to nuremic values (0 and 1)
df_new['decision'] = df_new['decision'].astype(int)
# Turn the 'ind-programming_exp' column to nuremic values (0 and 1)
df_new['ind-programming_exp'] = df_new['ind-programming_exp'].astype(int)
# Turn the 'ind-international_exp' column to nuremic values (0 and 1)
df_new['ind-international_exp'] = df_new['ind-international_exp'].astype(int)
# Turn the 'ind-entrepeneur_exp' column to nuremic values (0 and 1)
df_new['ind-entrepeneur_exp'] = df_new['ind-entrepeneur_exp'].astype(int)
# Turn the 'ind-exact_study' column to nuremic values (0 and 1)
df_new['ind-exact_study'] = df_new['ind-exact_study'].astype(int)
# Turn the 'ind-debateclub' column to nuremic values (0 and 1)
df_new['ind-debateclub'] = df_new['ind-debateclub'].astype(int)
# Noramlize the 'ind-languages' column to a nuremic value (between 0 and 1)
df_new['ind-languages'] = (df_new['ind-languages']-df_new['ind-languages'] .min())/(df_new['ind-languages'] .max()-df_new['ind-languages'] .min())
# Noramlize the 'ind-university_grade' column to a nuremic value (between 0 and 1)
df_new['ind-university_grade'] = (df_new['ind-university_grade']-df_new['ind-university_grade'] .min())/(df_new['ind-university_grade'] .max()-df_new['ind-university_grade'] .min())
# Noramlize the 'ind-age' column to a nuremic value (between 0 and 1)
df_new['age'] = (df_new['age']-df_new['age'] .min())/(df_new['age'] .max()-df_new['age'] .min())

is_company_A = df_new['company'] == 'A'
df_A_new = df_new[is_company_A]

font = {'size': 6}



matplotlib.rc('font', **font)
tmpCorr = df_A_new[['male','female','other','age','Dutch','German','Belgian','Swimming',"Cricket", "Golf","Chess", 'Football','Running','Tennis','Rugby']].corr()
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
sns.heatmap(tmpCorr, annot = True, cmap="Blues", annot_kws={'fontsize': 12}
)
plt.title("Correlation between descriptors", fontsize = 13)
plt.show()


tmpCorr = df_A_new[['male','female', 'other', 'age','Dutch','German','Belgian','Swimming',"Cricket","Golf","Chess",'Football','Running',     'Tennis','Rugby',"master","phd","bachelor",'ind-university_grade', 'ind-debateclub', 'ind-entrepeneur_exp', 'ind-international_exp','ind-programming_exp', 'ind-languages']].corr()

sns.heatmap(tmpCorr, annot = True,  cmap= "Blues",annot_kws={'fontsize': 8}
)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.title("Correlation between descriptors and indicators", fontsize = 13)
plt.show()


#PREDICTIVE POWER 


is_hired_A = df_A_new['decision'] == True
df_A_hired = df_A_new[is_hired_A]

not_hired_A = df_A_new['decision'] == False
df_not_hired = df_A_new[not_hired_A]

hiredCount = len(df_A_hired)
not_hired_count = len(df_not_hired)

percentages = []
distribution_A = {}
distribution_A_not_hired = {}

is_bachelor = df_A_hired['ind-degree'] == 'bachelor'
df_A_bachelor = df_A_hired[is_bachelor]
bachelorCount = len(df_A_bachelor)
bachelorPercantage = bachelorCount / hiredCount
percentages.append(bachelorPercantage)
distribution_A['bachelor'] = bachelorPercantage


is_phd = df_A_hired['ind-degree'] == 'phd'
df_A_phd = df_A_hired[is_phd]
phdCount = len(df_A_phd)
phdPercantage = phdCount / hiredCount
percentages.append(phdPercantage)
distribution_A['phd'] = phdPercantage

is_master = df_A_hired['ind-degree'] == 'master'
df_A_master = df_A_hired[is_master]
masterCount = len(df_A_master)
masterPercantage = masterCount / hiredCount
percentages.append(masterPercantage)
distribution_A['master'] = masterPercantage

#languages

for i in range(4):
  knows_languages = df_A_hired['ind-languages'] == i
  df_A_languages = df_A_hired[knows_languages]
  languages_Count = len(df_A_languages)
  languages_Percentage = languages_Count / hiredCount
  percentages.append(languages_Percentage)
  label = '%d lang' % (i)
  distribution_A[label] = languages_Percentage


indicators = ['ind-debateclub','ind-programming_exp','ind-international_exp','ind-entrepeneur_exp','ind-exact_study']

def checkPercantage():
  for indicator in indicators:
    is_indicator_true = df_A_hired[indicator] == True
    df_A_indicator = df_A_hired[is_indicator_true]
    indicatorCount = len(df_A_indicator)
    indicatorPercantage = indicatorCount / hiredCount
    percentages.append(indicatorPercantage)
    distribution_A[indicator] = indicatorPercantage
    
    is_indicator_false = df_A_hired[indicator] == False
    df_A_indicator = df_A_hired[is_indicator_false]
    indicatorCount = len(df_A_indicator)
    indicatorPercantage = indicatorCount / hiredCount
    percentages.append(indicatorPercantage)
    name = 'no %s' % (indicator)
    distribution_A[name] = indicatorPercantage
    
checkPercantage()
result = {key: value * 100 for key, value in distribution_A.items()}
sortedDistribution = dict(sorted(result.items(), key=lambda item: item[1]))
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.barh(list(sortedDistribution.keys()),list(sortedDistribution.values()))
plt.yticks(fontsize=13)
ax.set_xlabel("Percentage")
ax.set_ylabel("Feature")
ax.set_xlim([0,100])
ax.set_title("Percentage of hired applicants based on their features")

rects = ax.patches

plt.show()

is_hired = df['decision'] == True
df_hired = df[is_hired]

is_A = df_hired['company'] == 'A'
df_A_hired = df_hired[is_A]

# Visualize hired population company A vs hired population overall
plt.figure(figsize=(8,5))
sns.countplot(x='company',data=df_hired, hue='gender',palette = ['plum', 'lightskyblue', 'grey'])
plt.title("Distrib. of gender for hired people between companies", font = {'size': 12})
plt.xlabel('Company',font = {'size': 12})
plt.ylabel('Nr. of people',font = {'size': 12})
plt.show()

#Split age into categories 21-23, 24-26, 27-29, 30-32
df_hired['age'] = df_hired['age'].replace({
    21: '21-23',
    22: '21-23',
    23: '21-23',
    24: '24-26',
    25: '24-26',
    26: '24-26',
    27: '27-29',
    28: '27-29',
    29: '27-29',
    30: '30-32',
    31: '30-32',
    32: '30-32'})

# Sort dataframe based on age categories to prevent wrong order on next plot.
df_hired['age'] = pd.Categorical(df_hired['age'], categories = ['21-23','24-26','27-29','30-32'], ordered = True)

# Visualize hired population company A vs hired population overall
plt.figure(figsize=(8,5))
sns.countplot(x='company',data=df_hired, hue='age', palette= 'Set3')
plt.title("Distrib. of age for hired people between companies", font = {'size': 12})
plt.xlabel('Company')
plt.ylabel('Nr. of people')
plt.show()

# Visualize hired population company A vs hired population overall
plt.figure(figsize=(8,5))
sns.countplot(x='company',data=df_hired, hue='nationality', palette= 'Set3')
plt.title("Distrib. of nationality for hired people between companies", font = {'size': 12})
plt.xlabel('Company', font = {'size': 12})
plt.ylabel('Nr. of people', font = {'size': 12})
plt.show()

sns.set(font_scale=1.15)
# Visualize hired population company A vs hired population overall
plt.figure(figsize=(8,5))
sns.countplot(x='company',data=df_hired, hue='sport', palette= 'Set3')
plt.title("Distrib. of sport for hired people between companies", font = {'size': 12})
plt.xlabel('Company')
plt.ylabel('Nr. of people')
plt.show()

indicators = ["ind-degree", 'ind-debateclub', 'ind-entrepeneur_exp', 'ind-international_exp', 'ind-programming_exp', 'ind-languages', 'ind-exact_study']

for indicator in indicators:
  sns.set(font_scale=1.15)
  # Visualize hired population company A vs hired population overall
  plt.figure(figsize=(8,5))
  sns.countplot(x='company',data=df_hired, hue=indicator, palette= 'Set2')
  title = "Distrib. of %s for hired people between companies" % (indicator)
  plt.title(title, font = {'size': 12})
  plt.xlabel('Company')
  plt.ylabel('Nr. of people')
  plt.show()


#Load dataset into df

def assignColors(series):
  col = []
  for val in series.index:
    if val == 'Swimming':
        col.append('blue')
    elif val == 'Cricket':
        col.append('orange')
    elif val == 'Golf':
        col.append('green')
    elif val == 'Chess':
        col.append('black')
    elif val == 'Football':
        col.append('brown')
    elif val == 'Running':
        col.append('beige')
    elif val == 'Tennis':
        col.append('pink')
    elif val == 'Rugby':
        col.append('yellow')
    elif val == 'male':
        col.append('blue')
    elif val == 'female':
        col.append('red')
    elif val == 'other':
        col.append('yellow')
    elif val == 'Dutch':
        col.append('orange')
    elif val == 'German':
        col.append('yellow')
    elif val == 'Belgian':
        col.append('brown')
    else:
        col.append('blue')
  return col

def setTitle(counter, company):
  title = 'Title'
  if counter == 0:
      title = 'Percent of hired candidates based on sport'
  elif counter == 1:
      title = 'Percent of hired candidates based on gender'
  elif counter == 2:
      title = 'Percent of hired candidates based on nationality'
  else:
      title = 'Percent of hired candidates based on age'
  title += ' for company %s' % (company)
  return title

xRange = [0,0.05,0.10,0.15,0.2,0.25,0.3,0.35]
def plotBarChart(df_hired, company):
  hired_count = len(df_hired.index)
  sports_count = df_hired['sport'].value_counts()
  gender_count = df_hired['gender'].value_counts()
  nationality_count = df_hired['nationality'].value_counts()
  age_count = df_hired['age'].value_counts()
  percentageSportsCount = sports_count / hired_count
  percentageGenderCount = gender_count / hired_count
  percentageNationalityCount = nationality_count / hired_count
  percentageAgeCount = age_count / hired_count
  companyDistribution = [percentageSportsCount, percentageGenderCount, percentageNationalityCount, percentageAgeCount]
  discriptor_counter = 0
  x_counter = 0
  y_counter = 0
  for series in companyDistribution:
    color = assignColors(series)
    ax = series.plot(kind="bar")
    ax.bar(series.index,series, color = color)
    ax.set_title(setTitle(discriptor_counter, company))
    
    plt.ylim(0.0,0.35)
    
    rects = ax.patches
    labels = [f"label{i}" for i in range(len(rects))]
    discriptor_counter += 1
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2, height + 5, label, ha="center", va="bottom"
        )
 
    plt.show()
is_company_A = df['company'] == 'A'
df_A = df[is_company_A]
is_hired_A = df_A['decision'] == True
df_A_hired = df_A[is_hired_A]
plotBarChart(df_A_hired, 'A')



is_company_B = df['company'] == 'B'
df_B = df[is_company_B]
is_hired_B = df_B['decision'] == True
df_B_hired = df_B[is_hired_B]

plotBarChart(df_B_hired, 'B')

is_company_C = df['company'] == 'C'
df_C = df[is_company_C]
is_hired_C = df_C['decision'] == 1
df_C_hired = df_C[is_hired_C]
plotBarChart(df_C_hired, 'C')

is_company_D = df['company'] == 'D'
df_D = df[is_company_D]
is_hired_D = df_D['decision'] == True
df_D_hired = df_D[is_hired_D]
plotBarChart(df_D_hired, 'D')

