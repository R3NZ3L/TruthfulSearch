from bs4 import BeautifulSoup
import re
import requests
import json


def getLinksFromAbout(channel_id, channel_name):
    x = requests.get(f'https://www.youtube.com/channel/{channel_id}/about')

    soup = BeautifulSoup(x.content, 'html.parser')

    scripttags = soup.find_all("script")

    for script in scripttags:
        results = re.search(r"var ytInitialData = {.*}", script.text) 
        if results is not None:
            object = results.group(0).replace("var ytInitialData = ", "")
            try:
                link_information =  (json.loads(object) ['onResponseReceivedEndpoints'][0]
                                    ['showEngagementPanelEndpoint']
                                    ['engagementPanel']
                                    ['engagementPanelSectionListRenderer']
                                    ['content']
                                    ['sectionListRenderer']
                                    ['contents'][0]
                                    ['itemSectionRenderer']
                                    ['contents'][0]
                                    ['aboutChannelRenderer']
                                    ['metadata']
                                    ['aboutChannelViewModel']
                                    ['links']
                                    )
            except:
                print("No links provided for:", {channel_name})
            else:
                print("Available links provided for:", {channel_name})
                for link in link_information:   #print all available links from the about modal
                    print(f"{link['channelExternalLinkViewModel']['title']['content']}: {link['channelExternalLinkViewModel']['link']['content']}")
            print("---------------------------------------")


channels = {
                'UCvi6hEzLM-Z_unKPSuuzKvg' : 'ANC 24/7', 
                'UCvRAX-ujvZ0eTMLGG2vki9w': 'INQUIRER.net', 
                'UCdnZdQxYXnbN4uWJg96oGxw': 'Rappler',
                'UCNye-wNBqNL5ZzHSJj3l8Bg': 'Al Jazeera English',
                'UCqYw-CTd1dU2yGI71sEyqNw': 'GMA Integrated News',
            }

for channel_id, channel_name in channels.items():
    getLinksFromAbout(channel_id, channel_name)


