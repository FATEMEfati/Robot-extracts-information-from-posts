***Instagram Post Extractor Script***
# Overview
This Python script automates the process of extracting detailed information from Instagram posts. It logs into Instagram (if credentials are provided), navigates to specified post URLs, and extracts metadata such as likes, comments, article info, post date, and description. The results are saved into a JSON file for further analysis or record-keeping.

## Features
Headless Chrome WebDriver for scraping
Supports proxy configuration
Instagram login automation
Extracts post metadata including likes, comments, article, date, and description
Handles multiple URLs from a text file
Appends results to an existing JSON output file
Logs detailed process and error messages
Prerequisites
Python 3.x installed

## Required Python libraries:

selenium
instagrapi
re (standard library)
json (standard library)
logging (standard library)
argparse (standard library)
sys (standard library)
os (standard library)
time (standard library)
Chrome WebDriver installed and accessible in your PATH

## Installation
Clone or download this repository.
First create your virtual environment.
```bash
python -m venv myenv
```
then:
```bash
.\myenv\Scripts\activate
```
Install the required packages:
```bash
pip install -r requirements.txt
```
Download ChromeDriver compatible with your Chrome browser version from
here
and ensure it is in your system PATH or specify its location.

# Usage
## Login to Instagram
To log in before scraping:
```bash
python .\main.py login --username YOUR_USERNAME --password YOUR_PASSWORD
```
# Use Proxy (Optional)
```bash
python .\main.py proxy --proxy http://proxyserver:port
```
This script has the ability to connect to proxies that do not require authentication.
 # Running the Script
 
 Basic usage with URLs file and output file:
 ```bash
python .\main.py --links links.txt --output posts.json
```
If you do not specify the link and output file, by default the output name is instagram_posts.json and the input file is links.txt. The input file should be a list of links written as follows, for example:
```bash
https://www.instagram.com/reel/example1/?igsh=emV3dWU2bGI0OTQy

https://www.instagram.com/reel/example2/?igsh=czk0bnc0cnJuNmxr

https://www.instagram.com/reel/example3/?igsh=bWNiNW1qYmM3bGo4
```
And the output file should be a file containing a list.

# files
links.txt : Text file containing Instagram post URLs, one per line.
instagram_extractor.log : Log file recording process details and errors.
posts.json : Output JSON file with extracted post data (created or appended).

# Notes
Ensure your Instagram credentials are correct.
The script relies on Instagram's page structure and meta descriptions, which may change over time.
For large batches, consider adding delays or handling rate limits accordingly.
Use headless mode for faster operation, but you can disable headless by modifying the options in the script if needed.

# Troubleshooting
WebDriver issues: Ensure ChromeDriver is correctly installed and compatible with your Chrome version.
Login failures: Verify credentials and two-factor authentication settings.
Extraction errors: Check if Instagram page structures have changed; update regex patterns if necessary.
Proxy issues: Confirm the proxy address is correct and functional.
