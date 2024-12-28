"""
Two-Phase Commit Protocol Example

This example demonstrates how AlterCycle's binary state alternation
naturally maps to coordinator/participant roles in a two-phase commit protocol.

The binary state alternation maps perfectly to this problem:
- State 0: Coordinator role (sends commands)
- State 1: Participant role (sends responses)

This implementation ensures:
1. Strict role alternation
2. Proper message ordering
3. Protocol violation detection
4. Transaction state tracking
"""

from altercycle_core import AlterCycle
from typing import Optional, Dict, List
from enum import Enum
import threading
import time
import random

class MessageType(Enum):
    PREPARE = "PREPARE"      # Coordinator -> Participant
    PREPARED = "PREPARED"    # Participant -> Coordinator
    COMMIT = "COMMIT"        # Coordinator -> Participant
    COMMITTED = "COMMITTED"  # Participant -> Coordinator
    ABORT = "ABORT"         # Coordinator -> Participant
    ABORTED = "ABORTED"     # Participant -> Coordinator

class TransactionState(Enum):
    INITIAL = "INITIAL"
    PREPARING = "PREPARING"
    PREPARED = "PREPARED"
    COMMITTING = "COMMITTING"
    COMMITTED = "COMMITTED"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"

class Message:
    def __init__(self, msg_type: MessageType, transaction_id: str, 
                 sender: str, receiver: str):
        self.type = msg_type
        self.transaction_id = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.timestamp = time.time()

class TwoPhaseCommitProtocol:
    def __init__(self):
        self.message_sequence = AlterCycle[Message]()
        self.transactions: Dict[str, TransactionState] = {}
        self._lock = threading.Lock()
        
    def add_message(self, message: Message) -> None:
        """
        Add a message to the protocol sequence.
        AlterCycle ensures proper role alternation.
        """
        with self._lock:
            # Add message with metadata
            self.message_sequence.append(message, {
                'timestamp': message.timestamp,
                'transaction_id': message.transaction_id,
                'state': self.transactions.get(
                    message.transaction_id, 
                    TransactionState.INITIAL
                ).value
            })
            
            # Update transaction state
            self._update_transaction_state(message)
            
    def _update_transaction_state(self, message: Message) -> None:
        """Update transaction state based on message type."""
        current_state = self.transactions.get(
            message.transaction_id, 
            TransactionState.INITIAL
        )
        
        # State transition logic
        if message.type == MessageType.PREPARE:
            self.transactions[message.transaction_id] = TransactionState.PREPARING
        elif message.type == MessageType.PREPARED:
            self.transactions[message.transaction_id] = TransactionState.PREPARED
        elif message.type == MessageType.COMMIT:
            self.transactions[message.transaction_id] = TransactionState.COMMITTING
        elif message.type == MessageType.COMMITTED:
            self.transactions[message.transaction_id] = TransactionState.COMMITTED
        elif message.type == MessageType.ABORT:
            self.transactions[message.transaction_id] = TransactionState.ABORTING
        elif message.type == MessageType.ABORTED:
            self.transactions[message.transaction_id] = TransactionState.ABORTED
            
    def validate_sequence(self, transaction_id: str) -> bool:
        """
        Validate the message sequence for a transaction.
        AlterCycle's state alternation ensures proper role alternation.
        """
        valid_sequences = {
            MessageType.PREPARE: {MessageType.PREPARED, MessageType.ABORTED},
            MessageType.PREPARED: {MessageType.COMMIT, MessageType.ABORT},
            MessageType.COMMIT: {MessageType.COMMITTED},
            MessageType.ABORT: {MessageType.ABORTED}
        }
        
        # Get messages for this transaction in sequence
        messages = [
            msg for msg, state in self.message_sequence
            if msg.transaction_id == transaction_id
        ]
        
        if not messages:
            return False
            
        # Check sequence validity
        for i in range(len(messages) - 1):
            current_msg = messages[i]
            next_msg = messages[i + 1]
            
            # Check if the next message type is valid
            if (current_msg.type in valid_sequences and 
                next_msg.type not in valid_sequences[current_msg.type]):
                return False
                
        return True
        
    def detect_violations(self) -> List[str]:
        """
        Detect protocol violations using pattern analysis.
        Uses AlterCycle's pattern detection capability.
        """
        patterns = self.message_sequence.find_patterns(pattern_length=2)
        violations = []
        
        for pattern, frequency in patterns:
            if frequency > 1:  # Pattern repeats
                msgs = [msg.type.value for msg, _ in pattern]
                violations.append(" -> ".join(msgs))
                
        return violations

