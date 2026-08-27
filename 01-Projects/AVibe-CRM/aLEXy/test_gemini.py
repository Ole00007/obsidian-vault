from google import genai

client = genai.Client(api_key="AIzaSyDR-iPtmu_xbkDR3TjzK3hGAUtDlb9ao2g")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Return ONLY valid JSON with keys: urgency_override (High), risk_flag (potential conflict of interest), confidence (85)"
)

print(response.text)
