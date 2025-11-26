import { ChatInput } from "../ChatInput";
import { ThemeProvider } from "../ThemeProvider";

export default function ChatInputExample() {
  return (
    <ThemeProvider>
      <div className="bg-background">
        <ChatInput
          onSend={(message) => console.log("Message sent:", message)}
          disabled={false}
        />
      </div>
    </ThemeProvider>
  );
}
