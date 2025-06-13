import pandas as pd
import numpy as np
import nltk
nltk.download('punkt_tab')
import string
import pickle
import random

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Your seed dataset
data = {
    'text': [
        'I love this product, it is fantastic!',
        'This is the worst thing I have ever bought.',
        'Absolutely amazing experience.',
        'I hate it. Waste of money.',
        'Very good quality and fast delivery.',
        'Terrible customer service, never buying again.',
        'Highly recommended!',
        'Extremely disappointing.',
        'I am very satisfied with my purchase.',
        'The product broke after one day. Horrible.'
    ],
    'label': [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0
    ]
}

# Expand to a large dataset
seed_texts = data['text']
seed_labels = data['label']

large_data = {'text': [], 'label': []}

# Let's generate 10,000 samples
for _ in range(10000):
    idx = random.randint(0, len(seed_texts) - 1)

    # Add some noise/randomness to text
    text_variants = [
        seed_texts[idx],
        seed_texts[idx].lower(),
        seed_texts[idx].upper(),
        f"Review: {seed_texts[idx]}",
        f"{seed_texts[idx]} :)",
        f"{seed_texts[idx]}!",
        f"{seed_texts[idx]} (verified buyer)",
        f"{seed_texts[idx]} - Amazon customer"
    ]

    new_text = random.choice(text_variants)

    large_data['text'].append(new_text)
    large_data['label'].append(seed_labels[idx])

# Convert to DataFrame
df = pd.DataFrame(data)

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)

# Apply preprocessing
df['clean_text'] = df['text'].apply(preprocess_text)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label'], test_size=0.2, random_state=42)

# Build a pipeline: TF-IDF + Logistic Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# # Save the model to pickle file
# model_filename = 'sentiment_model.pkl'
# with open(model_filename, 'wb') as file:
#     pickle.dump(pipeline, file)
#
# print(f"Model saved as {model_filename}")
