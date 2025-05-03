import os
import json
import re
from collections import defaultdict

# Path to your LeetSync problems folder inside the repo
LEETSYNC_PATH = "Leetcode/problems"

# Path to your README.md
README_PATH = "README.md"

# Mapping: Display Name -> LeetCode Tag
TOPICS = {
    "Arrays": "array",
    "Binary Search": "binary-search",
    "Linked Lists": "linked-list",
    "Trees": "tree",
    "Stacks & Queues": "stack"
}

# Count solved problems per tag
def get_tag_wise_counts():
    topic_counts = defaultdict(int)
    total_count = 0

    for filename in os.listdir(LEETSYNC_PATH):
        if filename.endswith(".json"):
            filepath = os.path.join(LEETSYNC_PATH, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_count += 1
                    for tag in data.get("tags", []):
                        topic_counts[tag] += 1
            except json.JSONDecodeError:
                print(f"❌ JSON Decode Error in file: {filename}")

    return topic_counts, total_count

# Calculate percentage
def calculate_progress(topic_count, total_solved):
    if total_solved == 0:
        return 0
    return min(100, int((topic_count / total_solved) * 100))

# Update README.md with topic-wise progress
def update_readme_with_tags(tag_counts, total_count):
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    updated_content = content
    for topic, tag in TOPICS.items():
        topic_count = tag_counts.get(tag, 0)
        progress = calculate_progress(topic_count, total_count)
        progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
        progress_text = f"🌟 **{topic}:**   {progress_bar}  **{progress}% ({topic_count}/{total_count})**"

        updated_content = re.sub(
            f"🌟 \\*\\*{topic}:\\*\\*.*",
            progress_text,
            updated_content
        )

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated_content)
    
    print("✅ README.md updated successfully with real-time topic-wise LeetCode stats.")

# Run the script
if __name__ == "__main__":
    tag_counts, total_solved = get_tag_wise_counts()
    update_readme_with_tags(tag_counts, total_solved)
