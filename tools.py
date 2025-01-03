import openai
import requests
from config import OPENAI_API_KEY, WEATHER_API_KEY, NEWS_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def fetch_weather(city):
    """Fetch weather information for a city."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    except Exception as e:
        return f"Error fetching weather: {e}"

def fetch_news():
    """Fetch top news headlines."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])[:5]
        if not articles:
            return "No news articles found."
        return "Here are the top news headlines:\n" + "\n".join(
            [f"{i+1}. {a['title']}" for i, a in enumerate(articles)]
        )
    except Exception as e:
        return f"Error fetching news: {e}"

def process_with_openai(query):
    """Use OpenAI API with gpt-4o-mini to interpret the query and route it to the appropriate tool."""
    try:
        # Use OpenAI's ChatCompletion for gpt-4o-mini
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant. Interpret user queries and decide whether they pertain to 'weather', 'news', or something else. Provide clear and concise intent."},
                {"role": "user", "content": query}
            ],
            max_tokens=50
        )

        # Extract the assistant's response
        intent = response["choices"][0]["message"]["content"].strip().lower()

        # Route to the appropriate tool based on intent
        if "weather" in intent:
            return fetch_weather("Liepaja")  # Default city
        elif "news" in intent:
            return fetch_news()
        else:
            return "I'm sorry, I can help with weather or news. Please ask about one of those."
    except Exception as e:
        return f"Error processing query with OpenAI: {e}"

