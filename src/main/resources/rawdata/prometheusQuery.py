import requests

def get_prometheus_metric(query):
    res = requests.get("http://localhost:9090/api/v1/query", params={"query": query})
    data = res.json()
    print(data)
    return data['data']['result']

if __name__ == "__main__":
    print("Hello World!")
    get_prometheus_metric("jvm_memory_used_bytes")
