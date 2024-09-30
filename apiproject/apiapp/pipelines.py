from transformers import pipeline

sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
emotions_pipeline= pipeline(model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)
entities_pipeline = pipeline(model="Babelscape/wikineural-multilingual-ner", aggregation_strategy="simple")
clasify_pipeline = pipeline(model="facebook/bart-large-mnli")