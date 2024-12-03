"""Core reasoning game implementation.

This module implements the core reasoning game functionality for the Socratic framework.
It provides memory-enhanced reasoning capabilities through the following features:

1. Memory Management:
   - Store and retrieve insights and reasoning outputs
   - Search memories by content and type
   - Update memory context based on relevant memories

2. Reasoning Operations:
   - Process questions with memory-enhanced context
   - Generate Socratic questions for deeper understanding
   - Calculate ages and other numerical data

3. Conversation Management:
   - Maintain conversation history
   - Track question-answer pairs
   - Update memory context based on conversation flow
"""

import logging
from typing import List, Dict, Any, Optional
from mem0 import Memory
import dspy

from ..core.agent import SocraticPredictor, SocraticLM
from ..core.dialogue import SocraticDialogue
from ..utils.config import MEM0_CONFIG, MEMORY_CONFIG

logger = logging.getLogger(__name__)

class ReasoningGame:
    """Main reasoning game implementation.
    
    This class provides memory-enhanced reasoning capabilities by combining:
    1. Memory operations (store, search, retrieve)
    2. Language model reasoning
    3. Socratic dialogue generation
    
    The memory system uses the following types:
    - insight: Facts and observations
    - reasoning_output: Results from reasoning operations
    
    Memory operations are performed using the Mem0 client, which provides:
    - add: Store new memories
    - search: Search existing memories
    - get: Retrieve specific memories
    """
    
    def __init__(self, memory_client: Optional[Memory] = None):
        """Initialize the reasoning game.
        
        Args:
            memory_client: Optional memory client (creates new if None)
        """
        try:
            # Initialize memory client
            self.memory = memory_client or Memory()
            self.memory.api_key = MEMORY_CONFIG["api_key"]  # Set OpenAI API key for memory operations
            self.agent_id = MEM0_CONFIG["agent_id"]
            self.user_id = MEM0_CONFIG["user_id"]
            
            # Initialize language model
            self.lm = SocraticLM()
            dspy.settings.configure(lm=self.lm)
            
            # Initialize dialogue system
            self.dialogue = SocraticDialogue()
            
            # Initialize reasoning predictors
            self.reason = SocraticPredictor(
                signature="question: str, context: str -> answer: str",
                instructions="Provide clear, accurate answers using available context."
            )
            
            self.calculate = SocraticPredictor(
                signature="birth_date: str, reference_date: str -> age: str",
                instructions="Calculate age precisely, accounting for months and days."
            )
            
            # Initialize conversation history and memory context
            self.conversation_history: List[Dict[str, Any]] = []
            self.memory_context = ""
            
        except Exception as e:
            logger.error(f"Error initializing ReasoningGame: {str(e)}")
            raise
            
    def update_memory_context(self):
        """Update memory context from stored memories.
        
        This method:
        1. Searches for memories relevant to current context
        2. Extracts text content from memories
        3. Updates memory_context with concatenated text
        """
        try:
            memories = self.get_relevant_memories(self.memory_context)
            self.memory_context = "\n".join([m.get("text", "") for m in memories])
        except Exception as e:
            logger.error(f"Error updating memory context: {str(e)}")
            self.memory_context = ""
            
    def reason_with_memory(self, question: str) -> Dict[str, Any]:
        """Reason about a question using memory.
        
        Args:
            question: The question to reason about
            
        Returns:
            Dictionary containing the answer and related metadata
        """
        try:
            # Update memory context
            self.update_memory_context()
            
            # Generate answer using context
            result = self.reason.forward(
                question=question,
                context=self.memory_context
            )
            
            # Store the interaction
            self.conversation_history.append({
                'question': question,
                'answer': result.answer if hasattr(result, 'answer') else str(result),
                'context': self.memory_context
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error in reasoning: {str(e)}")
            return {'error': str(e)}
            
    def forward(self, question: str) -> Any:
        """Process reasoning step.
        
        Args:
            question: The input question
            
        Returns:
            Reasoning result
        """
        return self.reason_with_memory(question)
        
    def calculate_age(self, birth_date: str, reference_date: str) -> str:
        """Calculate age between two dates.
        
        Args:
            birth_date: Date of birth
            reference_date: Reference date for age calculation
            
        Returns:
            Formatted age string
        """
        try:
            result = self.calculate.forward(
                birth_date=birth_date,
                reference_date=reference_date
            )
            return result.age if hasattr(result, 'age') else str(result)
        except Exception as e:
            logger.error(f"Age calculation failed: {str(e)}")
            return str(e)
            
    def store_insight(self, insight: str, metadata: Optional[Dict[str, Any]] = None):
        """Store an insight in memory.
        
        Args:
            insight: The insight text to store
            metadata: Optional metadata about the insight
            
        Returns:
            Result from memory.add operation, or None if error
        """
        try:
            if metadata is None:
                metadata = {}
            metadata["type"] = "insight"
            result = self.memory.add(
                insight,
                user_id=self.user_id,
                metadata=metadata
            )
            logger.info(f"Stored insight: {result}")
            return result
        except Exception as e:
            logger.error(f"Error storing insight: {str(e)}")
            return None
            
    def store_reasoning_output(self, output: str, metadata: Optional[Dict[str, Any]] = None):
        """Store reasoning output in memory.
        
        Args:
            output: The reasoning output to store
            metadata: Optional metadata about the output
            
        Returns:
            Result from memory.add operation, or None if error
        """
        try:
            if metadata is None:
                metadata = {}
            metadata["type"] = "reasoning_output"
            result = self.memory.add(
                output,
                user_id=self.user_id,
                metadata=metadata
            )
            logger.info(f"Stored reasoning_output: {result}")
            return result
        except Exception as e:
            logger.error(f"Error storing reasoning output: {str(e)}")
            return None
            
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memories by query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching memories, or empty list if error
        """
        try:
            results = self.memory.search(
                query=query,
                user_id=self.user_id,
                limit=limit
            )
            logger.info(f"Found {len(results)} memories for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Error searching memories: {str(e)}")
            return []
            
    def get_relevant_memories(self, context: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get memories relevant to current context.
        
        Args:
            context: Context string to search against
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories, or empty list if error
        """
        try:
            results = self.memory.search(
                query=context,
                user_id=self.user_id,
                limit=limit
            )
            logger.info(f"Found {len(results)} relevant memories")
            return results
        except Exception as e:
            logger.error(f"Error getting relevant memories: {str(e)}")
            return []
            
    def get_memory_by_type(self, memory_type: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get memories by type.
        
        Args:
            memory_type: Type of memories to retrieve (insight or reasoning_output)
            limit: Maximum number of results to return
            
        Returns:
            List of memories of specified type, or empty list if error
        """
        try:
            results = self.memory.search(
                query=f"type:{memory_type}",
                user_id=self.user_id,
                limit=limit
            )
            logger.info(f"Found {len(results)} memories of type {memory_type}")
            return results
        except Exception as e:
            logger.error(f"Error getting memories by type: {str(e)}")
            return []
            
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history.
        
        Returns:
            List of conversation turns
        """
        return self.conversation_history
