import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def fetch_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProfileCalendar($username: String!) {
      matchedUser(username: $username) {
        userCalendar {
          submissionCalendar
        }
      }
    }
    """
    variables = {"username": username}
    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        data = response.json()
        # Extract submission calendar
        submission_calendar = data["data"]["matchedUser"]["userCalendar"]["submissionCalendar"]
        return json.loads(submission_calendar)
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def generate_graph(contributions, output_path="output/leetcode-contributions.png"):
    # Convert Unix timestamps to readable dates
    contributions_df = pd.DataFrame(
        {"date": list(contributions.keys()), "count": list(contributions.values())}
    )
    contributions_df["date"] = pd.to_datetime(contributions_df["date"].astype(int), unit='s')

    contributions_df.sort_values("date", inplace=True)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.bar(contributions_df["date"], contributions_df["count"], color="skyblue")
    plt.title("LeetCode Contributions")
    plt.xlabel("Date")
    plt.ylabel("Problems Solved")
    plt.tight_layout()

    # Save the graph
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    username = os.getenv("LEETCODE_USERNAME", "example_username")
    contributions = fetch_leetcode_data(username)
    generate_graph(contributions)
