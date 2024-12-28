from typing import Any, Optional, TypeVar

T = TypeVar('T')

class AlterNode:
    """
    A node in an AlterCycle that maintains binary state alternation.
    
    The node's orientation (0 or 1) represents its binary state,
    enabling strict alternation and pattern detection.
    
    Attributes:
        data: The data stored in the node
        orientation: Binary state (0 or 1) representing position on Möbius strip
        next: Reference to the next node in the sequence
        metadata: Optional dictionary for storing additional node information
    """
    
    def __init__(self, data: T, orientation: int = 0, metadata: Optional[dict] = None) -> None:
        """
        Initialize a new AlterNode.
        
        Args:
            data: The data to store in the node
            orientation: Initial orientation (0 or 1)
            metadata: Optional dictionary for additional node information
        
        Raises:
            ValueError: If orientation is not 0 or 1
        """
        if orientation not in (0, 1):
            raise ValueError("Orientation must be 0 or 1")
        
        self.data: T = data
        self.orientation: int = orientation
        self.next: Optional['AlterNode'] = None
        self.metadata: dict = metadata or {}
        
    def flip_orientation(self) -> None:
        """Invert the node's orientation."""
        self.orientation = 1 - self.orientation
        
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the node.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        
    def get_metadata(self, key: str) -> Any:
        """
        Retrieve metadata from the node.
        
        Args:
            key: Metadata key
            
        Returns:
            The metadata value if it exists
            
        Raises:
            KeyError: If the metadata key doesn't exist
        """
        return self.metadata[key]
        
    def __eq__(self, other: object) -> bool:
        """Enable node comparison based on data and orientation."""
        if not isinstance(other, AlterNode):
            return NotImplemented
        return (self.data == other.data and 
                self.orientation == other.orientation and 
                self.metadata == other.metadata)
                
    def __hash__(self) -> int:
        """Make nodes hashable for use in sets and as dict keys."""
        return hash((self.data, self.orientation, 
                    tuple(sorted(self.metadata.items()))))
        
    def __repr__(self) -> str:
        """Detailed string representation including metadata."""
        meta_str = f", metadata={self.metadata}" if self.metadata else ""
        return f"AlterNode(data={self.data}, orientation={self.orientation}{meta_str})"
