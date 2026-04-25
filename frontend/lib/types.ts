export type Severity = "info" | "low" | "medium" | "high" | "critical";
export type FindingStatus = "open" | "triaged" | "resolved" | "ignored";
export type CaseStatus = "open" | "investigating" | "contained" | "resolved" | "closed";
export type ActionApprovalStatus = "pending" | "approved" | "denied" | "rejected";
export type ActionExecutionStatus = "pending" | "running" | "succeeded" | "failed" | "cancelled";
export type Trend = "up" | "down" | "stable" | string;

export interface Device {
  id: string;
  user_id: string;
  agent_id: string;
  hostname: string;
  os_name: string;
  os_version: string;
  agent_version: string;
  last_seen_at: string;
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: string;
  device_id: string;
  event_type: string;
  category: string;
  severity: Severity;
  occurred_at: string;
  received_at: string;
  source: string;
  payload_json: Record<string, unknown>;
}

export interface Finding {
  id: string;
  device_id: string;
  event_id: string | null;
  finding_type: string;
  title: string;
  description: string;
  severity: Severity;
  status: FindingStatus;
  first_seen_at: string;
  last_seen_at: string;
  metadata_json: Record<string, unknown>;
}

export interface Case {
  id: string;
  device_id: string;
  title: string;
  summary: string;
  severity: Severity;
  status: CaseStatus;
  opened_at: string;
  updated_at: string;
  metadata_json: Record<string, unknown>;
}

export interface CaseDetail extends Case {
  findings: Finding[];
}

export interface Action {
  id: string;
  case_id: string;
  device_id: string;
  action_type: string;
  requested_by: string;
  approval_status: ActionApprovalStatus;
  execution_status: ActionExecutionStatus;
  requested_at: string;
  executed_at: string | null;
  result_json: Record<string, unknown>;
}

export interface PostureScore {
  overall_score: number;
  trend: Trend;
  summary_counts: {
    findings?: Partial<Record<Severity, number>>;
    cases?: Partial<Record<Severity, number>>;
    risk_points?: number;
    [key: string]: unknown;
  };
  drivers: string[];
}

export interface ListQuery {
  device_id?: string;
  severity?: string;
  category?: string;
  status?: string;
  event_type?: string;
  approval_status?: string;
  execution_status?: string;
  agent_id?: string;
  limit?: number;
  offset?: number;
}
