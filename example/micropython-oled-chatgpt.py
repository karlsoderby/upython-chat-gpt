import network, socket
from machine import Pin, SoftI2C
import ssd1306
import urequests as requests
import ujson

# WiFi network
SSID='' # Network SSID
KEY=''  # Network key

# GIGA R1's I2C pins
SDA_PIN = 'PB11'
SCL_PIN = 'PH4'

i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))

display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Init wlan module and connect to network
print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

# POST request
# Change the "api_key" to your own
# Change the "open_ai_question" to what you want to ask

url = "https://api.openai.com/v1/chat/completions"
open_ai_question = "Who are you?"
max_words = "Max 80 characters"
api_key = "YOUR_API_KEY"

payload = ujson.dumps({
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": open_ai_question + max_words
    },
  ],
  "temperature": 1,
  "top_p": 1,
  "n": 1,
  "stream": False,
  "max_tokens": 100,
  "presence_penalty": 0,
  "frequency_penalty": 0
})

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + api_key
}

# Custom function that prints letter by letter
# to the OLED SSD1306 display.
def print_oled(msg):
    display.fill(0)
    x=0 
    y=0
    z=0
    row = 0
    maxlength = (len(msg))
    print(maxlength)
    
    for line in range(maxlength/20):
        for row in range(20):
            if (row+z == maxlength):
                break
            display.text(msg[row+z], x, y)
            x = x+6
            display.show()

        z = z+20
        y = y+11
        x = 0
    x=0
    y=0
    z=0
    row=0

# Print the question (msg)
print(open_ai_question)
print_oled(open_ai_question)

# Post Data
response = requests.post(url, headers=headers, data=payload)
response_data = response.json()

# Access JSON object
open_ai_message = response_data["choices"][0]["message"]["content"]

# Close the connection
response.close()

# Print the response (open_ai_message)
print(open_ai_message)
print_oled(open_ai_message)


