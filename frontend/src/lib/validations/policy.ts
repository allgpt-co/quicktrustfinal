import { z } from "zod/v4";

export const policySchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  content: z.string().min(10, "Content must be at least 10 characters").max(100000),
  version: z.string().max(50).optional(),
  status: z.enum(["draft", "review", "approved", "published", "archived"]).optional(),
});

export type PolicyFormData = z.infer<typeof policySchema>;
