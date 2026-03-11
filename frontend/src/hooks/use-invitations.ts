"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

// Fetch org members (users)
export function useOrgMembers(orgId: string) {
  return useQuery({
    queryKey: ["org-members", orgId],
    queryFn: () =>
      api.get<{ items: any[]; total: number }>(
        `/organizations/${orgId}/users?page_size=100`
      ),
    enabled: !!orgId,
  });
}

// Fetch org invitations
export function useOrgInvitations(orgId: string) {
  return useQuery({
    queryKey: ["org-invitations", orgId],
    queryFn: () =>
      api.get<{ items: any[]; total: number }>(
        `/organizations/${orgId}/invitations`
      ),
    enabled: !!orgId,
  });
}

// Send invitation
export function useSendInvitation(orgId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { email: string; role: string }) =>
      api.post(`/organizations/${orgId}/invitations`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["org-invitations", orgId] });
    },
  });
}

// Revoke invitation
export function useRevokeInvitation(orgId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (invitationId: string) =>
      api.delete(`/organizations/${orgId}/invitations/${invitationId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["org-invitations", orgId] });
    },
  });
}

// Resend invitation
export function useResendInvitation(orgId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (invitationId: string) =>
      api.post(`/organizations/${orgId}/invitations/${invitationId}/resend`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["org-invitations", orgId] });
    },
  });
}
