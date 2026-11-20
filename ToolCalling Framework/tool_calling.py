import json
from datetime import datetime


# =========================================================
# WEATHER DATA
# =========================================================

WEATHER_DATA = {
    "Bangalore": {
        "temperature": "28°C",
        "condition": "Cloudy"
    },
    "Hyderabad": {
        "temperature": "31°C",
        "condition": "Sunny"
    },
    "Delhi": {
        "temperature": "35°C",
        "condition": "Hot"
    }
}


# =========================================================
# WEATHER TOOL
# =========================================================

def get_weather(city):
    """
    Returns weather information for the given city.
    """

    # Match city name without case sensitivity
    for city_name, weather in WEATHER_DATA.items():
        if city_name.lower() == city.lower():
            return weather

    return {
        "temperature": "Unknown",
        "condition": "City Not Found"
    }


# =========================================================
# TOOL SCHEMA
# =========================================================

WEATHER_SCHEMA = {
    "name": "get_weather",
    "description": "Get weather information for a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city."
            }
        },
        "required": ["city"]
    }
}


# =========================================================
# TOOL DISPATCHER
# =========================================================

def dispatch_tool(request):
    """
    Checks the tool request and calls the correct tool.
    """

    tool_name = request.get("tool")

    # Check whether the tool exists
    if tool_name != "get_weather":
        return {
            "status": "error",
            "message": f"Tool '{tool_name}' not found."
        }

    # Get arguments
    arguments = request.get("arguments", {})

    # Check required parameter
    if "city" not in arguments:
        return {
            "status": "error",
            "message": "Missing required parameter: city."
        }

    city = arguments["city"]

    # Validate city type
    if not isinstance(city, str):
        return {
            "status": "error",
            "message": "City must be a string."
        }

    # Call weather tool
    weather_result = get_weather(city)

    return {
        "status": "success",
        "result": weather_result
    }


# =========================================================
# MAIN CHAT PROGRAM
# =========================================================

def main():

    print("=" * 55)
    print("             WEATHER TOOL CALLING CHAT")
    print("=" * 55)

    print("Enter a city name to get its weather.")
    print("Available cities: Bangalore, Hyderabad, Delhi")
    print("Type 'exit' to stop the program.")

    print("=" * 55)

    while True:

        city = input("\nYou: ").strip()

        # Exit program
        if city.lower() == "exit":
            print("\nBot: Goodbye!")
            break

        # Check empty input
        if not city:
            print("Bot: Please enter a city name.")
            continue

        # -------------------------------------------------
        # CREATE TOOL REQUEST
        # -------------------------------------------------

        tool_request = {
            "tool": "get_weather",
            "arguments": {
                "city": city
            }
        }

        print("\n--- Tool Request ---")
        print(json.dumps(tool_request, indent=4))

        # -------------------------------------------------
        # CALL TOOL DISPATCHER
        # -------------------------------------------------

        tool_response = dispatch_tool(tool_request)

        print("\n--- Tool Response ---")
        print(json.dumps(tool_response, indent=4))

        # -------------------------------------------------
        # DISPLAY FINAL RESPONSE
        # -------------------------------------------------

        if tool_response["status"] == "success":

            weather = tool_response["result"]

            if weather["condition"] == "City Not Found":
                print(f"\nBot: Sorry, I don't have weather data for {city}.")
            else:
                print(
                    f"\nBot: The weather in {city.title()} is "
                    f"{weather['temperature']} and "
                    f"{weather['condition']}."
                )

        else:
            print(f"\nBot: {tool_response['message']}")


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    main()

    print("\n" + "=" * 55)
    print("Program finished at:")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 55)