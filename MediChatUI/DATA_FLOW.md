# Data Flow Documentation

## When User Types in Textbox and Hits Enter

### 1. **Frontend Input (ChatInput.tsx)**
- **Location**: `client/src/components/ChatInput.tsx`
- **Action**: User types in textbox and presses Enter (or clicks Send button)
- **Handler**: `handleKeyDown` → `handleSubmit` → calls `onSend(message.trim())`

### 2. **Frontend Processing (chat.tsx)**
- **Location**: `client/src/pages/chat.tsx`
- **Function**: `handleSendMessage(content: string)`
- **Data Prepared**:
  ```javascript
  {
    session_id: sessionId,        // string | null (from state)
    message: content,              // string (user's input text)
    developer_mode: developerMode, // boolean (default: false)
    stream: false                  // boolean (hardcoded to false)
  }
  ```

### 3. **API Request Sent**
- **Location**: `client/src/lib/queryClient.ts`
- **Function**: `apiRequest("POST", "/api/chat", payload)`
- **Format**: JSON POST request
- **Headers**: `Content-Type: application/json`
- **Body**: JSON stringified payload
- **URL**: `/api/chat` (relative, goes to same server)

### 4. **Backend Receives Request (Express)**
- **Location**: `server/routes.ts`
- **Endpoint**: `POST /api/chat`
- **Validation**: Uses `chatRequestSchema` (Zod schema) to validate:
  ```typescript
  {
    session_id: string | null | undefined,
    message: string (min 1 character),
    developer_mode: boolean (optional, default: false),
    stream: boolean (optional, default: false)
  }
  ```

### 5. **Backend Forwards to Flask API**
- **Location**: `server/routes.ts` (lines 23-32)
- **Target**: `http://127.0.0.1:8000/chat` (or `FLASK_API_URL` env variable)
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body Sent to Flask**:
  ```json
  {
    "session_id": "string or null",
    "message": "user's message text",
    "developer_mode": false,
    "stream": false
  }
  ```

### 6. **Flask API Response**
- **Expected Response Format** (from backend code):
  ```json
  {
    "answer": "string (the AI response)",
    "session_id": "string (optional, for session management)",
    "meta": {
      // optional metadata object
    }
  }
  ```

### 7. **Backend Returns Response**
- **Location**: `server/routes.ts` (line 39)
- **Format**: JSON response
- **Status**: 200 OK (or 500 if Flask API fails)
- **Response Body**: Same as Flask API response (passed through)

### 8. **Frontend Receives Response**
- **Location**: `client/src/pages/chat.tsx` (lines 44-55)
- **Processing**:
  ```javascript
  const data = await response.json();
  const answer = data.answer || "Error: No answer returned";
  const meta = data.meta || {};
  const sid = data.session_id;
  
  if (sid) setSessionId(sid); // Update session ID if provided
  ```

### 9. **Frontend Displays Response**
- **Location**: `client/src/pages/chat.tsx`
- **Action**: Adds message to state:
  ```javascript
  setMessages((prev) => [
    ...prev,
    { role: "assistant", content: answer, meta }
  ]);
  ```
- **Display**: Rendered by `ChatMessage` component

## Data Formats Summary

### **Request Flow:**
1. **User Input**: Plain text string
2. **Frontend → Express**: JSON
   ```json
   {
     "session_id": null,
     "message": "What are the symptoms of flu?",
     "developer_mode": false,
     "stream": false
   }
   ```
3. **Express → Flask**: JSON (same format)

### **Response Flow:**
1. **Flask → Express**: JSON
   ```json
   {
     "answer": "Common symptoms of flu include...",
     "session_id": "abc123xyz",
     "meta": {}
   }
   ```
2. **Express → Frontend**: JSON (same format, passed through)
3. **Frontend Display**: Extracts `answer`, `session_id`, and `meta` fields

## Error Handling

- **Validation Error**: Returns 400 with error message in `answer` field
- **Flask API Error**: Returns 500 with error message
- **Network Error**: Frontend catches and displays error message

## Session Management

- `session_id` is optional in requests (can be `null`)
- Flask API may return a `session_id` in response
- Frontend stores `session_id` in state and includes it in subsequent requests
- This allows maintaining conversation context across messages

