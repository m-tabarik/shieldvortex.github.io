# import requests
# import argparse

# # Mask the user agent so it doesn't show as python and get blocked, set global for request that needs to allow for redirects
# # Get function to swap the user agent
# def get(websiteToScan):
#     global user_agent
#     user_agent = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
#     }
#     return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)

# # Begin scan
# def scan():
#     # Check to see if the site argument was specified
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s", "--site", help="Use this option to specify the domain or IP to scan.")
#     args = parser.parse_args()
#     if args.site is None:
#         # Get the input from the user
#         print("Please enter the site or IP you would like to scan below.")
#         print("Examples - www.site.com, https://store.org/magento, 192.168.1.50")
#         websiteToScan = input('Site to scan: ')
#     else:
#         websiteToScan = args.site

#     # Check the input for HTTP or HTTPS and then remove it, if nothing is found assume HTTP
#     if websiteToScan.startswith('http://'):
#         proto = 'http://'
#         websiteToScan = websiteToScan[7:]
#     elif websiteToScan.startswith('https://'):
#         proto = 'https://'
#         websiteToScan = websiteToScan[8:]
#     else:
#         proto = 'http://'

#     # Check the input for an ending / and remove it if found
#     if websiteToScan.endswith('/'):
#         websiteToScan = websiteToScan.strip('/')

#     # Combine the protocol and site
#     websiteToScan = proto + websiteToScan

#     # Check to see if the site is online
#     print("[+] Checking to see if the site is online...")

#     try:
#         onlineCheck = get(websiteToScan)
#     except requests.exceptions.ConnectionError as ex:
#         print("[!] " + websiteToScan + " appears to be offline.")
#     else:
#         if onlineCheck.status_code == 200 or onlineCheck.status_code == 301 or onlineCheck.status_code == 302:
#             print(" |  " + websiteToScan + " appears to be online.")
#             print("Beginning scan...")

#             redirectCheck = requests.get(websiteToScan, headers=user_agent)
#             if len(redirectCheck.history) > 0:
#                 if '301' in str(redirectCheck.history[0]) or '302' in str(redirectCheck.history[0]):
#                     print("[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!")
#                     print("[!] It appears the site is redirecting to " + redirectCheck.url)
#             elif 'meta http-equiv="REFRESH"' in redirectCheck.text:
#                 print("[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!")
#             else:
#                 print(" | Site does not appear to be redirecting...")
#         else:
#             print("[!] " + websiteToScan + " appears to be online but returned a " + str(onlineCheck.status_code) + " error.")
#             exit()

#         print("[+] Attempting to get the HTTP headers...")
#         # Pretty print( the headers - courtesy of Jimmy
#         for header in onlineCheck.headers:
#             try:
#                 print(" | " + header + " : " + onlineCheck.headers[header])
#             except Exception as ex:
#                 print("[!] Error: " + str(ex))

#         # ... (remaining code)

#         print("Scan is now complete!")

# # Call the scan function
# scan()
import requests
import argparse

# Mask the user agent so it doesn't show as python and get blocked, set global for request that needs to allow for redirects
# Get function to swap the user agent
def get(websiteToScan):
    global user_agent
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }
    return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)

# Function to detect WordPress
def detect_wordpress(websiteToScan):
    wp_paths = ['/wp-login.php', '/wp-admin', '/wp-admin/upgrade.php', '/readme.html']
    
    for path in wp_paths:
        wp_check = get(websiteToScan + path)
        if wp_check.status_code == 200 and "404" not in wp_check.text:
            print("[!] Detected: WordPress at " + websiteToScan + path)
        else:
            print(" |  Not Detected: WordPress at " + websiteToScan + path)

# Function to detect Joomla
def detect_joomla(websiteToScan):
    joomla_paths = ['/administrator/', '/readme.txt']
    
    for path in joomla_paths:
        joomla_check = get(websiteToScan + path)
        if joomla_check.status_code == 200 and "404" not in joomla_check.text:
            print("[!] Detected: Joomla at " + websiteToScan + path)
        else:
            print(" |  Not Detected: Joomla at " + websiteToScan + path)

