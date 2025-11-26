import { Stethoscope, User, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  meta?: Record<string, unknown>;
  showMeta?: boolean;
}

export function ChatMessage({ role, content, meta, showMeta = false }: ChatMessageProps) {
  const [metaExpanded, setMetaExpanded] = useState(false);
  const isUser = role === "user";

  return (
    <div
      className={`flex items-start gap-3 ${isUser ? "flex-row-reverse animate-slide-in-right" : "animate-slide-in-left"}`}
    >
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-primary/20"
        }`}
      >
        {isUser ? (
          <User className="h-5 w-5" />
        ) : (
          <Stethoscope className="h-5 w-5 text-primary" />
        )}
      </div>

      <div className="flex flex-col gap-1 max-w-lg lg:max-w-2xl">
        <div
          className={`p-4 ${
            isUser
              ? "bg-primary text-primary-foreground rounded-2xl rounded-br-sm"
              : "bg-card border rounded-2xl rounded-bl-sm text-card-foreground"
          }`}
          data-testid={`message-${role}`}
        >
          <p className="text-sm whitespace-pre-wrap">{content}</p>
        </div>

        {showMeta && meta && Object.keys(meta).length > 0 && (
          <div className="ml-1">
            <button
              onClick={() => setMetaExpanded(!metaExpanded)}
              className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
              data-testid="button-toggle-meta"
            >
              {metaExpanded ? (
                <ChevronUp className="h-3 w-3" />
              ) : (
                <ChevronDown className="h-3 w-3" />
              )}
              Metadata
            </button>
            {metaExpanded && (
              <div className="mt-2 p-3 bg-muted rounded-md border-l-2 border-primary/50">
                <pre className="text-xs font-mono text-muted-foreground overflow-x-auto">
                  {JSON.stringify(meta, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
