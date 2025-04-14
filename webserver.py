from flask import Flask, request
import subprocess
import os
import openai
import base64
import wave
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

@app.route('/api/process_sound_img', methods=['POST'])
def process_sound_img():
    temp_pcm_path = os.path.join(os.getcwd(), "temp.pcm")
    if not os.path.exists(temp_pcm_path):
        return {"status": 400, "message": "No PCM data accumulated."}, 400

    wav_path = os.path.join(os.getcwd(), "key.wav")
    try:
        with open(temp_pcm_path, "rb") as pcm_file:
            pcm_data = pcm_file.read()
        with wave.open(wav_path, "wb") as wf:
            # Set these parameters to match your PCM data; for example:
            wf.setnchannels(1)         # Mono audio
            wf.setsampwidth(2)         # 16-bit audio => 2 bytes per sample
            wf.setframerate(16000)     # 44.1 kHz sample rate
            wf.writeframes(pcm_data)
    except Exception as e:
        return {"status": 500, "message": f"Error creating WAV file: {e}"}, 500

    # Clean up the temporary PCM file.
    os.remove(temp_pcm_path)
    return {"status":200, "message":"Created key.wav"}
    
    # img_path = os.path.join(os.getcwd(), 'key.png')
    
    # if os.path.exists(img_path):
    #     os.remove(img_path)
    
    # command = [
    #     'ffmpeg',
    #     '-i', 'key.wav',
    #     '-lavfi', 'showspectrumpic=s=800x400:mode=separate:fscale=lin:scale=log',
    #     'key.png'
    # ]
    
    # subprocess.run(command, check=True)
    
    # prompt = "Does this image contain \"Chicken Jockey\". Perhaps in the spectogram image. Say yes if it is in there."

    # analysis_result = analyze_image(img_path, prompt)
    
    # status = 200 if "yes" in analysis_result.lower() else 404
    
    return {"status":status}

@app.route('/api/process_pcm', methods=['POST'])
def process_pcm():
    temp_pcm_path = os.path.join(os.getcwd(), "temp.pcm")
    try:
        with open(temp_pcm_path, "ab") as f:
            f.write(request.data)
    except Exception as e:
        return {"status": 500, "message": f"Error appending PCM data: {e}"}, 500
    return {"status": 200, "message": "PCM segment appended."}
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
    