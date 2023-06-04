from dataclasses import dataclass


@dataclass
class Message:
    """Schema for a message received

    Used mostly for validation.
    """
    topic: str
    description: str
