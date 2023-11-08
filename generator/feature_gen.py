import pandas as pd
import numpy as np
import os
import magic
import json

def is_json(fname):
    with open(fname) as f:
        try:
            json.load(f)
            return True
        except Exception:
            return False

def recurse_find(curr_path, base_path):
    all_files = []
    for subpath_str in os.listdir(curr_path):
        subpath = os.path.join(curr_path, subpath_str)
        
        child_files = []
        if os.path.isdir(subpath):
            child_files += recurse_find(subpath, base_path)
        else:
            # This means that its a file
            content_type = "application/json" if is_json(subpath) else magic.from_file(subpath, mime=True)
            child_files.append((str(subpath).replace(base_path, ""), os.path.getsize(subpath), content_type))
        
        all_files += child_files
    
    return all_files

def gen_feature(site_data_path):
    feature_pd = pd.DataFrame([])
    site_tups = recurse_find(site_data_path, site_data_path)
    
    feature_list = ['path', 'size', 'type']
    feature_pd = pd.DataFrame(site_tups, columns=feature_list)
    return feature_pd