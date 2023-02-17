import os
import requests
import xmlrpc.client

def download_subtitles(movie_name):
    # Connect to OpenSubtitles API
    client = xmlrpc.client.ServerProxy("http://api.opensubtitles.org/xml-rpc")
    
    # Login to OpenSubtitles API
    user_agent = "Wget/1.19.4 (linux-gnu)"
    token = client.LogIn("", "", "en", user_agent)["token"]
    
    # Search for subtitles by movie name
    results = client.SearchSubtitles(token, [{"query": movie_name, "sublanguageid": "eng"}])
    
    # Check if the API call returned an error
    if "data" not in results:
        print("Error:", results["status"])
        return
    
    # Check if any subtitles were found
    if len(results["data"]) == 0:
        print("No subtitles found for movie:", movie_name)
        return
    
    # Display a list of subtitle choices
    print("\nSubtitle choices:")
    for i, subtitle in enumerate(results["data"]):
        print(f"{i + 1}. {subtitle['SubFileName']}")
    
    # Prompt the user to select a subtitle
    choice = int(input("\nEnter your choice (1-{}): ".format(len(results["data"]))))
    subtitle_url = results["data"][choice - 1]["ZipDownloadLink"]
    
    # Specify the download directory
    download_dir = r"C:\Desktop"
    
    # Download the subtitle file
    response = requests.get(subtitle_url)
    file_path = os.path.join(download_dir, f"{movie_name}.zip")
    with open(file_path, "wb") as f:
        f.write(response.content)
    
    # Logout from OpenSubtitles API
    client.LogOut(token)
    
    print("Subtitle downloaded to:", file_path)

# Example usage
movie_name = "TYPE_MOVIE_NAME_HERE"
download_subtitles(movie_name)
