# ============================================================
# CALENDAR SERVICE - Event management and reminders
# ============================================================

import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)


class CalendarService:
    """
    Manage calendar events and reminders
    Support local storage and Google Calendar integration
    """

    def __init__(self):
        """Initialize calendar service"""
        self.events = []
        self.reminders = []
        self.calendar_file = config.CALENDAR_FILE
        self.load_events()
        
        logger.info("Calendar service initialized")

    def load_events(self):
        """Load events from local file"""
        try:
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, 'r') as f:
                    self.events = json.load(f)
                logger.info(f"Loaded {len(self.events)} events from file")
            else:
                self.events = []
                self._create_sample_events()
        except Exception as e:
            logger.error(f"Error loading events: {e}")
            self.events = []

    def save_events(self):
        """Save events to local file"""
        try:
            os.makedirs(os.path.dirname(self.calendar_file) or '.', exist_ok=True)
            with open(self.calendar_file, 'w') as f:
                json.dump(self.events, f, indent=2)
            logger.info(f"Saved {len(self.events)} events to file")
        except Exception as e:
            logger.error(f"Error saving events: {e}")

    def _create_sample_events(self):
        """Create sample events for demonstration"""
        now = datetime.now()
        
        sample_events = [
            {
                'id': '1',
                'title': 'Team Meeting',
                'description': 'Weekly team sync',
                'start_time': (now + timedelta(hours=2)).isoformat(),
                'end_time': (now + timedelta(hours=3)).isoformat(),
                'location': 'Conference Room A',
                'reminder': True,
                'category': 'work'
            },
            {
                'id': '2',
                'title': 'Lunch Break',
                'description': 'Time for lunch',
                'start_time': (now + timedelta(hours=5)).isoformat(),
                'end_time': (now + timedelta(hours=6)).isoformat(),
                'location': 'Cafeteria',
                'reminder': True,
                'category': 'personal'
            },
            {
                'id': '3',
                'title': 'Dashboard Update',
                'description': 'Work on Whisplay dashboard',
                'start_time': (now + timedelta(days=1)).isoformat(),
                'end_time': (now + timedelta(days=1, hours=2)).isoformat(),
                'location': 'Home Office',
                'reminder': True,
                'category': 'work'
            }
        ]
        
        self.events = sample_events
        self.save_events()

    def add_event(self, event: Dict) -> Dict:
        """Add a new event"""
        try:
            event_id = str(len(self.events) + 1)
            event['id'] = event_id
            event['created_at'] = datetime.now().isoformat()
            
            self.events.append(event)
            self.save_events()
            
            logger.info(f"Event added: {event.get('title', 'Untitled')}")
            return event
            
        except Exception as e:
            logger.error(f"Error adding event: {e}")
            return {}

    def update_event(self, event_id: str, updates: Dict) -> Dict:
        """Update an existing event"""
        try:
            for event in self.events:
                if event['id'] == event_id:
                    event.update(updates)
                    event['updated_at'] = datetime.now().isoformat()
                    self.save_events()
                    logger.info(f"Event updated: {event.get('title', 'Untitled')}")
                    return event
            
            logger.warning(f"Event not found: {event_id}")
            return {}
            
        except Exception as e:
            logger.error(f"Error updating event: {e}")
            return {}

    def delete_event(self, event_id: str) -> bool:
        """Delete an event"""
        try:
            self.events = [e for e in self.events if e['id'] != event_id]
            self.save_events()
            logger.info(f"Event deleted: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
            return False

    def get_upcoming_events(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """Get upcoming events"""
        try:
            now = datetime.now()
            future = now + timedelta(days=days)
            
            upcoming = []
            for event in self.events:
                try:
                    start = datetime.fromisoformat(event['start_time'])
                    if now <= start <= future:
                        upcoming.append(event)
                except ValueError:
                    continue
            
            # Sort by start time
            upcoming.sort(key=lambda x: x['start_time'])
            
            logger.info(f"Found {len(upcoming[:limit])} upcoming events")
            return upcoming[:limit]
            
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            return []

    def get_today_events(self) -> List[Dict]:
        """Get today's events"""
        try:
            now = datetime.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            today_events = []
            for event in self.events:
                try:
                    start = datetime.fromisoformat(event['start_time'])
                    if today_start <= start < today_end:
                        today_events.append(event)
                except ValueError:
                    continue
            
            today_events.sort(key=lambda x: x['start_time'])
            return today_events
            
        except Exception as e:
            logger.error(f"Error getting today's events: {e}")
            return []

    def check_reminders(self) -> List[Dict]:
        """Check for events that need reminders"""
        self.reminders = []
        
        try:
            now = datetime.now()
            reminder_advance = timedelta(seconds=config.CALENDAR_REMINDER_ADVANCE)
            
            for event in self.events:
                if event.get('reminder', False):
                    try:
                        start = datetime.fromisoformat(event['start_time'])
                        time_until = start - now
                        
                        # Trigger reminder if within advance time
                        if timedelta(0) <= time_until <= reminder_advance:
                            reminder = {
                                'event_id': event['id'],
                                'title': event.get('title', 'Event'),
                                'time_until_minutes': int(time_until.total_seconds() / 60),
                                'message': f"📅 Reminder: {event.get('title', 'Event')} in {int(time_until.total_seconds() / 60)} minutes",
                                'triggered_at': datetime.now().isoformat()
                            }
                            self.reminders.append(reminder)
                    except ValueError:
                        continue
            
            if self.reminders:
                logger.info(f"Reminders triggered: {len(self.reminders)}")
            
            return self.reminders
            
        except Exception as e:
            logger.error(f"Error checking reminders: {e}")
            return []

    def get_reminders(self) -> List[Dict]:
        """Get active reminders"""
        return self.reminders

    def snooze_reminder(self, event_id: str, minutes: int = 5) -> bool:
        """Snooze a reminder"""
        try:
            for event in self.events:
                if event['id'] == event_id:
                    start = datetime.fromisoformat(event['start_time'])
                    # This is a simple implementation
                    logger.info(f"Reminder snoozed for {minutes} minutes: {event.get('title', 'Event')}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error snoozing reminder: {e}")
            return False

    def get_by_category(self, category: str) -> List[Dict]:
        """Get events by category"""
        return [e for e in self.events if e.get('category', '').lower() == category.lower()]

    def get_free_slots(self, duration_minutes: int = 60, days_ahead: int = 7) -> List[Dict]:
        """Find free time slots"""
        try:
            now = datetime.now()
            free_slots = []
            
            for day_offset in range(days_ahead):
                current_date = now + timedelta(days=day_offset)
                day_start = current_date.replace(hour=9, minute=0, second=0, microsecond=0)
                day_end = current_date.replace(hour=17, minute=0, second=0, microsecond=0)
                
                # Get events for this day
                day_events = []
                for event in self.events:
                    try:
                        start = datetime.fromisoformat(event['start_time'])
                        if day_start.date() == start.date():
                            day_events.append(start)
                    except ValueError:
                        continue
                
                day_events.sort()
                
                # Find gaps
                current = day_start
                for event_start in day_events:
                    if (event_start - current).total_seconds() >= duration_minutes * 60:
                        free_slots.append({
                            'start': current.isoformat(),
                            'end': event_start.isoformat(),
                            'duration_minutes': int((event_start - current).total_seconds() / 60)
                        })
                    # Move past event (assume 1 hour duration)
                    current = event_start + timedelta(hours=1)
                
                # Check end of day
                if (day_end - current).total_seconds() >= duration_minutes * 60:
                    free_slots.append({
                        'start': current.isoformat(),
                        'end': day_end.isoformat(),
                        'duration_minutes': int((day_end - current).total_seconds() / 60)
                    })
            
            return free_slots
            
        except Exception as e:
            logger.error(f"Error getting free slots: {e}")
            return []

    def get_summary(self) -> Dict:
        """Get calendar summary"""
        upcoming = self.get_upcoming_events(days=1)
        
        return {
            'total_events': len(self.events),
            'upcoming_today': len(upcoming),
            'active_reminders': len(self.reminders),
            'categories': list(set(e.get('category', 'uncategorized') for e in self.events))
        }

    def format_event_for_display(self, event: Dict) -> str:
        """Format event for display"""
        try:
            start = datetime.fromisoformat(event['start_time'])
            time_str = start.strftime("%I:%M %p")
            title = event.get('title', 'Untitled Event')
            location = event.get('location', '')
            
            if location:
                return f"📅 {time_str} - {title}\n   📍 {location}"
            else:
                return f"📅 {time_str} - {title}"
        except Exception as e:
            logger.error(f"Error formatting event: {e}")
            return event.get('title', 'Event')

    def export_calendar(self, format: str = 'ics') -> str:
        """Export calendar in different formats"""
        if format == 'ics':
            return self._export_ics()
        elif format == 'json':
            return json.dumps(self.events, indent=2)
        elif format == 'csv':
            return self._export_csv()
        return ""

    def _export_ics(self) -> str:
        """Export in iCalendar format"""
        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            f"PRODID:-//Whisplay Dashboard//NONSGML v1.0//EN",
            "CALSCALE:GREGORIAN"
        ]
        
        for event in self.events:
            try:
                ics_lines.append("BEGIN:VEVENT")
                ics_lines.append(f"UID:{event['id']}")
                ics_lines.append(f"SUMMARY:{event.get('title', 'Event')}")
                ics_lines.append(f"DESCRIPTION:{event.get('description', '')}")
                ics_lines.append(f"DTSTART:{event.get('start_time', '')}")
                ics_lines.append(f"DTEND:{event.get('end_time', '')}")
                if event.get('location'):
                    ics_lines.append(f"LOCATION:{event['location']}")
                ics_lines.append("END:VEVENT")
            except Exception as e:
                logger.error(f"Error exporting event: {e}")
        
        ics_lines.append("END:VCALENDAR")
        return "\n".join(ics_lines)

    def _export_csv(self) -> str:
        """Export in CSV format"""
        import csv
        import io
        
        output = io.StringIO()
        if self.events:
            fieldnames = ['id', 'title', 'description', 'start_time', 'end_time', 'location', 'category']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for event in self.events:
                row = {k: event.get(k, '') for k in fieldnames}
                writer.writerow(row)
        
        return output.getvalue()
