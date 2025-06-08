import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

API_KEY = '30d4741c779ba94c470ca1f63045390a'

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Forecast")
        self.geometry("800x700")
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", foreground="white")
        self.style.configure('Header.TFrame', background="#4a86e8")
        self.style.configure('Header.TLabel', background="#4a86e8", foreground="white", font=("Arial", 24, "bold"))
        self.style.configure('Weather.TFrame', background="white")
        self.style.configure('Weather.TLabel', background="white", foreground="white")
        self.style.configure('Hourly.TLabelframe', background="white", font=("Arial", 12, "bold"))
        self.style.configure('Hourly.TFrame', background="white")
        self.style.configure('Hourly.TLabel', background="white", foreground="white")
        
        self.create_widgets()
        self.weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Smoke": "💨",
            "Haze": "😶‍🌫️",
            "Fog": "🌁"
        }
        
    def create_widgets(self):
        # Header frame
        header_frame = ttk.Frame(self, style='Header.TFrame', height=80)
        header_frame.pack(fill="x")
        
        header_label = ttk.Label(header_frame, text="Weather Forecast", style='Header.TLabel')
        header_label.pack(pady=20)
        
        # Input frame - using grid for precise alignment
        input_frame = ttk.Frame(self, padding=(15, 15))
        input_frame.pack(fill="x", padx=10)
        
        # Configure grid columns
        input_frame.columnconfigure(0, weight=0)  # Label
        input_frame.columnconfigure(1, weight=3)  # Entry
        input_frame.columnconfigure(2, weight=0)  # Unit label
        input_frame.columnconfigure(3, weight=1)  # Unit dropdown
        input_frame.columnconfigure(4, weight=0)  # Button
        
        # City label
        city_label = ttk.Label(input_frame, text="Enter City:", font=("Arial", 12))
        city_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        # City entry
        self.city_var = tk.StringVar()
        city_entry = ttk.Entry(input_frame, textvariable=self.city_var, font=("Arial", 12))
        city_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        city_entry.insert(0, "e.g. London, Sydney")
        city_entry.bind("<FocusIn>", lambda e: city_entry.delete(0, tk.END) 
                         if city_entry.get() == "e.g. London, Sydney" else None)
        
        # Unit label
        unit_label = ttk.Label(input_frame, text="Unit:", font=("Arial", 12))
        unit_label.grid(row=0, column=2, padx=(10, 5), sticky="e")
        
        # Unit dropdown
        self.unit_var = tk.StringVar(value="metric")
        unit_dropdown = ttk.Combobox(input_frame, textvariable=self.unit_var, 
                                    values=["metric", "imperial"], width=10, state="readonly")
        unit_dropdown.grid(row=0, column=3, padx=(0, 10), sticky="ew")
        
        # Search button
        self.search_btn = ttk.Button(input_frame, text="Get Weather", command=self.get_weather, width=15)
        self.search_btn.grid(row=0, column=4, sticky="e")
        
        # Current weather frame
        self.current_weather_frame = ttk.Frame(self, style='Weather.TFrame', padding=(20, 20))
        self.current_weather_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        # Hourly forecast frame
        self.hourly_frame = ttk.LabelFrame(self, text="Next 12 Hours Forecast", style='Hourly.TLabelframe', padding=(10, 10))
        self.hourly_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initialize weather display widgets
        self.init_weather_display()
        
    def init_weather_display(self):
        # Clear previous widgets
        for widget in self.current_weather_frame.winfo_children():
            widget.destroy()
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        
        # Default "no data" display
        no_data_label = ttk.Label(self.current_weather_frame, text="Enter a city to see weather information", 
                                 font=("Arial", 14), foreground="gray", style='Weather.TLabel')
        no_data_label.pack(expand=True)
        
    def get_weather(self):
        city = self.city_var.get().strip()
        unit = self.unit_var.get()
        
        if not city or city == "e.g. London, Sydney":
            messagebox.showerror("Error", "Please enter a valid city name.")
            return
            
        try:
            # Disable button during API call
            self.search_btn.config(state="disabled")
            self.update()
            
            # Fetch current weather data
            current_response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}"
            )
            current_data = current_response.json()
            
            if current_data.get('cod') != 200:
                messagebox.showerror("Error", current_data.get('message', 'City not found. Please try again.'))
                return
                
            # Fetch 5-day forecast data for hourly predictions
            forecast_response = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={API_KEY}"
            )
            forecast_data = forecast_response.json()
            
            if forecast_data.get('cod') != "200":
                messagebox.showerror("Error", "Could not fetch forecast data.")
                return
                
            # Process weather data
            self.display_current_weather(current_data, unit)
            self.display_hourly_forecast(forecast_data, unit)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            # Re-enable button
            self.search_btn.config(state="enabled")
    
    def display_current_weather(self, data, unit):
        # Clear previous weather display
        for widget in self.current_weather_frame.winfo_children():
            widget.destroy()
        
        # Extract data
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description'].title()
        weather_main = data['weather'][0]['main']
        icon = self.weather_icons.get(weather_main, "🌡️")
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        
        # Unit symbols
        temp_unit = "°C" if unit == "metric" else "°F"
        speed_unit = "m/s" if unit == "metric" else "mph"
        
        # Create layout
        # Header with city and icon
        header_frame = ttk.Frame(self.current_weather_frame, style='Weather.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))
        
        city_label = ttk.Label(header_frame, text=f"{city}, {country}", 
                              font=("Arial", 20, "bold"), style='Weather.TLabel')
        city_label.pack(side="left")
        
        icon_label = ttk.Label(header_frame, text=icon, font=("Arial", 24), style='Weather.TLabel')
        icon_label.pack(side="right", padx=10)
        
        # Weather details
        details_frame = ttk.Frame(self.current_weather_frame, style='Weather.TFrame')
        details_frame.pack(fill="x", pady=10)
        
        # Left column
        left_frame = ttk.Frame(details_frame, style='Weather.TFrame')
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Main temperature
        temp_label = ttk.Label(left_frame, text=f"{temp}{temp_unit}", 
                             font=("Arial", 36, "bold"), style='Weather.TLabel')
        temp_label.pack(anchor="w")
        
        # Weather description
        desc_label = ttk.Label(left_frame, text=description, font=("Arial", 14), 
                             style='Weather.TLabel')
        desc_label.pack(anchor="w", pady=(0, 10))
        
        # Feels like
        feels_label = ttk.Label(left_frame, text=f"Feels like: {feels_like}{temp_unit}", 
                              font=("Arial", 12), style='Weather.TLabel')
        feels_label.pack(anchor="w")
        
        # Right column
        right_frame = ttk.Frame(details_frame, style='Weather.TFrame')
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Weather details
        ttk.Label(right_frame, text=f"Humidity: {humidity}%", font=("Arial", 12), 
                 style='Weather.TLabel').pack(anchor="w", pady=2)
        ttk.Label(right_frame, text=f"Wind: {wind_speed} {speed_unit}", font=("Arial", 12), 
                 style='Weather.TLabel').pack(anchor="w", pady=2)
        ttk.Label(right_frame, text=f"Sunrise: {sunrise}", font=("Arial", 12), 
                 style='Weather.TLabel').pack(anchor="w", pady=2)
        ttk.Label(right_frame, text=f"Sunset: {sunset}", font=("Arial", 12), 
                 style='Weather.TLabel').pack(anchor="w", pady=2)

    def display_hourly_forecast(self, data, unit):
        # Clear previous hourly forecast
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        
        # Get the first 5 forecast items (3-hour intervals)
        forecasts = data['list'][:5]
        timezone_offset = data['city']['timezone']
        
        # Unit symbols
        temp_unit = "°C" if unit == "metric" else "°F"
        
        # Create a frame for the hourly boxes
        hourly_container = ttk.Frame(self.hourly_frame, style='Hourly.TFrame')
        hourly_container.pack(fill="both", expand=True, pady=10)
        
        for i, forecast in enumerate(forecasts):
            # Create frame for each hour
            hour_frame = ttk.Frame(hourly_container, style='Hourly.TFrame', padding=(10, 10))
            hour_frame.grid(row=0, column=i, padx=5, sticky="nsew")
            hourly_container.columnconfigure(i, weight=1)
            
            # Calculate local time
            dt = datetime.fromtimestamp(forecast['dt'] + timezone_offset)
            time_str = dt.strftime('%H:%M')
            
            # Weather data
            temp = forecast['main']['temp']
            weather_main = forecast['weather'][0]['main']
            icon = self.weather_icons.get(weather_main, "🌡️")
            description = forecast['weather'][0]['description'].title()
            
            # Display time
            time_label = ttk.Label(hour_frame, text=time_str, font=("Arial", 12, "bold"), 
                                 style='Hourly.TLabel')
            time_label.pack(pady=(0, 5))
            
            # Display icon
            icon_label = ttk.Label(hour_frame, text=icon, font=("Arial", 24), 
                                 style='Hourly.TLabel')
            icon_label.pack()
            
            # Display temperature
            temp_label = ttk.Label(hour_frame, text=f"{temp}{temp_unit}", 
                                 font=("Arial", 14), style='Hourly.TLabel')
            temp_label.pack(pady=(5, 0))
            
            # Display weather description
            desc_label = ttk.Label(hour_frame, text=description, font=("Arial", 10), 
                                 style='Hourly.TLabel', wraplength=80)
            desc_label.pack(pady=(5, 0))

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()