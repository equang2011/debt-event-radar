import json
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT
    / "data"
    / "debt_classifier"
    / "labeled"
    / "candidate_exhibits_v2_flattened.json"
)


with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [obj["text"] for obj in data]
labels = [obj["human_label"] for obj in data]
names = [obj["document_name"] for obj in data]
doc_urls = [obj["document_url"] for obj in data]

def basic_stats():
    print("total:", len(data))
    print("positive:", sum(obj["human_label"] == 1 for obj in data))
    print("negative:", sum(obj["human_label"] == 0 for obj in data))

X_train, X_test, y_train, y_test, doc_urls_train, doc_urls_test = train_test_split(
    texts,
    labels,
    doc_urls,
    test_size=0.25,
    random_state=42,
    stratify=labels,
)

def print_train():
    print("train size:", len(X_train))
    print("test size:", len(X_test))
    print("train positives:", sum(y_train))
    print("train negatives:", len(y_train) - sum(y_train))
    print("test positives:", sum(y_test))
    print("test negatives:", len(y_test) - sum(y_test))

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
feature_names = vectorizer.get_feature_names_out()


def print_tdidf_feats():
    print("train matrix shape:", X_train_tfidf.shape)
    print("test matrix shape:", X_test_tfidf.shape)
    print("number of features:", len(feature_names))
    print(feature_names[200:300])


model = LogisticRegression()

model.fit(X_train_tfidf, y_train)

predictions = model.predict(X_test_tfidf)
probabilities = model.predict_proba(X_test_tfidf)[:, 1]

coefficients = model.coef_[0]
pairs = list(zip(feature_names, coefficients))

top_positive = sorted(pairs, key=lambda x: x[1], reverse=True)[:15]
top_negative = sorted(pairs, key = lambda x: x[1])[:15]

print("TOP POSITIVE FEATURES")
for feature, weight in top_positive:
    print(feature, round(weight, 3))

print("\nTOP NEGATIVE FEATURES")
for feature, weight in top_negative:
    print(feature, round(weight, 3))


def print_predictions():
    for doc_url, true_label, prediction, probability in zip(
        doc_urls_test,
        y_test,
        predictions,
        probabilities,
    ):
        print(
            "actual:", true_label,
            "predicted:", prediction,
            "probability:", round(probability, 3),
            doc_url,
        )
print_predictions()


"""
labeled_examples_1.json
        ↓
load JSON
        ↓
texts  = [obj["text"], ...]
labels = [obj["human_label"], ...]
        ↓
split into train/test
        ↓
TF-IDF.fit_transform(training text)
        ↓
LogisticRegression.fit(X_train, y_train)
        ↓
TF-IDF.transform(test text)
        ↓
model.predict / predict_proba
        ↓
compare prediction to human_label

"""

