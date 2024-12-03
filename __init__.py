"""
Socratic: A Context-Aware AI Reasoning Framework
"""

__version__ = "0.1.0"
__author__ = "Codeium"
__email__ = "support@codeium.com"

from socratic.core.agent import SocraticLM
from socratic.core.dialogue import SocraticDialogue
from socratic.core.judge import ReasoningJudge
from socratic.games.reasoning import ReasoningGame
from socratic.games.creativity import CreativityGame

__all__ = [
    'SocraticLM',
    'SocraticDialogue',
    'ReasoningJudge',
    'ReasoningGame',
    'CreativityGame',
]