# Function to detect Magento
def detect_magento(websiteToScan):
    magento_paths = ['/index.php/admin/', '/RELEASE_NOTES.txt', '/js/mage/cookies.js', '/skin/frontend/default/default/css/styles.css', '/errors/design.xml']
    
    for path in magento_paths:
        magento_check = get(websiteToScan + path)
        if magento_check.status_code == 200 and "404" not in magento_check.text:
            print("[!] Detected: Magento at " + websiteToScan + path)
        else:
            print(" |  Not Detected: Magento at " + websiteToScan + path)

# Function to detect Drupal
def detect_drupal(websiteToScan):
    drupal_paths = ['/readme.txt', '/core/COPYRIGHT.txt', '/modules/README.txt']
    
    for path in drupal_paths:
        drupal_check = get(websiteToScan + path)
        if drupal_check.status_code == 200 and "404" not in drupal_check.text:
            print("[!] Detected: Drupal at " + websiteToScan + path)
        else:
            print(" |  Not Detected: Drupal at " + websiteToScan + path)

# Function to detect phpMyAdmin
def detect_phpmyadmin(websiteToScan):
    phpmyadmin_paths = ['/index.php', '/config.inc.php']
    
    for path in phpmyadmin_paths:
        phpmyadmin_check = get(websiteToScan + path)
        if phpmyadmin_check.status_code == 200 and "404" not in phpmyadmin_check.text:
            print("[!] Detected: phpMyAdmin at " + websiteToScan + path)
        else:
            print(" |  Not Detected: phpMyAdmin at " + websiteToScan + path)

# Begin scan
def scan():
    # Check to see if the site argument was specified
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="Use this option to specify the domain or IP to scan.")
    args = parser.parse_args()
    if args.site is None:
        # Get the input from the user
        print("Please enter the site or IP you would like to scan below.")
        print("Examples - www.site.com, https://store.org/magento, 192.168.1.50")
        websiteToScan = input('Site to scan: ')
    else:
        websiteToScan = args.site

    # Check the input for HTTP or HTTPS and then remove it, if nothing is found assume HTTP
    if websiteToScan.startswith('http://'):
        proto = 'http://'
        websiteToScan = websiteToScan[7:]
    elif websiteToScan.startswith('https://'):
        proto = 'https://'
        websiteToScan = websiteToScan[8:]
    else:
        proto = 'http://'

    # Check the input for an ending / and remove it if found
    if websiteToScan.endswith('/'):
        websiteToScan = websiteToScan.strip('/')

    # Combine the protocol and site
    websiteToScan = proto + websiteToScan

    # Check to see if the site is online
    print("[+] Checking to see if the site is online...")

    try:
        onlineCheck = get(websiteToScan)
    except requests.exceptions.ConnectionError as ex:
        print("[!] " + websiteToScan + " appears to be offline.")
    else:
        if onlineCheck.status_code == 200 or onlineCheck.status_code == 301 or onlineCheck.status_code == 302:
            print(" |  " + websiteToScan + " appears to be online.")
            print("Beginning scan...")

            detect_wordpress(websiteToScan)
            detect_joomla(websiteToScan)
            detect_magento(websiteToScan)
            detect_drupal(websiteToScan)
            detect_phpmyadmin(websiteToScan)

        else:
            print("[!] " + websiteToScan + " appears to be online but returned a " + str(onlineCheck.status_code) + " error.")
            exit()

        print("[+] Attempting to get the HTTP headers...")
        # Pretty print( the headers - courtesy of Jimmy
        for header in onlineCheck.headers:
            try:
                print(" | " + header + " : " + onlineCheck.headers[header])
            except Exception as ex:
                print("[!] Error: " + str(ex))

        print("Scan is now complete!")

# Call the scan function
scan()
