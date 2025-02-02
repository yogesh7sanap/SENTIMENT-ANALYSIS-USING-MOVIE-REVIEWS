import streamlit as st

#changing background color
# st.markdown("""
#     <style>
#         body {
#             background-color: lightblue;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

# Load the model, vectorizer, and encoder
model_xgb = pickle.load(open("model_xgb.pkl", "rb"))
model = pickle.load(open("model_logistic.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
encoder = pickle.load(open("label_encoder.pkl", "rb"))  # Load the saved LabelEncoder

# Create the Streamlit app title
st.title("Sentiment Analysis Model")

# User input
review_main = st.text_input("Enter your review:")
submit = st.button("Predict")

if submit:
    if not review_main.strip():
        st.warning("Please enter a valid review.")
    else:
        # ----------------------------Text Preprocessing----------------------------
        lemmatizer = WordNetLemmatizer()
        stopwords_to_remove = stopwords.words("english")

        def preprocess_text(text):
            # Convert to lowercase
            text = text.lower()
            # Remove special characters and numbers
            text = re.sub(r"[^a-zA-Z\s]", "", text)
            # Tokenize words
            words = nltk.word_tokenize(text)
            # Remove stopwords and lemmatize
            words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords_to_remove]
            return " ".join(words)

        # Preprocess the input review
        cleaned_review = preprocess_text(review_main)

        # Transform using the loaded vectorizer
        review_transformed = vectorizer.transform([cleaned_review])  # Wrap in a list

        # Predict the sentiment
        prediction = model.predict(review_transformed)

        print(prediction)
        # Decode the prediction to its label
        decoded_sentiment = encoder.inverse_transform(prediction)

        # Display the decoded prediction
        st.write(f"Predicted Sentiment: {decoded_sentiment[0]}")
