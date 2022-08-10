import json
import requests
import boto3
import os

# Globals 
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',}
COOKIE = {'Conversation_UUID': 'ebb70b20-1852-11ed-8da1-db987a46d195', ' geolocation_aka_jar': '{"zipCode":"93101-93103+93105-93111+93120-93121+93130+93140+93150+93160+93190","region":"CA","country":"US","metro":"SANTABARBARA","metroCode":"855"}', ' localeCookie_jar_aka': '{"contentLocale":"en_US","version":"3","precedence":0,"akamai":"true"}', ' languageSelection_jar_aka': '{"preferredLanguage":"en_US","version":"1","precedence":0,"language":"en_US","akamai":"true"}', ' bm_sz': 'A7369335F5A53B192756D8F1C67FBDB7~YAAQKS0tF1/9ymaCAQAADh2NhRBK7SnCIxM1lPPIbIoz235y1IMSv6qFXLIT92CmfNkR67JRkdq+T+LUcufDyL4iQzw8hiI0abO5SalWNc+w9tpbiGuZEE6UlykatttaFP4p9QI7TVDXge5UN1WG9/Kew8dusB8myuZJcECOToQhXq9NdcnwXxTt6SHBmzo3Onj95JKndhyi0BX/mTFR/YL31SckFcPnLIZO8lM97wAJ5Eyqdiw8NnSnTs/PFFICPzfFz4+ZNT8FdQr3pjWdWh4vgFFCF5YK20r8Vk8jqA', ' check': 'true', ' _gcl_au': '1.1.1815096034.1660097997', ' AMCV_EDA101AC512D2B230A490D4C@AdobeOrg': '-330454231|MCMID|64698728618928567654265571124657024329|MCIDTS|19215|MCAID|NONE|MCOPTOUT-1660105215s|NONE|vVersion|3.1.2', ' s_ecid': 'MCMID|64698728618928567654265571124657024329', ' AMCVS_EDA101AC512D2B230A490D4C@AdobeOrg': '1', ' WDPROView': '{"version":2,"preferred":{"device":"desktop","screenWidth":1280,"screenHeight":1024},"deviceInfo":{"device":"desktop","screenWidth":1280,"screenHeight":1024},"browserInfo":{"agent":"Chrome","version":"104.0.0.0"}}', ' PHPSESSID': 'uokju03smfvn7tu5lqurr1nbh2', ' GEOLOCATION_jar': '{"zipCode":"92688","region":"california","country":"united+states","metro":"santabarbra-sanmar-sanluob","metroCode":"855","countryisocode":"USA"}', ' ak_bmsc': 'AA3DB0F35D876C58FBAA8F1E627D46D7~000000000000000000000000000000~YAAQKS0tF939ymaCAQAAFiKNhRBPL0qoCn5x4TD5ePBb4sf4XYgXal+FiUbGdRUtgOyVzWXEo1yTutPDE221RiGCKydF8DpJGBs4HwJ6Pfm2hZLOl3nlE+KPyIQCOxbfl5tJq0JD7Or+FxS7Qed61y4QTAfhskXN3LJDnn/tyzc4raJIUe9LWey01cNKCsQQIOA+Ey4DfMvA72weXcAqLvcsGUwZe6/vVCugAyvi5hXnFUYFvX30ZA77TLPki1fOjqqkVUKi1nBUlCoAJLD2DUgHzOFZxtcmqt6y7CUq0fB9uoO/ZdAnCt1OOkczzWxEqXL+NvA2vqAMmY83PmkwvPRs9EJBGii7Xaz5MFmr8Gj9k06o+iznMQ4cxAlkeE30eeJHHf4aaAoyqjssU36943N/2iiOFRpdXqZRptbnn1Fz/cLe5fqYl9St05i8zrkCaqeh+yGIM9aLTvdjINORXTg5KnBAtLmhwLDhkfVCJloRTw2YZhUD31B+6IGk', ' surveyThreshold_jar': '{"pageViewThreshold":1}', ' SWID': '5a08fb0c-770d-4d7e-a9f7-17d720e3cfaa', ' __d': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhY2Nlc3NfdG9rZW4iOiIwOGNjMzU0MjBiNjk0ZjU3YTY4OWZjZGY0MWIzYzk5NSIsInRva2VuX3R5cGUiOiJCRUFSRVIiLCJleHBpcmVzX2luIjoiMjg4MDAiLCJpYXQiOjE2NjAwOTc5OTV9.ZxdqIj52oLK0WEsoq0YqY_hNegvUOfMBM1QRmVS7yxShtU_pLBZsPacp2kQ3MoAX6_5Tu-FRYuqbrw7P4kyd5w', ' finderPublicTokenExpireTime': '1660126737280', ' WDPROGeoIP': 'YToxODp7czo4OiJhcmVhY29kZSI7czozOiI5NDkiO3M6NzoiY291bnRyeSI7czoxMzoidW5pdGVkIHN0YXRlcyI7czo5OiJjb250aW5lbnQiO3M6MjoibmEiO3M6MTA6ImNvbm5lY3Rpb24iO3M6OToiYnJvYWRiYW5kIjtzOjExOiJjb3VudHJ5Y29kZSI7czozOiI4NDAiO3M6MTQ6ImNvdW50cnlpc29jb2RlIjtzOjM6InVzYSI7czo2OiJkb21haW4iO3M6NzoiY294Lm5ldCI7czozOiJkc3QiO3M6MToieSI7czozOiJpc3AiO3M6MjM6ImNveCBjb21tdW5pY2F0aW9ucyBpbmMuIjtzOjU6Im1ldHJvIjtzOjI2OiJzYW50YWJhcmJyYS1zYW5tYXItc2FubHVvYiI7czo5OiJtZXRyb2NvZGUiO3M6MzoiODU1IjtzOjY6Im9mZnNldCI7czo0OiItNzAwIjtzOjg6InBvc3Rjb2RlIjtzOjU6IjkyNjg4IjtzOjM6InNpYyI7czozMzoiV2lyZWQgVGVsZWNvbW11bmljYXRpb25zIENhcnJpZXJzIjtzOjc6InNpY2NvZGUiO3M6NjoiNTE3MzExIjtzOjU6InN0YXRlIjtzOjEwOiJjYWxpZm9ybmlhIjtzOjM6InppcCI7czo1OiI5MjY4OCI7czoyOiJpcCI7czoxMzoiNzIuMTk0LjQyLjE4MSI7fTs', ' bkSent': 'true', ' LPVID': 'JjMjI5ZGMzOTgxMDM1Y2Uy', ' LPSID-88271365': 'B6pqR0i5Rrexn3gONfS9tg', ' dvicSpaApplication': '{"dvicSpaApplication":true}', ' mbox': 'session#9736256cd1a04aa7b5877ae5802ba7b5#1660099857|PC#9736256cd1a04aa7b5877ae5802ba7b5.35_0#1723342802', ' mboxEdgeCluster': '35', ' s_pers': ' s_gpv_pn', ' _uetsid': 'f060a220185211ed955517e4a58f2f68', ' _uetvid': 'f060f290185211edb923cddbd2f61dff', ' _scid': '48c0ac97-2ab5-46c3-a682-d5a279a42b92', ' _ga': 'GA1.2.341866886.1660098002', ' _gid': 'GA1.2.1528396399.1660098002', ' _gat_gtag_UA_99867646_1': '1', ' ajs_user_id': 'null', ' ajs_group_id': 'null', ' ajs_anonymous_id': '"488f2a35-0537-4a4d-b3e8-ab4fa304ce38"', ' _fbp': 'fb.1.1660098002974.14115226', ' s_sess': ' s_slt', ' s_cc': 'true', ' s_tp': '6939', ' s_ppv': 'wdpro%2Fdlr%2Fus%2Fen%2Ftools%2Ffinder%2Fdining%2C14%2C14%2C975', ' _cs_c': '0', ' _cs_cvars': '{"1":["s cVAR","wdpro/dlr/us/en/tools/finder/dining"]}', ' _cs_id': 'ebff8235-8c83-abab-86a6-66b8c12f15ae.1660098006.1.1660098006.1660098006.1588953526.1694262006718', ' _cs_s': '1.1.0.1660099806719', ' _CT_RS_': 'Recording', ' WRUIDCD24102019': '3932612286777651', ' __CT_Data': 'gpv', ' ADRUM_BT': 'R:0|i:13860988|g:fa292089-99e7-4b36-9658-f1e0052a07151285373|e:14|n:Disney-Prod_e4dfe7aa-6e26-4d68-9dc7-886d09949252', ' akavpau_dining_wr_au_wr': '1660098311~id', ' _abck': '82A8604081E1AD8A4494A3D0B586F87C~0~YAAQKS0tF2MFy2aCAQAA5WGNhQi1U13EiMG13T7yx5i0H9xoTaGbHg+V1W+na9lSpfp7uJrY9Ms9DA8LOQ4jJ7UMtXN73gs+HUCz0NE5TUNOUb4jOPrhFTgY0zck/LAmaiu9h1rT6qvnZdpZIMKOScPXl9mQWi1PRMtTeWqeoCfBDCWS7EfxldvqTH/PAGN9jYTbubJkWqUdqVthGlKgDyAwZ/CEeCEO9ClxhMH1KhlC/EQWx12cxxwokJ33pR7wkAn+xpC4RAcGVLEHmTYHpGFtTK2O8t7IYnnzSevvI/OJnoNwYEaowG4i8BDd5QNnGZQRbyuhvKkzVOIccvTuSP4baDplBpBEveZyODYGQyQuGxwK7UmGV8jOIccRfpkolD9MW6QmkCTSZ8T2JjubuLHBR/Y', ' akavpau_disneyland_disney_go_com_FullSite': '1660098613~id', ' bm_sv': '05AF1A67E6C4D46D0C50F0BB5D046FA1~YAAQKS0tFyUGy2aCAQAAAmmNhRB8lpJlGJGuW9orUqtQu9qq0uNJHY+qKQ/GFbhKY5YlGCdOaWn5CIk6Ns5eZKol3SMt6DRBZob2py3psTqukhJOiY1n/pqA/+a/l/Z8vRylt5TMtInqTW25rr04VtUIsgmpqcXL0Eg3xJfcuVGG8Xc7UzL8G/BMVfXjmTp6va+q78ayh4hJ5axBqvXv1S01Dkf3qNp3DSUX+tXrgrIBKRd89FrlDiCTMtAcAHHBQuXc~1'}
TARGET_DATE = "2022-08-12"
S3_BUCKET_NAME = "magic-reservations"

def get_request(url):
    """
    Helper function to get a request to the disneyland website, they need the headers and the cookie which includes an auth token.
    TODO: Determine if the auth token expires
    """
    resp = requests.get(url, headers=HEADERS, cookies=COOKIE, timeout=10)

    if resp.status_code == 200:
        return resp.json()
    else:
        raise RuntimeError(f"Error: {resp.json()}")

def get_s3_record():
    """Fetch the latest record from aws or None if there isn't one"""
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)

    data = "{}"
    for obj in bucket.objects.all():
        if obj.key.endswith(".json"):
            print("Found record in S3")
            data = obj.get()["Body"].read().decode("utf-8")
            break

    return json.loads(data)

