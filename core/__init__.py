"""Core components of the Socratic framework."""

from .agent import SocraticLM
from .dialogue import SocraticDialogue
from .judge import ReasoningJudge

__all__ = ['SocraticLM', 'SocraticDialogue', 'ReasoningJudge']
