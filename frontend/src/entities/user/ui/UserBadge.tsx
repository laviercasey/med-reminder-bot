import { Badge } from "@telegram-apps/telegram-ui";
import { useCurrentUser } from "../model/queries";

export function UserBadge() {
  const { data: user } = useCurrentUser();

  if (!user) {
    return null;
  }

  const isPremiumActive =
    user.is_premium &&
    (user.premium_until === null || new Date(user.premium_until) > new Date());

  return (
    <Badge
      type="dot"
      style={{
        backgroundColor: isPremiumActive
          ? "var(--tg-theme-link-color, #2481cc)"
          : "var(--tg-theme-hint-color, #999)",
      }}
    />
  );
}
