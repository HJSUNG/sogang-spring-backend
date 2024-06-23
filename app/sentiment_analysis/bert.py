from transformers import BertTokenizer, BertForSequenceClassification
import torch

def sentiment_analysis(text):
    model_name = "beomi/kcbert-base"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    positive_score, negative_score = probabilities[0]

    if positive_score > negative_score:
        sentiment = "긍정"
    else:
        sentiment = "부정"

    return [sentiment, positive_score.item(), negative_score.item()]
