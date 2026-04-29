"""
Server-Sent Events (SSE) management for real-time agent streaming
"""
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from config import logger


class StreamEventType(str, Enum):
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    PROGRESS = "progress"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class StreamEvent:
    """Represents a single streaming event"""
    type: StreamEventType
    content: str
    timestamp: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_sse_format(self) -> str:
        """Convert to Server-Sent Events format"""
        event_data = {
            "type": self.type.value,
            "content": self.content,
            "timestamp": self.timestamp,
        }
        return f"data: {json.dumps(event_data)}\n\n"


@dataclass
class Calculation:
    """Tracks a single calculation"""
    id: str
    company_name: str
    status: str  # "running", "complete", "failed"
    created_at: datetime
    events: List[StreamEvent]
    results: Optional[Dict] = None
    pdf_path: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "events_count": len(self.events),
            "results": self.results,
            "pdf_path": self.pdf_path,
            "error": self.error,
        }


class StreamManager:
    """Manages all active calculations and their streams"""

    def __init__(self, expiry_hours: int = 24):
        self.calculations: Dict[str, Calculation] = {}
        self.subscribers: Dict[str, List[Callable]] = {}  # calc_id -> list of callbacks
        self.lock = threading.RLock()
        self.expiry_hours = expiry_hours

    def create_calculation(self, company_name: str) -> str:
        """Create a new calculation and return its ID"""
        calc_id = str(uuid.uuid4())

        with self.lock:
            self.calculations[calc_id] = Calculation(
                id=calc_id,
                company_name=company_name,
                status="running",
                created_at=datetime.now(),
                events=[],
                results=None,
                pdf_path=None,
            )
            self.subscribers[calc_id] = []

        logger.info(f"✓ Created calculation: {calc_id} for {company_name}")
        return calc_id

    def add_event(self, calc_id: str, event_type: StreamEventType, content: str):
        """Add an event to a calculation stream"""
        if calc_id not in self.calculations:
            logger.warning(f"Calculation {calc_id} not found")
            return

        event = StreamEvent(type=event_type, content=content)

        with self.lock:
            self.calculations[calc_id].events.append(event)

        logger.debug(f"Event added: {event_type.value} for {calc_id}")

        # Notify subscribers
        self._notify_subscribers(calc_id, event)

    def complete_calculation(self, calc_id: str, results: Dict, pdf_path: Optional[str] = None):
        """Mark calculation as complete"""
        if calc_id not in self.calculations:
            logger.warning(f"Calculation {calc_id} not found")
            return

        with self.lock:
            calc = self.calculations[calc_id]
            calc.status = "complete"
            calc.results = results
            calc.pdf_path = pdf_path

        logger.info(f"✓ Calculation complete: {calc_id}")

        # Send final event
        self.add_event(calc_id, StreamEventType.COMPLETE, "Analysis complete")

    def fail_calculation(self, calc_id: str, error: str):
        """Mark calculation as failed"""
        if calc_id not in self.calculations:
            logger.warning(f"Calculation {calc_id} not found")
            return

        with self.lock:
            calc = self.calculations[calc_id]
            calc.status = "failed"
            calc.error = error

        logger.error(f"Calculation failed: {calc_id} - {error}")

        # Send error event
        self.add_event(calc_id, StreamEventType.ERROR, error)

    def get_calculation(self, calc_id: str) -> Optional[Calculation]:
        """Retrieve a calculation"""
        with self.lock:
            return self.calculations.get(calc_id)

    def get_events(self, calc_id: str) -> List[StreamEvent]:
        """Get all events for a calculation"""
        calc = self.get_calculation(calc_id)
        return calc.events if calc else []

    def subscribe(self, calc_id: str, callback: Callable):
        """Subscribe to calculation events"""
        with self.lock:
            if calc_id in self.subscribers:
                self.subscribers[calc_id].append(callback)
                logger.debug(f"✓ Subscriber added to {calc_id}")

    def _notify_subscribers(self, calc_id: str, event: StreamEvent):
        """Notify all subscribers of an event"""
        with self.lock:
            callbacks = self.subscribers.get(calc_id, [])

        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    def cleanup_expired(self):
        """Remove calculations older than expiry_hours"""
        cutoff = datetime.now() - timedelta(hours=self.expiry_hours)

        with self.lock:
            expired = [
                calc_id
                for calc_id, calc in self.calculations.items()
                if calc.created_at < cutoff
            ]

            for calc_id in expired:
                del self.calculations[calc_id]
                if calc_id in self.subscribers:
                    del self.subscribers[calc_id]

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired calculations")

    def get_stats(self) -> Dict:
        """Get stream manager statistics"""
        with self.lock:
            running = sum(1 for c in self.calculations.values() if c.status == "running")
            completed = sum(1 for c in self.calculations.values() if c.status == "complete")
            failed = sum(1 for c in self.calculations.values() if c.status == "failed")

            return {
                "total_calculations": len(self.calculations),
                "running": running,
                "completed": completed,
                "failed": failed,
            }


# Global stream manager instance
stream_manager = StreamManager()
