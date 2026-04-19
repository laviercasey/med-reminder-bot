import "@testing-library/jest-dom/vitest";

vi.mock("@telegram-apps/sdk-react", () => ({
  retrieveRawInitData: () => "test_init_data",
  retrieveLaunchParams: () => ({
    initDataRaw: "test_init_data",
    initData: {
      user: {
        id: 123456789,
        languageCode: "en",
      },
    },
  }),
  postEvent: vi.fn(),
  useSignal: (signal: unknown) => signal,
  SDKProvider: ({ children }: { children: React.ReactNode }) => children,
  useLaunchParams: () => ({
    initDataRaw: "test_init_data",
    initData: { user: { id: 123456789 } },
  }),
  useHapticFeedback: () => ({
    impactOccurred: vi.fn(),
    notificationOccurred: vi.fn(),
  }),
  useMainButton: () => ({
    setText: vi.fn(),
    show: vi.fn(),
    hide: vi.fn(),
    enable: vi.fn(),
    disable: vi.fn(),
    showProgress: vi.fn(),
    hideProgress: vi.fn(),
    on: vi.fn(),
    off: vi.fn(),
  }),
  useBackButton: () => ({
    show: vi.fn(),
    hide: vi.fn(),
    on: vi.fn(),
    off: vi.fn(),
  }),
}));

beforeEach(async () => {
  const { setTokens, clearTokens } = await import("@/shared/auth/token-store");
  const { resetCoordinator } = await import("@/shared/auth/refresh-coordinator");
  const { resetBootstrap } = await import("@/shared/auth/bootstrap");
  resetBootstrap();
  clearTokens();
  resetCoordinator();
  setTokens({
    accessToken: "test-access-token",
    accessExpiresAt: Math.floor(Date.now() / 1000) + 3600,
    refreshToken: "test-refresh-token",
  });
});

afterEach(async () => {
  const { clearTokens } = await import("@/shared/auth/token-store");
  const { resetCoordinator } = await import("@/shared/auth/refresh-coordinator");
  const { resetBootstrap } = await import("@/shared/auth/bootstrap");
  resetBootstrap();
  clearTokens();
  resetCoordinator();
});
