import requests

api_key = "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"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.1-70b-versatile",
    "prompt": "Summarize the following data:\nSample data here.",
    "max_tokens": 200
}

response = requests.post("https://api.groq.com/generate", headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response Text:", response.text)
