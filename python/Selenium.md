# Baidu Search with Selenium

This Python script uses Selenium to automatically open Baidu.com and search for a keyword.

## Prerequisites

1. Python 3.x installed
2. Google Chrome browser installed
3. ChromeDriver matching your Chrome version

## Setup Instructions

1. Install required Python packages:
   ```
   pip install selenium
   ```

2. Download ChromeDriver:
   - Check your Chrome version by going to `chrome://settings/help` in your browser
   - Download the matching ChromeDriver version from https://chromedriver.chromium.org/
   - Extract the chromedriver.exe file

3. Place ChromeDriver:
   - Put chromedriver.exe in one of these locations:
     - `./driver/chromedriver.exe` (inside this project's driver folder)
     - Or in your system PATH

## Usage

Run the script:
```
python baidu_search.py
```

The script will:
1. Open Google Chrome
2. Navigate to www.baidu.com
3. Search for "你好"
4. Display the page title
5. Close the browser

## Troubleshooting

- If you get "ChromeDriver not found" error, make sure chromedriver.exe is in the correct location
- If you get version mismatch errors, ensure ChromeDriver version matches your Chrome browser version