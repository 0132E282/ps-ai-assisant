# API Models Endpoint

## Endpoint
```
GET /api/models
```

## Description
Lấy danh sách tất cả các AI models có thể sử dụng trong hệ thống, cùng với model mặc định hiện tại.

## Response
```json
{
  "models": {
    "gemini-2.5 pro": "models/gemini-2.5-pro",
    "Gemini 2.5 Flash": "models/gemini-2.5-flash",
    "Gemini 3 Pro Preview": "gemini-3-pro-preview",
    "Gemini 2.0 Flash": "gemini-2.0-flash-exp",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro"
  },
  "default_model": "models/gemini-2.5-flash"
}
```

## Usage in Frontend (React)

### Example 1: Fetch models on component mount
```jsx
import { useEffect, useState } from 'react';

function ModelSelector() {
  const [models, setModels] = useState({});
  const [defaultModel, setDefaultModel] = useState('');
  const [selectedModel, setSelectedModel] = useState('');

  useEffect(() => {
    fetch('/api/models')
      .then(res => res.json())
      .then(data => {
        setModels(data.models);
        setDefaultModel(data.default_model);
        setSelectedModel(data.default_model);
      });
  }, []);

  return (
    <select value={selectedModel} onChange={e => setSelectedModel(e.target.value)}>
      {Object.entries(models).map(([name, value]) => (
        <option key={value} value={value}>
          {name} {value === defaultModel && '(Default)'}
        </option>
      ))}
    </select>
  );
}
```

### Example 2: Update Settings.jsx to use dynamic models
```jsx
// In Settings.jsx, replace hardcoded options with:

const [availableModels, setAvailableModels] = useState({});

useEffect(() => {
  // Fetch available models
  fetch('/api/models')
    .then(res => res.json())
    .then(data => setAvailableModels(data.models));
}, []);

// Then in the select element:
<select
  value={promptData.gemini_model}
  onChange={e => setPromptData({ ...promptData, gemini_model: e.target.value })}
>
  {Object.entries(availableModels).map(([name, value]) => (
    <option key={value} value={value}>{name}</option>
  ))}
</select>
```

## Benefits
- ✅ **Dynamic**: Models are loaded from backend config
- ✅ **Maintainable**: Add new models in `config.py` only
- ✅ **Consistent**: Frontend always shows available models
- ✅ **No hardcoding**: Remove duplicate model lists

## Testing
```bash
# Test the API
curl http://localhost:8000/api/models

# Pretty print JSON
curl -s http://localhost:8000/api/models | python3 -m json.tool
```
