import sys
import requests
from urllib.parse import urlparse


 
def fuzz_web_application(file_path, target_url, allowed_status_codes):
    banner = r"""
                         
    """

    headings = ["URI", "Status Code"]
    col_widths = [max(len(heading), 8) for heading in headings]  
    uri_col_width = col_widths[0]
    status_code_width = 10  # Fixed width for the status code column
  
    print(banner)
    print("\n")
    print("{:<{}}  {:>{}}".format(headings[0], uri_col_width, headings[1], status_code_width))
    print("-" * (sum(col_widths) + status_code_width + 2))

    with open(file_path, 'r') as file:
        for line in file:
            entry = line.strip()
            url = f"http://{target_url}/{entry}"  # Construct the URL with the directory path

            try:
                response = requests.get(url, stream=True)
                uri = urlparse(url).path  # Extract the URI from the URL
                status_code = str(response.status_code)

                if status_code in allowed_status_codes:
                    print("{:<{}}  {:>{}}".format(uri, uri_col_width, status_code, status_code_width))
            except requests.exceptions.RequestException:
                pass

    print("-" * (sum(col_widths) + status_code_width + 2))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python fuzz.py <file_path> <target_url> <status_codes>")
        sys.exit(1)

    file_path = sys.argv[1]
    target_url = sys.argv[2]
    allowed_status_codes = sys.argv[3].split(',')

    if not file_path.endswith('.txt'):
        print("Error: The input file must be a text file (.txt)")
        sys.exit(1)

    fuzz_web_application(file_path, target_url, allowed_status_codes)
