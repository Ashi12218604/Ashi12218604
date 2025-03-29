import requests
import json
import os
import re

# Your LeetCode Username
LEETCODE_USERNAME = "Ashi12218604"  

# GitHub README Path
README_PATH = "README.md"  

# Mapping topics to relevant tags
TOPICS = {
    "Arrays": "array",
    "Binary Search": "binary-search",
    "Linked Lists": "linked-list",
    "Trees": "tree",
    "Stacks & Queues": "stack"
}

# Function to get LeetCode stats
def get_leetcode_stats():
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        {
            matchedUser(username: "%s") {
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """ % LEETCODE_USERNAME
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=query)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
    else:
        return None

# Function to calculate progress percentage
def calculate_progress(topic_count, total_solved):
    if total_solved == 0:
        return 0
    return min(100, int((topic_count / total_solved) * 100))

# Function to update README
def update_readme(stats):
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    total_solved = sum(entry["count"] for entry in stats)
    updated_content = content

    for topic, tag in TOPICS.items():
        topic_count = next((entry["count"] for entry in stats if entry["difficulty"] == tag), 0)
        progress = calculate_progress(topic_count, total_solved)

        progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
        progress_text = f"🌟 **{topic}:**   {progress_bar}  **{progress}%**"

        updated_content = re.sub(f"🌟 \\*\\*{topic}:\\*\\*.*", progress_text, updated_content)

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated_content)

# Run the script
if __name__ == "__main__":
    stats = get_leetcode_stats()
    if stats:
        update_readme(stats)
