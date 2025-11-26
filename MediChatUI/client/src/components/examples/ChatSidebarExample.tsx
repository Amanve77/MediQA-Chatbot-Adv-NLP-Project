import { ChatSidebar } from "../ChatSidebar";
import { ThemeProvider } from "../ThemeProvider";

export default function ChatSidebarExample() {
  return (
    <ThemeProvider>
      <div className="h-[600px]">
        <ChatSidebar
          sessionId="abc123-def456-ghi789"
          messageCount={5}
          developerMode={false}
          onDeveloperModeChange={(value) => console.log("Developer mode:", value)}
          onClearChat={() => console.log("Clear chat clicked")}
        />
      </div>
    </ThemeProvider>
  );
}
