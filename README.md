# Web Scraper for YallaKora Match Schedule

This is a Python script that performs web scraping on the YallaKora website to retrieve the schedule of matches for a specific date. The script extracts relevant information from the HTML content and saves the data in a CSV file.

## Prerequisites

To run this script, you need to have the following:

- Python: Make sure Python is installed on your machine. You can download it from the official Python website: https://www.python.org/downloads/

## Getting Started

1. Clone the repository or download the `scraper.py` file.

2. Open a terminal or command prompt and navigate to the directory where `scraper.py` is located.

3. Install the required Python packages by running the following command:

   ```
   pip install requests beautifulsoup4
   ```

4. Run the script by executing the following command:

   ```
   python scraper.py
   ```

5. The script will prompt you to enter a date in the format `MM/DD/YYYY`. Enter the desired date and press Enter.

6. The script will scrape the YallaKora website for the matches on that date and save the data in a CSV file.

   - If no matches are found for the selected date, a file named `matches-<date>.csv` will be created in the `csv/` directory, containing a single row indicating that no matches were found.
   
   - If matches are found, a file named `matches-<date>.csv` will be created in the `csv/` directory, containing the details of each match in separate rows.

7. Check the `csv/` directory for the generated CSV file.

## Project Structure

The project directory contains the following files and directories:

- `scraper.py`: The main Python script that performs the web scraping. It contains functions to fetch the HTML content, extract match details, create a CSV file, and handle user input. The `main()` function serves as the entry point for the script.

- `csv/`: A directory where the generated CSV files will be stored. The script creates a separate CSV file for each date.

## Disclaimer

Please note that web scraping can be subject to the website's terms of service. Make sure to review the website's policies and terms before scraping its content. Be mindful of the legality and ethics of scraping specific websites and respect the website's guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This script was developed using the `requests` library to fetch web content and the `beautifulsoup4` library for HTML parsing. Special thanks to the authors and contributors of these libraries.