def simulate_transaction():
    """Simulate a two-phase commit transaction."""
    protocol = TwoPhaseCommitProtocol()
    transaction_id = f"tx_{random.randint(1000, 9999)}"
    
    # Successful transaction sequence
    messages = [
        Message(MessageType.PREPARE, transaction_id, "coordinator", "participant1"),
        Message(MessageType.PREPARED, transaction_id, "participant1", "coordinator"),
        Message(MessageType.COMMIT, transaction_id, "coordinator", "participant1"),
        Message(MessageType.COMMITTED, transaction_id, "participant1", "coordinator")
    ]
    
    print(f"\nSimulating transaction: {transaction_id}")
    
    start_time = time.time()
    for msg in messages:
        protocol.add_message(msg)
        print(f"Added message: {msg.type.value}")
        
    # Validate sequence
    is_valid = protocol.validate_sequence(transaction_id)
    print(f"\nTransaction sequence valid: {is_valid}")
    
    # Check for violations
    violations = protocol.detect_violations()
    if violations:
        print("\nDetected protocol violations:")
        for violation in violations:
            print(f"  {violation}")
            
    end_time = time.time()
    print(f"\nTransaction processing time: {end_time - start_time:.6f}s")
    
    return protocol

if __name__ == "__main__":
    # Simulate multiple transactions
    protocols = [simulate_transaction() for _ in range(3)]
    
    # Compare with traditional approach
    print("\nComparing with traditional approach...")
    
    def traditional_validate_sequence(messages: List[Message]) -> bool:
        """Traditional sequence validation without AlterCycle."""
        valid_sequences = {
            MessageType.PREPARE: {MessageType.PREPARED, MessageType.ABORTED},
            MessageType.PREPARED: {MessageType.COMMIT, MessageType.ABORT},
            MessageType.COMMIT: {MessageType.COMMITTED},
            MessageType.ABORT: {MessageType.ABORTED}
        }
        
        for i in range(len(messages) - 1):
            if (messages[i].type in valid_sequences and 
                messages[i + 1].type not in valid_sequences[messages[i].type]):
                return False
        return True
    
    # Performance comparison
    transaction_id = "tx_9999"
    messages = [
        Message(MessageType.PREPARE, transaction_id, "coordinator", "participant1"),
        Message(MessageType.PREPARED, transaction_id, "participant1", "coordinator"),
        Message(MessageType.COMMIT, transaction_id, "coordinator", "participant1"),
        Message(MessageType.COMMITTED, transaction_id, "participant1", "coordinator")
    ] * 100  # Create a longer sequence for testing
    
    # AlterCycle approach
    protocol = TwoPhaseCommitProtocol()
    start = time.time()
    for msg in messages:
        protocol.add_message(msg)
    protocol.validate_sequence(transaction_id)
    altercycle_time = time.time() - start
    
    # Traditional approach
    start = time.time()
    traditional_validate_sequence(messages)
    traditional_time = time.time() - start
    
    print(f"\nPerformance Comparison (sequence length: {len(messages)})")
    print(f"AlterCycle approach:     {altercycle_time:.6f}s")
    print(f"Traditional approach:    {traditional_time:.6f}s")
    print(f"Speedup factor:         {traditional_time/altercycle_time:.2f}x")
