import { Stethoscope } from "lucide-react";

export function ThinkingIndicator() {
  return (
    <div className="flex items-start gap-3 animate-slide-in-left">
      <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
        <Stethoscope className="h-5 w-5 text-primary" />
      </div>
      <div className="bg-card border rounded-2xl rounded-bl-sm p-4 max-w-2xl">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot" style={{ animationDelay: "0ms" }} />
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot" style={{ animationDelay: "200ms" }} />
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot" style={{ animationDelay: "400ms" }} />
          <span className="text-sm text-muted-foreground ml-2">Thinking...</span>
        </div>
      </div>
    </div>
  );
}
