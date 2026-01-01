import json
import random
from datetime import datetime, timedelta

def generate_mock_data():
    start_date = datetime.now() - timedelta(days=365*2) # 2 years of data
    data = []
    
    # Simulate a relationship arc
    # Early phase: Frequent laughs, few ILYs
    # Middle phase: Consistent laughs, increasing ILYs
    # Current phase: Deep comfort, stable frequency
    
    current_date = start_date
    end_date = datetime.now()
    
    while current_date < end_date:
        # Seasonality/Randomness
        day_factor = random.random()
        
        # 1. Laughs (The Spiral Arms)
        # Randomly 0-15 laughs per day based on "day_factor"
        if day_factor > 0.2:
            num_laughs = random.randint(1, 15)
            # Add some spikes
            if random.random() > 0.95:
                num_laughs += 20
                
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "type": "laugh",
                "count": num_laughs,
                "context": f"{num_laughs} laughs"
            })
            
        # 2. ILYs (The Stars)
        # Starts rare, becomes frequent
        days_since_start = (current_date - start_date).days
        total_days = (end_date - start_date).days
        relationship_progress = days_since_start / total_days
        
        ily_chance = 0.1 + (0.8 * relationship_progress) # Starts at 10% chance, ends at 90%
        
        if random.random() < ily_chance:
            # Sometimes just 1, sometimes many
            intensity = random.choice([1, 1, 1, 2, 3, 5])
            if random.random() > 0.98: # Special occasions
                intensity = 10
                
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "type": "ily",
                "count": intensity,
                "context": "I love you"
            })
            
        current_date += timedelta(days=1)
        
    # Write to file
    output_path = "../data/galaxy_data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Generated {len(data)} data points to {output_path}")

if __name__ == "__main__":
    generate_mock_data()
