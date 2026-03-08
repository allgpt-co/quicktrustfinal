import { z } from "zod/v4";

export const evidenceSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  control_id: z.string().min(1, "Control is required"),
  collection_method: z.enum(["manual", "automated"]).optional(),
  status: z.enum(["pending", "collected", "approved", "rejected", "expired"]).optional(),
});

export type EvidenceFormData = z.infer<typeof evidenceSchema>;
