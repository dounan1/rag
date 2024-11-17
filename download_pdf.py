
import subprocess

def download_pdf(url, pdf_file_name):
    # Define the curl command
    curl_command = [
        "curl",
        "-f",
        "-u", "demo:ce544b6ea52a5621fb9d55f8b542d14d",
        "-o", pdf_file_name,
        "-F", "content_viewport_width=balanced",
        "-F", f"content_fit_mode=smart-scaling",
        "-F", f"url={url}",
        "https://api.pdfcrowd.com/convert/24.04/"
    ]

    try:
        # Run the curl command
        subprocess.run(curl_command, check=True)
        print(f"PDF successfully downloaded as {pdf_file_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Get input from the user
    url = input("Enter the URL to convert to PDF: ").strip()
    pdf_file_name = input("Enter the name for the output PDF file (e.g., example.pdf): ").strip()

    # Download the PDF
    download_pdf(url, pdf_file_name)


# From curl:
# curl -f -u demo:ce544b6ea52a5621fb9d55f8b542d14d \
#     -o example.pdf \
#     -F content_viewport_width=balanced \
#     -F url=https://teenage.engineering/products \
#     https://api.pdfcrowd.com/convert/24.04/
