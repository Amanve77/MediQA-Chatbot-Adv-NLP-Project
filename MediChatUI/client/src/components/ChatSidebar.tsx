import { Cross, Trash2, Code, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

interface ChatSidebarProps {
  sessionId: string | null;
  messageCount: number;
  developerMode: boolean;
  onDeveloperModeChange: (value: boolean) => void;
  onClearChat: () => void;
  isMobile?: boolean;
  onClose?: () => void;
}

export function ChatSidebar({
  sessionId,
  messageCount,
  developerMode,
  onDeveloperModeChange,
  onClearChat,
  isMobile = false,
  onClose,
}: ChatSidebarProps) {
  return (
    <aside className={`${isMobile ? 'w-full' : 'w-72'} bg-sidebar h-full flex flex-col p-4 gap-4 border-r`}>
      {isMobile && (
        <div className="flex justify-end">
          <Button variant="ghost" size="icon" onClick={onClose} data-testid="button-close-sidebar">
            <X className="h-5 w-5" />
          </Button>
        </div>
      )}

      <div className="flex items-center gap-2 mb-2">
        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
          <Cross className="h-4 w-4 text-primary" />
        </div>
        <h2 className="text-lg font-semibold text-sidebar-foreground">Session Info</h2>
      </div>

      <Card className="p-4 space-y-3">
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Session ID</p>
          <p className="text-sm font-mono text-foreground truncate" data-testid="text-session-id">
            {sessionId || "Not started"}
          </p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Messages</p>
          <p className="text-sm font-semibold text-foreground" data-testid="text-message-count">
            {messageCount}
          </p>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Code className="h-4 w-4 text-muted-foreground" />
            <Label htmlFor="developer-mode" className="text-sm cursor-pointer">
              Developer Mode
            </Label>
          </div>
          <Switch
            id="developer-mode"
            checked={developerMode}
            onCheckedChange={onDeveloperModeChange}
            data-testid="switch-developer-mode"
          />
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          Show API response metadata
        </p>
      </Card>

      <div className="flex-1" />

      <AlertDialog>
        <AlertDialogTrigger asChild>
          <Button
            variant="outline"
            className="w-full gap-2"
            data-testid="button-clear-chat"
          >
            <Trash2 className="h-4 w-4" />
            Clear Chat
          </Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Clear chat history?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete all messages in this session. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel data-testid="button-cancel-clear">Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={onClearChat}
              data-testid="button-confirm-clear"
            >
              Clear
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <p className="text-xs text-center text-muted-foreground">
        Your AI Healthcare Companion
      </p>
    </aside>
  );
}
