import json
import os
import urllib.request
import ssl
import traceback

def download_failed_country_images(failed_downloads_file):
    """
    Download country images for failed downloads from Holidify
    """
    # Create output directory for fallback images
    output_dir = 'fallback_country_images'
    os.makedirs(output_dir, exist_ok=True)
    
    # List to track countries with download failures
    new_failed_downloads = []
    successful_downloads = []
    
    # Bypass SSL certificate verification (use cautiously)
    context = ssl._create_unverified_context()
    
    # Read the failed downloads file
    try:
        with open(failed_downloads_file, 'r', encoding='utf-8') as f:
            failed_countries = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error reading failed downloads file: {e}")
        return []

    # Print total number of countries to download
    print(f"Total countries to download: {len(failed_countries)}")
    
    # Download images
    for country_name in failed_countries:
        # Convert country name to uppercase for Holidify URL
        country_name_upper = country_name.upper()
        
        # Construct the image URL
        image_url = f'https://www.holidify.com/images/bgImages/{country_name_upper}.jpg'
        
        try:
            # Comprehensive headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            # Create a request with headers
            req = urllib.request.Request(image_url, headers=headers)
            
            # Output path for the image
            output_path = os.path.join(output_dir, f'{country_name_upper}.jpg')
            
            # Download the image
            with urllib.request.urlopen(req, context=context) as response:
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.read())
            
            print(f'Successfully downloaded image for {country_name}')
            successful_downloads.append(country_name)
        
        except urllib.error.HTTPError as e:
            print(f'HTTP Error {e.code} for {country_name}: {image_url}')
            new_failed_downloads.append(country_name)
        except Exception as e:
            print(f'Failed to download image for {country_name}: {image_url}')
            print(f'Error details: {traceback.format_exc()}')
            new_failed_downloads.append(country_name)
    
    # Print summary
    print(f"\nTotal successful downloads: {len(successful_downloads)}")
    print(f"Total failed downloads: {len(new_failed_downloads)}")
    
    # Print failed downloads
    if new_failed_downloads:
        print('\nCountries with failed downloads:')
        for country in new_failed_downloads:
            print(country)
    
    # Write failed and successful downloads to files
    with open('fallback_successful_downloads.txt', 'w') as f:
        for country in successful_downloads:
            f.write(f'{country}\n')
    
    with open('fallback_failed_downloads.txt', 'w') as f:
        for country in new_failed_downloads:
            f.write(f'{country}\n')
    
    return new_failed_downloads

# Example usage
if __name__ == '__main__':
    # Use the previously generated failed downloads list
    failed = download_failed_country_images('failed_downloads.txt')

    print("Script execution completed.")
