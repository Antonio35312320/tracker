# Phone Number Tracker

Phone Number Tracker is a Python application built using Tkinter and various APIs to fetch and display information about a phone number. It provides details such as country, operator, timezone, geographical coordinates, and more.

## Features

- Validate phone numbers using `phonenumbers` library.
- Fetch and display country, operator (SIM provider), and timezone information.
- Retrieve longitude and latitude coordinates using `geopy` and display city and state information.
- Show current phone time based on the detected timezone.
- Option to view the phone's location on Google Maps.
- History feature to store previously searched phone numbers.
- Export history to a CSV file.
- Copy detailed information to the clipboard.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/phone-number-tracker.git
   ```
   
2. Navigate into the project directory:
   ```bash
   cd phone-number-tracker
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python phone_number_tracker.py
   ```

## Dependencies

- `tkinter`: Python's de-facto standard GUI package.
- `phonenumbers`: Library for parsing, formatting, storing, and validating international phone numbers.
- `timezonefinder`: Provides fast and accurate timezone calculations using latitude and longitude.
- `geopy`: A Python client for several popular geocoding web services.
- `pytz`: World timezone definitions, modern and historical timezone calculations.
- `pyperclip`: A cross-platform Python module for copying text to the clipboard.

## Usage

1. Enter a phone number including the country code in the provided entry box.
2. Click on the "Search" button to fetch and display information about the phone number.
3. The information such as country, SIM operator, timezone, geographical coordinates, city, state, and phone time will be displayed.
4. Use the "Show on Map" button to open Google Maps and view the location based on latitude and longitude (if available).
5. The history of searched phone numbers is displayed on the left. Clicking on a history item loads its details.
6. Use the "Clear History" button to remove all entries from the history list.
7. The "Export History" option in the menu exports the history of searched phone numbers to a CSV file named `phone_number_history.csv`.
8. Use the "Copy to Clipboard" button to copy all displayed details to the clipboard for easy sharing or saving.


