export const mockRetrieveLaunchParams = vi.fn(() => ({
  initDataRaw: "test_init_data",
  initData: {
    user: {
      id: 123456789,
      languageCode: "en",
    },
  },
}));

export const mockPostEvent = vi.fn();

export function resetTelegramMocks() {
  mockRetrieveLaunchParams.mockReturnValue({
    initDataRaw: "test_init_data",
    initData: {
      user: {
        id: 123456789,
        languageCode: "en",
      },
    },
  });
  mockPostEvent.mockReset();
}
