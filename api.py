from typing import List, Dict

import fasttext
from fastapi import FastAPI
from pydantic import BaseModel

from models.classification.commands import process_text, format_labels

MODEL_PATH = 'model.bin'


class PostModel(BaseModel):
	title: str
	text: str


class SubredditModel(BaseModel):
	labels: List[str]
	probas: List[float]


app = FastAPI()


@app.post("/predict", response_model=SubredditModel)
def predict(post: PostModel):
	model = fasttext.load_model(MODEL_PATH)

	# Concatenate title and text to preprocess
	print(f'title: {post.title}, text: {post.text}')
	data = process_text(f'{post.title} {post.text}')

	# Get predictions
	# TODO: parametrize k
	labels, probas = model.predict(data, k=10)

	return SubredditModel(labels=format_labels(labels), probas=list(probas))
