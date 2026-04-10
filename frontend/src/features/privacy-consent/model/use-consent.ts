import { useState, useCallback } from "react";

const STORAGE_KEY = "med_reminder_consent_accepted";

function readConsent(): boolean {
  try {
    return localStorage.getItem(STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

export function useConsent() {
  const [accepted, setAccepted] = useState(readConsent);

  const accept = useCallback(() => {
    try {
      localStorage.setItem(STORAGE_KEY, "true");
      setAccepted(true);
    } catch {
      setAccepted(true);
    }
  }, []);

  return { accepted, accept } as const;
}
