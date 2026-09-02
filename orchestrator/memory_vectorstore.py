# Source Generated with Decompyle++
# File: memory_vectorstore.cpython-312.pyc (Python 3.12)

import os
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
import json
import hashlib
import threading
from typing import List, Dict, Any
import numpy as np
import faiss

class VectorMemory:

    def __init__(self = None, path = None, model_name = None, local_files_only = ('all-MiniLM-L6-v2', True)):
        self.path = path
        os.makedirs(self.path, exist_ok = True)
        self.index_file = os.path.join(self.path, 'faiss.index')
        self.data_file = os.path.join(self.path, 'vectors.json')
        self.model_name = model_name
        self.local_files_only = local_files_only
        self.model = None
        self.model_lock = threading.Lock()
        self.dimension = 384
        self.index = faiss.IndexFlatIP(self.dimension)
        self.data = []
        self._load()


    def _load(self):
        if os.path.exists(self.data_file):

            try:
                f = open(self.data_file, 'r', encoding = 'utf-8')
                self.data = json.load(f)

                try:
                    None(None, None)
                    if os.path.exists(self.index_file):

                        try:
                            self.index = faiss.read_index(self.index_file)
                            return None
                            return None
                            with None:
                                if not None:
                                    pass

                            try:
                                continue
                            except Exception:
                                self.data = []
                                continue
                                except Exception:
                                    self.index = faiss.IndexFlatIP(self.dimension)
                                    return None






    def _save(self):
        faiss.write_index(self.index, self.index_file)
        f = open(self.data_file, 'w', encoding = 'utf-8')
        json.dump(self.data, f, indent = 2, ensure_ascii = False)
        None(None, None)
        return None
        with None:
            if not None:
                pass


    def _normalize_vector(self = None, vector = None):
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return None / norm


    def _get_model(self):
        self.model_lock
    # WARNING: Decompyle incomplete


    def _embed(self = None, text = None):
        vector = self._get_model().encode(text, convert_to_numpy = True).astype('float32')
        return self._normalize_vector(vector)


    def _hash_content(self = None, content = None):
        return hashlib.md5(content.encode('utf-8')).hexdigest()


    def add(self = None, entry = None):
        pass
    # WARNING: Decompyle incomplete


    def search(self = None, query = None, k = None):
        if not self.data:
            return []

        try:
            query_vector = self._embed(query)
            k = min(k, len(self.data))
            (distances, indices) = self.index.search(np.array([
                query_vector]), k)
            results = []
            for score, idx in zip(distances[0], indices[0]):
                if idx < 0:
                    continue
                if idx >= len(self.data):
                    continue
                item = self.data[idx]
                results.append({
                    'score': float(score),
                    'content': item['content'] })
            return results
        except Exception:
            return



    def clear(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.data = []
        self._save()


    def stats(self = None):
        return {
            'entries': len(self.data),
            'dimension': self.dimension,
            'index_type': 'FAISS-IP',
            'embedding_model': self._get_model().__class__.__name__,
            'storage_path': self.path }
