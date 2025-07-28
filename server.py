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

        prompt = (
            f"Create an outfit as text in 20 to 30 words including top, bottoms, and footwear based on: "
            f"{request.style_idea} for a {request.gender} of {request.ethnicity} ethnicity, "
            f"{request.age} years old, with {request.skin_color} skin tone. The outfit should suit "
            f"{request.season} season and include {request.accessories} as accessories for a {request.occasion}. "
            f"The description should be detailed and stylish."
        )

        outfit_description = generate_outfit_text(prompt)

        if not outfit_description:
            raise Exception("Text generation failed. Received empty response.")

        print("Generated outfit description:", outfit_description)

        # Generate image from text (same logic as your code)
        image_path = "generated_images/outfit.png"
        image_prompt = (
            f"A {request.gender} model, age {request.age}, {request.ethnicity} ethnicity, "
            f"{request.skin_color} complexion, looking into the camera, perfect lighting, full body, "
            f"wearing: {outfit_description}. Background should complement the outfit."
        )

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
