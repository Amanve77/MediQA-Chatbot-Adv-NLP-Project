import { ThinkingIndicator } from "../ThinkingIndicator";
import { ThemeProvider } from "../ThemeProvider";

export default function ThinkingIndicatorExample() {
  return (
    <ThemeProvider>
      <div className="p-6 bg-background min-h-[200px]">
        <ThinkingIndicator />
      </div>
    </ThemeProvider>
  );
}
