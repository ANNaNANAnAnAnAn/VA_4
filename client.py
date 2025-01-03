import tkinter as tk
import requests
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

# Web Service URL
WEB_SERVICE_URL = "http://127.0.0.1:5000/ask"

def send_query():
    """Send user query to the Flask web service and display the response."""
    query = user_input.get()
    if not query.strip():
        response_label.config(text="Please enter a query.")
        return

    try:
        # Send request to the Flask web service
        response = requests.post(WEB_SERVICE_URL, json={"query": query}, timeout=5)
        response.raise_for_status()
        data = response.json()
        response_label.config(text=data.get("response", "No response from server."))
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with web service: {e}")
        response_label.config(text="Error: Unable to contact web service.")

# Create Tkinter GUI
root = tk.Tk()
root.title("Assistant Client")

# Input Field
user_input = tk.Entry(root, width=50)
user_input.pack(pady=10)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=send_query)
submit_button.pack(pady=5)

# Response Label
response_label = tk.Label(root, text="", wraplength=400, justify="left")
response_label.pack(pady=10)

# Start Tkinter Main Loop
root.mainloop()
