"""Performance monitoring and metrics tracking."""

import time
import logging
from typing import Dict, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and track performance metrics."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.start_times: Dict[str, float] = {}
        
    def start_operation(self, operation_name: str) -> None:
        """Start timing an operation.
        
        Args:
            operation_name: Name of the operation to time
        """
        self.start_times[operation_name] = time.time()
        
    def end_operation(self, operation_name: str, success: bool = True) -> None:
        """End timing an operation and record metrics.
        
        Args:
            operation_name: Name of the operation
            success: Whether the operation succeeded
        """
        if operation_name in self.start_times:
            duration = time.time() - self.start_times[operation_name]
            
            if operation_name not in self.metrics:
                self.metrics[operation_name] = {
                    'count': 0,
                    'success_count': 0,
                    'total_duration': 0,
                    'min_duration': float('inf'),
                    'max_duration': 0
                }
                
            metrics = self.metrics[operation_name]
            metrics['count'] += 1
            if success:
                metrics['success_count'] += 1
            metrics['total_duration'] += duration
            metrics['min_duration'] = min(metrics['min_duration'], duration)
            metrics['max_duration'] = max(metrics['max_duration'], duration)
            metrics['avg_duration'] = metrics['total_duration'] / metrics['count']
            metrics['success_rate'] = metrics['success_count'] / metrics['count']
            
            del self.start_times[operation_name]
            
    def get_metrics(self, operation_name: Optional[str] = None) -> Dict[str, Any]:
        """Get metrics for an operation or all operations.
        
        Args:
            operation_name: Optional name of specific operation
            
        Returns:
            Dictionary of metrics
        """
        if operation_name:
            return self.metrics.get(operation_name, {})
        return dict(self.metrics)
        
    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.start_times.clear()
