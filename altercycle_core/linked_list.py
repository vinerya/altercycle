from typing import Any, Optional, Iterator, TypeVar, Generic, List, Tuple, Callable
from collections import deque
from .node import AlterNode
import threading
import time

T = TypeVar('T')

class AlterCycle(Generic[T]):
    """
    A specialized data structure for handling alternating binary states in cyclic sequences.
    
    This implementation provides:
    1. Strict state alternation enforcement
    2. Pattern detection in alternating sequences
    3. Concurrent processing capabilities
    4. Real-world applications in:
       - Protocol validation
       - Binary state machines
       - Cyclic pattern analysis
       - Alternating role management
    """
    
    def __init__(self) -> None:
        """Initialize an empty AlterCycle."""
        self.head: Optional[AlterNode[T]] = None
        self._lock = threading.Lock()
        self._size: int = 0
        
    def append(self, data: T, metadata: Optional[dict] = None) -> None:
        """
        Add a new node to the sequence with automatic state alternation.
        
        Args:
            data: The data to store in the node
            metadata: Optional metadata for the node
            
        Thread-safe: Uses lock to ensure thread safety
        """
        with self._lock:
            new_node = AlterNode(data, metadata=metadata)
            if not self.head:
                self.head = new_node
                self.head.next = self.head
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                new_node.orientation = 1 - current.orientation
                current.next = new_node
                new_node.next = self.head
            self._size += 1
            
    def insert_after(self, target_data: T, new_data: T) -> bool:
        """
        Insert a new node after the first occurrence of target_data.
        
        Args:
            target_data: Data to search for
            new_data: Data for the new node
            
        Returns:
            bool: True if insertion was successful
        """
        with self._lock:
            if not self.head:
                return False
                
            current = self.head
            while True:
                if current.data == target_data:
                    new_node = AlterNode(new_data)
                    new_node.next = current.next
                    new_node.orientation = 1 - current.orientation
                    current.next = new_node
                    self._size += 1
                    return True
                current = current.next
                if current == self.head:
                    break
            return False
            
    def remove(self, data: T) -> bool:
        """
        Remove the first occurrence of a node with the given data.
        
        Args:
            data: Data to remove
            
        Returns:
            bool: True if removal was successful
        """
        with self._lock:
            if not self.head:
                return False
                
            if self.head.data == data:
                if self.head.next == self.head:
                    self.head = None
                else:
                    current = self.head
                    while current.next != self.head:
                        current = current.next
                    current.next = self.head.next
                    self.head = self.head.next
                self._size -= 1
                return True
                
            current = self.head
            while current.next != self.head:
                if current.next.data == data:
                    current.next = current.next.next
                    self._size -= 1
                    return True
                current = current.next
            return False
            
    def flip_states(self, positions: int = 1) -> None:
        """
        Flip binary states for a specified number of positions.
        
        Args:
            positions: Number of positions to flip states
        """
        if not self.head or positions == 0:
            return
            
        current = self.head
        for _ in range(abs(positions)):
            while True:
                current.flip_orientation()
                current = current.next
                if current == self.head:
                    break
                    
    def find_patterns(self, pattern_length: int) -> List[Tuple[List[T], int]]:
        """
        Detect recurring patterns in alternating sequences.
        
        Args:
            pattern_length: Length of patterns to search for
            
        Returns:
            List of (pattern, frequency) tuples
        """
        if not self.head or pattern_length > len(self):
            return []
            
        patterns = {}
        current = self.head
        
        while True:
            pattern = []
            node = current
            for _ in range(pattern_length):
                pattern.append((node.data, node.orientation))
                node = node.next
            pattern_tuple = tuple(pattern)
            patterns[pattern_tuple] = patterns.get(pattern_tuple, 0) + 1
            current = current.next
            if current == self.head:
                break
                
        return [(list(p), f) for p, f in patterns.items() if f > 1]
        
    def process_parallel(self, func: Callable[[T, int], None], 
                        num_threads: int = 4) -> None:
        """
        Process nodes in parallel using multiple threads.
        
        Args:
            func: Function to apply to each node (params: data, state)
            num_threads: Number of threads to use
        """
        if not self.head:
            return
            
        def worker(start_node: AlterNode[T], count: int) -> None:
            current = start_node
            for _ in range(count):
                func(current.data, current.orientation)
                current = current.next
                
        length = len(self)
        nodes_per_thread = length // num_threads
        threads = []
        current = self.head
        
        for i in range(num_threads):
            count = nodes_per_thread + (1 if i < length % num_threads else 0)
            thread = threading.Thread(target=worker, args=(current, count))
            threads.append(thread)
            thread.start()
            for _ in range(count):
                current = current.next
                
        for thread in threads:
            thread.join()
            
    def create_checkpoint(self) -> str:
        """
        Create a serializable checkpoint of the current state sequence.
        
        Returns:
            str: JSON-serializable checkpoint data
        """
        checkpoint = {
            'nodes': [],
            'timestamp': time.time()
        }
        if self.head:
            current = self.head
            while True:
                checkpoint['nodes'].append({
                    'data': current.data,
                    'orientation': current.orientation,
                    'metadata': current.metadata
                })
                current = current.next
                if current == self.head:
                    break
        return str(checkpoint)
        
    def apply_transformation(self, transform_func: Callable[[T, int], T]) -> None:
        """
        Apply a transformation function to all nodes while preserving alternation.
        
        Args:
            transform_func: Function that takes (data, state) and returns new data
        """
        if not self.head:
            return
            
        current = self.head
        while True:
            current.data = transform_func(current.data, current.orientation)
            current = current.next
            if current == self.head:
                break
                
    def __iter__(self) -> Iterator[Tuple[T, int]]:
        """Iterator yielding (data, state) tuples."""
        if not self.head:
            return
            
        current = self.head
        while True:
            yield (current.data, current.orientation)
            current = current.next
            if current == self.head:
                break
                
    def __len__(self) -> int:
        """Return the number of nodes in the sequence."""
        return self._size
        
    def __repr__(self) -> str:
        """Detailed string representation including metadata."""
        if not self.head:
            return "AlterCycle([])"
        nodes = []
        current = self.head
        while True:
            meta_str = f"::{current.metadata}" if current.metadata else ""
            nodes.append(f"{current.data}({current.orientation}{meta_str})")
            current = current.next
            if current == self.head:
                break
        return "AlterCycle([" + " -> ".join(nodes) + "])"
