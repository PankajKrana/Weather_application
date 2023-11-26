import tkinter as tk
import requests
import webbrowser
from PIL import Image, ImageTk

# Constants
WEATHER_API_KEY = "5dfc76d8e11e42a58de163730232609"
NEWS_API_KEY = "47ee4c511abc4a28a997bb1f92890ed5"
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def get_weather():
    city = entry.get()
    params = {
        'key': WEATHER_API_KEY,
        'q': city,
        'aqi': 'no',
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Raise an error for unsuccessful responses
        data = response.json()
        update_weather_info(data)
        update_city_label(city)
        fetch_and_display_news(city)
    except requests.exceptions.RequestException as e:
        weather_info.set(f"Error fetching data: {str(e)}")
        clear_news()

def update_weather_info(data):
    condition = data['current']['condition']['text']
    temperature = data['current']['temp_c']
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_kph']
    weather_info.set(f"Weather: {condition}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} km/h")

def update_city_label(city):
    city_label.config(text=f"Weather and News for {city}")

def fetch_and_display_news(city):
    news_articles = fetch_news(NEWS_API_KEY, city)
    display_news(news_articles)

def open_news_link(event):
    index = news_text.index(tk.CURRENT)
    article_number = index.split('.')[0]
    webbrowser.open(news_links[int(article_number) - 1])

def fetch_news(api_key, query):
    params = {
        'apiKey': api_key,
        'q': query,
    }
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def display_news(news_articles):
    news_text.delete('1.0', tk.END)
    global news_links
    news_links = []
    for i, article in enumerate(news_articles, start=1):
        news_links.append(article['url'])
        news_text.insert(tk.END, f"{i}. {article['title']}\n{article['description']}\n\n")
    news_text.tag_configure('link', foreground='blue', underline=True)
    news_text.tag_bind('link', '<Button-1>', open_news_link)
    news_text.tag_add('link', '1.0', tk.END)

def clear_news():
    news_text.delete('1.0', tk.END)

def show_news_window():
    news_window = tk.Toplevel(root)
    news_window.title("News Window")

    news_text_window = tk.Text(news_window, wrap=tk.WORD, height=10, width=40, fg="white")
    news_text_window.pack()

    city = entry.get()
    news_articles = fetch_news(NEWS_API_KEY, city)
    display_news(news_articles, text_widget=news_text_window)

root = tk.Tk()
root.title("Weather App")
root.geometry("700x600")

# Load and resize the background image
bg_image = Image.open("background_image.png")
bg_image = bg_image.resize((700, 600), Image.ADAPTIVE)
background_image = ImageTk.PhotoImage(bg_image)

# Create a label to use the background image
bg_label = tk.Label(root, image=background_image)
bg_label.place(relwidth=1, relheight=1)  #

# Create an Entry widget for user input of location
original_image = Image.open("weather_icon.png")
resized_image = original_image.resize((100, 100), Image.ADAPTIVE)
weather_icon = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(root, image=weather_icon, bg = "#6febf2")
image_label.pack(pady=10)

# Text below the Weather Icon
text_below_image_label = tk.Label(root, text="Weather Application", fg="white", bg="#6febf2", font=("Helvetica", 14, "bold"))
text_below_image_label.place(relx=0.50, rely=0.2, anchor='center')

label = tk.Label(root, text="Enter city:", fg="white",bg = "#6febf2" )
label.pack(pady=5)

entry = tk.Entry(root, font=("Helvetica", 12), bg="#6febf2", fg="white")
entry.place(relx=0.39, rely=0.25)

get_weather_button = tk.Button(root, text="Get Weather & News", command=get_weather, font=("Helvetica", 12), bg="#6febf2")  # Green button
get_weather_button.place(relx=0.40, rely=0.31)

weather_info = tk.StringVar()
weather_label = tk.Label(root, textvariable=weather_info, fg="white", bg="#6febf2")
weather_label.place(relx=0.4, rely=0.35)

city_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), fg="white", bg = "#6febf2")
city_label.pack()

news_text = tk.Text(root, wrap=tk.WORD, height=10, width=40, fg="black", bg="#6febf2")
news_text.place(relx=0.52, rely=0.60, anchor='center')

show_news_button = tk.Button(root, text="Show News", command=show_news_window, bg= "#6febf2")
show_news_button.place(relx=0.52, rely=0.82, anchor='center')

root.mainloop()







