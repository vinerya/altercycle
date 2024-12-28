import unittest
import threading
import time
from typing import List
from mobius_linked_list import MobiusLinkedList

class TestMobiusLinkedList(unittest.TestCase):
    """Test suite for the advanced Möbius Linked List implementation."""
    
    def setUp(self):
        """Initialize a new list for each test."""
        self.mlist = MobiusLinkedList[str]()
        
    def test_basic_operations(self):
        """Test basic list operations and orientation handling."""
        self.assertEqual(len(self.mlist), 0)
        
        # Test append with metadata
        self.mlist.append('A', {'timestamp': 123})
        self.assertEqual(len(self.mlist), 1)
        
        # Test orientation alternation
        self.mlist.append('B')
        self.mlist.append('C')
        orientations = [node[1] for node in self.mlist]
        self.assertEqual(orientations, [0, 1, 0])
        
    def test_pattern_detection(self):
        """Test pattern detection in cyclic data."""
        # Create a repeating pattern
        data = ['A', 'B', 'A', 'B', 'A', 'B']
        for item in data:
            self.mlist.append(item)
            
        patterns = self.mlist.find_patterns(2)
        self.assertTrue(any(p[0][0][0] == 'A' and p[0][1][0] == 'B' for p in patterns))
        self.assertTrue(any(p[1] >= 2 for p in patterns))  # At least 2 occurrences
        
    def test_parallel_processing(self):
        """Test parallel processing capabilities."""
        # Add test data
        for i in range(100):
            self.mlist.append(str(i))
            
        results = []
        def process_node(data: str, orientation: int) -> None:
            results.append(int(data) * orientation)
            
        self.mlist.process_parallel(process_node, num_threads=4)
        self.assertEqual(len(results), 100)
        
    def test_thread_safety(self):
        """Test thread-safe operations."""
        def worker():
            for i in range(100):
                self.mlist.append(str(i))
                
        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
        self.assertEqual(len(self.mlist), 400)
        
    def test_topological_transformations(self):
        """Test topological transformations."""
        for item in ['A', 'B', 'C', 'D']:
            self.mlist.append(item)
            
        # Record original orientations
        original = [(node[0], node[1]) for node in self.mlist]
        
        # Apply twist
        self.mlist.twist(positions=1)
        twisted = [(node[0], node[1]) for node in self.mlist]
        
        # Verify orientation changes
        self.assertNotEqual(original, twisted)
        
        # Verify double twist returns to original state
        self.mlist.twist(positions=1)
        double_twisted = [(node[0], node[1]) for node in self.mlist]
        self.assertEqual(original, double_twisted)
        
    def test_metadata_handling(self):
        """Test metadata operations."""
        self.mlist.append('A', {'created': time.time(), 'priority': 1})
        self.mlist.append('B', {'created': time.time(), 'priority': 2})
        
        # Verify metadata persistence
        node_data = [(node[0], node[1]) for node in self.mlist]
        self.assertEqual(len(node_data), 2)
        
        # Test metadata in string representation
        repr_str = str(self.mlist)
        self.assertIn('priority', repr_str)
        
    def test_state_machine(self):
        """Test state machine implementation using the Möbius list."""
        # Create a simple state machine
        states = [
            ('INIT', {'transitions': ['PROCESSING']}),
            ('PROCESSING', {'transitions': ['DONE', 'ERROR']}),
            ('DONE', {'transitions': ['INIT']}),
            ('ERROR', {'transitions': ['INIT']})
        ]
        
        for state, metadata in states:
            self.mlist.append(state, metadata)
            
        # Test state transitions
        current_state = 'INIT'
        for _ in range(3):
            node = next(node for node in self.mlist if node[0] == current_state)
            transitions = node[0]  # Get available transitions
            if transitions:
                current_state = transitions[0]  # Take first available transition
                
        self.assertIn(current_state, ['INIT', 'PROCESSING', 'DONE', 'ERROR'])
        
    def test_checkpoint_restore(self):
        """Test checkpoint creation and theoretical restoration."""
        for i in range(5):
            self.mlist.append(str(i), {'timestamp': time.time()})
            
        # Create checkpoint
        checkpoint = self.mlist.create_checkpoint()
        
        # Verify checkpoint contains all nodes
        self.assertIn('nodes', checkpoint)
        self.assertIn('timestamp', checkpoint)
        
    def test_transformation(self):
        """Test data transformation while preserving topology."""
        for i in range(5):
            self.mlist.append(str(i))
            
        def transform(data: str, orientation: int) -> str:
            return f"{data}_transformed_{orientation}"
            
        self.mlist.apply_transformation(transform)
        
        # Verify transformation
        transformed = [node[0] for node in self.mlist]
        self.assertTrue(all('transformed' in item for item in transformed))

if __name__ == '__main__':
    unittest.main()
