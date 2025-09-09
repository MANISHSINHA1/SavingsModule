import requests
import json

# CONFIGURATION
PROMETHEUS_URL = "http://localhost:9090"
LM_STUDIO_URL = "http://localhost:1234/v1/completions"  # Mistral endpoint in LM Studio
MISTRAL_MODEL = "mistral"  # adjust if you're using a custom model name

def query_prometheus(query):
    """Query Prometheus and return the result"""
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {'query': query}
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'success':
        return data['data']['result']
    else:
        raise Exception("Failed to query Prometheus")

def send_to_mistral(prompt_text):
   
    """Send prompt to local Mistral model via LM Studio"""
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": MISTRAL_MODEL,
        "prompt": prompt_text,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.01
    }
    
    response = requests.post(LM_STUDIO_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    
    return result

def main():
    # maximum amount of memory in bytes used for memory management
    query = 'jvm_memory_max_bytes{job="SavingsServiceForING", area="heap",id="G1 Old Gen"}'

    try:
        prom_data = query_prometheus(query)
 
        # Format the data into a prompt for Mistral
        formatted = json.dumps(prom_data, indent=2)
       
        prompt = f"""What is Giga Byte of memory I should have in my server to run this application without facing Out of Memory issue:\n\n{formatted}"""
   
        # Send to Mistral model
        answer = send_to_mistral(prompt)

        print("\n🔍 Mistral's Response:")
        print(answer)

    except Exception as e:
        print(f"Error: {e}")

# Only run if this file is executed directly
if __name__ == "__main__":
    main()
