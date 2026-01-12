from django.db import models
from core.models import Profile
from datetime import datetime, timezone

# Create your models here.


class Chat(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="message_group_id"
    )
    sender = models.CharField(max_length=8)  # user/manager
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="chat/images/", null=True, blank=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def format_time_ago(sent_at):
        now = datetime.now(timezone.utc)
        diff = now - sent_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return "just now"
        minutes = seconds // 60
        if minutes < 60:
            return f"{int(minutes)} min ago"
        hours = minutes // 60
        if hours < 24:
            return f"{int(hours)} hours ago"
        days = diff.days
        if days < 7:
            return f"{int(days)} days ago"
        if days < 30:
            weeks = days // 7
            return f"{int(weeks)} {'week' if weeks == 1 else 'weeks'} ago"
        if days < 365:
            months = days // 30
            return f"{int(months)} {'month' if months == 1 else 'months'} ago"
        years = days // 365
        return f"{int(years)} {'year' if years == 1 else 'years'} ago"

    @property
    def time_ago(self):
        return self.format_time_ago(self.sent_at)

    def last_chat_group():
        data = []
        for x in Chat.objects.order_by("sent_at"):
            is_unique = True
            if len(data) >= 10:
                break
            for y in range(len(data)):
                if data[y]["profile_id"] == x.profile.uid:
                    is_unique = False
                    break
            if is_unique:
                data.append(
                    {
                        "profile_id": x.profile.uid,
                        "sender": x.sender,
                        "name": x.profile.user.email,
                        "message": x.message,
                        "image": x.image,
                        "sent_at": x.time_ago,
                    }
                )

        return data

    def __str__(self) -> str:
        return self.profile.full_name
