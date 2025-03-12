from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()
model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.post("/predict/")
def predict_balance(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    output = model(**inputs)
    return {"prediction": output.logits.argmax().item()}