import { z } from "zod/v4";

export const riskSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  description: z.string().max(5000).optional(),
  category: z.enum(["operational", "compliance", "security", "financial"]),
  likelihood: z.number().int().min(1).max(5),
  impact: z.number().int().min(1).max(5),
  risk_level: z.enum(["low", "medium", "high", "critical"]),
  treatment_type: z.enum(["mitigate", "accept", "transfer", "avoid"]).optional(),
});

export type RiskFormData = z.infer<typeof riskSchema>;
