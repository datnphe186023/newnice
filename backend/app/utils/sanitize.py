"""HTML sanitization utilities for security."""

import bleach
from typing import Optional

# Allowed HTML tags and attributes for rich content
ALLOWED_TAGS = {
    'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ol', 'ul', 'li',
    'blockquote', 'a', 'img',
    'table', 'thead', 'tbody', 'th', 'tr', 'td',
    'div', 'span', 'hr',
}

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'div': ['class'],
    'span': ['class'],
    'table': ['class'],
    'thead': ['class'],
    'tbody': ['class'],
    'tr': ['class'],
    'th': ['class'],
    'td': ['class'],
}

# CSS tags that can be used in class attributes
ALLOWED_CSS_CLASSES = {
    'text-center', 'text-left', 'text-right',
    'font-bold', 'font-italic',
    'py-2', 'py-4', 'px-2', 'px-4',
    'border', 'rounded', 'bg-gray-100',
    'w-full', 'max-w-full',
    'table-auto', 'w-full',
}


def sanitize_html(html_content: Optional[str]) -> Optional[str]:
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Removes any potentially dangerous HTML tags and attributes,
    while preserving safe formatting and structure.
    
    Args:
        html_content: Raw HTML string from user input
        
    Returns:
        Cleaned HTML string safe for display, or None if input is None
        
    Examples:
        >>> sanitize_html('<p>Safe</p><script>alert("xss")</script>')
        '<p>Safe</p>&lt;script&gt;alert("xss")&lt;/script&gt;'
        
        >>> sanitize_html('<p><a href="https://example.com">Link</a></p>')
        '<p><a href="https://example.com">Link</a></p>'
    """
    if not html_content:
        return html_content
    
    # Use bleach to clean the HTML
    cleaned = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,  # Remove disallowed tags instead of escaping
    )
    
    # Additional validation: ensure no javascript: URLs
    cleaned = _remove_javascript_urls(cleaned)
    
    return cleaned


def _remove_javascript_urls(html: str) -> str:
    """Remove javascript: protocol from href and src attributes."""
    import re
    
    # Remove javascript: from href
    html = re.sub(
        r'href\s*=\s*["\']?\s*javascript:',
        'href="',
        html,
        flags=re.IGNORECASE,
    )
    
    # Remove javascript: from src
    html = re.sub(
        r'src\s*=\s*["\']?\s*javascript:',
        'src="',
        html,
        flags=re.IGNORECASE,
    )
    
    # Remove data: from src (potential XSS vector)
    html = re.sub(
        r'src\s*=\s*["\']?\s*data:',
        'src="',
        html,
        flags=re.IGNORECASE,
    )
    
    return html


def sanitize_plain_text(text: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
    """
    Sanitize plain text input.
    
    Escapes HTML entities and optionally truncates length.
    
    Args:
        text: Raw text from user input
        max_length: Optional maximum length to enforce
        
    Returns:
        Escaped and optionally truncated text
    """
    if not text:
        return text
    
    # Escape HTML entities
    escaped = bleach.clean(
        text,
        tags=[],  # No tags allowed
        strip=True,
    )
    
    # Optionally truncate
    if max_length and len(escaped) > max_length:
        escaped = escaped[:max_length].rsplit(' ', 1)[0] + '...'
    
    return escaped
