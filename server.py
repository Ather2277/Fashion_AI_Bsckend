import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from image import generate_image
from fastapi.responses import FileResponse

# ---- Gemini Setup ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in your environment
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---- FastAPI Setup ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI Gemini SDK server is running!"}

class StyleRequest(BaseModel):
    style_idea: str
    gender: str
    ethnicity: str
    age: str
    skin_color: str
    season: str
    accessories: str
    occasion: str

# ---- Gemini-based Text Generator ----
def generate_outfit_text(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Gemini SDK error: {str(e)}")

# ---- Outfit Generator Endpoint ----
@app.post("/generate-outfit/")
async def generate_outfit(request: StyleRequest):
    try:
        print("Received request:", request.dict())

        prompt = f"""
                You are a creative fashion designer. Return the outfit description as a stylish paragraph (20–30 words).

                Requirements:
                    - Must include top, bottoms, and footwear.
                    - Style idea: {request.style_idea}
                    - Gender: {request.gender}
                    - Ethnicity: {request.ethnicity}
                    - Age: {request.age}
                    - Skin tone: {request.skin_color}
                    - Season: {request.season}
                    - Accessories: {request.accessories}
                    - Occasion: {request.occasion}
                    - The description must be balanced, creative, fashion-forward, trendy, and pleasing to both Millennials and Gen Z.
                    - Write in a natural, flowing tone (not a list).
                """



        outfit_description = generate_outfit_text(prompt)

        if not outfit_description:
            raise Exception("Text generation failed. Received empty response.")

        print("Generated outfit description:", outfit_description)

        # Generate image from text (same logic as your code)
        image_path = "generated_images/outfit.png"
        image_prompt = f"""
            Return the response strictly as valid JSON in the following format:

            {{
              "image_prompt": "A detailed image generation prompt here"
            }}

            Requirements:
            - Gender: {request.gender}
            - Age: {request.age}
            - Ethnicity: {request.ethnicity}
            - Skin complexion: {request.skin_color}
            - The model should be captured in a **full-body shot from head to toe**, facing the camera, with perfect studio-like lighting.
            - Outfit: {outfit_description}
            - Background should complement and enhance the outfit style, without distracting from the subject.
            - Ensure clear visibility of the entire outfit, footwear, and accessories.
            """



        generated_image = generate_image(image_prompt)

        if generated_image is None:
            raise Exception("Image generation failed.")

        generated_image.save(image_path)

        return {
            "outfit_description": outfit_description,
            "image_url": f"https://fashion-ai-bsckend.onrender.com/generated_images/outfit.png"
        }

    except Exception as e:
        print("Error in /generate-outfit/:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/generated_images/{filename}")
async def get_generated_image(filename: str):
    image_path = os.path.join("generated_images", filename)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Image not found")