def save_s3_record(data):
    """Save the data to S3"""
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.put_object(Key=f"record.json", Body=json.dumps(data))


def get_availability_data():
    # Get all the dining data currently available
    raw_dining_data = get_request(f"https://disneyland.disney.go.com/finder/api/v1/explorer-service/list-ancestor-entities/dlr/80008297;entityType=destination/{TARGET_DATE}/dining")

    # For now what we really want out of this is the mapping of dining locations to their IDS
    restaurants = raw_dining_data["results"]

    # Create a map of id to name while filtering for only restaurants and not events 
    restaurant_map = {restaurant["id"]: restaurant["name"] for restaurant in restaurants if "entityType=restaurant" in restaurant["id"]}

    # print(restaurant_map)

    # Now that we have that we can try our filtered request
    # This includes it looks like the mealPeriod as the only filter and the date we care about (2022-08-12) and number of people (5)
    raw_availability_data = get_request("https://disneyland.disney.go.com/finder/api/v1/explorer-service/dining-availability-list/{13019931-306C-4B87-AFAD-050364842981}/dlr/80008297;entityType=destination/2022-08-12/5/?mealPeriod=80000717")
    # print(raw_availability_data)

    # This is a dictionary of ids to {
    #    hasAvailability: true/false
    #    singleLocation: {
    #       reaosn why unavailable or dictionary of offers}
    #    multipleLocations: {
    #       reasons why unavailable - seems more for events}
    # }

    # Filter out locations to only have those that are available and are single locations and not events
    availablility_map = {}
    for restaurant_id, data in raw_availability_data["availability"].items():
        if data["hasAvailability"] and "singleLocation" in data.keys():
            availablility_map[restaurant_map[restaurant_id]] = data["singleLocation"]["offers"]
    
    # At this point we have a dictionary of names to a list of offers
    # Each offer contains a date, time, and url to go make the reservation!
    # Now we can create a local record 
    local_record = {name: offers for name, offers in availablility_map.items()}
    return local_record

