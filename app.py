import os
import re
import json
import time
import random
import tempfile
import requests
import numpy as np
import uuid
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import gradio as gr
from dotenv import load_dotenv
import moviepy.editor as mpy
from moviepy.editor import *
from moviepy.audio.fx.all import volumex
from moviepy.video.fx.all import crop

# Suppress the asyncio "Event loop is closed" warning on Windows
import sys
if sys.platform.startswith('win'):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from .env file if present
load_dotenv()

# Directory structure constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
MUSIC_DIR = os.path.join(STATIC_DIR, "music")
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# Create necessary directories
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(STORAGE_DIR, exist_ok=True)

# Helper functions for logging
def info(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] [INFO] {message}"
    print(formatted_message)
    return formatted_message

def success(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] [SUCCESS] {message}"
    print(formatted_message)
    return formatted_message

def warning(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] [WARNING] {message}"
    print(formatted_message)
    return formatted_message

def error(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] [ERROR] {message}"
    print(formatted_message)
    return formatted_message

def get_music_files():
    """Get list of available music files in the music directory."""
    if not os.path.exists(MUSIC_DIR):
        return ["none"]
    
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
    if not music_files:
        return ["none"]
    
    return ["random"] + music_files

def get_font_files():
    """Get list of available font files in the fonts directory."""
    if not os.path.exists(FONTS_DIR):
        return ["default"]
    
    font_files = [f.split('.')[0] for f in os.listdir(FONTS_DIR) if f.endswith(('.ttf', '.otf'))]
    if not font_files:
        return ["default"]
    
    return ["random"] + font_files

def choose_random_music():
    """Selects a random music file from the music directory."""
    if not os.path.exists(MUSIC_DIR):
        error(f"Music directory {MUSIC_DIR} does not exist")
        return None
    
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
    if not music_files:
        warning(f"No music files found in {MUSIC_DIR}")
        return None
    
    return os.path.join(MUSIC_DIR, random.choice(music_files))

def choose_random_font():
    """Selects a random font file from the fonts directory."""
    if not os.path.exists(FONTS_DIR):
        error(f"Fonts directory {FONTS_DIR} does not exist")
        return "default"
    
    font_files = [f for f in os.listdir(FONTS_DIR) if f.endswith(('.ttf', '.otf'))]
    if not font_files:
        warning(f"No font files found in {FONTS_DIR}")
        return None
    
    return font_files[0].split('.')[0] if len(font_files) == 1 else random.choice([f.split('.')[0] for f in font_files])

