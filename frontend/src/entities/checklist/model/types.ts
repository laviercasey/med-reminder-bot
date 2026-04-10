export interface ChecklistEntry {
  id: number;
  medication_id: number;
  medication_name: string;
  medication_time: string;
  schedule: string;
  date: string;
  status: boolean;
  updated_at: string | null;
}

export interface ChecklistResponse {
  items: ChecklistEntry[];
  date: string;
  total: number;
  taken: number;
}
