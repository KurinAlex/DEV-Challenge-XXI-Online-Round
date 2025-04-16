"""
Hugging Face transformers pipelines.
"""

from transformers import pipeline

sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
"""Pipeline for text sentiment analysis."""

emotions_pipeline = pipeline(model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)
"""Pipeline for text emotions extraction."""

entities_pipeline = pipeline(model="dslim/bert-base-NER-uncased", aggregation_strategy="simple")
"""Pipeline for text entities extraction."""

clasify_pipeline = pipeline(model="typeform/distilbert-base-uncased-mnli", multi_label=True)
"""Pipeline for text classification."""
