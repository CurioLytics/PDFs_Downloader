import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize the WebDriver
def init_webdriver(chromedriver_path, headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to login to the LMS
def login_to_lms(driver, login_url, username, password):
    driver.get(login_url)
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "loginbtn")
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    time.sleep(5)  # Adjust for page load time
    
    # Check if login was successful
    try:
        success_element = driver.find_element(By.ID, "instance-445733-header")
        print("Đã tìm thấy:", success_element.text)
    except Exception as e:
        print("Login failed. Error:", e)
        return False
    return True

# Function to get all PDF links from the course page
def get_pdf_links(driver, course_url):
    driver.get(course_url)
    links = driver.find_elements(By.TAG_NAME, "a")
    pdf_links = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("https://lms.neu.edu.vn/mod/resource/view.php?id="):
            pdf_links.append(href)
    return pdf_links

# Function to download PDF files
def download_pdfs(pdf_links, session_cookies, download_directory):
    for i, link in enumerate(pdf_links):
        try:
            print(f"Downloading: {link}")
            response = requests.get(link, cookies=session_cookies, stream=True)
            response.raise_for_status()
            
            file_path = f"{download_directory}\\file_{i + 1}.pdf"
            with open(file_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)
            print(f"Saved: {file_path}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")

# Main function to handle user inputs and orchestrate the workflow
def main():
    # User inputs and handling each step
    try:
        # Step 1: Get ChromeDriver path and initialize WebDriver
        chromedriver_path = input("Enter ChromeDriver path: ")
        driver = init_webdriver(chromedriver_path)
        print("WebDriver initialized successfully!")
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return

    try:
        # Step 2: Get LMS login details
        login_url = input("Enter the login URL: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Perform login
        if login_to_lms(driver, login_url, username, password):
            print("Login successful!")
        else:
            print("Login failed!")
            driver.quit()
            return
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return

    try:
        # Step 3: Get the course URL
        course_url = input("Enter the course URL: ")

        # Retrieve PDF links
        pdf_links = get_pdf_links(driver, course_url)
        if pdf_links:
            print("Collected PDF Links:")
            for pdf in pdf_links:
                print(pdf)
        else:
            print("No PDF links found!")
            driver.quit()
            return
    except Exception as e:
        print(f"Error retrieving PDF links: {e}")
        driver.quit()
        return

    try:
        # Step 4: Get directory to save downloaded files
        download_directory = input("Enter the directory to save downloaded files: ")

        # Get cookies and download PDFs
        selenium_cookies = driver.get_cookies()
        session_cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
        download_pdfs(pdf_links, session_cookies, download_directory)
        print("PDFs downloaded successfully!")
    except Exception as e:
        print(f"Error during download: {e}")
        driver.quit()
        return

    # Close WebDriver after completing all tasks
    driver.quit()

# Run the program
if __name__ == "__main__":
    main()
