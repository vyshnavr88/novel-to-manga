# main.py - FIXED VERSION (Works on all platforms!)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from groq import Groq
import httpx

app = FastAPI(title="Novel to Manga API - FREE Edition")

# CORS - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
groq_client = None
if os.getenv("GROQ_API_KEY"):
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

fal_api_key = os.getenv("FAL_API_KEY")

# Pydantic Models (v1 compatible)
class NovelInput(BaseModel):
    text: str
    groq_key: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "text": "Your novel text here...",
                "groq_key": "optional_groq_key"
            }
        }

class Scene(BaseModel):
    id: int
    type: str
    panels: int
    characters: List[str]
    description: str
    dialogue: List[str]
    shot: str
    emotion: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "action",
                "panels": 2,
                "characters": ["Hero", "Villain"],
                "description": "Epic battle scene",
                "dialogue": ["Hero: I won't give up!"],
                "shot": "wide",
                "emotion": "intense"
            }
        }

class ImagePromptRequest(BaseModel):
    scene: Scene

class ImageGenerationRequest(BaseModel):
    prompt: str
    width: int = 512
    height: int = 768

# Routes
@app.get("/")
async def root():
    return {
        "message": "Novel to Manga API - FREE Edition",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "POST /api/analyze",
            "prompts": "POST /api/generate-prompts", 
            "image": "POST /api/generate-image",
            "health": "GET /health"
        }
    }

@app.post("/api/analyze")
async def analyze_novel(input_data: NovelInput):
    """Analyze novel text and break into manga scenes"""
    
    # Use provided key or default
    client = groq_client
    if input_data.groq_key:
        client = Groq(api_key=input_data.groq_key)
    
    if not client:
        raise HTTPException(
            status_code=400, 
            detail="Groq API key required. Sign up free at groq.com"
        )
    
    try:
        prompt = f"""Analyze this novel excerpt and break it into manga scenes.
        
For each scene provide:
1. Scene type (action/dialogue/reaction/climax/internal)
2. Number of panels needed (1-4)
3. Characters present
4. Visual description for each panel
5. Dialogue lines
6. Camera shot (close-up/medium/wide/extreme-close-up)
7. Primary emotion/intensity

Return ONLY a valid JSON array with this structure:
[
  {{
    "id": 1,
    "type": "action",
    "panels": 2,
    "characters": ["Character1", "Character2"],
    "description": "Detailed visual description of what happens",
    "dialogue": ["Character1: Quote", "Character2: Quote"],
    "shot": "wide",
    "emotion": "shock"
  }}
]

Novel text:
{input_data.text}

Remember: Return ONLY the JSON array, no markdown formatting, no explanations."""

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON array found in response")
        
        json_str = content[json_start:json_end]
        scenes = json.loads(json_str)
        
        return {"scenes": scenes, "count": len(scenes)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate-prompts")
async def generate_image_prompts(request: ImagePromptRequest):
    """Generate detailed image prompts for a scene"""
    
    if not groq_client:
        raise HTTPException(
            status_code=400,
            detail="Groq API key required"
        )
    
    scene = request.scene
    
    try:
        prompt = f"""Create {scene.panels} detailed manga panel image generation prompts for this scene.

Scene Details:
- Type: {scene.type}
- Characters: {', '.join(scene.characters)}
- Description: {scene.description}
- Camera Shot: {scene.shot}
- Emotion: {scene.emotion}
- Dialogue: {', '.join(scene.dialogue)}

For EACH panel, create a detailed prompt that includes:
1. Manga art style specifications (black and white, ink, screen tones)
2. Specific character poses, expressions, and positions
3. Background elements and setting details
4. Visual effects (speed lines, impact effects, motion blur, etc.)
5. Camera angle and framing
6. Emotional atmosphere

Return ONLY a valid JSON array of strings:
["Detailed prompt for panel 1...", "Detailed prompt for panel 2...", ...]

Each prompt should be 100-200 words and extremely detailed for accurate image generation."""

        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=3000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        
        if json_start == -1:
            raise ValueError("No JSON found")
        
        json_str = content[json_start:json_end]
        prompts = json.loads(json_str)
        
        return {"prompts": prompts}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prompt generation failed: {str(e)}")

@app.post("/api/generate-image")
async def generate_image(request: ImageGenerationRequest):
    """Generate manga panel image using FAL.ai"""
    
    if not fal_api_key:
        raise HTTPException(
            status_code=400,
            detail="FAL.ai API key required. Sign up free at fal.ai"
        )
    
    try:
        # Enhance prompt for manga style
        full_prompt = f"""manga panel, black and white, ink drawing, professional manga art,
        high contrast, screen tones, detailed linework, {request.prompt}"""
        
        negative_prompt = """color, colored, photorealistic, 3d render, blurry,
        low quality, bad anatomy, western comic style, watermark"""
        
        # Call FAL.ai API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://fal.run/fal-ai/fast-sdxl",
                headers={
                    "Authorization": f"Key {fal_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": full_prompt,
                    "negative_prompt": negative_prompt,
                    "image_size": {
                        "width": request.width,
                        "height": request.height
                    },
                    "num_inference_steps": 25,
                    "guidance_scale": 7.5,
                    "num_images": 1
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Image generation failed: {response.text}"
                )
            
            result = response.json()
            image_url = result["images"][0]["url"]
            
            return {
                "image_url": image_url,
                "prompt_used": full_prompt
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "groq_configured": groq_client is not None,
        "fal_configured": fal_api_key is not None,
        "python_version": os.sys.version
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)