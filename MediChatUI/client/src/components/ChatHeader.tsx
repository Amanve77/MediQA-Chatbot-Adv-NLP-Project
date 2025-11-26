import { Heart, Stethoscope, Menu } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  onMenuClick?: () => void;
  showMenuButton?: boolean;
}

export function ChatHeader({ onMenuClick, showMenuButton = false }: ChatHeaderProps) {
  return (
    <header className="h-16 border-b bg-gradient-to-r from-primary/10 via-accent/20 to-primary/10 flex items-center justify-between px-4 gap-4">
      <div className="flex items-center gap-2">
        {showMenuButton && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onMenuClick}
            data-testid="button-menu"
            className="lg:hidden"
          >
            <Menu className="h-5 w-5" />
          </Button>
        )}
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
            <Stethoscope className="h-5 w-5 text-primary" />
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Heart className="h-5 w-5 text-primary animate-heartbeat" />
        <h1 className="text-lg font-semibold text-foreground">
          Medical Wellness Assistant
        </h1>
      </div>

      <ThemeToggle />
    </header>
  );
}
