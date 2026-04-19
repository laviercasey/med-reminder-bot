export function AuthErrorScreen() {
  return (
    <div
      role="alert"
      className="min-h-dvh flex items-center justify-center bg-surface px-6 text-center"
    >
      <div className="max-w-sm">
        <h1 className="text-xl font-semibold mb-3">Session expired</h1>
        <p className="text-sm opacity-80">
          Please reopen the app from Telegram to continue.
        </p>
      </div>
    </div>
  );
}
