# utils.py
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

def load_model():
    """Load model ViT5 một lần"""
    model_name = "VietAI/vit5-base-vietnews-summarization"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def clean_text(text: str) -> str:
    """Làm sạch văn bản"""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def summarize_text(text: str, max_length: int = 150, min_length: int = 50):
    """Hàm tóm tắt chính"""
    tokenizer, model = load_model()
    
    input_text = clean_text(text)
    
    # Tokenize
    encoding = tokenizer(
        input_text,
        max_length=1024,
        truncation=True,
        return_tensors="pt"
    )
    
    # Generate summary
    with torch.no_grad():
        output = model.generate(
            input_ids=encoding["input_ids"],
            attention_mask=encoding["attention_mask"],
            max_length=max_length + 50,
            min_length=min_length,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
            length_penalty=1.0
        )
    
    summary = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return summary