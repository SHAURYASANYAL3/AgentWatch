const BASE = process.env.NEXT_PUBLIC_API_URL ?? '/api/v1'

export type ExecutionStatus = 'pending' | 'running' | 'success' | 'failure' | 'blocked' | 'rolled_back' | 'timeout'

export interface TokenUsage {
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
  estimated_cost_usd?: number
}

export interface SafetyData {
  risk_level: string
  risk_score: number
  blocked: boolean
  reasons: string[]
  matched_policies: string[]
  requires_approval: boolean
}

export interface ToolCallData {
  tool_name: string
  raw_command?: string
  arguments: Record<string, unknown>
  affected_resources: string[]
}

export interface ToolResultData {
  tool_name: string
  output?: string
  error?: string
}

export interface AgentEvent {
  event_id: string
  session_id: string
  agent_id: string
  agent_name?: string
  framework: string
  event_type: string
  status: ExecutionStatus
  timestamp: string
  step_number: number
  tool_call?: ToolCallData
  tool_result?: ToolResultData
  safety?: SafetyData
  token_usage?: TokenUsage
  planner_output_preview?: string
}

export interface AgentSession {
  session_id: string
  agent_id: string
  agent_name?: string
  framework: string
  started_at: string
  ended_at?: string
  status: ExecutionStatus
  goal?: string
  total_events: number
  total_tokens: number
  estimated_cost_usd: number
  final_confidence?: number
}

export interface DashboardSummary {
  total_sessions: number
  active_sessions: number
  failed_sessions: number
  blocked_sessions: number
  total_tokens: number
  estimated_cost_usd: number
  safety_stats: { checked: number; blocked: number; approved: number }
  event_bus_stats: Record<string, number>
}

export interface ReplayStep {
  index: number
  event: AgentEvent
  annotations: string[]
  is_failure_point: boolean
}

export interface FailureAnalysis {
  primary_cause: string
  contributing_factors: string[]
  first_anomaly_step?: number
  failure_step?: number
  tool_error_counts: Record<string, number>
  repeated_tools: string[]
  blocked_action_count: number
  summary: string
  recommendations: string[]
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...init?.headers },
    ...init,
  })
  if (!response.ok) {
    throw new Error(await response.text())
  }
  return response.json()
}

export const api = {
  rollback: (sessionId: string, body: { checkpoint_id?: string; to_step?: number; restore_filesystem?: boolean; restore_git?: boolean }) =>
    request(`/sessions/${sessionId}/rollback`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
}

export function createEventSocket(onEvent: (event: AgentEvent) => void, wsUrl?: string): WebSocket {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const url = wsUrl ?? `${protocol}://${window.location.hostname}:8000/ws/events`
  const socket = new WebSocket(url)
  socket.onmessage = (message) => {
    try {
      onEvent(JSON.parse(message.data) as AgentEvent)
    } catch {
      // Ignore malformed payloads from partial reconnects.
    }
  }
  return socket
}
