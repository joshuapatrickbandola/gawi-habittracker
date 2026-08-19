# habittracker/management/commands/send_due_notifications.py
import json
from datetime import timedelta

from accounts.models import PushSubscription
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from habittracker.models import Habit
from pywebpush import WebPushException, webpush


class Command(BaseCommand):
    help = "Send push notifications for habits that are due, based on notification_interval."

    def handle(self, *args, **kwargs):
        now = timezone.now()
        due_habits = Habit.objects.filter(
            notification_interval__gt=0,
            is_archived=False,
        )

        sent_count = 0
        skipped_count = 0
        error_count = 0

        for habit in due_habits:
            if habit.last_notified_at is not None:
                elapsed = now - habit.last_notified_at
                if elapsed < timedelta(hours=habit.notification_interval):
                    skipped_count += 1
                    continue

            subscriptions = PushSubscription.objects.filter(profile=habit.profile)
            if not subscriptions.exists():
                skipped_count += 1
                continue

            payload = json.dumps(
                {
                    "title": "Habit reminder",
                    "body": f"Time to work on: {habit.name}",
                }
            )

            habit_had_success = False

            for sub in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": sub.endpoint,
                            "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                        },
                        data=payload,
                        vapid_private_key=settings.VAPID_PRIVATE_KEY,
                        vapid_claims={"sub": f"mailto:{settings.VAPID_ADMIN_EMAIL}"},
                    )
                    habit_had_success = True
                    sent_count += 1
                except WebPushException as e:
                    error_count += 1
                    status_code = e.response.status_code if e.response else None
                    if status_code in (404, 410):
                        # Subscription expired or gone — clean it up
                        sub.delete()
                        self.stdout.write(f"Removed expired subscription {sub.id}")
                    else:
                        self.stdout.write(f"Error sending to {sub.id}: {e}")

            if habit_had_success:
                habit.last_notified_at = now
                habit.save(update_fields=["last_notified_at"])

        self.stdout.write(
            f"Done. Sent: {sent_count}, Skipped: {skipped_count}, Errors: {error_count}"
        )
