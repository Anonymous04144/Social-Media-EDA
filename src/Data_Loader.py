import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "Data", "social_media_data.csv")

def _create_sample_data_if_missing():
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    if not os.path.exists(RAW_DATA_PATH):
        np.random.seed(42)
        n = 400
        data = {
            "post_id": [f"POST_{i:04d}" for i in range(1, n + 1)],
            "platform": np.random.choice(["Instagram", "LinkedIn", "Twitter", "YouTube"], n),
            "content_type": np.random.choice(["Video", "Carousel", "Static Image", "Text"], n),
            "post_date": pd.date_range(start="2025-01-01", periods=n, freq="6h"),
            "impressions": np.random.randint(1000, 50000, n),
            "reach": np.random.randint(800, 45000, n),
            "likes": np.random.randint(20, 3000, n),
            "comments": np.random.randint(2, 500, n),
            "shares": np.random.randint(0, 400, n),
            "saves": np.random.randint(0, 600, n)
        }
        pd.DataFrame(data).to_csv(RAW_DATA_PATH, index=False)

def load_data(filepath=RAW_DATA_PATH):
    _create_sample_data_if_missing()
    return pd.read_csv(filepath)