class YouTube:
    def __init__(self, niche: str, language: str, 
                 text_gen="g4f", text_model="gpt-4", 
                 image_gen="g4f", image_model="flux", 
                 tts_engine="edge", tts_voice="en-US-AriaNeural", 
                 subtitle_font="default", font_size=80,
                 text_color="white", highlight_color="blue",
                 subtitles_enabled=True, highlighting_enabled=True,
                 subtitle_position="bottom", music_file="random",
                 transition_type="none", transition_duration=0.5,
                 api_keys=None, progress=gr.Progress()) -> None:
        
        """Initialize the YouTube Shorts Generator."""
        self.progress = progress
        self.progress(0, desc="Initializing")
        
        # Store basic parameters
        info(f"Initializing YouTube class")
        self._niche = niche
        self._language = language
        self.text_gen = text_gen
        self.text_model = text_model
        self.image_gen = image_gen
        self.image_model = image_model
        self.tts_engine = tts_engine
        self.tts_voice = tts_voice
        self.subtitle_font = subtitle_font
        self.font_size = font_size
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.subtitles_enabled = subtitles_enabled
        self.highlighting_enabled = highlighting_enabled
        self.subtitle_position = subtitle_position
        self.music_file = music_file
        self.transition_type = transition_type
        self.transition_duration = transition_duration
        self.api_keys = api_keys or {}
        self.images = []
        self.logs = []
        
        # Set API keys from parameters or environment variables
        if 'gemini' in self.api_keys and self.api_keys['gemini']:
            os.environ["GEMINI_API_KEY"] = self.api_keys['gemini']
        
        if 'assemblyai' in self.api_keys and self.api_keys['assemblyai']:
            os.environ["ASSEMBLYAI_API_KEY"] = self.api_keys['assemblyai']
        
        if 'elevenlabs' in self.api_keys and self.api_keys['elevenlabs']:
            os.environ["ELEVENLABS_API_KEY"] = self.api_keys['elevenlabs']
        
        if 'segmind' in self.api_keys and self.api_keys['segmind']:
            os.environ["SEGMIND_API_KEY"] = self.api_keys['segmind']
        
        if 'openai' in self.api_keys and self.api_keys['openai']:
            os.environ["OPENAI_API_KEY"] = self.api_keys['openai']
            
        info(f"Niche: {niche}, Language: {language}")
        self.log(f"Initialized with niche: {niche}, language: {language}")
        self.log(f"Text generator: {text_gen} - Model: {text_model}")
        self.log(f"Image generator: {image_gen} - Model: {image_model}")
        self.log(f"TTS engine: {tts_engine} - Voice: {tts_voice}")
        self.log(f"Subtitles: {'Enabled' if subtitles_enabled else 'Disabled'} - Highlighting: {'Enabled' if highlighting_enabled else 'Disabled'}")
        self.log(f"Music: {music_file}")
    
    def log(self, message):
        """Add a log message to the logs list."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        return log_entry
    
    @property
    def niche(self) -> str:
        return self._niche
    
    @property
    def language(self) -> str:
        return self._language
    
    def generate_response(self, prompt: str, model: str = None) -> str:
        """Generate a response using the selected text generation model."""
        self.log(f"Generating response for prompt: {prompt[:50]}...")
        
        try:
            if self.text_gen == "gemini":
                self.log("Using Google's Gemini model")
                
                # Check if API key is set
                gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
                if not gemini_api_key:
                    raise ValueError("Gemini API key is not set. Please provide a valid API key.")
                
                import google.generativeai as genai
                genai.configure(api_key=gemini_api_key)
                model_to_use = model if model else self.text_model
                genai_model = genai.GenerativeModel(model_to_use)
                response = genai_model.generate_content(prompt).text
                
            elif self.text_gen == "g4f":
                self.log("Using G4F for text generation")
                import g4f
                model_to_use = model if model else self.text_model
                self.log(f"Using G4F model: {model_to_use}")
                response = g4f.ChatCompletion.create(
                    model=model_to_use,
                    messages=[{"role": "user", "content": prompt}]
                )
                
            elif self.text_gen == "openai":
                self.log("Using OpenAI for text generation")
                openai_api_key = os.environ.get("OPENAI_API_KEY", "")
                if not openai_api_key:
                    raise ValueError("OpenAI API key is not set. Please provide a valid API key.")
                
                from openai import OpenAI
                client = OpenAI(api_key=openai_api_key)
                model_to_use = model if model else "gpt-3.5-turbo"
                
                response = client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": "user", "content": prompt}]
                ).choices[0].message.content
                
            else:
                # No fallback, raise an exception for unsupported text generator
                error_msg = f"Unsupported text generator: {self.text_gen}"
                self.log(error(error_msg))
                raise ValueError(error_msg)
                
            self.log(f"Response generated successfully, length: {len(response)} characters")
            return response
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            self.log(error(error_msg))
            raise Exception(error_msg)

    def generate_topic(self) -> str:
        """Generate a topic based on the YouTube Channel niche."""
        self.progress(0.05, desc="Generating topic")
        self.log("Generating topic based on niche")
        
        completion = self.generate_response(
            f"Please generate a specific video idea that takes about the following topic: {self.niche}. "
            f"Make it exactly one sentence. Only return the topic, nothing else."
        )

        if not completion:
            self.log(error("Failed to generate Topic."))
            raise Exception("Failed to generate a topic. Please try again with a different niche.")

        self.subject = completion
        self.log(success(f"Generated topic: {completion}"))
        return completion

    def generate_script(self) -> str:
        """Generate a script for a video, based on the subject and language."""
        self.progress(0.1, desc="Creating script")
        self.log("Generating script for video")
        
        prompt = f"""
        Generate a script for youtube shorts video, depending on the subject of the video.

        The script is to be returned as a string with the specified number of paragraphs.

        Here is an example of a string:
        "This is an example string."

        Do not under any circumstance reference this prompt in your response.

        Get straight to the point, don't start with unnecessary things like, "welcome to this video".

        Obviously, the script should be related to the subject of the video.
        
        YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
        YOU MUST WRITE THE SCRIPT IN THE LANGUAGE SPECIFIED IN [LANGUAGE].
        ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS.
        
        Subject: {self.subject}
        Language: {self.language}
        """
        completion = self.generate_response(prompt)

        # Apply regex to remove *
        completion = re.sub(r"\*", "", completion)
        
        if not completion:
            self.log(error("The generated script is empty."))
            raise Exception("Failed to generate a script. Please try again.")
        
        if len(completion) > 5000:
            self.log(warning("Generated script is too long."))
            raise ValueError("Generated script exceeds 5000 characters. Please try again.")
        
        self.script = completion
        self.log(success(f"Generated script ({len(completion)} chars)"))
        return completion

    def generate_metadata(self) -> dict:
        """Generate video metadata (title, description)."""
        self.progress(0.15, desc="Creating title and description")
        self.log("Generating metadata (title and description)")
        
        title = self.generate_response(
            f"Please generate a YouTube Video Title for the following subject, including hashtags: "
            f"{self.subject}. Only return the title, nothing else. Limit the title under 100 characters."
        )

        if len(title) > 100:
            self.log(warning("Generated title exceeds 100 characters."))
            raise ValueError("Generated title exceeds 100 characters. Please try again.")

        description = self.generate_response(
            f"Please generate a YouTube Video Description for the following script: {self.script}. "
            f"Only return the description, nothing else."
        )
        
        self.metadata = {
            "title": title,
            "description": description
        }
        
        self.log(success(f"Generated title: {title}"))
        self.log(success(f"Generated description: {description[:50]}..."))
        return self.metadata
    
    def generate_prompts(self, count=5) -> list:
        """Generate AI Image Prompts based on the provided Video Script."""
        self.progress(0.2, desc="Creating image prompts")
        self.log(f"Generating {count} image prompts")
        
        prompt = f"""
        Generate {count} Image Prompts for AI Image Generation,
        depending on the subject of a video.
        Subject: {self.subject}

        The image prompts are to be returned as
        a JSON-Array of strings.

        Each search term should consist of a full sentence,
        always add the main subject of the video.

        Be emotional and use interesting adjectives to make the
        Image Prompt as detailed as possible.
        
        YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
        YOU MUST NOT RETURN ANYTHING ELSE. 
        YOU MUST NOT RETURN THE SCRIPT.
        
        The search terms must be related to the subject of the video.
        Here is an example of a JSON-Array of strings:
        ["image prompt 1", "image prompt 2", "image prompt 3"]

        For context, here is the full text:
        {self.script}
        """

        completion = str(self.generate_response(prompt))\
            .replace("```json", "") \
            .replace("```", "")

        image_prompts = []

        if "image_prompts" in completion:
            try:
                image_prompts = json.loads(completion)["image_prompts"]
            except:
                self.log(warning("Failed to parse 'image_prompts' from JSON response."))
                
        if not image_prompts:
            try:
                image_prompts = json.loads(completion)
                self.log(f"Parsed image prompts from JSON response.")
            except Exception:
                self.log(warning("JSON parsing failed. Attempting to extract array using regex..."))

                # Get everything between [ and ], and turn it into a list
                r = re.compile(r"\[.*\]", re.DOTALL)
                matches = r.findall(completion)
                if len(matches) == 0:
                    self.log(warning("Failed to extract array. Unable to create image prompts."))
                    raise ValueError("Failed to generate valid image prompts. Please try again.")
                else:
                    try:
                        image_prompts = json.loads(matches[0])
                    except:
                        self.log(error("Failed to parse array from regex match."))
                        # Use regex to extract individual strings
                        string_pattern = r'"([^"]*)"'
                        strings = re.findall(string_pattern, matches[0])
                        if strings:
                            image_prompts = strings
                        else:
                            self.log(error("Failed to extract strings from regex match."))
                            raise ValueError("Failed to parse image prompts. Please try again.")

        # Ensure we have the requested number of prompts
        if len(image_prompts) < count:
            self.log(warning(f"Received fewer prompts ({len(image_prompts)}) than requested ({count})."))
            raise ValueError(f"Received only {len(image_prompts)} prompts instead of {count}. Please try again.")
            
        # Limit to the requested count
        image_prompts = image_prompts[:count]
        
        self.image_prompts = image_prompts
        self.log(success(f"Generated {len(self.image_prompts)} Image Prompts"))
        for i, prompt in enumerate(self.image_prompts):
            self.log(f"Image Prompt {i+1}: {prompt}")
            
        return image_prompts

    def generate_image(self, prompt) -> str:
        """Generate an image using the selected image generation model."""
        self.log(f"Generating image for prompt: {prompt[:50]}...")
        
        # Always save images directly to the generation folder when it exists
        if hasattr(self, 'generation_folder') and os.path.exists(self.generation_folder):
            image_path = os.path.join(self.generation_folder, f"img_{uuid.uuid4()}_{int(time.time())}.png")
        else:
            # Use STORAGE_DIR if no generation folder
            image_path = os.path.join(STORAGE_DIR, f"img_{uuid.uuid4()}_{int(time.time())}.png")
        
        if self.image_gen == "prodia":
            self.log("Using Prodia provider for image generation")
            s = requests.Session()
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            # Generate job
            self.log("Sending generation request to Prodia API")
            resp = s.get(
                "https://api.prodia.com/generate",
                params={
                    "new": "true",
                    "prompt": prompt,
                    "model": self.image_model,
                    "negative_prompt": "verybadimagenegative_v1.3",
                    "steps": "20",
                    "cfg": "7",
                    "seed": random.randint(1, 10000),
                    "sample": "DPM++ 2M Karras",
                    "aspect_ratio": "square"
                },
                headers=headers
            )
            
            if resp.status_code != 200:
                raise Exception(f"Prodia API error: {resp.text}")
            
            job_id = resp.json()['job']
            self.log(f"Job created with ID: {job_id}")
            
            # Wait for generation to complete
            max_attempts = 30
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                time.sleep(2)
                status = s.get(f"https://api.prodia.com/job/{job_id}", headers=headers).json()
                
                if status["status"] == "succeeded":
                    self.log("Image generation successful, downloading result")
                    img_data = s.get(f"https://images.prodia.xyz/{job_id}.png?download=1", headers=headers).content
                    with open(image_path, "wb") as f:
                        f.write(img_data)
                    self.images.append(image_path)
                    self.log(success(f"Image saved to: {image_path}"))
                    return image_path
                
                elif status["status"] == "failed":
                    raise Exception(f"Prodia job failed: {status.get('error', 'Unknown error')}")
                
                # Still processing
                self.log(f"Still processing, attempt {attempts}/{max_attempts}...")
            
            raise Exception("Prodia job timed out")
        
        elif self.image_gen == "hercai":
            self.log("Using Hercai provider for image generation")
            url = f"https://hercai.onrender.com/{self.image_model}/text2image?prompt={prompt}"
            r = requests.get(url)
            
            if r.status_code != 200:
                raise Exception(f"Hercai API error: {r.text}")
            
            parsed = r.json()
            if "url" in parsed and parsed["url"]:
                self.log("Image URL received from Hercai")
                image_url = parsed["url"]
                img_data = requests.get(image_url).content
                with open(image_path, "wb") as f:
                    f.write(img_data)
                self.images.append(image_path)
                self.log(success(f"Image saved to: {image_path}"))
                return image_path
            else:
                raise Exception("No image URL in Hercai response")
        
        elif self.image_gen == "g4f":
            self.log("Using G4F provider for image generation")
            from g4f.client import Client
            client = Client()
            response = client.images.generate(
                model=self.image_model,
                prompt=prompt,
                response_format="url"
            )
            
            if response and response.data and len(response.data) > 0:
                image_url = response.data[0].url
                image_response = requests.get(image_url)
                
                if image_response.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(image_response.content)
                    self.images.append(image_path)
                    self.log(success(f"Image saved to: {image_path}"))
                    return image_path
                else:
                    raise Exception(f"Failed to download image from {image_url}")
            else:
                raise Exception("No image URL received from G4F")
        
        elif self.image_gen == "segmind":
            self.log("Using Segmind provider for image generation")
            api_key = os.environ.get("SEGMIND_API_KEY", "")
            if not api_key:
                raise ValueError("Segmind API key is not set. Please provide a valid API key.")
            
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.segmind.com/v1/sdxl-turbo",
                json={
                    "prompt": prompt,
                    "negative_prompt": "blurry, low quality, distorted face, text, watermark",
                    "samples": 1,
                    "size": "1024x1024",
                    "guidance_scale": 1.0
                },
                headers=headers
            )
            
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(response.content)
                self.images.append(image_path)
                self.log(success(f"Image saved to: {image_path}"))
                return image_path
            else:
                raise Exception(f"Segmind request failed: {response.status_code} {response.text}")
        
        elif self.image_gen == "pollinations":
            self.log("Using Pollinations provider for image generation")
            response = requests.get(f"https://image.pollinations.ai/prompt/{prompt}{random.randint(1,10000)}")
            
            if response.status_code == 200:
                self.log("Image received from Pollinations")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                self.images.append(image_path)
                self.log(success(f"Image saved to: {image_path}"))
                return image_path
            else:
                raise Exception(f"Pollinations request failed with status code: {response.status_code}")
        
        else:
            # No fallback, raise an exception for unsupported image generator
            error_msg = f"Unsupported image generator: {self.image_gen}"
            self.log(error(error_msg))
            raise ValueError(error_msg)

    def generate_speech(self, text, output_format='mp3') -> str:
        """Generate speech from text using the selected TTS engine."""
        self.progress(0.6, desc="Creating voiceover")
        self.log("Generating speech from text")
        
        # Clean text
        text = re.sub(r'[^\w\s.?!,;:\'"-]', '', text)
        
        self.log(f"Using TTS Engine: {self.tts_engine}, Voice: {self.tts_voice}")
        
        # Always save to the generation folder when available
        if hasattr(self, 'generation_folder') and os.path.exists(self.generation_folder):
            audio_path = os.path.join(self.generation_folder, f"speech_{uuid.uuid4()}_{int(time.time())}.{output_format}")
        else:
            # Use STORAGE_DIR if no generation folder
            audio_path = os.path.join(STORAGE_DIR, f"speech_{uuid.uuid4()}_{int(time.time())}.{output_format}")
        
        if self.tts_engine == "elevenlabs":
            self.log("Using ElevenLabs provider for speech generation")
            elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY", "")
            if not elevenlabs_api_key:
                raise ValueError("ElevenLabs API key is not set. Please provide a valid API key.")
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": elevenlabs_api_key
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_turbo_v2",  # Using latest and most capable model
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                },
                "output_format": "mp3_44100_128",  # Higher quality audio (44.1kHz, 128kbps)
                "optimize_streaming_latency": 0    # Optimize for quality over latency
            }
            
            # Map voice names to ElevenLabs voice IDs
            voice_id_mapping = {
                "Sarah": "21m00Tcm4TlvDq8ikWAM",
                "Brian": "hxppwzoRmvxK7YkDrjhQ",
                "Lily": "p7TAj7L6QVq1fE6XGyjR",
                "Monika Sogam": "Fc3XhIu9tfgOPOsU1hMr", 
                "George": "o7lPjDgzlF8ZAeSpqmaN",
                "River": "f0k5evLkhJxrIRJXQJvy",
                "Matilda": "XrExE9yKIg1WjnnlVkGX",
                "Will": "pvKWM1B1sNRNTlEYYAEZ",
                "Jessica": "A5EAMYWMCSsLNL1wYxOv",
                "default": "21m00Tcm4TlvDq8ikWAM"  # Default to Sarah
            }
            
            # Get the voice ID from mapping or use the voice name as ID if not found
            voice_id = voice_id_mapping.get(self.tts_voice, self.tts_voice)
            
            self.log(f"Using ElevenLabs voice: {self.tts_voice} (ID: {voice_id})")
            
            response = requests.post(
                url=f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                self.log(success(f"Speech generated successfully using ElevenLabs at {audio_path}"))
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('detail', {}).get('message', response.text)
                    error_status = error_data.get('status', 'error')
                    raise Exception(f"ElevenLabs API error ({response.status_code}, {error_status}): {error_message}")
                except ValueError:
                    # If JSON parsing fails, use the raw response
                    raise Exception(f"ElevenLabs API error ({response.status_code}): {response.text}")
            
        elif self.tts_engine == "gtts":
            self.log("Using Google TTS provider for speech generation")
            from gtts import gTTS
            tts = gTTS(text=text, lang=self.language[:2].lower(), slow=False)
            tts.save(audio_path)
            
        elif self.tts_engine == "openai":
            self.log("Using OpenAI provider for speech generation")
            openai_api_key = os.environ.get("OPENAI_API_KEY", "")
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set. Please provide a valid API key.")
            
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            
            voice = self.tts_voice if self.tts_voice else "alloy"
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            response.stream_to_file(audio_path)
            
        elif self.tts_engine == "edge":
            self.log("Using Edge TTS provider for speech generation")
            import edge_tts
            import asyncio
            
            voice = self.tts_voice if self.tts_voice else "en-US-AriaNeural"
            
            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(audio_path)
            
            asyncio.run(generate())
        
        else:
            # No fallback, raise an exception for unsupported TTS engine
            error_msg = f"Unsupported TTS engine: {self.tts_engine}"
            self.log(error(error_msg))
            raise ValueError(error_msg)
        
        self.log(success(f"Speech generated and saved to: {audio_path}"))
        self.tts_path = audio_path
        return audio_path

    def generate_subtitles(self, audio_path: str) -> dict:
        """Generate subtitles from audio using AssemblyAI."""
        self.log("Generating subtitles from audio")
        try:
            import assemblyai as aai
            
            # Check if API key is set
            aai_api_key = os.environ.get("ASSEMBLYAI_API_KEY", "")
            if not aai_api_key:
                raise ValueError("AssemblyAI API key is not set. Please provide a valid API key.")
            
            aai.settings.api_key = aai_api_key
            
            config = aai.TranscriptionConfig(speaker_labels=False, word_boost=[], format_text=True)
            transcriber = aai.Transcriber(config=config)
            
            self.log("Submitting audio for transcription")
            transcript = transcriber.transcribe(audio_path)
            
            if not transcript or not transcript.words:
                raise ValueError("Transcription returned no words.")
                
            # Process word-level information
            wordlevel_info = []
            for word in transcript.words:
                word_data = {
                    "word": word.text.strip(),
                    "start": word.start / 1000.0,  # Convert from ms to seconds
                    "end": word.end / 1000.0       # Convert from ms to seconds
                }
                wordlevel_info.append(word_data)
            
            self.log(success(f"Transcription successful. Got {len(wordlevel_info)} words."))
            
            # Define constants for subtitle generation
            # Handle random font selection if configured
            if self.subtitle_font == "random":
                FONT = choose_random_font()
                self.log(f"Using random font: {FONT}")
            else:
                FONT = self.subtitle_font
            
            FONTSIZE = self.font_size
            COLOR = self.text_color
            BG_COLOR = self.highlight_color if self.highlighting_enabled else None
            FRAME_SIZE = (1080, 1920)  # Vertical video format
            
            # Constants for line splitting
            MAX_CHARS = 30  # Maximum characters per line for vertical video format
            MAX_DURATION = 3.0  # Maximum duration for a single line
            MAX_GAP = 1.5  # Split if nothing is spoken for this many seconds
            
            # Split text into lines
            subtitles = []
            line = []
            line_duration = 0

            for idx, word_data in enumerate(wordlevel_info):
                word = word_data["word"]
                start = word_data["start"]
                end = word_data["end"]
                
                line.append(word_data)
                line_duration += end - start
                
                temp = " ".join(item["word"] for item in line)
                new_line_chars = len(temp)
                
                duration_exceeded = line_duration > MAX_DURATION
                chars_exceeded = new_line_chars > MAX_CHARS
                
                if idx > 0:
                    gap = word_data['start'] - wordlevel_info[idx-1]['end'] 
                    maxgap_exceeded = gap > MAX_GAP
                else:
                    maxgap_exceeded = False

                if duration_exceeded or chars_exceeded or maxgap_exceeded:
                    if line:
                        subtitle_line = {
                            "text": " ".join(item["word"] for item in line),
                            "start": line[0]["start"],
                            "end": line[-1]["end"],
                            "words": line
                        }
                        subtitles.append(subtitle_line)
                        line = []
                        line_duration = 0

            # Add remaining words as last line
            if line:
                subtitle_line = {
                    "text": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "words": line
                }
                subtitles.append(subtitle_line)
            
            self.log(success(f"Generated {len(subtitles)} subtitle lines"))
            
            # Pre-wrap subtitle lines for more efficient rendering
            self.log("Pre-calculating subtitle line wrapping...")
            wrapped_subtitles = self._pre_wrap_subtitle_lines(subtitles, FRAME_SIZE, FONT, FONTSIZE)
            self.log(success(f"Pre-wrapped {len(wrapped_subtitles)} subtitle lines"))
            
            # Return the subtitle data and settings
            return {
                "wordlevel": wordlevel_info,
                "linelevel": subtitles,
                "wrappedlines": wrapped_subtitles,
                "settings": {
                    "font": FONT,
                    "fontsize": FONTSIZE,
                    "color": COLOR,
                    "bg_color": BG_COLOR,
                    "position": self.subtitle_position,
                    "highlighting_enabled": self.highlighting_enabled,
                    "subtitles_enabled": self.subtitles_enabled
                }
            }
            
        except Exception as e:
            error_msg = f"Error generating subtitles: {str(e)}"
            self.log(error(error_msg))
            raise Exception(error_msg)
    
    def _pre_wrap_subtitle_lines(self, subtitles, frame_size, font_name, font_size):
        """Pre-calculate line wrapping for subtitles based on video dimensions."""
        self.log("Pre-calculating subtitle line wrapping")
        
        # Load the font once
        try:
            font_path = os.path.join(FONTS_DIR, f"{font_name}.ttf")
            if os.path.exists(font_path):
                pil_font = ImageFont.truetype(font_path, font_size)
            else:
                self.log(warning(f"Font {font_name} not found, using default"))
                pil_font = ImageFont.load_default()
        except Exception as e:
            self.log(warning(f"Error loading font: {str(e)}"))
            pil_font = ImageFont.load_default()
        
        # Calculate max width for text (80% of frame width)
        max_width = frame_size[0] * 0.8
        x_buffer = frame_size[0] * 0.1  # 10% buffer on each side
        space_width = 20  # Approximate space width
        
        wrapped_subtitles = []
        
        for line in subtitles:
            # Process the line into visual lines with exact positions
            visual_lines = []
            current_line = []
            current_x = 0
            line_number = 0
            
            # Break points for natural text wrapping
            break_points = {'.', ',', '!', '?', ';', ':', '-', '—'}
            
            for word_data in line["words"]:
                word = word_data["word"]
                # Get word width including space
                try:
                    word_width = pil_font.getbbox(word)[2] + space_width
                except:
                    # Fallback if getbbox fails
                    word_width = len(word) * (font_size // 2) + space_width
                
                # Check if word contains a break point
                has_break = any(char in break_points for char in word)
                
                # If this word would overflow or has a break point, start a new visual line
                if (current_x + word_width > max_width and current_line) or (has_break and current_line and current_x > max_width * 0.7):
                    # Store this completed visual line
                    visual_line_text = " ".join(w["word"] for w in current_line)
                    visual_lines.append({
                        "line_number": line_number,
                        "text": visual_line_text,
                        "words": current_line.copy()
                    })
                    current_line = []
                    current_x = 0
                    line_number += 1
                
                # Add word position information
                positioned_word = word_data.copy()
                positioned_word["x_offset"] = current_x
                positioned_word["y_line"] = line_number
                positioned_word["width"] = word_width
                
                current_line.append(positioned_word)
                current_x += word_width
            
            # Add the last line if it exists
            if current_line:
                visual_line_text = " ".join(w["word"] for w in current_line)
                visual_lines.append({
                    "line_number": line_number,
                    "text": visual_line_text,
                    "words": current_line
                })
            
            # Return the wrapped line with visual formatting
            wrapped_subtitles.append({
                "original_text": line["text"],
                "start": line["start"],
                "end": line["end"],
                "visual_lines": visual_lines
            })
        
        return wrapped_subtitles

    def create_subtitle_clip(self, subtitle_data, frame_size):
        """Create subtitle clips for a line of text with word-level highlighting."""
        # Early return if subtitles are disabled
        if not self.subtitles_enabled:
            return []
            
        settings = subtitle_data["settings"]
        font_name = settings["font"]
        fontsize = settings["fontsize"]
        color = settings["color"]
        bg_color = settings["bg_color"]
        highlighting_enabled = settings["highlighting_enabled"]
        
        # Pre-calculate text and background colors once
        if color.startswith('#'):
            text_color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        else:
            text_color_rgb = (255, 255, 255)  # Default white
            
        if bg_color and bg_color.startswith('#'):
            bg_color_rgb = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        else:
            bg_color_rgb = (0, 0, 255)  # Default blue
        
        # Load font only once
        try:
            font_path = os.path.join(FONTS_DIR, f"{font_name}.ttf")
            if os.path.exists(font_path):
                pil_font = ImageFont.truetype(font_path, fontsize)
            else:
                self.log(warning(f"Font {font_name} not found, using default"))
                pil_font = ImageFont.load_default()
        except Exception as e:
            self.log(warning(f"Error loading font: {str(e)}"))
            pil_font = ImageFont.load_default()
            
        # Pre-calculate common values
        padding = 10
        subtitle_clips = []
        
        # Check if we have pre-wrapped lines (faster method)
        if "wrappedlines" in subtitle_data and subtitle_data["wrappedlines"]:
            self.log("Using pre-wrapped subtitle lines for faster rendering")
            wrapped_subtitles = subtitle_data["wrappedlines"]
            
            # Calculate vertical position offset based on subtitle position setting
            if settings["position"] == "top":
                y_buffer = frame_size[1] * 0.1  # 10% from top
            elif settings["position"] == "middle":
                y_buffer = frame_size[1] * 0.4  # 40% from top
            else:  # bottom
                y_buffer = frame_size[1] * 0.7  # 70% from top
            
            # Create optimized text clip function that reuses font and color calculations
            def create_text_clip(text, bg_color=None):
                try:
                    # Get text size
                    text_width, text_height = pil_font.getbbox(text)[2:4]
                    
                    # Add padding
                    img_width = text_width + padding * 2
                    img_height = text_height + padding * 2
                    
                    # Create image with background color or transparent
                    if bg_color:
                        img = Image.new('RGB', (img_width, img_height), color=bg_color_rgb)
                    else:
                        img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
                    
                    # Draw text
                    draw = ImageDraw.Draw(img)
                    draw.text((padding, padding), text, font=pil_font, fill=text_color_rgb)
                    
                    # Convert to numpy array for MoviePy
                    img_array = np.array(img)
                    clip = ImageClip(img_array)
                    return clip, img_width, img_height
                
                except Exception as e:
                    self.log(warning(f"Error creating text clip: {str(e)}"))
                    # Create a simple colored rectangle as fallback
                    img = Image.new('RGB', (100, 50), color=(100, 100, 100))
                    img_array = np.array(img)
                    clip = ImageClip(img_array)
                    return clip, 100, 50
            
            # Process each pre-wrapped line
            for wrapped_line in wrapped_subtitles:
                line_start = wrapped_line["start"]
                line_end = wrapped_line["end"]
                line_duration = line_end - line_start
                
                # Process each visual line separately
                for visual_line in wrapped_line["visual_lines"]:
                    line_number = visual_line["line_number"]
                    line_text = visual_line["text"]
                    
                    # Calculate vertical position including line number offset
                    line_y = y_buffer + (line_number * (fontsize + 20))
                    
                    # Create the line clip
                    line_clip, line_width, _ = create_text_clip(line_text)
                    line_clip = line_clip.set_position(('center', line_y))
                    line_clip = line_clip.set_start(line_start).set_duration(line_duration)
                    subtitle_clips.append(line_clip)
                    
                    # Add word highlights if enabled
                    if highlighting_enabled and bg_color:
                        # Calculate center offset for word positioning
                        center_offset = (frame_size[0] - line_width) / 2
                        
                        for word_data in visual_line["words"]:
                            word = word_data["word"]
                            word_start = word_data["start"]
                            word_end = word_data["end"]
                            x_offset = word_data["x_offset"]
                            
                            # Create highlight clip
                            highlight_clip, _, _ = create_text_clip(word, bg_color)
                            highlight_clip = highlight_clip.set_position((center_offset + x_offset, line_y))
                            highlight_clip = highlight_clip.set_start(word_start).set_duration(word_end - word_start)
                            subtitle_clips.append(highlight_clip)
            
            return subtitle_clips
            
        # Fallback to old method if pre-wrapped lines aren't available
        else:
            self.log("Using standard subtitle rendering method")
            
            # Legacy code for compatibility (should not normally be used)
            # (existing code from current create_subtitle_clip method)
            space_width = 20
            
            # Process each line
            for line in subtitle_data["linelevel"]:
                # Calculate vertical position once per line
                if settings["position"] == "top":
                    y_buffer = frame_size[1] * 0.1  # 10% from top
                elif settings["position"] == "middle":
                    y_buffer = frame_size[1] * 0.4  # 40% from top
                else:  # bottom
                    y_buffer = frame_size[1] * 0.7  # 70% from top
                
                x_buffer = frame_size[0] * 0.1  # 10% from left
                
                # Process line in batches where possible
                x_pos = 0
                y_pos = 0
                word_positions = []
                line_duration = line["end"] - line["start"]
                
                # Pre-calculate word metrics to avoid redundant calculations
                word_metrics = []
                for word_data in line["words"]:
                    word = word_data["word"]
                    # Get word width including space
                    try:
                        word_width = pil_font.getbbox(word)[2] + space_width
                    except:
                        # Fallback if getbbox fails
                        word_width = len(word) * (fontsize // 2) + space_width
                    
                    word_metrics.append({
                        "word": word,
                        "width": word_width,
                        "height": fontsize,
                        "start": word_data["start"],
                        "end": word_data["end"]
                    })
                
                # Create optimized text clip function
                def create_text_clip(text, bg_color=None):
                    try:
                        # Get text size
                        text_width, text_height = pil_font.getbbox(text)[2:4]
                        
                        # Add padding
                        img_width = text_width + padding * 2
                        img_height = text_height + padding * 2
                        
                        # Create image with background color or transparent
                        if bg_color:
                            img = Image.new('RGB', (img_width, img_height), color=bg_color_rgb)
                        else:
                            img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
                        
                        # Draw text
                        draw = ImageDraw.Draw(img)
                        draw.text((padding, padding), text, font=pil_font, fill=text_color_rgb)
                        
                        # Convert to numpy array for MoviePy
                        img_array = np.array(img)
                        clip = ImageClip(img_array)
                        return clip, img_width, img_height
                    
                    except Exception as e:
                        self.log(warning(f"Error creating text clip: {str(e)}"))
                        # Create a simple colored rectangle as fallback
                        img = Image.new('RGB', (100, 50), color=(100, 100, 100))
                        img_array = np.array(img)
                        clip = ImageClip(img_array)
                        return clip, 100, 50
                
                # First, create and position all the regular words at once
                for i, metric in enumerate(word_metrics):
                    word = metric["word"]
                    word_width = metric["width"]
                    word_height = metric["height"]
                    
                    # Check if word fits on current line
                    if x_pos + word_width > frame_size[0] - 2 * x_buffer:
                        x_pos = 0
                        y_pos += word_height + 20
                    
                    # Store position info for highlighting
                    word_positions.append({
                        "word": word,
                        "x_pos": x_pos + x_buffer,
                        "y_pos": y_pos + y_buffer,
                        "width": word_width,
                        "height": word_height,
                        "start": metric["start"],
                        "end": metric["end"]
                    })
                    
                    # Create the word clip
                    word_clip, _, _ = create_text_clip(word)
                    word_clip = word_clip.set_position((x_pos + x_buffer, y_pos + y_buffer))
                    word_clip = word_clip.set_start(line["start"]).set_duration(line_duration)
                    subtitle_clips.append(word_clip)
                    
                    # Add space after word (except for last word)
                    if i < len(word_metrics) - 1:
                        space_clip, _, _ = create_text_clip(" ")
                        space_clip = space_clip.set_position((x_pos + word_width + x_buffer - space_width, y_pos + y_buffer))
                        space_clip = space_clip.set_start(line["start"]).set_duration(line_duration)
                        subtitle_clips.append(space_clip)
                    
                    x_pos += word_width
                
                # Only add highlighted words if highlighting is enabled
                if highlighting_enabled and bg_color:
                    for word_pos in word_positions:
                        highlight_clip, _, _ = create_text_clip(word_pos["word"], bg_color)
                        highlight_clip = highlight_clip.set_position((word_pos["x_pos"], word_pos["y_pos"]))
                        highlight_clip = highlight_clip.set_start(word_pos["start"]).set_duration(word_pos["end"] - word_pos["start"])
                        subtitle_clips.append(highlight_clip)
            
            return subtitle_clips

    def combine(self) -> str:
        """Combine images, audio, and subtitles into a final video."""
        self.progress(0.8, desc="Creating final video")
        self.log("Combining images and audio into final video")
        try:
            # Always save to the generation folder when available
            if hasattr(self, 'generation_folder') and os.path.exists(self.generation_folder):
                output_path = os.path.join(self.generation_folder, f"output_{int(time.time())}.mp4")
            else:
                output_path = os.path.join(STORAGE_DIR, f"output_{int(time.time())}.mp4")
            
            # Check for required files
            if not self.images:
                raise ValueError("No images available for video creation")
            
            if not hasattr(self, 'tts_path') or not self.tts_path or not os.path.exists(self.tts_path):
                raise ValueError("No TTS audio file available")
            
            # Load audio
            tts_clip = AudioFileClip(self.tts_path)
            max_duration = tts_clip.duration
            
            # Calculate duration for each image
            num_images = len(self.images)
            req_dur = max_duration / num_images
            
            # Create video clips from images more efficiently
            self.log("Processing images for video")
            clips = []
            tot_dur = 0
            
            # Pre-compute standard size and aspect ratio
            target_size = (1080, 1920)
            aspect_ratio = 9/16
            
            # Process all images at once
            for image_path in self.images:
                # Check if image exists and is valid
                if not os.path.exists(image_path):
                    self.log(warning(f"Image not found: {image_path}, skipping"))
                    continue
                
                # Calculate remaining duration
                duration = min(req_dur, max_duration - tot_dur)
                if duration <= 0:
                    break
                    
                try:
                    clip = ImageClip(image_path)
                    clip = clip.set_duration(duration)
                    clip = clip.set_fps(30)
                    
                    # Handle aspect ratio (vertical video for shorts)
                    if clip.w / clip.h < aspect_ratio:
                        # Image is too tall, crop height
                        clip = crop(
                            clip, 
                            width=clip.w, 
                            height=round(clip.w / aspect_ratio), 
                            x_center=clip.w / 2, 
                            y_center=clip.h / 2
                        )
                    else:
                        # Image is too wide, crop width
                        clip = crop(
                            clip, 
                            width=round(aspect_ratio * clip.h), 
                            height=clip.h, 
                            x_center=clip.w / 2, 
                            y_center=clip.h / 2
                        )
                    
                    # Resize to standard size for shorts
                    clip = clip.resize(target_size)
                    clips.append(clip)
                    tot_dur += duration
                    
                    # If we've exceeded the duration, break
                    if tot_dur >= max_duration:
                        break
                except Exception as e:
                    self.log(warning(f"Error processing image {image_path}: {str(e)}"))
            
            # Create video from clips
            self.log(f"Creating video from {len(clips)} clips")
            if self.transition_type == "crossfade" and self.transition_duration > 0:
                final_clip = concatenate_videoclips(
                    clips,
                    method="compose",
                    padding=-self.transition_duration
                )
            else:
                final_clip = concatenate_videoclips(clips)
            final_clip = final_clip.set_fps(30)
            
            # Add subtitles if enabled - skip entirely if disabled
            subtitle_clips = []
            if self.subtitles_enabled and hasattr(self, 'subtitle_data'):
                self.log("Generating subtitle clips")
                subtitle_clips = self.create_subtitle_clip(self.subtitle_data, target_size)
                if subtitle_clips:
                    final_clip = CompositeVideoClip([final_clip] + subtitle_clips)
            
            # Add background music if available
            music_path = None
            if self.music_file == "random":
                music_path = choose_random_music()
            elif self.music_file != "none" and os.path.exists(os.path.join(MUSIC_DIR, self.music_file)):
                music_path = os.path.join(MUSIC_DIR, self.music_file)
                
            if music_path and os.path.exists(music_path):
                self.log(f"Adding background music: {music_path}")
                try:
                    music_clip = AudioFileClip(music_path)
                    # Loop music if it's shorter than the video
                    if music_clip.duration < max_duration:
                        num_loops = int(np.ceil(max_duration / music_clip.duration))
                        music_clip = concatenate_audioclips([music_clip] * num_loops)
                    # Trim music if it's longer than the video
                    music_clip = music_clip.subclip(0, max_duration)
                    # Reduce music volume
                    music_clip = music_clip.volumex(0.1)
                    # Combine with TTS audio
                    final_audio = CompositeAudioClip([tts_clip, music_clip])
                except Exception as e:
                    self.log(warning(f"Error processing music: {str(e)}"))
                    final_audio = tts_clip
            else:
                final_audio = tts_clip
            
            # Set final audio
            final_clip = final_clip.set_audio(final_audio)
            
            # Write final video - use faster preset
            self.log("Writing final video file")
            final_clip.write_videofile(
                output_path,
                fps=30,
                codec="libx264",
                audio_codec="aac",
                threads=4,
                preset="ultrafast"  # Changed from "medium" to "ultrafast" for faster rendering
            )
            
            self.log(success(f"Video saved to: {output_path}"))
            return output_path
            
        except Exception as e:
            error_msg = f"Error combining video: {str(e)}"
            self.log(error(error_msg))
            raise Exception(error_msg)

    def generate_video(self) -> dict:
        """Generate complete video with all components."""
        try:
            self.log("Starting video generation process")
            
            # Create a unique folder with sequential numbering
            folder_num = 1
            # Check existing folders to find the latest number
            if os.path.exists(STORAGE_DIR):
                existing_folders = [d for d in os.listdir(STORAGE_DIR) if os.path.isdir(os.path.join(STORAGE_DIR, d))]
                numbered_folders = []
                for folder in existing_folders:
                    try:
                        # Extract folder number from format "N_UUID"
                        if "_" in folder:
                            num = int(folder.split("_")[0])
                            numbered_folders.append(num)
                    except (ValueError, IndexError):
                        continue
                
                if numbered_folders:
                    folder_num = max(numbered_folders) + 1
            
            folder_id = f"{folder_num}_{str(uuid.uuid4())}"
            self.generation_folder = os.path.join(STORAGE_DIR, folder_id)
            os.makedirs(self.generation_folder, exist_ok=True)
            self.log(f"Created generation folder: {self.generation_folder}")
            
            # Step 1: Generate topic
            self.log("Generating topic")
            self.generate_topic()
            
            # Step 2: Generate script
            self.progress(0.1, desc="Creating script")
            self.log("Generating script")
            self.generate_script()
            
            # Step 3: Generate metadata
            self.progress(0.2, desc="Creating metadata")
            self.log("Generating metadata")
            self.generate_metadata()
            
            # Step 4: Generate image prompts
            self.progress(0.3, desc="Creating image prompts")
            self.log("Generating image prompts")
            self.generate_prompts()
            
            # Step 5: Generate images
            self.progress(0.4, desc="Generating images")
            self.log("Generating images")
            for i, prompt in enumerate(self.image_prompts, 1):
                self.progress(0.4 + 0.2 * (i / len(self.image_prompts)), 
                             desc=f"Generating image {i}/{len(self.image_prompts)}")
                self.log(f"Generating image {i}/{len(self.image_prompts)}")
                self.generate_image(prompt)
            
            # Step 6: Generate speech
            self.progress(0.6, desc="Creating speech")
            self.log("Generating speech")
            self.generate_speech(self.script)
            
            # Step 7: Generate subtitles
            self.progress(0.7, desc="Generating subtitles")
            if self.subtitles_enabled and hasattr(self, 'tts_path') and os.path.exists(self.tts_path):
                self.subtitle_data = self.generate_subtitles(self.tts_path)
                # Save subtitles to generation folder
                if self.subtitle_data:
                    try:
                        # Save word-level subtitles
                        if 'wordlevel' in self.subtitle_data:
                            word_subtitles_path = os.path.join(self.generation_folder, "word_subtitles.json")
                            with open(word_subtitles_path, 'w') as f:
                                json.dump(self.subtitle_data['wordlevel'], f, indent=2)
                            self.log(f"Saved word-level subtitles to: {word_subtitles_path}")
                        
                        # Save line-level subtitles
                        if 'linelevel' in self.subtitle_data:
                            line_subtitles_path = os.path.join(self.generation_folder, "line_subtitles.json")
                            with open(line_subtitles_path, 'w') as f:
                                json.dump(self.subtitle_data['linelevel'], f, indent=2)
                            self.log(f"Saved line-level subtitles to: {line_subtitles_path}")
                    except Exception as e:
                        self.log(warning(f"Error saving subtitles to generation folder: {str(e)}"))
            
            # Step 8: Save content.txt with all metadata and generation info
            self.progress(0.75, desc="Saving generation data")
            try:
                content_path = os.path.join(self.generation_folder, "content.txt")
                with open(content_path, 'w', encoding='utf-8') as f:
                    f.write(f"NICHE: {self.niche}\n\n")
                    f.write(f"LANGUAGE: {self.language}\n\n")
                    f.write(f"GENERATED TOPIC: {self.subject}\n\n")
                    f.write(f"GENERATED SCRIPT:\n{self.script}\n\n")
                    f.write(f"GENERATED PROMPTS:\n")
                    for i, prompt in enumerate(self.image_prompts, 1):
                        f.write(f"{i}. {prompt}\n")
                    f.write("\n")
                    f.write(f"GENERATED METADATA:\n")
                    for key, value in self.metadata.items():
                        f.write(f"{key}: {value}\n")
                self.log(f"Saved content.txt to: {content_path}")
            except Exception as e:
                self.log(warning(f"Error saving content.txt: {str(e)}"))
            
            # Step 9: Combine all elements into final video
            self.progress(0.8, desc="Creating final video")
            self.log("Combining all elements into final video")
            path = self.combine()
            
            self.progress(0.95, desc="Finalizing")
            self.log(f"Video generation complete. Files saved in: {self.generation_folder}")
            
            # Return the result
            return {
                'video_path': path,
                'generation_folder': self.generation_folder,
                'title': self.metadata['title'],
                'description': self.metadata['description'],
                'subject': self.subject,
                'script': self.script,
                'logs': self.logs
            }
            
        except Exception as e:
            error_msg = f"Error during video generation: {str(e)}"
            self.log(error(error_msg))
            raise Exception(error_msg)

# Data for dynamic dropdowns
def get_text_generator_models(generator):
    """Get available models for the selected text generator."""
    models = {
        "gemini": [
            "gemini-2.0-flash", 
            "gemini-2.0-flash-lite", 
            "gemini-1.5-flash", 
            "gemini-1.5-flash-8b", 
            "gemini-1.5-pro"
        ],
        "g4f": [
            "gpt-4",
            "gpt-4o", 
            "gpt-3.5-turbo", 
            "llama-3-70b-chat", 
            "claude-3-opus-20240229", 
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307"
        ],
        "openai": [
            "gpt-4o",
            "gpt-4-turbo", 
            "gpt-3.5-turbo"
        ]
    }
    return models.get(generator, ["default"])

def get_image_generator_models(generator):
    """Get available models for the selected image generator."""
    models = {
        "prodia": [
            "sdxl", 
            "realvisxl", 
            "juggernaut", 
            "dreamshaper", 
            "dalle"
        ],
        "hercai": [
            "v1", 
            "v2", 
            "v3", 
            "lexica"
        ],
        "g4f": [
            "flux",
            "dall-e-3", 
            "dall-e-2", 
            "midjourney"
        ],
        "segmind": [
            "sdxl-turbo", 
            "realistic-vision", 
            "sd3"
        ],
        "pollinations": [
            "default"
        ]
    }
    return models.get(generator, ["default"])

def get_tts_voices(engine):
    """Get available voices for the selected TTS engine."""
    voices = {
        "elevenlabs": [
            "Sarah",      # Female, American accent
            "Brian",      # Male, British accent
            "Lily",       # Female, British accent 
            "Monika Sogam", # Female, Indian accent
            "George",     # Male, American accent
            "River",      # Female, American accent
            "Matilda",    # Female, British accent
            "Will",       # Male, American accent
            "Jessica"     # Female, American accent
        ],
        "openai": [
            "alloy", 
            "echo", 
            "fable", 
            "onyx", 
            "nova", 
            "shimmer"
        ],
        "edge": [
            "en-US-AriaNeural", 
            "en-US-GuyNeural", 
            "en-GB-SoniaNeural", 
            "en-AU-NatashaNeural"
        ],
        "gtts": [
            "en", 
            "es", 
            "fr", 
            "de", 
            "it", 
            "pt", 
            "ru", 
            "ja", 
            "zh", 
            "hi"
        ]
    }
    return voices.get(engine, ["default"])

# Create the Gradio interface
def create_interface():
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="red", radius_size="lg"),
        title="YouTube Shorts Generator",
        css="""
        body { background-color: #0f0f0f; color: #f1f1f1; }
        .gr-button-primary { background-color: #ff0000; border-color: #ff0000; }
        """
    ) as demo:
        with gr.Row():
            gr.Markdown(
                """
                # 📱 YouTube Shorts Generator
                Generate engaging YouTube Shorts videos with AI. Just provide a niche and language to get started!
                """
            )
            
        with gr.Row(equal_height=True):
            # Left panel: Content Settings
            with gr.Column(scale=2, min_width=500):
                with gr.Group():
                    gr.Markdown("### 📝 Content")
                    niche = gr.Textbox(
                        label="Niche/Topic", 
                        placeholder="What's your video about?",
                        value="Historical Facts"
                    )
                    language = gr.Dropdown(
                        choices=["English", "Spanish", "French", "German", "Italian", "Portuguese", 
                                "Russian", "Japanese", "Chinese", "Hindi"],
                        label="Language",
                        value="English"
                    )
                
                # Generator Settings
                with gr.Group():
                    gr.Markdown("### 🔧 Generator Settings")
                    with gr.Tabs():
                        with gr.TabItem("Text"):
                            text_gen = gr.Dropdown(
                                choices=["g4f", "gemini", "openai"], 
                                label="Text Generator",
                                value="gemini"
                            )
                            text_model = gr.Dropdown(
                                choices=get_text_generator_models("g4f"), 
                                label="Text Model",
                                value="gemini-2.0-flash"
                            )
                        
                        with gr.TabItem("Image"):
                            image_gen = gr.Dropdown(
                                choices=["g4f", "prodia", "hercai", "segmind", "pollinations"],
                                label="Image Generator",
                                value="g4f"
                            )
                            image_model = gr.Dropdown(
                                choices=get_image_generator_models("g4f"),
                                label="Image Model",
                                value="flux"
                            )
                        
                        with gr.TabItem("Audio"):
                            tts_engine = gr.Dropdown(
                                choices=["edge", "elevenlabs", "gtts", "openai"],
                                label="Speech Engine",
                                value="edge"
                            )
                            tts_voice = gr.Dropdown(
                                choices=get_tts_voices("edge"),
                                label="Voice",
                                value="en-US-AriaNeural"
                            )
                            # Fix for music_file - Get available music and set proper default
                            music_choices = get_music_files()
                            default_music = "none" if "random" not in music_choices else "random"
                            music_file = gr.Dropdown(
                                choices=music_choices,
                                label="Background Music",
                                value=default_music
                            )
                        
                        with gr.TabItem("Subtitles"):
                            subtitles_enabled = gr.Checkbox(label="Enable Subtitles", value=True)
                            highlighting_enabled = gr.Checkbox(label="Enable Word Highlighting", value=True)
                            subtitle_font = gr.Dropdown(
                                choices=get_font_files(),
                                label="Font",
                                value="random"
                            )
                            with gr.Row():
                                font_size = gr.Slider(
                                    minimum=40,
                                    maximum=120,
                                    value=80,
                                    step=5,
                                    label="Font Size"
                                )
                                subtitle_position = gr.Dropdown(
                                    choices=["bottom", "middle", "top"],
                                    label="Position",
                                    value="bottom"
                                )
                            with gr.Row():
                                text_color = gr.ColorPicker(label="Text Color", value="#FFFFFF")
                                highlight_color = gr.ColorPicker(label="Highlight Color", value="#0000FF")

                        with gr.TabItem("Transitions"):
                            transition_type = gr.Dropdown(
                                choices=["none", "crossfade"],
                                label="Transition Type",
                                value="crossfade"
                            )
                            transition_duration = gr.Slider(
                                minimum=0.0,
                                maximum=2.0,
                                value=0.5,
                                step=0.1,
                                label="Transition Duration (s)"
                            )
                
                # Generate button
                generate_btn = gr.Button("🎬 Generate Video", variant="primary", size="lg")
            
            # Right panel: Output display
            with gr.Column(scale=1, min_width=300):
                with gr.Tabs():
                    with gr.TabItem("Video"):
                        # Larger video preview with proper mobile proportions
                        video_output = gr.Video(label="Generated Video", height=580, width=330)
                        
                    with gr.TabItem("Metadata"):
                        title_output = gr.Textbox(label="Title", lines=2)
                        description_output = gr.Textbox(label="Description", lines=4)
                        script_output = gr.Textbox(label="Script", lines=8)
                    
                    # API Keys section as a tab    
                    with gr.TabItem("🔑 API Keys"):
                        gemini_api_key = gr.Textbox(
                            label="Gemini API Key", 
                            type="password",
                            value=os.environ.get("GEMINI_API_KEY", "")
                        )
                        assemblyai_api_key = gr.Textbox(
                            label="AssemblyAI API Key", 
                            type="password",
                            value=os.environ.get("ASSEMBLYAI_API_KEY", "")
                        )
                        elevenlabs_api_key = gr.Textbox(
                            label="ElevenLabs API Key", 
                            type="password",
                            value=os.environ.get("ELEVENLABS_API_KEY", "")
                        )
                        segmind_api_key = gr.Textbox(
                            label="Segmind API Key", 
                            type="password",
                            value=os.environ.get("SEGMIND_API_KEY", "")
                        )
                        openai_api_key = gr.Textbox(
                            label="OpenAI API Key", 
                            type="password",
                            value=os.environ.get("OPENAI_API_KEY", "")
                        )
                        
                    with gr.TabItem("Log"):
                        log_output = gr.Textbox(label="Process Log", lines=15, max_lines=100)
        
        # Dynamic dropdown updates
        def update_text_models(generator):
            return gr.Dropdown(choices=get_text_generator_models(generator))
        
        def update_image_models(generator):
            return gr.Dropdown(choices=get_image_generator_models(generator))
        
        def update_tts_voices(engine):
            return gr.Dropdown(choices=get_tts_voices(engine))
        
        # Connect the change events
        text_gen.change(fn=update_text_models, inputs=text_gen, outputs=text_model)
        image_gen.change(fn=update_image_models, inputs=image_gen, outputs=image_model)
        tts_engine.change(fn=update_tts_voices, inputs=tts_engine, outputs=tts_voice)
        
        # Main generation function
        def generate_youtube_short(niche, language, text_gen, text_model, image_gen, image_model,
                                  tts_engine, tts_voice, subtitles_enabled, highlighting_enabled,
                                  subtitle_font, font_size, subtitle_position,
                                  text_color, highlight_color, music_file,
                                  transition_type, transition_duration,
                                  gemini_api_key, assemblyai_api_key,
                                  elevenlabs_api_key, segmind_api_key, openai_api_key,
                                  progress=gr.Progress()):
            
            if not niche.strip():
                return {
                    video_output: None,
                    title_output: "ERROR: Please enter a niche/topic",
                    description_output: "",
                    script_output: "",
                    log_output: "Error: Niche/Topic is required. Please enter a valid topic and try again."
                }
            
            # Create API keys dictionary
            api_keys = {
                'gemini': gemini_api_key,
                'assemblyai': assemblyai_api_key,
                'elevenlabs': elevenlabs_api_key,
                'segmind': segmind_api_key,
                'openai': openai_api_key
            }
            
            try:
                # Initialize YouTube class
                yt = YouTube(
                    niche=niche,
                    language=language,
                    text_gen=text_gen,
                    text_model=text_model,
                    image_gen=image_gen,
                    image_model=image_model,
                    tts_engine=tts_engine,
                    tts_voice=tts_voice,
                    subtitle_font=subtitle_font,
                    font_size=font_size,
                    text_color=text_color,
                    highlight_color=highlight_color,
                    subtitles_enabled=subtitles_enabled,
                    highlighting_enabled=highlighting_enabled,
                    subtitle_position=subtitle_position,
                    music_file=music_file,
                    transition_type=transition_type,
                    transition_duration=transition_duration,
                    api_keys=api_keys,
                    progress=progress
                )
                
                # Generate video
                result = yt.generate_video()
                
                # Check if video was successfully created
                if not result or not result.get('video_path') or not os.path.exists(result.get('video_path', '')):
                    return {
                        video_output: None,
                        title_output: "ERROR: Video generation failed",
                        description_output: "",
                        script_output: "",
                        log_output: "\n".join(yt.logs)
                    }
                
                return {
                    video_output: result['video_path'],
                    title_output: result['title'],
                    description_output: result['description'],
                    script_output: result['script'],
                    log_output: "\n".join(result['logs'])
                }
                
            except Exception as e:
                import traceback
                error_details = f"Error: {str(e)}\n\n{traceback.format_exc()}"
                return {
                    video_output: None,
                    title_output: f"ERROR: {str(e)}",
                    description_output: "",
                    script_output: "",
                    log_output: error_details
                }
        
        # Connect the button click event
        generate_btn.click(
            fn=generate_youtube_short,
            inputs=[
                niche, language, text_gen, text_model, image_gen, image_model,
                tts_engine, tts_voice, subtitles_enabled, highlighting_enabled,
                subtitle_font, font_size, subtitle_position, text_color, highlight_color, music_file,
                transition_type, transition_duration,
                gemini_api_key, assemblyai_api_key, elevenlabs_api_key, segmind_api_key, openai_api_key
            ],
            outputs=[video_output, title_output, description_output, script_output, log_output]
        )
        
        # Add examples
        music_choices = get_music_files()
        default_music = "none" if "random" not in music_choices else "random"
        
        gr.Examples(
            [
                ["Historical Facts", "English", "g4f", "gpt-4", "g4f", "flux", "edge", "en-US-AriaNeural", True, True, "default", 80, "bottom", "#FFFFFF", "#0000FF", default_music, "crossfade", 0.5],
                ["Cooking Tips", "English", "g4f", "gpt-4", "g4f", "flux", "edge", "en-US-AriaNeural", True, True, "default", 80, "bottom", "#FFFFFF", "#FF0000", default_music, "crossfade", 0.5],
                ["Technology News", "English", "g4f", "gpt-4", "g4f", "flux", "edge", "en-US-GuyNeural", True, True, "default", 80, "bottom", "#FFFFFF", "#00FF00", default_music, "crossfade", 0.5],
            ],
            [niche, language, text_gen, text_model, image_gen, image_model, tts_engine, tts_voice,
             subtitles_enabled, highlighting_enabled, subtitle_font, font_size,
             subtitle_position, text_color, highlight_color, music_file, transition_type, transition_duration],
            label="Quick Start Templates"
        )
        
    return demo

# Create and launch the interface
if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)
    os.makedirs(FONTS_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    # Launch the app
    demo = create_interface()
    demo.launch()