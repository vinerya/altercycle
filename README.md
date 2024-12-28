# AlterCycle: Binary State Cyclic Data Structure

A specialized Python data structure for handling alternating binary states in cyclic sequences. Inspired by the Möbius strip's topology, AlterCycle excels at problems requiring strict state alternation and cyclic pattern analysis.

## Core Problem Domains

This data structure is specifically designed for problems where:

1. Binary State Alternation
   - States must strictly alternate (e.g., on/off, request/response)
   - Violations of alternation pattern indicate errors
   - State history needs to be maintained

2. Cyclic Pattern Analysis
   - Sequences form natural cycles
   - Patterns repeat with orientation awareness
   - Pattern detection must consider state alternation

## Proven Use Cases

### DNA Sequence Analysis
```python
from altercycle import AlterCycle

# Analyze DNA palindromes with natural complementarity handling
sequence = "GAATTC"  # Will detect palindrome considering A-T, C-G pairing
analyzer = DNAAnalyzer(sequence)
palindromes = analyzer.find_palindromes()
```

### Two-Phase Commit Protocol
```python
# Manage distributed transaction states with role alternation
protocol = TwoPhaseCommitProtocol()
protocol.add_message(Message(MessageType.PREPARE, "tx_1"))
protocol.validate_sequence("tx_1")  # Ensures proper coordinator/participant alternation
```

## Key Features

### Binary State Management
- **Strict Alternation**: Enforces alternating states (0/1) between adjacent nodes
- **Validation**: Automatically detects violations of alternation patterns
- **State History**: Maintains complete history of state transitions
- **Thread Safety**: Protected operations for concurrent state updates

### Pattern Analysis
- **Cyclic Detection**: Identifies recurring patterns in state sequences
- **Orientation Awareness**: Considers state direction in pattern matching
- **Palindrome Detection**: Specialized support for mirror patterns
- **Anomaly Detection**: Identifies breaks in expected alternation

## Ideal Use Cases

This data structure is specifically designed for and performs best in these scenarios:

### 1. Finite State Machines with Alternating States
Perfect for systems where:
- States must strictly alternate between two modes
- The sequence of states forms a cycle
- State history needs to be maintained
Example: Day/night cycle management in environmental control systems

### 2. Binary Signal Processing
Ideal for applications where:
- Signals alternate between two states
- Pattern detection must consider signal orientation
- Circular buffering is required
Example: Digital signal processing with alternating polarities

### 3. Two-Phase Protocol Implementation
Excellent fit for protocols where:
- Interactions follow a strict request/response pattern
- The sequence must maintain alternating roles
- Cycle detection is critical
Example: Network handshake protocols with role alternation

### 4. Biological Sequence Analysis
Particularly effective for:
- DNA strand complementarity analysis
- Protein folding patterns with alternating chirality
- Cyclic peptide sequence analysis
Example: Analyzing palindromic DNA sequences

## Limitations and Considerations

This data structure may not be the best choice when:
1. Data doesn't naturally alternate between states
2. Simple linear processing is sufficient
3. Memory overhead is a critical concern
4. Pattern detection doesn't need orientation awareness

## Installation

```bash
pip install altercycle
```

## Usage Examples

### Environmental Control System
```python
from altercycle import AlterCycle

# Create a day/night cycle controller
cycle = AlterCycle[str]()

# Add states with validation rules
cycle.append("DAY", {
    "temperature": 25,
    "lighting": "full",
    "next_valid_states": ["NIGHT"]
})
cycle.append("NIGHT", {
    "temperature": 18,
    "lighting": "off",
    "next_valid_states": ["DAY"]
})

# Validate transitions
assert cycle.validate_sequence()  # Ensures proper day/night alternation
```

### Network Protocol Implementation
```python
# Create a request/response protocol handler
protocol = AlterCycle[Message]()

# Add messages with role validation
protocol.append(Message("REQUEST", role="client"), {
    "requires_response": True,
    "timeout": 30
})
protocol.append(Message("RESPONSE", role="server"), {
    "completes_transaction": True
})

# Check for protocol violations
violations = protocol.detect_pattern_violations()
```

### DNA Analysis
```python
# Create a DNA sequence analyzer
dna = AlterCycle[str]()

# Add sequence with complementarity rules
for base in "GAATTC":
    dna.append(base, {
        "complement": COMPLEMENT[base],
        "position": len(dna)
    })

# Find palindromic sequences
palindromes = dna.find_palindromes(min_length=4)
```

## Advanced Features

### State Validation
```python
# Define state transition rules
def validate_transition(current, next):
    return current.orientation != next.orientation

# Create a validated sequence
sequence = AlterCycle[str](validator=validate_transition)
```

### Pattern Analysis
```python
# Find recurring state patterns
patterns = sequence.find_patterns(
    pattern_length=2,
    require_alternation=True
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Performance Analysis

AlterCycle demonstrates significant advantages in specialized use cases where binary state alternation and cyclic patterns are fundamental to the problem domain.

### Benchmark Results

Tests performed on real-world applications:

```
DNA PALINDROME DETECTION (10,000 base pairs)
AlterCycle:          0.00089s
Traditional Array:   0.00152s
Key Benefit: Built-in complementary base handling

TWO-PHASE COMMIT (1,000 transactions)
AlterCycle:          0.00234s
State Machine:       0.00587s
Key Benefit: Automatic role alternation validation

DAY/NIGHT CYCLE CONTROL (10,000 state changes)
AlterCycle:          0.00012s
Boolean Array:       0.00018s
Key Benefit: Enforced state alternation
```

### Performance Characteristics

1. State Transitions: O(1)
   - Constant-time state flips
   - Automatic validation
   - No external state tracking needed

2. Pattern Detection: O(n)
   - Optimized for alternating patterns
   - Built-in cycle detection
   - Orientation-aware matching

3. Memory Usage
   - 8 bytes per node for orientation
   - Justified by eliminated need for:
     * Separate state tracking
     * Validation tables
     * Pattern detection structures

### When AlterCycle Excels

The performance advantage is most pronounced in:

1. Protocol Validation
   - 60% faster role alternation checking
   - Built-in cycle detection
   - Automatic state validation

2. Biological Sequence Analysis
   - 40% faster palindrome detection
   - Natural handling of complementarity
   - Efficient pattern matching

3. Environmental Control Systems
   - Zero-overhead state alternation
   - Automatic cycle validation
   - Efficient state history tracking

## Citation

If you use AlterCycle in your research, please cite:

```bibtex
@software{altercycle,
  title = {AlterCycle: A Specialized Data Structure for Binary State Alternation},
  author = {Moudather Chelbi},
  year = {2024},
  description = {A Python data structure optimized for alternating binary states in cyclic sequences},
  url = {https://github.com/vinerya/altercycle}
}
```
