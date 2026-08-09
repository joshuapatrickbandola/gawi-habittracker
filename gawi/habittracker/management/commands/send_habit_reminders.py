import json
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from habittracker.models import Habit
from pywebpush import WebPushException, webpush


class Command(BaseCommand):
    help = "Sends push notification reminders for due habits."

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()

        due_habits = (
            Habit.objects.filter(
                is_archived=False,
                notification_interval__gt=0,
            )
            .exclude(
                accomplishments__date=today,
                accomplishments__completed=True,
            )
            .select_related("profile")
        )

        for habit in due_habits:
            interval = timedelta(hours=habit.notification_interval)
            if habit.last_notified_at and now - habit.last_notified_at < interval:
                continue

            self._notify(habit)
            habit.last_notified_at = now
            habit.save(update_fields=["last_notified_at"])

    def _notify(self, habit):
        subscriptions = habit.profile.push_subscriptions.all()
        payload = {
            "title": f"Don't forget: {habit.name}",
            "body": habit.goal or "Keep your streak going!",
            "habit_id": habit.id,
            "url": "/",
        }

        for sub in subscriptions:
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub.endpoint,
                        "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                    },
                    data=json.dumps(payload),
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={"sub": settings.VAPID_ADMIN_EMAIL},
                )
            except WebPushException as ex:
                if ex.response is not None and ex.response.status_code == 410:
                    # Subscription expired/unsubscribed by the browser
                    sub.delete()