def compare_records(local_record, s3_record):
    # At this point we only care about restaurants that still have offers, if there are restaurants that are no longer available we can delete them from the s3 record
    for restaurant in s3_record.keys():
        if restaurant not in local_record.keys():
            del s3_record[restaurant]

    # Start to keep track of new offers
    new_offers = {}
        
    # Now we can compare the two and see if there are any changes
    for restaurant, offers in local_record.items():
        if restaurant not in s3_record.keys():
            print(f"{restaurant} has new offers!")
            s3_record[restaurant] = offers
            new_offers[restaurant] = offers
        else:
            # Get all the times that are in the s3 record 
            s3_times = [offer["time"] for offer in s3_record[restaurant]]

            # Loop through each current offer to see if there are any new ones
            for offer in offers:
                if offer["time"] not in s3_times:
                    print(f"{restaurant} has new offers (and had some repeat ones)!")
                    s3_record[restaurant].append(offer)
                    new_offers[restaurant].append(offer)
    
    return new_offers, s3_record

def send_email(subject, body):
    """Send an email using AWS SES with the content"""
    ses = boto3.client("ses")
    ses.send_email(
        Source=os.environ["EMAIL"],
        Destination={
            "ToAddresses": [os.environ["EMAIL"]]
        },
        Message={
            "Subject": {
                "Data": subject
            },
            "Body": {
                "Text": {
                    "Data": body
                }
            }
        }
    )
    

def handler(event, context):
    print("Starting...")

    try:
        # Get the latest available record from disney's website
        local_record = get_availability_data()
        s3_record = get_s3_record()
        new_offers, updated_s3_record = compare_records(local_record, s3_record)


        # If there are no new offers we are done
        if not new_offers:
            print("No new offers")
            return 

        # Log the new offers
        email_content = ""
        for restaurant, offers in new_offers.items():
            email_content += f"{restaurant} Times:\n"
            for offer in offers:
                email_content += f"{offer['date']}: {offer['time']}\n"

        print(email_content)
        
        # Send an email with the new offers
        subject = "New offers at Disneyland!"
    except Exception as e:
        print(f"Error: {e}")
        subject = "Error getting new offers at Disneyland!"
        email_content = f"Error: {e}"

    # Send the email, if this fails cloudwatch should pick it up 
    send_email(subject, email_content) 
    save_s3_record(updated_s3_record)
    print("Done!")

if __name__ == "__main__":
    handler(None, None)