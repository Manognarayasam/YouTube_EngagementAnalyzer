# scripts/fetch_comments.py
import os
from googleapiclient.discovery import build
# from apiclient import discovery

from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# def get_comments(video_id, max_results=500):
#     youtube = build("youtube", "v3", developerKey=API_KEY)
#     comments = []

#     request = youtube.commentThreads().list(
#         part="snippet",
#         videoId=video_id,
#         maxResults=100,
#         textFormat="plainText"
#     )

#     while request and len(comments) < max_results:
#         response = request.execute()
#         for item in response["items"]:
#             snippet = item["snippet"]["topLevelComment"]["snippet"]
#             comments.append({
#                 "author": snippet["authorDisplayName"],
#                 "text": snippet["textDisplay"],
#                 "likes": snippet["likeCount"],
#                 "published": snippet["publishedAt"]
#             })
#         request = youtube.commentThreads().list_next(request, response)

#     df = pd.DataFrame(comments)
#     df.to_csv("data/raw_comments.csv", index=False)
#     print(f"Saved {len(df)} comments to data/raw_comments.csv")

# if __name__ == "__main__":
#     vid = input("Enter YouTube video ID: ")
#     get_comments(vid)


def get_comments(video_id="-WS6gkK-030", max_results=500):
    print("Initializing YouTube API client...")
    youtube = build("youtube", "v3", developerKey=API_KEY)
    print("YouTube client initialized.")

    comments = []
    print(f"Fetching comments for video ID: {video_id}")

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    page = 1
    while request and len(comments) < max_results:
        print(f"\n[Page {page}] Sending request to YouTube API...")
        response = request.execute()
        print(f"[Page {page}] Received {len(response['items'])} comments.")

        for idx, item in enumerate(response["items"]):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_data = {
                "author": snippet["authorDisplayName"],
                "text": snippet["textDisplay"],
                "likes": snippet["likeCount"],
                "published": snippet["publishedAt"]
            }
            print(f"Comment #{len(comments)+1} by {comment_data['author']} | Likes: {comment_data['likes']}")
            comments.append(comment_data)

        print(f"Total comments collected so far: {len(comments)}")
        request = youtube.commentThreads().list_next(request, response)
        page += 1

    print("\nCreating DataFrame from collected comments...")
    df = pd.DataFrame(comments)

    output_path = "data/raw_comments.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} comments to {output_path}")

# if __name__ == "__main__":
#     print("Script started.")
#     vid = input("Enter YouTube video ID: ")
#     print(f"Video ID entered: {vid}")
#     get_comments(vid)
#     print("Script finished.")
