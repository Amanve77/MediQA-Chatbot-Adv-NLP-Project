import { ChatMessage } from "../ChatMessage";
import { ThemeProvider } from "../ThemeProvider";

export default function ChatMessageExample() {
  return (
    <ThemeProvider>
      <div className="p-6 space-y-4 bg-background min-h-[400px]">
        <ChatMessage
          role="user"
          content="What are the common symptoms of a cold?"
        />
        <ChatMessage
          role="assistant"
          content="Common cold symptoms include: runny or stuffy nose, sore throat, cough, congestion, mild body aches, sneezing, low-grade fever, and generally feeling unwell. These symptoms typically develop 1-3 days after exposure to a cold virus and can last for about 7-10 days."
          meta={{ source: "medical_database", confidence: 0.95 }}
          showMeta={true}
        />
      </div>
    </ThemeProvider>
  );
}
