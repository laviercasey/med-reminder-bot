import { hapticFeedback, getUserLanguage, getUserId, closeMiniApp } from "../telegram";
import { postEvent, retrieveLaunchParams } from "@telegram-apps/sdk-react";

vi.mock("@telegram-apps/sdk-react", () => ({
  postEvent: vi.fn(),
  retrieveLaunchParams: vi.fn(),
}));

describe("hapticFeedback", () => {
  afterEach(() => vi.clearAllMocks());

  it("sends impact feedback with default style", () => {
    hapticFeedback("impact");
    expect(postEvent).toHaveBeenCalledWith("web_app_trigger_haptic_feedback", {
      type: "impact",
      impact_style: "light",
    });
  });

  it("sends impact feedback with custom style", () => {
    hapticFeedback("impact", "heavy");
    expect(postEvent).toHaveBeenCalledWith("web_app_trigger_haptic_feedback", {
      type: "impact",
      impact_style: "heavy",
    });
  });

  it("sends notification feedback with default style", () => {
    hapticFeedback("notification");
    expect(postEvent).toHaveBeenCalledWith("web_app_trigger_haptic_feedback", {
      type: "notification",
      notification_type: "success",
    });
  });

  it("sends notification feedback with custom style", () => {
    hapticFeedback("notification", "error");
    expect(postEvent).toHaveBeenCalledWith("web_app_trigger_haptic_feedback", {
      type: "notification",
      notification_type: "error",
    });
  });

  it("sends selection_change feedback", () => {
    hapticFeedback("selection_change");
    expect(postEvent).toHaveBeenCalledWith("web_app_trigger_haptic_feedback", {
      type: "selection_change",
    });
  });

  it("silently catches errors", () => {
    vi.mocked(postEvent).mockImplementation(() => {
      throw new Error("not available");
    });
    expect(() => hapticFeedback("impact")).not.toThrow();
  });
});

describe("getUserLanguage", () => {
  afterEach(() => vi.clearAllMocks());

  it("returns user language from launch params", () => {
    vi.mocked(retrieveLaunchParams).mockReturnValue({
      tgWebAppData: { user: { languageCode: "ru" } },
    } as ReturnType<typeof retrieveLaunchParams>);

    expect(getUserLanguage()).toBe("ru");
  });

  it("returns 'en' when no language code", () => {
    vi.mocked(retrieveLaunchParams).mockReturnValue({
      tgWebAppData: { user: {} },
    } as ReturnType<typeof retrieveLaunchParams>);

    expect(getUserLanguage()).toBe("en");
  });

  it("returns 'en' on error", () => {
    vi.mocked(retrieveLaunchParams).mockImplementation(() => {
      throw new Error("no params");
    });

    expect(getUserLanguage()).toBe("en");
  });
});

describe("getUserId", () => {
  afterEach(() => vi.clearAllMocks());

  it("returns user id from launch params", () => {
    vi.mocked(retrieveLaunchParams).mockReturnValue({
      tgWebAppData: { user: { id: 123456789 } },
    } as ReturnType<typeof retrieveLaunchParams>);

    expect(getUserId()).toBe(123456789);
  });

  it("returns null when no user", () => {
    vi.mocked(retrieveLaunchParams).mockReturnValue({
      tgWebAppData: {},
    } as ReturnType<typeof retrieveLaunchParams>);

    expect(getUserId()).toBeNull();
  });

  it("returns null on error", () => {
    vi.mocked(retrieveLaunchParams).mockImplementation(() => {
      throw new Error("no params");
    });

    expect(getUserId()).toBeNull();
  });
});

describe("closeMiniApp", () => {
  afterEach(() => vi.clearAllMocks());

  it("sends web_app_close event", () => {
    closeMiniApp();
    expect(postEvent).toHaveBeenCalledWith("web_app_close");
  });

  it("silently catches errors", () => {
    vi.mocked(postEvent).mockImplementation(() => {
      throw new Error("not available");
    });
    expect(() => closeMiniApp()).not.toThrow();
  });
});
