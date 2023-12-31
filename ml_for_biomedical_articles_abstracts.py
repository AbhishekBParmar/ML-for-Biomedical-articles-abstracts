# -*- coding: utf-8 -*-
"""ML for Biomedical articles abstracts.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uK5Cn-5T0T0Tq5vuX8jdZPBy288u_N4S
"""

!pip install stanza
import pandas as pd
import stanza
 # Load the Stanza pipeline for English
nlp = stanza.Pipeline('en')
 # Load the Excel file
data = pd.read_excel('/content/Book9.xlsx')
 # Define a function to perform POS tagging and count the number of each POS tag
def count_pos_tags(text):
    # Perform POS tagging
    doc = nlp(text)
    # Initialize the counters
    num_nouns = 0
    num_pronouns = 0
    num_verbs = 0
    num_adverbs = 0
    num_adjectives = 0
    # Count the number of each POS tag
    for sent in doc.sentences:
        for word in sent.words:
            if word.pos == 'NOUN':
                num_nouns += 1
            elif word.pos == 'PRON':
                num_pronouns += 1
            elif word.pos == 'VERB':
                num_verbs += 1
            elif word.pos == 'ADV':
                num_adverbs += 1
            elif word.pos == 'ADJ':
                num_adjectives += 1
    # Return the counts as a dictionary
    return {'num_nouns': num_nouns, 'num_pronouns': num_pronouns, 'num_verbs': num_verbs, 'num_adverbs': num_adverbs, 'num_adjectives': num_adjectives}
 # Apply the function to each abstract in the Excel file and add the counts as columns to the same sheet
data[['num_nouns', 'num_pronouns', 'num_verbs', 'num_adverbs', 'num_adjectives']] = data['ABSTRACT'].apply(lambda x: pd.Series(list(count_pos_tags(x).values()) if isinstance(x, str) else [0, 0, 0, 0, 0]))
 # Save the updated Excel file
data.to_excel('Category 9.xlsx', index=False)

!pip install stanza
import openpyxl
import stanza
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import numpy as np
 # Download the NLTK resources
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)
 # Read the data from an Excel file
data = pd.read_excel('/content/Test.xlsx')
 # Calculate the POS tag frequencies
data['POS'] = data['ABSTRACT'].apply(nltk.word_tokenize).apply(nltk.pos_tag)
data['Adjectives'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('JJ')]))
data['Adverbs'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('RB')]))
data['Pronouns'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('PR')]))
 # Calculate the ratios
data['R1'] = data['Adverbs'] / data['Adjectives']
data['R2'] = data['Adjectives'] / data['Pronouns']
 # Get unique categories
categories = data['Category'].unique()
 # Create a color map for categories
color_map = plt.cm.get_cmap('tab10', len(categories))
 # Plot the data for each category with different colors
fig, ax = plt.subplots()
for i, category in enumerate(categories):
    category_data = data[data['Category'] == category]
    ax.scatter(category_data['R1'], category_data['R2'], color=color_map(i), label=category, alpha=0.7)
plt.xlabel('Ratio of Adverbs to Adjectives (R1)')
plt.ylabel('Ratio of Adjectives to Pronouns (R2)')
plt.title('POS Tag Ratios by Category')
plt.legend()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the Excel sheet
data = pd.read_excel('/content/Test.xlsx')

# Select the columns with POS tag frequencies
pos_columns = ['num_nouns', 'num_pronouns', 'num_verbs', 'num_adverbs', 'num_adjectives']

# Group the data by Category and calculate descriptive statistics for each group
grouped_stats = data.groupby('Category')[pos_columns].describe()

# Create box plots for each POS tag frequency column by Category
for column in pos_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Category', y=column, data=data)
    plt.xlabel('Category')
    plt.ylabel('Frequency')
    plt.title(f'{column.capitalize()} Frequency Distribution by Category')
    plt.xticks(rotation=90)
    plt.show()

# Print the grouped descriptive statistics
print("Grouped Descriptive Statistics:")
print(grouped_stats)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

# Download the NLTK resources
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt', quiet=True)

# Read the data from an Excel file
data = pd.read_excel('/content/Test.xlsx')

# Calculate the POS tag frequencies
data['POS'] = data['ABSTRACT'].apply(nltk.word_tokenize).apply(nltk.pos_tag)
data['Adjectives'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('JJ')]))
data['Adverbs'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('RB')]))
data['Pronouns'] = data['POS'].apply(lambda x: len([w for w, pos in x if pos.startswith('PR')]))

