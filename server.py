import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from text import generate_output
from image import generate_image
from fastapi.responses import FileResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint
@app.get("/")
def home():
    return {"message": "FastAPI server is running!"}

# Define Input Schema
class StyleRequest(BaseModel):
    style_idea: str
    gender: str
    ethnicity: str
    age: str
    skin_color: str
    season: str
    accessories: str
    occasion: str

@app.post("/generate-outfit/")
async def generate_outfit(request: StyleRequest):
    try:
        print("Received request:", request.dict())  # Debugging
        
        # Generate outfit text
        model_name = "tunedModels/outfitsuggestiongenerator-usqw4b296kfe"
        prompt = f"Create an outfit as text including Top,Bottoms and Foot wear based on: {request.style_idea} for {request.gender} from {request.ethnicity} , {request.age} years old,hoving {request.skin_color} complexion,to be worne in {request.season}, with {request.accessories} accessories,for {request.occasion} with matching footware and model looking at the camera."
        
        outfit_description = generate_output(model_name, prompt)
        
        if not outfit_description:
            raise Exception("Text generation failed. Received empty response.")

        print("Generated outfit description:", outfit_description)  # Debugging

        # Generate image
        image_path = "generated_images/outfit.png"
        generated_image = generate_image(f"a {request.gender} model of age {request.age} from ethinicity {request.ethnicity} with {request.skin_color} complexion see into the camera with perfect lightining and wearing {outfit_description} with complementing background that enhances the outfit and model, full body image")

        if generated_image is None:
            raise Exception("Image generation failed.")

        generated_image.save(image_path)

        return {
            "outfit_description": outfit_description,
            "image_url": f"https://fashion-ai-bsckend.onrender.com/generated_images/outfit.png"
        }

    except Exception as e:
        print("Error in /generate-outfit/:", str(e))  # Debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/generated_images/{filename}")
async def get_generated_image(filename: str):
    image_path = os.path.join("generated_images", filename)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Image not found")
