Description

This project is a Python script that uses Selenium WebDriver to crawl a forum (specifically, the "What's New" section of the RoForum) and extract external links from the threads. The script performs the following tasks:

    Initializes the Selenium WebDriver with Chrome and sets up the Chrome profile settings.
    Defines a function append_external_link to append extracted links to a file, excluding unwanted links.
    Defines a function get_thread_links to retrieve thread links from the forum.
    Defines a function extract_external_links_from_thread to extract external links from a thread as the page scrolls.
    Defines a function paginate_within_thread to handle pagination within a thread.
    Defines a function close_popup to close any popups that may appear during the crawling process.
    Defines a function process_threads to process each thread and extract links.
    Defines a main function to orchestrate the crawling process, including error handling and closing the WebDriver.
    Executes the main function if the script is run as the main program.

Requirements

    Python 3.x
    Selenium WebDriver
    Chrome browser
    ChromeDriver

Installation

    Install Python 3.x if not already installed.
    Install Selenium WebDriver by running pip install selenium in your terminal.
    Download the appropriate version of ChromeDriver for your system from ChromeDriver Downloads and place it in a directory that is in your system's PATH.

Usage

    Clone the repository to your local machine.
    Install the required dependencies by running pip install -r requirements.txt.
    Run the script using the command python script_name.py.

Customization

To customize the script, you can modify the following variables:

    driver_path: The path to the ChromeDriver executable.
    forum_url: The URL of the forum to crawl.
    chrome_options: Add or remove Chrome options as needed.
    your-popup-close-button-selector: The CSS selector for the popup close button on the forum.

License

This project is licensed under the MIT License.
Contributing

To contribute to this project, please follow the guidelines in the CONTRIBUTING.md file.
