import requests
import json

# CONFIGURATION
PROMETHEUS_URL = "http://localhost:9090"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"  # Mistral endpoint in LM Studio
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
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.7
    }

    response = requests.post(LM_STUDIO_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    #return result['choices'][0]['message']['content']
    return result

def main():
    # Define a Prometheus query (example: CPU usage)
    query = 'rate(node_cpu_seconds_total[1m])'

    try:
        prom_data = query_prometheus(query)

        # Format the data into a prompt for Mistral
        formatted = json.dumps(prom_data, indent=2)
        prompt = f"""Analyze the following Prometheus metrics and summarize any important trends or anomalies:\n\n{formatted}"""

        # Send to Mistral model
        answer = send_to_mistral(prompt)

        print("\n🔍 Mistral's Response:")
        print(answer)

    except Exception as e:
        print(f"Error: {e}")

# Only run if this file is executed directly
if __name__ == "__main__":
    main()
