import tkinter as tk
import requests
import json
import datetime

# Get data from NWS, county based alert
headers = {'User-Agent' : 'myapp'}
# endpoint = 'https://api.weather.gov/alerts?area=MO'
# endpoint = 'https://api.weather.gov/alerts/active?point=38.50,-90.33'
endpoint = 'https://api.weather.gov/alerts/active?zone=MOZ063'

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
        alert_text = "There are no current weather alerts for St. Louis County."
    else:
        alert_text += f" There are { len(data['features']) } weather alert(s) that includes St. Louis County."

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

            date_string = date_object.strftime("%A, %B %d, %Y at %I:%M %p")
            if date_object.date() == datetime.date.today():
                date_string = date_object.strftime("%I:%M %p") + " today"
            elif date_object.date() == datetime.date.today() + datetime.timedelta(days=1):
                date_string = date_object.strftime("%I:%M %p") + " tomorrow"
            elif date_object.date() < datetime.date.today() + datetime.timedelta(days=6):
                date_string = date_object.strftime("%I:%M %p %A")


            description_parts = properties['description'].split('\n\n')
            alert_text +=  f" ({ alert_number }) The National Weather Service has issued a {properties['event']} for the counties of {properties['areaDesc']} until { date_string }."

            # Get what/hazard
            for part in description_parts:
                if "WHAT..." in part:
                    alert_text +=  f" { part } "
                    break
                if "HAZARD..." in part:
                    alert_text +=  f" { part } "
                    break

            # Action text
            if properties['event'] == "Severe Thunderstorm Warning":
                alert_text +=  f" Stay inside away from windows and trees. "
                # Thunderstorm intensity
                if "thunderstormDamageThreat" in properties['parameters']:
                    if properties['parameters']["thunderstormDamageThreat"][0] == "CONSIDERABLE":
                        alert_text +=  f" This is a CONSIDERABLE severe thunderstorm which could cause major impacts. Take action now! "
                    elif properties['parameters']["thunderstormDamageThreat"][0] == "DESTRUCTIVE":
                        alert_text +=  f" This is a DESTRUCTIVE severe thunderstorm which could cause significant impacts. Take action now! "
                else:
                    alert_text +=  f" This is a standard severe thunderstorm warning. "

                # A tornado is possible
                if "tornadoDetection" in properties['parameters']:
                    if properties['parameters']["tornadoDetection"][0] == "POSSIBLE":
                        alert_text +=  f" This storm has the potential to form a tornado. "

            elif properties['event'] == "Tornado Warning":
                            alert_text +=  f" Go to the lowest, most interior room away from windows and trees. "

                            # Observed tornado?
                            if "tornadoDetection" in properties['parameters']:
                                if properties['parameters']["tornadoDetection"][0] == "OBSERVED":
                                    alert_text +=  f" This is an OBSERVED tornado. Take action now! "
                                elif properties['parameters']["tornadoDetection"][0] == "RADAR INDICATED":
                                    alert_text +=  f" Radar indicated. "

                            # Tornado intensity
                            if "tornadoDamageThreat" in properties['parameters']:
                                if properties['parameters']["tornadoDamageThreat"][0] == "CONSIDERABLE":
                                    alert_text +=  f" This is a CONSIDERABLE tornado. "
                                elif properties['parameters']["tornadoDamageThreat"][0] == "CATASTROPHIC":
                                    alert_text +=  f" This is a CATASTROPHIC tornado! Expect major damage. "

            elif properties['event'] == "Flash Flood Warning":
                            alert_text +=  f" Use caution driving. Never drive through flooded roads; turn around, don't drown! "
            
                            # Flooding intensity
                            if "flashFloodDamageThreat" in properties['parameters']:
                                if properties['parameters']["flashFloodDamageThreat"][0] == "CONSIDERABLE":
                                    alert_text +=  f" This is CONSIDERABLE flooding which could cause major impacts. Take action now! "
                                elif properties['parameters']["flashFloodDamageThreat"][0] == "CATASTROPHIC":
                                    alert_text +=  f" This is CATASTROPHIC flash flooding which could be deadly. Seek higher ground! "

            elif properties['event'] == "Heat Advisory" or properties['event'] == "Extreme Heat Warning":
                 alert_text +=  f" Stay hydrated, bring extra water, limit time outdoors, spend time in the A/C, wear light clothing, and NEVER leave people/pets unattended in a car! "

            else:
                if properties.get('instruction', "") != None:
                    alert_text += properties['instruction']

            # County codes, to deal with later
            # properties['geocode']['UGC']


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