# Calculate the ratios
data['R1'] = data['Adverbs'] / data['Adjectives']
data['R2'] = data['Adjectives'] / data['Pronouns']

# Create a boxplot for each category
plt.figure(figsize=(10, 6))
sns.boxplot(x='Category', y='R1', data=data)
plt.xlabel('Category')
plt.ylabel('Ratio of Adverbs to Adjectives (R1)')
plt.title('Boxplot of R1 by Category')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Category', y='R2', data=data)
plt.xlabel('Category')
plt.ylabel('Ratio of Adjectives to Pronouns (R2)')
plt.title('Boxplot of R2 by Category')
plt.xticks(rotation=90)
plt.show()

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
 # Load the data
df = pd.read_excel('/content/Test.xlsx')
 # Replace the categories with 'fiction' and 'nonfiction'
df['Category'] = df['Category'].replace(['Ecology', 'Epidemiology', 'Evolutionary Biology', 'learned', 'hobbies'], 'nonfiction')
df['Category'] = df['Category'].replace(['fiction', 'mystery', 'science_fiction', 'adventure', 'romance'], 'fiction')
 # Drop the rows that are not 'fiction' or 'nonfiction'
df = df[(df['Category'] == 'fiction') | (df['Category'] == 'nonfiction')]
 # Calculate the ratios
df['Rnum_adjectivesnum_pronouns'] = df['num_adjectives'] / df['num_pronouns']
df['Rnum_adverbsnum_adjectives'] = df['num_adverbs'] / df['num_adjectives']
 # Replace the categories with 0 and 1
df['Category'] = df['Category'].replace('nonfiction', 0)
df['Category'] = df['Category'].replace('fiction', 1)
 # Check if both classes are present in the data
unique_classes = df['Category'].unique()
if len(unique_classes) < 2:
    if 0 not in unique_classes:
        df.loc[0] = 0
    if 1 not in unique_classes:
        df.loc[1] = 1
 # Convert abstract text into numerical features using TF-IDF
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(df['ABSTRACT'].astype(str))  # Convert to string type
 # Split the data into train and test sets
y = df['Category']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
 # Fit the logistic regression model
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(x_train, y_train)
 # Calculate the accuracy
y_pred_train = logreg.predict(x_train)
accuracy_train = metrics.accuracy_score(y_train, y_pred_train)
print("Training Accuracy : ", accuracy_train)
y_pred_test = logreg.predict(x_test)
accuracy_test = metrics.accuracy_score(y_test, y_pred_test)
print("Testing Accuracy : ", accuracy_test)
 # Print the confusion matrix
print("Confusion Matrix : \n", confusion_matrix(y_test, y_pred_test))

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
 # Step 1: Prepare the data
data = pd.read_excel('/content/Test.xlsx')  # Replace 'Test.xlsx' with your dataset file
abstracts = data['ABSTRACT']
categories = data['Category']
 # Step 2: Extract features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(abstracts)
features = pd.DataFrame(X.toarray())
 # Calculate ratios of adverbs and adjectives
num_adverbs = features.sum(axis=1)
num_adjectives = features.sum(axis=1)
total_words = features.sum(axis=1)
features['adverb_ratio'] = num_adverbs / total_words
features['adjective_ratio'] = num_adjectives / total_words
 # Calculate ratio of adjectives and pronouns
num_pronouns = features.sum(axis=1)
features['pronoun_ratio'] = num_pronouns / num_adjectives
 # Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, categories, test_size=0.2, random_state=42)
 # Convert feature names to strings
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)
 # Step 4: Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)
 # Step 5: Make predictions on test data
y_pred = model.predict(X_test)
 # Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Prepare the data
data = pd.read_excel('/content/Test.xlsx')  # Replace 'Test.xlsx' with your dataset file
abstracts = data['ABSTRACT']
categories = data['Category']

# Step 2: Extract features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(abstracts)
features = pd.DataFrame(X.toarray())

# Calculate ratios of adverbs and adjectives
num_adverbs = features.sum(axis=1)
num_adjectives = features.sum(axis=1)
total_words = features.sum(axis=1)
features['adverb_ratio'] = num_adverbs / total_words
features['adjective_ratio'] = num_adjectives / total_words

# Calculate ratio of adjectives and pronouns
num_pronouns = features.sum(axis=1)
features['pronoun_ratio'] = num_pronouns / num_adjectives

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, categories, test_size=0.2, random_state=42)

# Convert feature names to strings
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)

# Reset indices of X_test, y_test, and y_pred
X_test.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

# Step 4: Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 5: Make predictions on test data
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Overall Accuracy:", accuracy)

