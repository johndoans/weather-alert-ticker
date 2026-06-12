import tkinter as tk
import requests
import json

# Get data from NWS
headers = {'User-Agent' : 'myapp'}
# endpoint = 'https://api.weather.gov/alerts?area=MO'
endpoint = 'https://api.weather.gov/alerts/active?point=38.50,-90.33'

response = requests.get(endpoint, headers = headers)
data = response.json()

alert_text = ""

if response.status_code == 200:
    # Parse the data
    data = json.loads(response.text)
    alert_text = " ***** "

    # No alerts?
    if len(data['features']) == 0:
        alert_text = "There are no current weather alerts for South St. Louis County."
    else:
        alert_text += f" The National Weather Service has issued { len(data['features']) } alert(s) for South St. Louis County."

        alert_number = 0
        # Go through each alert
        for alert in data['features']:
            alert_number += 1

            properties = alert['properties']
            alert_text +=  f" ({ alert_number }) The National Weather Service has issued a {properties['event']} for South St. Louis County."
            alert_text +=  f"  {properties['description']}  "
        alert_text += " ***** "

    # Remove line break
    alert_text = alert_text.replace('\r', ' ').replace('\n', ' ')
else:
    print(f"Error! {response.status_code}")

# Main window
root = tk.Tk()
root.title("Severe Weather Graphics")
root.minsize(800, 600)
root.geometry("800x600")

# Scrolling text
text_variable = tk.StringVar()
def shift_text():
    if len(shift_text.msg) > 200:
        shift_text.msg = shift_text.msg[1:] + shift_text.msg[0]
    text_variable.set(shift_text.msg)
    root.after(60, shift_text)

shift_text.msg = alert_text
    

# The ticker itself
footer_frame = tk.Frame(root)
label = tk.Label(footer_frame, textvariable= text_variable, background="black", foreground="white", font=24, height=2, justify="left")
footer_frame.pack(side="bottom", fill="x")
label.pack(fill="x")
#label["text"] = alert_text
print(alert_text)
root.after(1000, shift_text)
root.mainloop()
