import time
import numpy as np

class PerformanceBaseline:
    def __init__(self):
        self.baseline_times = []
        self.baseline_completeness = []
    
    def measure_explanation_generation(self, input_data, explanation_func):
        start_time = time.time()
        result = explanation_func(input_data)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000
        self.baseline_times.append(processing_time)
        
        return result, processing_time
    
    def get_performance_stats(self):
        return {
            'mean_time_ms': np.mean(self.baseline_times),
            'std_time_ms': np.std(self.baseline_times),
            'sample_size': len(self.baseline_times)
        }
