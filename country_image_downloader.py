import json
import os
import urllib.request
import ssl
import traceback

def convert_country_name(name):
    """
    Convert country name to lowercase and replace spaces with hyphens
    """
    return name.lower().replace(' ', '-')

def download_country_images(json_file):
    """
    Download country image thumbnails with comprehensive logging
    """
    # Validate JSON file exists
    if not os.path.exists(json_file):
        print(f"Error: JSON file {json_file} does not exist!")
        return []

    # Create output directory if it doesn't exist
    output_dir = 'country_images'
    os.makedirs(output_dir, exist_ok=True)
    
    # List to track countries with download failures
    failed_downloads = []
    successful_downloads = []
    
    # Bypass SSL certificate verification (use cautiously)
    context = ssl._create_unverified_context()
    
    # Read the JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            countries = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
        return []
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

    # Print total number of countries
    print(f"Total countries in JSON: {len(countries)}")
    
    # Download images
    for country in countries:
        # Convert country name to URL-friendly format
        country_name = convert_country_name(country['name'])
        
        # Construct the image URL
        image_url = f'https://static.travala.com/resources/images-pc/countries/thumbnail/thumbnail-{country_name}.jpg'
        
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
            output_path = os.path.join(output_dir, f'{country_name}.jpg')
            
            # Download the image
            with urllib.request.urlopen(req, context=context) as response:
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.read())
            
            print(f'Successfully downloaded image for {country["name"]}')
            successful_downloads.append(country['name'])
        
        except urllib.error.HTTPError as e:
            print(f'HTTP Error {e.code} for {country["name"]}: {image_url}')
            failed_downloads.append(country['name'])
        except Exception as e:
            print(f'Failed to download image for {country["name"]}: {image_url}')
            print(f'Error details: {traceback.format_exc()}')
            failed_downloads.append(country['name'])
    
    # Print summary
    print(f"\nTotal successful downloads: {len(successful_downloads)}")
    print(f"Total failed downloads: {len(failed_downloads)}")
    
    # Print failed downloads
    if failed_downloads:
        print('\nCountries with failed downloads:')
        for country in failed_downloads:
            print(country)
    
    # Write failed and successful downloads to files
    with open('successful_downloads.txt', 'w') as f:
        for country in successful_downloads:
            f.write(f'{country}\n')
    
    with open('failed_downloads.txt', 'w') as f:
        for country in failed_downloads:
            f.write(f'{country}\n')
    
    return failed_downloads

# Example usage
if __name__ == '__main__':
    # Assumes your JSON file is named 'countries.json' in the same directory
    failed = download_country_images('countries.json')

    print("Script execution completed.")