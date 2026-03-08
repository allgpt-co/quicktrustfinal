import { z } from "zod/v4";

export const controlSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  description: z.string().max(5000).optional(),
  implementation_details: z.string().max(5000).optional(),
  status: z.enum([
    "draft",
    "in_progress",
    "implemented",
    "not_implemented",
    "not_applicable",
    "needs_review",
  ]),
  automation_level: z.enum(["manual", "semi_automated", "automated"]).optional(),
  test_procedure: z.string().max(5000).optional(),
});

export type ControlFormData = z.infer<typeof controlSchema>;
