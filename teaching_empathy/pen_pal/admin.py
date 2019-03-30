from django.contrib import admin
import pen_pal.models as ppm

# Register your models here.
admin.site.register(ppm.Topic)
admin.site.register(ppm.Literature)
admin.site.register(ppm.TopicLiterature)
admin.site.register(ppm.User)
admin.site.register(ppm.Question)
admin.site.register(ppm.Matches)
admin.site.register(ppm.Conversation)
admin.site.register(ppm.ConversationText)
admin.site.register(ppm.Notification)
admin.site.register(ppm.Survey)
admin.site.register(ppm.Reports)
