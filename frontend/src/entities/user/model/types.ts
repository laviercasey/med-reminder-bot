export interface User {
  id: number;
  telegram_id: number;
  language: string;
  is_admin: boolean;
  is_premium: boolean;
  premium_until: string | null;
  is_blocked: boolean;
  created_at: string;
  last_active: string;
}

export interface UserSettings {
  reminders_enabled: boolean;
  reminder_repeat_minutes: number;
}
