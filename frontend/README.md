# ConsensusAI Frontend

React-based web interface for ConsensusAI that provides a clean, intuitive chat experience with transparent visibility into all stages of the AI deliberation process.

## Features

- **ChatGPT-like Interface**: Familiar chat UI with conversation history
- **Multi-stage Response View**: Tabbed interface to inspect all stages of deliberation
- **Stage 1 Tabs**: View individual responses from each AI model
- **Stage 2 Tabs**: See peer evaluations and extracted rankings
- **Aggregate Rankings**: Visual ranking summary with average positions
- **Markdown Rendering**: Rich text support using react-markdown
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS Modules
- **Markdown**: react-markdown
- **HTTP Client**: fetch API
- **State Management**: React useState/useEffect

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx              # Application entry point
│   ├── App.jsx               # Main app component, conversation management
│   ├── api.js                # Backend API client
│   ├── index.css             # Global styles and markdown styling
│   ├── App.css               # App component styles
│   └── components/
│       ├── ChatInterface.jsx  # Main chat UI
│       ├── Stage1.jsx         # Individual responses viewer
│       ├── Stage2.jsx         # Peer review viewer
│       ├── Stage3.jsx         # Final synthesis viewer
│       ├── ChatInterface.css
│       ├── Stage1.css
│       ├── Stage2.css
│       └── Stage3.css
├── package.json
└── vite.config.js
```

## Components

### App.jsx
Main application component that manages:
- Conversation list and selection
- Current conversation state
- Message sending and receiving
- Metadata storage (label mappings, rankings)

### ChatInterface.jsx
Chat UI with:
- Message history display
- Multiline textarea input (Enter to send, Shift+Enter for new line)
- Stage 1/2/3 response rendering
- Loading states

### Stage1.jsx
Individual model responses:
- Tab navigation between models
- ReactMarkdown rendering of each response
- Displays model identifier

### Stage2.jsx
Peer review interface:
- Tab navigation for each model's evaluation
- Raw evaluation text (models saw anonymized labels)
- Extracted ranking display below each evaluation
- De-anonymization happens client-side for display
- Aggregate rankings summary with:
  - Average position (lower is better)
  - Number of votes received
  - Sorted best to worst

### Stage3.jsx
Final synthesis:
- Chairman's synthesized answer
- Green-tinted background to highlight conclusion
- Full markdown rendering

## Styling

The app uses a light mode theme with:
- **Primary Color**: `#4a90e4` (blue)
- **Background**: White and light grays
- **Stage 3 Highlight**: `#f0fff0` (light green)
- **Global Markdown Styling**: `.markdown-content` class with 12px padding

All markdown content is wrapped in `<div className="markdown-content">` for consistent spacing.

## API Integration

The frontend communicates with the backend via `api.js`:

```javascript
// Get all conversations
const conversations = await fetchConversations()

// Create new conversation
const conv = await createConversation("Optional Title")

// Get specific conversation
const conv = await fetchConversation(conversationId)

// Send message
const response = await sendMessage(conversationId, message)

// Delete conversation
await deleteConversation(conversationId)
```

API base URL is configured in `api.js`:
```javascript
const API_BASE_URL = "http://localhost:8001/api"
```

## Development

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```
Opens at http://localhost:5173

### Build for Production
```bash
npm run build
```
Output in `dist/` directory

### Preview Production Build
```bash
npm run preview
```

## Key Design Decisions

### Metadata Handling
- Metadata (label_to_model, aggregate_rankings) is returned by backend but NOT persisted
- Frontend stores it in component state for display
- If you reload the page, metadata is lost (by design - it's computed on-demand)

### De-anonymization Display
- Models receive anonymous labels ("Response A", "Response B") during Stage 2
- Frontend displays actual model names in **bold** for user readability
- Explanatory text clarifies this is for display only

### Markdown Styling
All markdown content uses global `.markdown-content` class (defined in `index.css`):
```css
.markdown-content {
  padding: 12px;
}

.markdown-content p {
  margin-bottom: 12px;
}

.markdown-content code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
}
```

### Input Handling
- **Enter**: Send message
- **Shift+Enter**: New line in textarea
- Textarea is multiline (3 rows) and vertically resizable

## Customization

### Change Theme Colors
Edit `index.css` and component CSS files:
```css
/* Primary color */
--primary-color: #4a90e4;

/* Stage 3 background */
--stage3-bg: #f0fff0;
```

### Adjust Layout
- Main app layout: `App.css`
- Chat interface: `components/ChatInterface.css`
- Stage components: `components/Stage1.css`, `Stage2.css`, `Stage3.css`

### Add Features
Common extension points:
- Export conversations: Add export button in `App.jsx`
- Dark mode: Add theme toggle and CSS variables
- Model filtering: Add UI in `Stage1.jsx` to filter which models to show
- Real-time updates: Implement WebSocket or SSE for streaming responses

## Troubleshooting

### CORS Errors
Ensure backend CORS settings include your frontend origin:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed
- Check backend is running on port 8001
- Verify `API_BASE_URL` in `src/api.js` matches backend

### Markdown Not Rendering
- Ensure content is wrapped in `<div className="markdown-content">`
- Check ReactMarkdown import and usage

### Slow Loading
- Large conversations may slow down due to JSON file size
- Consider pagination or lazy loading for message history
- Backend response time depends on AI model speeds (typically 5-30 seconds)

## Performance Considerations

- **Initial Load**: Fetches all conversations on mount (optimize with pagination if many)
- **Message Send**: Blocks UI while waiting for 3-stage process (5-30s typical)
- **Re-renders**: Optimized with React keys and proper state management
- **Markdown Rendering**: react-markdown is fast; no special optimization needed

## Future Enhancements

- Streaming responses instead of batch loading
- Conversation search and filtering
- Export to markdown/PDF
- Dark mode support
- Mobile-optimized responsive design
- Real-time collaboration (multiple users)
- Conversation analytics dashboard
