API Testing and Troubleshooting Guide

1. Overview

This document provides guidelines for testing and troubleshooting API functionality in the weather analysis script. It covers status code validation, error handling, testing scenarios, and debugging techniques.

2. Status Code Validation

The script makes API requests to OpenWeatherMap and Google Gemini. It is crucial to check the HTTP response status codes to ensure correct functionality.

OpenWeatherMap API Responses:

200 OK: Successful request.

400 Bad Request: Incorrect or missing parameters.

401 Unauthorized: Invalid API key.

404 Not Found: Location not found.

500 Internal Server Error: Server issue on OpenWeatherMap's end.

Gemini API Responses:

200 OK: Successful response.

400 Bad Request: Malformed request.

401 Unauthorized: Invalid API key.

429 Too Many Requests: Rate limit exceeded.

500 Internal Server Error: Issue with Google's servers.

3. Error Handling Implementation

The script uses try-except blocks to handle API request failures. The following strategies are applied:

OpenWeatherMap API Error Handling:

except requests.exceptions.RequestException as e:
    logging.error(f"API request failed: {e}")
    return None, None
except KeyError:
    logging.error("Unexpected response format from API.")
    return None, None
except ValueError as e:
    logging.error(e)
    return None, None

Gemini API Error Handling:

except Exception as e:
    logging.error(f"Gemini API error: {e}")
    return "Weather analysis unavailable at the moment."

4. Testing Scenarios

The script should be tested with various inputs to ensure robustness. Here are key test cases:

4.1 Successful Case

Input:

cityname = "Stamford"
statecode = "CT"
countrycode = "US"

Expected Outcome:

OpenWeatherMap returns valid latitude and longitude.

Weather data is fetched successfully.

Gemini API generates an AI-based weather analysis.

4.2 Invalid API Key

Setup:

Set an incorrect API key in .env:

OWM_API_KEY="INVALID_KEY"
GEMINI_API_KEY="INVALID_KEY"

Expected Outcome:

OpenWeatherMap returns 401 Unauthorized.

Gemini API fails authentication.

Logged errors: API request failed: 401 Client Error.

Output: Failed to retrieve weather data.

4.3 Invalid Location Input

Input:

cityname = "InvalidCity"
statecode = "XX"
countrycode = "ZZ"

Expected Outcome:

OpenWeatherMap returns 404 Not Found or an empty response.

Logged error: No location data found. Check city/state/country inputs.

Output: Failed to retrieve weather data.

4.4 API Rate Limit Exceeded

Expected Outcome:

OpenWeatherMap or Gemini API returns 429 Too Many Requests.

Logged error: API request failed: 429 Too Many Requests.

Output: Failed to retrieve weather data.

5. Debugging and Troubleshooting

Step 1: Check Environment Variables

Ensure API keys are set correctly:

print(os.getenv("OWM_API_KEY"))
print(os.getenv("GEMINI_API_KEY"))

Step 2: Verify API Response

Manually test API endpoints using curl:

curl -X GET "http://api.openweathermap.org/geo/1.0/direct?q=Stamford,CT,US&appid=YOUR_OWM_API_KEY"

Step 3: Enable Debug Logging

Modify logging level for more details:

logging.basicConfig(level=logging.DEBUG)