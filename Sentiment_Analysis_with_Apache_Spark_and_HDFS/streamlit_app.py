import streamlit as st
from pyspark.ml.feature import CountVectorizerModel, IDFModel, StringIndexerModel, StopWordsRemover, Tokenizer
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, udf
from pyspark.sql.types import ArrayType, StringType
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Initialize Spark
spark = SparkSession.builder.appName("SentimentApp").getOrCreate()

# Load Models
cv_model = CountVectorizerModel.load("count_vectorizer2")
idf_model = IDFModel.load("idf_model")
indexer_model = StringIndexerModel.load("indexer_main")
lr_model = LogisticRegressionModel.load("logistic_reg_model")

# Stopwords
stop_words = stopwords.words("english")
stopword_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=stop_words)

# Tokenizer
tokenizer = Tokenizer(inputCol="Review", outputCol="words")

# Lemmatization Function
lemmatizer = WordNetLemmatizer()
lemmatize_udf = udf(lambda words: [lemmatizer.lemmatize(word) for word in words], ArrayType(StringType()))

# Streamlit UI
st.title("Sentiment Analysis App")

user_input = st.text_area("Enter a review:", "")

if st.button("Analyze Sentiment"):
    if user_input:
        # Create Spark DataFrame
        df = spark.createDataFrame([(user_input,)], ["Review"])

        # Preprocessing: Lowercase & Remove Non-Alphabetic Characters
        df = df.withColumn("Review", lower(col("Review")))
        df = df.withColumn("Review", regexp_replace(col("Review"), "[^a-zA-Z\s]", ""))

        # Tokenization
        df = tokenizer.transform(df)

        # Stopword Removal
        df = stopword_remover.transform(df)

        # Lemmatization
        df = df.withColumn("lemmatized_words", lemmatize_udf(col("filtered_words")))

        # Transform using CountVectorizer
        df = cv_model.transform(df)

        # Apply IDF Model to get TF-IDF Features
        df = idf_model.transform(df)

        # Predict Sentiment
        prediction = lr_model.transform(df).select("prediction").first()[0]
        sentiment_label = indexer_model.labels[int(prediction)]

        st.write(f"Predicted Sentiment: **{sentiment_label}**")

