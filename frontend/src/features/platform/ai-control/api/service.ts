import { apiClient } from "@/core/api";

import type {
  AIControlSnapshot,
} from "../domain";


export async function getAIControlSnapshot(): Promise<AIControlSnapshot> {
  const response = await apiClient.get<AIControlSnapshot>(
    "/ai-control/",
  );

  return response.data;
}


export async function setAIApplicationEnabled(
  applicationId: string,
  enabled: boolean,
): Promise<AIControlSnapshot> {
  const response = await apiClient.post<AIControlSnapshot>(
    `/ai-control/${applicationId}/toggle/`,
    { enabled },
  );

  return response.data;
}
