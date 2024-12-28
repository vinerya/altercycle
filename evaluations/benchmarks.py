import time
import random
import threading
import statistics
from typing import List, Tuple, Any, Dict
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
from mobius_linked_list import MobiusLinkedList

class DataStructureEvaluation:
    """Comprehensive evaluation suite for the Möbius Linked List."""
    
    def __init__(self, sizes: List[int] = [100, 1000, 10000, 100000]):
        self.sizes = sizes
        self.results: Dict[str, Dict[str, List[float]]] = {}
        
    def generate_data(self, size: int) -> List[Any]:
        """Generate test data with repeating patterns."""
        pattern = ['A', 'B', 'C', 'D']
        return [pattern[i % len(pattern)] for i in range(size)]
        
    def benchmark_insertion(self) -> Dict[str, List[float]]:
        """Compare insertion performance."""
        results = {'mobius': [], 'deque': [], 'list': []}
        
        for size in self.sizes:
            data = self.generate_data(size)
            
            # Möbius Linked List
            start = time.time()
            mlist = MobiusLinkedList[str]()
            for item in data:
                mlist.append(item)
            results['mobius'].append(time.time() - start)
            
            # Deque
            start = time.time()
            dq = deque()
            for item in data:
                dq.append(item)
            results['deque'].append(time.time() - start)
            
            # Regular List
            start = time.time()
            lst = []
            for item in data:
                lst.append(item)
            results['list'].append(time.time() - start)
            
        self.results['insertion'] = results
        return results
        
    def benchmark_pattern_detection(self) -> Dict[str, List[float]]:
        """Compare pattern detection performance."""
        results = {'mobius': [], 'traditional': []}
        pattern_length = 2
        
        def find_patterns_traditional(data: List[str], length: int) -> List[Tuple[List[str], int]]:
            patterns = {}
            for i in range(len(data) - length + 1):
                pattern = tuple(data[i:i+length])
                patterns[pattern] = patterns.get(pattern, 0) + 1
            return [(list(p), f) for p, f in patterns.items() if f > 1]
        
        for size in self.sizes:
            data = self.generate_data(size)
            
            # Möbius Linked List
            mlist = MobiusLinkedList[str]()
            for item in data:
                mlist.append(item)
            start = time.time()
            mlist.find_patterns(pattern_length)
            results['mobius'].append(time.time() - start)
            
            # Traditional approach
            start = time.time()
            find_patterns_traditional(data, pattern_length)
            results['traditional'].append(time.time() - start)
            
        self.results['pattern_detection'] = results
        return results
        
    def benchmark_concurrent_operations(self) -> Dict[str, List[float]]:
        """Compare concurrent operation performance."""
        results = {'mobius': [], 'synchronized_list': []}
        num_threads = 4
        operations_per_thread = 1000
        
        class SynchronizedList:
            def __init__(self):
                self.data = []
                self.lock = threading.Lock()
                
            def append(self, item):
                with self.lock:
                    self.data.append(item)
        
        for size in self.sizes:
            # Möbius Linked List
            mlist = MobiusLinkedList[str]()
            start = time.time()
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for _ in range(num_threads):
                    futures.append(executor.submit(
                        lambda: [mlist.append(str(i)) for i in range(operations_per_thread)]
                    ))
                for future in futures:
                    future.result()
            results['mobius'].append(time.time() - start)
            
            # Synchronized List
            slist = SynchronizedList()
            start = time.time()
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for _ in range(num_threads):
                    futures.append(executor.submit(
                        lambda: [slist.append(str(i)) for i in range(operations_per_thread)]
                    ))
                for future in futures:
                    future.result()
            results['synchronized_list'].append(time.time() - start)
            
        self.results['concurrent_operations'] = results
        return results
        
    def benchmark_memory_usage(self) -> Dict[str, List[float]]:
        """Compare memory usage."""
        import sys
        results = {'mobius': [], 'deque': [], 'list': []}
        
        for size in self.sizes:
            data = self.generate_data(size)
            
            # Möbius Linked List
            mlist = MobiusLinkedList[str]()
            for item in data:
                mlist.append(item)
            results['mobius'].append(sys.getsizeof(mlist) / 1024)  # KB
            
            # Deque
            dq = deque(data)
            results['deque'].append(sys.getsizeof(dq) / 1024)
            
            # Regular List
            lst = list(data)
            results['list'].append(sys.getsizeof(lst) / 1024)
            
        self.results['memory_usage'] = results
        return results
        
    def plot_results(self) -> None:
        """Generate performance comparison plots."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Insertion Performance
        self._plot_metric(ax1, 'insertion', 'Insertion Performance',
                         'Data Size', 'Time (seconds)')
        
        # Pattern Detection
        self._plot_metric(ax2, 'pattern_detection', 'Pattern Detection Performance',
                         'Data Size', 'Time (seconds)')
        
        # Concurrent Operations
        self._plot_metric(ax3, 'concurrent_operations', 'Concurrent Operations Performance',
                         'Data Size', 'Time (seconds)')
        
        # Memory Usage
        self._plot_metric(ax4, 'memory_usage', 'Memory Usage',
                         'Data Size', 'Memory (KB)')
        
        plt.tight_layout()
        plt.savefig('performance_evaluation.png')
        
    def _plot_metric(self, ax, metric: str, title: str, xlabel: str, ylabel: str) -> None:
        """Helper method for plotting a specific metric."""
        if metric not in self.results:
            return
            
        for structure, times in self.results[metric].items():
            ax.plot(self.sizes, times, marker='o', label=structure)
            
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True)
        
    def run_all_benchmarks(self) -> None:
        """Run all benchmarks and generate plots."""
        print("Running benchmarks...")
        
        print("1. Insertion Performance")
        self.benchmark_insertion()
        
        print("2. Pattern Detection")
        self.benchmark_pattern_detection()
        
        print("3. Concurrent Operations")
        self.benchmark_concurrent_operations()
        
        print("4. Memory Usage")
        self.benchmark_memory_usage()
        
        print("\nGenerating plots...")
        self.plot_results()
        
        print("\nResults Summary:")
        self._print_summary()
        
    def _print_summary(self) -> None:
        """Print a summary of the benchmark results."""
        for metric, results in self.results.items():
            print(f"\n{metric.upper()} COMPARISON:")
            for structure, times in results.items():
                avg_time = statistics.mean(times)
                print(f"{structure:15} Average: {avg_time:.6f}")
                
if __name__ == '__main__':
    evaluation = DataStructureEvaluation()
    evaluation.run_all_benchmarks()
