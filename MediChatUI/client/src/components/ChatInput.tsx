import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="p-4 border-t bg-background/80 backdrop-blur-sm">
      <div className="flex items-center gap-2 max-w-4xl mx-auto">
        <div className="flex-1 relative">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a medical or wellness question..."
            disabled={disabled}
            className="w-full h-12 px-5 pr-12 rounded-full border bg-card text-card-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
            data-testid="input-chat-message"
          />
        </div>
        <Button
          size="icon"
          onClick={handleSubmit}
          disabled={!message.trim() || disabled}
          className="h-12 w-12 rounded-full shrink-0"
          data-testid="button-send-message"
        >
          <Send className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}
