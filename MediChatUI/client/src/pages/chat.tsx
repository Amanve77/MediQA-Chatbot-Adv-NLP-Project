import { useState, useRef, useEffect } from "react";
import { ChatHeader } from "@/components/ChatHeader";
import { ChatSidebar } from "@/components/ChatSidebar";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { ThinkingIndicator } from "@/components/ThinkingIndicator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { apiRequest } from "@/lib/queryClient";

interface Message {
  role: "user" | "assistant";
  content: string;
  meta?: Record<string, unknown>;
}

export default function ChatPage() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [developerMode, setDeveloperMode] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isThinking]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsThinking(true);

    try {
      const payload = {
        session_id: sessionId,
        message: content,
        developer_mode: developerMode,
        stream: false,
      };

      const response = await apiRequest("POST", "/api/chat", payload);
      const data = await response.json();
      const answer = data.answer || "Error: No answer returned";
      const meta = data.meta || {};
      const sid = data.session_id;

      if (sid) setSessionId(sid);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer, meta },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error instanceof Error ? error.message : "Failed to connect to server"}`,
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await apiRequest("POST", "/api/clear_memory", { session_id: sessionId });
    } catch {
      console.log("Failed to clear server memory");
    }
    setMessages([]);
    setSidebarOpen(false);
  };

  return (
    <div className="flex h-screen bg-background">
      <div className="hidden lg:block">
        <ChatSidebar
          sessionId={sessionId}
          messageCount={messages.length}
          developerMode={developerMode}
          onDeveloperModeChange={setDeveloperMode}
          onClearChat={handleClearChat}
        />
      </div>

      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetContent side="left" className="p-0 w-72">
          <ChatSidebar
            sessionId={sessionId}
            messageCount={messages.length}
            developerMode={developerMode}
            onDeveloperModeChange={setDeveloperMode}
            onClearChat={handleClearChat}
            isMobile
            onClose={() => setSidebarOpen(false)}
          />
        </SheetContent>
      </Sheet>

      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatHeader
          onMenuClick={() => setSidebarOpen(true)}
          showMenuButton
        />

        <ScrollArea className="flex-1" ref={scrollRef}>
          <div className="p-4 lg:p-6 space-y-6 max-w-4xl mx-auto pb-24">
            {messages.length === 0 && !isThinking && (
              <div className="text-center py-12">
                <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-4">
                  <svg
                    className="w-10 h-10 text-primary"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-foreground mb-2">
                  Welcome to Medical Wellness Assistant
                </h2>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Ask me anything about symptoms, treatments, medications, or
                  general wellness advice. I'm here to help!
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                role={message.role}
                content={message.content}
                meta={message.meta}
                showMeta={developerMode}
              />
            ))}

            {isThinking && <ThinkingIndicator />}
          </div>
        </ScrollArea>

        <ChatInput onSend={handleSendMessage} disabled={isThinking} />
      </div>
    </div>
  );
}
