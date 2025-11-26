import { ChatHeader } from "../ChatHeader";
import { ThemeProvider } from "../ThemeProvider";

export default function ChatHeaderExample() {
  return (
    <ThemeProvider>
      <ChatHeader
        showMenuButton={true}
        onMenuClick={() => console.log("Menu clicked")}
      />
    </ThemeProvider>
  );
}
