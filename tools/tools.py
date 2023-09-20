import requests
import json
import re
from bs4 import BeautifulSoup

def get_website_content(url: str):

    """Scrape a website content"""
    
    from requests import get, exceptions
    from bs4 import BeautifulSoup

    if not url.startswith("https://"):
        url = "https://" + url
    
    try:
        # Send an HTTP GET request to the URL
        response = get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the HTML content
            html_content = response.text
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find and remove all script and style tags and their contents
            for script in soup(['script', 'style']):
                script.extract()
            
            # Get the text content of the remaining elements
            text_content = soup.get_text()
            
            # Remove extra whitespaces and line breaks
            #cleaned_content = re.sub(r'\s+', ' ', text_content).strip()
            
            if url[-4:] == ".pdf":
                text_content = extract_text_from_pdf(text_content)

            cleaned_content = re.sub(r'\s+', ' ', text_content).strip()

            return cleaned_content
        
        else:
            # If the request was not successful, raise an exception
            response.raise_for_status()
    
    except exceptions.RequestException as e:
        # Handle exceptions such as network errors or invalid URLs
        print(f"An error occurred: {e}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def extract_text_from_pdf(pdf_content):
    
    import PyPDF2

    try:
        # Create a PDF object from the provided content
        pdf = PyPDF2.PdfReader(pdf_content)
        
        # Initialize a variable to store extracted text
        extracted_text = ""
        
        # Iterate through each page and extract text
        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            extracted_text += page.extractText()
        
        return extracted_text
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def google_search_2(query, num_results=10):

    # Define the base Google search URL
    base_url = "https://www.google.com/search"

    # Set up headers with a User-Agent to mimic a web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Set up the query parameters
    params = {
        "q": query,
        "num": num_results
    }

    # Send a GET request to Google with headers
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find and remove specific elements like script and style tags
        for tag in soup(["script", "style"]):
            tag.extract()

        # Extract and clean up the text content
        text_content = soup.get_text()
        cleaned_text = re.sub(r'\s+', ' ', text_content).strip()

        return cleaned_text
    else:
        # Request was not successful
        return json.dumps({"error": "Failed to fetch Google search results"}, indent=2)