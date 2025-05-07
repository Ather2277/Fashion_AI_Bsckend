import time
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

def generate_image(prompt, model="black-forest-labs/FLUX.1-dev", retries=5, delay=10):
    token = os.getenv("HUGGINGFACE_TOKEN")
    client = InferenceClient(model, token=token)

    for attempt in range(retries):
        try:
            return client.text_to_image(prompt)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    raise Exception("All retries failed. Please try again later.")
