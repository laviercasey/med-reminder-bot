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
