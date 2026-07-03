"""Serialize objects as files."""
import json
import numpy as np
import pandas as pd
import io
from typing import Tuple


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return str(obj)

class SerializeAsFiles():
    def serialize(self, obj) -> Tuple[str, str]:
        if isinstance(obj, pd.DataFrame):
            return obj.to_csv(), 'csv'
        if isinstance(obj, np.ndarray):
            output = io.BytesIO()
            np.save(output, obj)
            return output.getvalue(), 'npy'
        if isinstance(obj, dict):
            return json.dumps(obj, cls=NpEncoder), 'json'
        if isinstance(obj, list):
            return json.dumps(obj, cls=NpEncoder), 'json'
        if isinstance(obj, str):
            return obj, 'txt'
        return str(obj), 'txt'
    
    