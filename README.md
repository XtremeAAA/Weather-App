# Weather Forecast App

This is a desktop weather application built with Python and Tkinter that provides current weather conditions and a 5-hour forecast for any city worldwide.

## Features

- Current weather display with temperature, feels-like, humidity, wind speed, sunrise, and sunset times
- 5-hour weather forecast with temperature and conditions
- Temperature unit selection (Celsius/Fahrenheit)
- Responsive and modern UI with weather icons
- Timezone-adjusted time displays
- Error handling for invalid city names

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Step 1: Install Python
- **Windows**: Download from [python.org](https://python.org) and run the installer
- **macOS**: Use Homebrew: `brew install python` or download from [python.org](https://python.org)
- **Linux**: Use package manager:
  ```bash
  # Debian/Ubuntu
  sudo apt update
  sudo apt install python3 python3-pip
  
  # Fedora
  sudo dnf install python3 python3-pip
  ```

### Step 2: Install Required Modules
Open a terminal or command prompt and run:

```bash
pip install requests
```

### Step 3: Get an API Key
1. Go to [OpenWeatherMap](https://openweathermap.org) and create a free account
2. Navigate to the [API Keys section](https://home.openweathermap.org/api_keys)
3. Copy your API key

### Step 4: Configure the App
Open the Python file in a text editor and replace the placeholder API key with your own:

```python
API_KEY = 'your_api_key_here'  # Replace with your actual API key
```

## Usage

1. Run the application:
   ```bash
   python weather_app.py
   ```
2. Enter a city name in the input field (e.g., "London" or "New York")
3. Select your preferred temperature unit (Celsius or Fahrenheit)
4. Click "Get Weather"
5. View current weather conditions and 5-hour forecast

## Troubleshooting

- **Invalid city name**: Ensure you've entered a valid city name
- **API key issues**: Verify your OpenWeatherMap API key is correct and activated
- **Network connection**: Make sure you have an active internet connection
- **Module errors**: Ensure you've installed the required modules with pip