import tkinter as tk
import requests
import json

# Get data from NWS
headers = {'User-Agent' : 'myapp'}
endpoint = 'https://api.weather.gov/alerts?area=MO'

response = requests.get(endpoint, headers = headers)
data = response.json()

alert_text = "*****"

if response.status_code == 200:
    # Parse the data
    data = json.loads(response.text)
    for alert in data['features']:
        properties = alert['properties']
        alert_text +=  f"  {properties['description']}  "
    alert_text += "*****"
    alert_text.replace('\r', '').replace('\n', '')
else:
    print(f"Error! {response.status_code}")

# Main window
root = tk.Tk()
root.title("Severe Weather Graphics")
root.minsize(800, 600)
root.geometry("800x600")

# The ticker itself
footer_frame = tk.Frame(root)
label = tk.Label(footer_frame, text="", background="black", foreground="white", font=24, height=2)
footer_frame.pack(side="bottom", fill="x")
label.pack(fill="x")

label["text"] = alert_text

root.mainloop()
