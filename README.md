# fetch-webpages

## Overview
This repository contains a Python-based application designed to fetch and download web pages and their associated assets. Additionally, the application provides an option to display metadata about the fetched pages.

## Features:
- Fetch specified web pages and download them to an output directory.
- Download assets (images, scripts, stylesheets) related to the fetched pages.
- Option to display metadata about the fetched pages, including the number of links, the number of images, and the date of the last fetch.

## Prerequisites:
1. Ensure you have Docker installed on your system to build and run the containerized application.
2. Ensure you have cloned this repository to your local machine and changed into the directory.

## How to Run:

1. **Build Docker Image**:
    ```
    docker build -t fetch-webpages .
    ```

2. **Run Tests**:
    ```
    docker run fetch-webpages -m unittest discover tests
    ```

3. **Fetch and Download Web Pages**:
    To download web pages and their assets and also display metadata, use the following command:
    ```
    docker run -v $PWD/output:/app/output --env-file .env fetch-webpages fetch.py --metadata autify.com www.google.com
    ```
   
4. **Check results**:
    Make sure the sites are fetched properly using the following command to open them in a browser (macOS):
    ```
    open output/autify.com/index.html
    open output/www.google.com/index.html
    ```

## Code Structure:
The application consists of various components:
- **fetch.py**: The main script.
- **lib/**: A directory containing helper libraries.
- **tests/**: Contains unit tests for the downloader and parser modules.

## Contribute:
Feel free to fork this repository, make changes, and submit pull requests.

