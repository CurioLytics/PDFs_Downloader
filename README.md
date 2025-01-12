## Inspiration
The idea for this project originated from my workflow. I often need to download all course files and store them in NotebookLM. However, this process is repetitive, which led me to think about automating it.

## Constraints:
No Multiple Authentications:
The program can only authenticate once during the session. It cannot handle multiple logins or switch between accounts in a single run. The session must remain active throughout the entire process of downloading PDFs.

PDF Files Only:
This program is designed to download only PDF files. It will automatically filter out non-PDF resources or any other file types. If a link does not lead to a PDF file, it will be ignored. Any attempt to download non-PDF files (e.g., images, videos, etc.) will not be executed.

## Required Inputs: (Use the same pattern as the examples provided)
ChromeDriver Path:
"C:\Users\admin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

Login URL:
https://lms.neu.edu.vn/login/index.php

Username:
<<>>

Password:
<<>>

Course URL:
https://lms.neu.edu.vn/course/view.php?id=47173

Directory to save downloaded files:
C:\Users\admin\Downloads\Lya\Web_Scraper\downloaded_files


## Outputs: All pdf files (as in the folder "downloaded_files")

## Structure
Imports

Function: init_webdriver
Function: login_to_lms
Function: get_pdf_links
Function: download_pdfs

Main Function: main
Execution: if __name__ == "__main__": main()

## Future Development Ideas
- Create a User Interface
- Handle Multiple Authentications
- Support Additional File Types
