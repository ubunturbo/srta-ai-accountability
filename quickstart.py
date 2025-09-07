print("Apertus SRTA Quick Start")
try:
    import torch, transformers, pandas
    print("Dependencies OK!")
except ImportError as e:
    print(f"Missing: {e}")