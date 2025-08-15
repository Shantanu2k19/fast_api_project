"""
Utility helper functions for common operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import hashlib
import uuid


def generate_uuid() -> str:
    """Generate a unique UUID string."""
    return str(uuid.uuid4())


def generate_hash(data: str) -> str:
    """Generate SHA-256 hash of data."""
    return hashlib.sha256(data.encode()).hexdigest()


def format_datetime(dt: datetime, include_timezone: bool = True) -> str:
    """Format datetime to ISO format string."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    if include_timezone:
        return dt.isoformat()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(date_string: str) -> Optional[datetime]:
    """Parse datetime string to datetime object."""
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except ValueError:
        try:
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default fallback."""
    return data.get(key, default)


def filter_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """Filter dictionary to only include allowed keys."""
    return {k: v for k, v in data.items() if k in allowed_keys}


def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dictionary."""
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """Flatten a nested list."""
    return [item for sublist in nested_list for item in sublist]


def is_valid_email(email: str) -> bool:
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize string by removing extra whitespace and limiting length."""
    sanitized = ' '.join(text.split())
    
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip() + '...'
    
    return sanitized


def create_slug(text: str) -> str:
    """Create URL-friendly slug from text."""
    import re
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def paginate_results(
    items: List[Any], 
    page: int, 
    page_size: int
) -> Dict[str, Any]:
    """Paginate list of items."""
    total = len(items)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_items = items[start_idx:end_idx]
    
    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "has_next": end_idx < total,
        "has_prev": page > 1
    }
