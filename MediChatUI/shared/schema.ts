import { sql } from "drizzle-orm";
import { pgTable, text, varchar } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export const chatRequestSchema = z.object({
  session_id: z.string().nullable().optional(),
  message: z.string().min(1, "Message cannot be empty"),
  developer_mode: z.boolean().optional().default(false),
  stream: z.boolean().optional().default(false),
});

export const clearMemorySchema = z.object({
  session_id: z.string().nullable().optional(),
});

export type ChatRequest = z.infer<typeof chatRequestSchema>;
export type ClearMemoryRequest = z.infer<typeof clearMemorySchema>;