# Calculate accuracy for each category
category_accuracy = {}
unique_categories = categories.unique()
for category in unique_categories:
    category_indices = y_test[y_test == category].index
    category_y_test = y_test.loc[category_indices]
    category_y_pred = y_pred[category_indices]
    category_accuracy[category] = accuracy_score(category_y_test, category_y_pred)
    print(f"Accuracy for {category}: {category_accuracy[category]}")

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
 # Step 1: Prepare the data
data = pd.read_excel('/content/Test.xlsx')  # Replace 'Test.xlsx' with your dataset file
abstracts = data['ABSTRACT']
categories = data['Category']
 # Step 2: Extract features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(abstracts)
features = pd.DataFrame(X.toarray())
 # Calculate ratios of adverbs and adjectives
num_adverbs = features.sum(axis=1)
num_adjectives = features.sum(axis=1)
total_words = features.sum(axis=1)
features['adverb_ratio'] = num_adverbs / total_words
features['adjective_ratio'] = num_adjectives / total_words
 # Calculate ratio of adjectives and pronouns
num_pronouns = features.sum(axis=1)
features['pronoun_ratio'] = num_pronouns / num_adjectives
 # Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, categories, test_size=0.2, random_state=42)
 # Convert feature names to strings
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)
 # Reset indices of X_test, y_test, and y_pred
X_test.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)
 # Step 4: Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)
 # Step 5: Make predictions on test data
y_pred = model.predict(X_test)
 # Step 6: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Overall Accuracy:", accuracy)
 # Calculate confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
 # Calculate precision, recall, and F1 score
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)



import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
 # Read the Excel file
data = pd.read_excel('/content/Test.xlsx')  # Replace 'File.xlsx' with your dataset file
 # Get the abstracts and categories
abstracts = data['ABSTRACT']
categories = data['Category']
 # Initialize a CountVectorizer
vectorizer = CountVectorizer()
 # Transform the abstracts into feature vectors
X = vectorizer.fit_transform(abstracts)
 # Train the Naive Bayes model
model = MultinomialNB()
model.fit(X, categories)
 # Get the feature names (words)
feature_names = vectorizer.get_feature_names_out()
 # Compare feature importances for pairs of categories
unique_categories = categories.unique()
pairwise_important_words = {}
for i in range(len(unique_categories) - 1):
    for j in range(i + 1, len(unique_categories)):
        category1 = unique_categories[i]
        category2 = unique_categories[j]
         # Get the feature importances for each category
        category1_idx = model.classes_.tolist().index(category1)
        category2_idx = model.classes_.tolist().index(category2)
        category1_importance = model.feature_log_prob_[category1_idx]
        category2_importance = model.feature_log_prob_[category2_idx]
         # Calculate the relative importance of words
        relative_importance = category1_importance - category2_importance
         # Get the top 10 relatively important words for each category
        top_10_words_idx = relative_importance.argsort()[-10:][::-1]
        important_words = [feature_names[idx] for idx in top_10_words_idx]
         # Store the important words for the pair of categories
        pair_key = f"{category1} vs {category2}"
        pairwise_important_words[pair_key] = important_words
 # Create a DataFrame from the pairwise_important_words dictionary
df = pd.DataFrame(pairwise_important_words)
 # Save the DataFrame as an Excel file
df.to_excel('/content/Results.xlsx', index=False)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Read the Excel file
data = pd.read_excel('/content/Test.xlsx')  # Replace 'File.xlsx' with your dataset file

# Get the abstracts and categories
abstracts = data['ABSTRACT']
categories = data['Category']

# Initialize a CountVectorizer with stopwords
vectorizer = CountVectorizer(stop_words='english')

# Transform the abstracts into feature vectors
X = vectorizer.fit_transform(abstracts)

# Train the Naive Bayes model
model = MultinomialNB()
model.fit(X, categories)

# Get the feature names (words)
feature_names = vectorizer.get_feature_names_out()

# Get the feature importances for each category
category_feature_importance = {}
for i, category in enumerate(model.classes_):
    feature_importance = model.feature_log_prob_[i]

    # Sort feature indices based on importance
    sorted_indices = feature_importance.argsort()[::-1]

    # Exclude stopwords from important words
    important_words = [feature_names[idx] for idx in sorted_indices if feature_names[idx] not in vectorizer.get_stop_words()]

    # Take top 10 important words for each category
    important_words = important_words[:10]

    category_feature_importance[category] = important_words

# Print the important words for each category
for category, words in category_feature_importance.items():
    print(f"Category: {category}")
    print("Important Words:", ", ".join(words))
    print()