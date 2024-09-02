from flask import Flask, render_template, request, send_file
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)


def get_weather(city):
    url = (f"http://api.weatherstack.com/current?access_key=f60920e756c57db15eb7e01e97195f5d&query=" +
           city + "&forecast_days=5")  # weather api url and link
    response = requests.get(url)
    if response.status_code == 200:
        data_forc = response.json()
        return data_forc
    else:
        print("Error, Status Code", response.status_code)
        return None


@app.route('/')
def display_weather():
    response = requests.get("https://ipinfo.io/json")  # auto detect location based on ip
    data = response.json()  # getting json data
    city = data.get("city")
    # city = input("What is the name of the city?")       #uncomment this to take user input

    fore_cast = get_weather(city)
    if not 'success' in fore_cast:  # checks if the city is invalid, if it is it will respond respectively
        date_time = fore_cast['location']['localtime']
        weather = fore_cast['current']['temperature']
        text = ("Time of reading: " + date_time + "\nTemperature: " + str(weather) + " °C" + "\nWeather Condition: " +
                (fore_cast['current']['weather_descriptions'])[0] + "\nUV Index: " + str(
                    fore_cast['current']['uv_index']) + "\nVisibility: " +
                str(fore_cast['current']['visibility']))
        text += "\nCity: " + city
        im = Image.open(r"sky-background.png")  # change path to where the background image is in the directory
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("arial.ttf", 40)  # change path to where the arial font is in the directory
        draw.text((200, 200), text, fill=(0, 0, 0), font=font)
        image_path = "weather_image.png"
        im.save(image_path)

        return send_file(image_path, mimetype='image/png')
    else:
        return "Invalid City Name", 400


if __name__ == '__main__':
    app.run(debug=True)
