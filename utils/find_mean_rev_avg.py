"""
Find Mean Reversion Average
Analyzes historical data to find the optimal MEAN_REVERS_EXPAND value.
"""

import pandas as pd
from pathlib import Path
import sys
import os
from datetime import timedelta

# Add parent directory to path to import config
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

try:
    from config_trinchera import BIG_VOLUME_TRIGGER, MEAN_REVERSE_TIMEOUT_ORDER
except ImportError:
    print("Could not import config_trinchera. Using defaults.")
    BIG_VOLUME_TRIGGER = 300
    MEAN_REVERSE_TIMEOUT_ORDER = 3

def analyze_file(file_path):
    """Analyzes a single CSV file."""
    try:
        # Read CSV with correct separator and decimal
        df = pd.read_csv(file_path, sep=';', decimal=',', low_memory=False)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Ensure timestamp is datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Filter for big volume events (Orange Dot)
        # Assuming 'Volumen' is the column name based on previous inspection
        events = df[df['Volumen'] >= BIG_VOLUME_TRIGGER].copy()
        
        if len(events) == 0:
            return []
            
        deviations = []
        
        for idx, event in events.iterrows():
            event_time = event['Timestamp']
            event_price = event['Precio']
            target_time = event_time + timedelta(minutes=MEAN_REVERSE_TIMEOUT_ORDER)
            
            # Find the row closest to target_time
            # We look for rows after the event
            future_data = df[df['Timestamp'] >= target_time]
            
            if not future_data.empty:
                # Get the first row after or at target time
                target_row = future_data.iloc[0]
                
                # Check if it's within a reasonable window (e.g., not days later)
                if (target_row['Timestamp'] - target_time).total_seconds() < 60:
                    target_price = target_row['Precio']
                    deviation = target_price - event_price
                    deviations.append(deviation)
                    
        return deviations
        
    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return []

def main():
    data_dir = parent_dir / "data" / "historic"
    
    if not data_dir.exists():
        print(f"Directory not found: {data_dir}")
        return

    all_deviations = []
    files = [f for f in data_dir.glob("*.csv") if "all.csv" not in f.name]
    
    print(f"Found {len(files)} daily files in {data_dir}")
    print(f"Analyzing with BIG_VOLUME_TRIGGER={BIG_VOLUME_TRIGGER}, TIMEOUT={MEAN_REVERSE_TIMEOUT_ORDER} min...")
    
    for file_path in files:
        print(f"Processing {file_path.name}...", end="\r")
        deviations = analyze_file(file_path)
        all_deviations.extend(deviations)
        
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    
    if not all_deviations:
        print("No events found or no data available.")
        return

    series = pd.Series(all_deviations)
    
    mean_val = series.mean()
    abs_mean_val = series.abs().mean()
    median_val = series.median()
    abs_median_val = series.abs().median()
    
    print(f"Total Events Analyzed: {len(series)}")
    print(f"Average Deviation (Net): {mean_val:.4f}")
    print(f"Average Absolute Deviation: {abs_mean_val:.4f}")
    print(f"Median Deviation: {median_val:.4f}")
    print(f"Median Absolute Deviation: {abs_median_val:.4f}")
    print("-" * 30)
    print("Top 5 Absolute Deviations:")
    print(series.abs().sort_values(ascending=False).head(5))
    print("-" * 30)
    print(f"Suggested MEAN_REVERS_EXPAND (Avg Abs): {abs_mean_val:.2f}")
    print(f"Suggested MEAN_REVERS_EXPAND (Median Abs): {abs_median_val:.2f}")

if __name__ == "__main__":
    main()

