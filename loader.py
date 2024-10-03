from transformers import AutoModelForCausalLM, AutoTokenizer
import truststore
import os

truststore.inject_into_ssl()

model_name = "unsloth/Llama-3.2-3B-Instruct-GGUF"
save_directory = "./models/Llama-3.2-3B-Instruct-GGUF"

os.makedirs(save_directory, exist_ok=True)

# model = AutoModelForCausalLM.from_pretrained(model_name, use_safetensors=False)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(save_directory)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

    