export type MedicationSchedule = "morning" | "day" | "evening" | "custom";

export interface Medication {
  id: number;
  user_id: number;
  name: string;
  schedule: MedicationSchedule;
  time: string;
  created_at: string;
}

export interface CreateMedicationPayload {
  name: string;
  schedule: MedicationSchedule;
  time: string;
}

export interface UpdateMedicationPayload {
  name: string;
  schedule: MedicationSchedule;
  time: string;
}
