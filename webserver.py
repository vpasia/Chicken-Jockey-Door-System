from flask import Flask, request
import subprocess
import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, prompt):
    base64_image = encode_image(image_path)
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high"
                    },
                },
            ],
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message.content

app = Flask(__name__)

@app.route('/api/process_sound', methods=['POST'])
def process_sound():
    save_path = os.path.join(os.getcwd(), 'key.wav')
    request.files['chicken-jockey-key2.wav'].save(save_path)
    
    img_path = os.path.join(os.getcwd(), 'key.png')
    
    if os.path.exists(img_path):
        os.remove(img_path)
    
    command = [
        'ffmpeg',
        '-i', 'key.wav',
        '-lavfi', 'showspectrumpic=s=800x400:mode=separate:fscale=lin:scale=log',
        'key.png'
    ]
    
    subprocess.run(command, check=True)
    
    prompt = "Does this image contain \"Chicken Jockey\". Perhaps in the spectogram image. Say yes if it is in there."

    analysis_result = analyze_image(img_path, prompt)
    
    status = 200 if "yes" in analysis_result.lower() else 404
    
    return {"status":status}
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
    