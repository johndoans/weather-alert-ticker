import tkinter as tk
import requests
import json
import datetime

# Get data from NWS
headers = {'User-Agent' : 'myapp'}
# endpoint = 'https://api.weather.gov/alerts?area=MO'
endpoint = 'https://api.weather.gov/alerts/active?point=38.50,-90.33'

response = requests.get(endpoint, headers = headers)
data = response.json()

alert_text = ""

if response.status_code == 200:
    # Parse the data
    print(response.text)
    data = json.loads(response.text)
    alert_text = " ------ "

    # No alerts?
    if len(data['features']) == 0:
        alert_text = "There are no current weather alerts for South St. Louis County."
    else:
        alert_text += f" There are { len(data['features']) } weather alert(s) that includes South St. Louis County."

        alert_number = 0
        # Go through each alert
        for alert in data['features']:
            alert_number += 1

            properties = alert['properties']

            # Parse the expire time
            expires = properties['expires']
            date = expires.split('T')[0].split("-")
            time = expires.split('T')[1].split("+")[0].split(":")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            hour = int(time[0])
            minute = int(time[1])
            date_object = datetime.datetime(year, month, day, hour, minute)

            description_parts = properties['description'].split('\n\n')
            alert_text +=  f" ({ alert_number }) The National Weather Service has issued a {properties['event']} for the counties of {properties['areaDesc']} until {date_object.strftime("%A, %B %d, %Y at %I:%M %p")}."

            # Get what/hazard
            for part in description_parts:
                if "WHAT..." in part:
                    alert_text +=  f" { part } "
                    break
                if "HAZARD..." in part:
                    alert_text +=  f" { part } "
                    break

        alert_text += " ---END---                  "

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
