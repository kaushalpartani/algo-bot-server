from abc import ABC, abstractmethod
from pydantic import BaseModel

class ProblemSetOptions(BaseModel):
    """
    Base class for problem set options.
    All problem set option classes should inherit from this.
    """
    pass


class ProblemSetInterface(ABC):
    """
    Abstract base class defining the interface for all problem sets.
    All problem set classes should inherit from this and implement the required methods.
    """
    
    def __init__(self):
        """
        Initialize the problem set. Should set up:
        - self.parser: argparse.ArgumentParser instance
        - self.url_base: base URL for the problem set
        - Any other necessary initialization
        """
        pass
    
    @abstractmethod
    def _get_random_problem(self) -> str:
        """
        Get a random problem URL based on the current options.
        
        Returns:
            str: The URL of a random problem, or an error message if unable to fetch
        """
        pass
    
    def process_command(self, options: str) -> str:
        """
        Process a command string and return either a problem URL or help text.
        
        Args:
            options (str): Command line options as a string
            
        Returns:
            str: Either a problem URL or help text
        """
        pass