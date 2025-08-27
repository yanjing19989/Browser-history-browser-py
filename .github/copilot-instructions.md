# GitHub Copilot Instructions

## Project Overview

Browser History Browser (BHB) is a Python-based web application for visualizing and analyzing browser history data. It provides a modern web interface to explore browsing patterns, statistics, and detailed history records.

## Architecture & Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for serving the FastAPI application
- **Pydantic**: Data validation and settings management
- **SQLite**: Database for browser history storage
- **Python 3.8+**: Minimum required Python version

### Frontend
- **Native HTML/CSS/JavaScript**: No framework dependencies
- **Modern responsive design**: Mobile-first approach
- **Theme switching**: Light/dark/auto themes supported
- **Material Design principles**: Clean, modern UI components

## Project Structure

```
Browser-history-browser-py/
├── backend/                 # Python backend code
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Pydantic data models
│   ├── services.py         # Business logic layer
│   └── database.py         # Database operations
├── static/                 # Frontend static files
│   ├── index.html          # Main application page
│   ├── settings.html       # Configuration page
│   ├── main.js             # Core application logic
│   ├── settings.js         # Settings page logic
│   ├── theme.js            # Theme switching functionality
│   └── style.css           # Application styles
├── server.py               # Application startup script
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Coding Conventions

### Python Backend
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Docstrings in Chinese for user-facing functions, English for internal functions
- FastAPI dependency injection patterns for database connections
- Async/await for all API endpoints
- Pydantic models for request/response validation

### Frontend JavaScript
- Use modern ES6+ features
- Consistent naming: camelCase for variables and functions
- Event-driven architecture for UI interactions
- Modular function organization by feature
- Chinese text for user-facing messages

### CSS
- CSS custom properties (variables) for theming
- Mobile-first responsive design approach
- BEM-like naming conventions for components
- Glass morphism design elements with transparency effects

## Development Workflow

### API Endpoints
- RESTful design principles
- Consistent response formats using Pydantic models
- Error handling with appropriate HTTP status codes
- API documentation auto-generated via FastAPI

### Configuration Management
- User configuration stored in `%USERPROFILE%\AppData\Local\BHB\config.json`
- Environment-agnostic path handling using `pathlib.Path`
- Graceful fallbacks for missing configuration files

### Database Operations
- Read-only access to browser databases
- Copy browser databases to application directory to avoid conflicts
- SQLite queries for history data retrieval and analysis

## Key Features to Understand

### Browser Database Integration
- Supports multiple browser history databases
- Handles locked database files by creating copies
- Validates database paths before processing

### Statistics and Analytics
- Time-based filtering (7d, 30d, 90d, 1y)
- Top sites analysis with configurable limits
- Visit frequency and pattern analysis

### User Interface
- Keyboard shortcuts (Ctrl+K for search)
- Real-time search and filtering
- Detailed record views with copy/open actions
- Theme persistence across sessions

## Privacy & Security
- All data processing happens locally
- No external data transmission
- Read-only browser database access
- Local configuration storage only

## Common Patterns

### Error Handling
```python
# Backend error handling pattern
try:
    # Operation
    result = perform_operation()
    return {"success": True, "data": result}
except Exception as e:
    raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")
```

### Frontend API Calls
```javascript
// Standard API call pattern
async function apiCall(endpoint, data = null) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: data ? 'POST' : 'GET',
            headers: { 'Content-Type': 'application/json' },
            body: data ? JSON.stringify(data) : null
        });
        return await response.json();
    } catch (error) {
        showToast('操作失败', 'error');
        throw error;
    }
}
```

## Development Notes

- The application is designed for local use only
- UI text is primarily in Chinese for the target audience
- Code comments and documentation can be in English
- Focus on performance for large browser history datasets
- Maintain compatibility with major browsers (Chrome, Firefox, Edge)