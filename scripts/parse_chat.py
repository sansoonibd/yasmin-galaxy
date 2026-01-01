import re
import json
import os
from datetime import datetime

def parse_whatsapp_chat(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    data = []
    
    # Regex Patterns
    # Date format in WhatsApp exports can vary. Common: "[dd/mm/yyyy, HH:MM:SS] Sender: Message"
    # Or "mm/dd/yy, HH:MM PM - Sender: Message"
    # We will try a generic approach or specific one. Let's assume standard iOS "[date] name: msg"
    
    # Updated Regex to capture date/time with AM/PM (including possible invisible chars)
    # Matches: [18/09/2021, 11:21:25 PM] or similar
    line_pattern = re.compile(r'^\[(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}:\d{2}.*?)\] ([^:]+): (.*)')
    
    # Content Regex
    # Matches: haha, aha, ahaha, hahaha, hehe, lol, lmao (case insensitive)
    # \b ensures we don't match inside words like "Yamaha" or "hat"
    # Logic: (start of word) -> optional 'a' -> 'h' -> 'a' -> optional repeating 'h' or 'a' -> (end of word)
    # Actually simpler: looking for repeating ha sequences or aha.
    # regex: \b(a*ha+h[ha]*|h+e+h+e+|l+o+l+|l+m+a+o+)\b
    laugh_pattern = re.compile(r'\b(a*ha+h[ha]*|h+e+h+e+|l+o+l+|l+m+a+o+)\b|😂|🤣|💀', re.IGNORECASE)
    # Added Arabic transliterations: bahebak/bahebek (I love you), bamoot feek/feeki (I die for you/love you to death)
    ily_pattern = re.compile(r'(i love you|love u|ily\b|bahebak|bahebek|bamoot feek|bamoot feeki)', re.IGNORECASE)

    with open(file_path, 'r', encoding='utf-8') as f:
        daily_counts = {}
        
        for line in f:
            # Handle RTL/LTR marks if present (often in WhatsApp exports)
            line = line.strip().replace('\u200e', '').replace('\u202f', ' ')
            
            match = line_pattern.match(line)
            if match:
                dt_str, sender, msg = match.groups()
                
                try:
                    # Clean up date string just in case
                    dt_str = dt_str.replace('\u202f', ' ').strip()
                    
                    # Try parsing with AM/PM
                    try:
                        dt = datetime.strptime(dt_str, "%d/%m/%Y, %I:%M:%S %p")
                    except ValueError:
                        # Fallback for other formats if needed
                        dt = datetime.strptime(dt_str, "%d/%m/%Y, %H:%M:%S")

                    # Filter for 2025 only
                    if dt.year != 2025:
                        continue
                        
                    date_key = dt.strftime("%Y-%m-%d")
                    
                    if date_key not in daily_counts:
                        daily_counts[date_key] = {"laughs": 0, "ilys": 0}

                    # Check Content
                    if laugh_pattern.search(msg):
                        daily_counts[date_key]["laughs"] += 1
                        
                    if ily_pattern.search(msg):
                         # For ILYs, we might want individual events or just count?
                         # Let's count them for the star scale.
                        daily_counts[date_key]["ilys"] += 1
                        
                except ValueError as e:
                    # print(f"Skipping date parse error: {dt_str} - {e}")
                    continue

    # Flatten aggregated data to list, ensuring EVERY day is present for consistency
    if not daily_counts:
        return # No data found

    sorted_dates = sorted(daily_counts.keys())
    
    # Enforce full year range for 2025 consistency
    # Even if chat starts in Feb or ends in Nov, we want the spiral to represent the FULL year.
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        # User requested to remove April specifically
        if current_date.month == 4:
            current_date = current_date.fromordinal(current_date.toordinal() + 1)
            continue

        date_str = current_date.strftime("%Y-%m-%d")
        
        counts = daily_counts.get(date_str, {"laughs": 0, "ilys": 0})
        
        data.append({
            "date": date_str,
            "laughCount": counts['laughs'],
            "ilyCount": counts['ilys']
        })
        
        current_date = current_date.fromordinal(current_date.toordinal() + 1)

    output_path = "../web/public/galaxy_data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Parsed chat. saved {len(data)} points to {output_path}")

if __name__ == "__main__":
    # Point this to your actual file
    parse_whatsapp_chat("../data/_chat.txt") 
