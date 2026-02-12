import urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:5173") as response:
        print(f"Status: {response.getcode()}")
        print(f"Headers: {response.info()}")
except Exception as e:
    print(f"Error: {e}")
