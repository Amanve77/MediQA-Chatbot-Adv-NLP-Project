import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { chatRequestSchema, clearMemorySchema } from "@shared/schema";
import { fromZodError } from "zod-validation-error";

const FLASK_API_URL = process.env.FLASK_API_URL || "http://127.0.0.1:8000";

export async function registerRoutes(app: Express): Promise<Server> {
  app.post("/api/chat", async (req: Request, res: Response) => {
    const validation = chatRequestSchema.safeParse(req.body);

    if (!validation.success) {
      const errorMessage = fromZodError(validation.error).toString();
      return res.status(400).json({
        answer: `Validation Error: ${errorMessage}`,
        meta: { validation_error: true },
      });
    }

    const { session_id, message, developer_mode, stream } = validation.data;

    try {
      const response = await fetch(`${FLASK_API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id,
          message,
          developer_mode,
          stream,
        }),
      });

      if (!response.ok) {
        throw new Error(`Flask API responded with status ${response.status}`);
      }

      const data = await response.json();
      res.json(data);
    } catch (error) {
      console.error("Chat API error:", error);
      res.status(500).json({
        answer: "Error: Unable to connect to the medical assistant backend. Please ensure the Flask API is running.",
        meta: { error: error instanceof Error ? error.message : "Unknown error" },
      });
    }
  });

  app.post("/api/clear_memory", async (req: Request, res: Response) => {
    const validation = clearMemorySchema.safeParse(req.body);

    if (!validation.success) {
      const errorMessage = fromZodError(validation.error).toString();
      return res.status(400).json({
        success: false,
        error: errorMessage,
      });
    }

    const { session_id } = validation.data;

    try {
      const response = await fetch(`${FLASK_API_URL}/clear_memory`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id }),
      });

      if (!response.ok) {
        throw new Error(`Flask API responded with status ${response.status}`);
      }

      const data = await response.json();
      res.json(data);
    } catch (error) {
      console.error("Clear memory API error:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
