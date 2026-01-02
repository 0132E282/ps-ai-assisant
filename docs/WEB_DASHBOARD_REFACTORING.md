# Web Dashboard Refactoring

## Overview
The web dashboard has been refactored to follow a clean MVC architecture pattern. All API endpoints have been moved from `web_dashboard.py` into dedicated controller files for better organization and maintainability.

## New Structure

### Main Application File
**`web_dashboard.py`** - Now only contains:
- FastAPI app initialization
- CORS middleware configuration
- Router registration
- Static file mounting
- Server startup logic

### Controllers Directory (`controllers/`)

#### 1. **chat_controller.py**
Handles all chat-related operations:
- `GET /api/chat` - Get chat history
- `POST /api/chat` - Send new message
- `DELETE /api/chat/{chat_id}` - Delete specific chat message
- `DELETE /api/chat` - Clear all chat history

#### 2. **behavior_controller.py**
Manages robot behaviors:
- `GET /api/behaviors` - Get all active behaviors
- `POST /api/execute-behavior/{behavior_id}` - Execute a specific behavior
- `POST /api/add-behavior` - Add new behavior
- `DELETE /api/behavior/{behavior_id}` - Delete a behavior

#### 3. **settings_controller.py**
Handles system settings and prompts:
- `GET /api/current-prompt` - Get current system prompt
- `POST /api/update-prompt` - Update system prompt
- `GET /api/settings` - Get all settings
- `POST /api/settings` - Update settings

#### 4. **frontend_controller.py**
Serves the frontend application:
- `GET /` - Serve the React frontend HTML

#### 5. **robot_controller.py**
Hardware robot control logic (existing)

#### 6. **pc_controller.py**
PC application control logic (existing)

## Benefits of This Refactoring

1. **Separation of Concerns**: Each controller handles a specific domain
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Scalability**: Simple to add new endpoints by creating new controllers
4. **Testability**: Controllers can be tested independently
5. **Readability**: Main application file is now clean and focused

## API Endpoints Summary

### Chat Endpoints
```
GET    /api/chat                    - Get chat history
POST   /api/chat                    - Send message
DELETE /api/chat/{chat_id}          - Delete message
DELETE /api/chat                    - Clear history
```

### Behavior Endpoints
```
GET    /api/behaviors               - List behaviors
POST   /api/execute-behavior/{id}   - Execute behavior
POST   /api/add-behavior            - Add behavior
DELETE /api/behavior/{id}           - Delete behavior
```

### Settings Endpoints
```
GET    /api/current-prompt          - Get system prompt
POST   /api/update-prompt           - Update prompt
GET    /api/settings                - Get all settings
POST   /api/settings                - Update settings
GET    /api/models                  - Get available AI models
```

### Frontend
```
GET    /                            - Serve frontend app
```

## Migration Notes

- All existing API endpoints remain unchanged
- No breaking changes to the API contract
- Frontend code does not need any modifications
- Database operations remain the same
