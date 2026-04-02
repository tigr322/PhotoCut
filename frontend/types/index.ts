export type JobStatus = 'pending' | 'queued' | 'processing' | 'completed' | 'failed'

export interface User {
  id: number
  email: string
  is_active: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiKeyRecord {
  id: string
  name: string
  key_prefix: string
  last_used_at: string | null
  revoked_at: string | null
  created_at: string
}

export interface ApiKeyCreateResponse {
  id: string
  name: string
  key_prefix: string
  key: string
  created_at: string
}

export interface Job {
  id: string
  type: string
  status: JobStatus
  input_file_id: string
  result_file_id: string | null
  options: Record<string, unknown>
  error_message: string | null
  created_at: string
  started_at: string | null
  completed_at: string | null
  result_url: string | null
}
