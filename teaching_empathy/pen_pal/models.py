from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Topic(models.Model):
    # Fields
    name = models.TextField()
    category = models.TextField()

    # Metadata
    class Meta: 
        ordering = ['name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Topic."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Topic object (in Admin site etc.)."""
        return f"{self.name}"


class Literature(models.Model):
    # Fields
    link = models.TextField()
    title = models.TextField()
    authors = models.TextField()
    year_of_publication = models.IntegerField()
    journal = models.TextField()

    # Metadata
    class Meta: 
        ordering = ['title']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Topic."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Literature object (in Admin site etc.)."""
        return f"{self.title}"


class TopicLiterature(models.Model):
    # Fields
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    literature_id = models.ForeignKey(Literature, on_delete=models.PROTECT)

    # Metadata
    class Meta: 
        ordering = ['topic_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Topic."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the TopicLiterature object (in Admin site etc.)."""
        return f"{self.topic_id} {self.literature_id}"


class Profile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    POLITICAL_CHOICES = (
        ("Democrat", "Democrat"),
        ("Republican", "Republican"),
        ("Libertarian", "Libertarian"),
        ("Green Party", "Green Party"),
        ("Other", "Other"),
    )

    # Fields
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    email = models.EmailField()
    age = models.IntegerField(null=True)
    gender = models.TextField(choices=GENDER_CHOICES, null=True)
    political_status = models.TextField(choices=POLITICAL_CHOICES, null=True)
    interested_topics = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True)  # Not sure what to do for data model where users indicate multiple topics

    # Metadata
    class Meta: 
        ordering = ['last_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of User."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the User object (in Admin site etc.)."""
        return f"{self.first_name} {self.last_name}"


class UserTopic(models.Model):
    VIEW_CHOICES = (
        ("Strong Agree with Liberal View", "Strong Agree with Liberal View"),
        ("Leaning towards Liberal View", "Leaning towards Liberal View"),
        ("Neutral", "Neutral"),
        ("Leaning towards Conservative View", "Leaning towards Conservative View"),
        ("Strongly Agree with Conservative View", "Strongly Agree with Conservative View"),
    )

    # Fields
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    view = models.TextField(choices=VIEW_CHOICES)
    progress = models.IntegerField()
    interest_other_side = models.BooleanField()

    # Metadata
    class Meta: 
        ordering = ['user_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of User."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the UserTopic object (in Admin site etc.)."""
        return f"{self.user_id} {self.topic_id}"        


class Question(models.Model):
    # Fields
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    description = models.TextField()

    # Metadata
    class Meta: 
        ordering = ['description']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Question."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Question object (in Admin site etc.)."""
        return f"{self.description}"


class Matches(models.Model):
    # Fields
    user1_id = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="match_user1")
    user2_id = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="match_user2")
    topic1_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic1")
    topic2_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic2")
    topic3_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic3")

    # Metadata
    class Meta: 
        ordering = ['user1_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of User."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the User object (in Admin site etc.)."""
        return f"{self.user1_id} {self.user2_id}"


class Conversation(models.Model):
    # Fields
    user1_id = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="user1")
    user2_id = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="user2")

    # Metadata
    class Meta: 
        ordering = ['user1_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Conversation."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Conversation object (in Admin site etc.)."""
        return f"{self.user1_id}"


class ConversationText(models.Model):
    # Fields
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.PROTECT)
    response = models.TextField()

    # Metadata
    class Meta: 
        ordering = ['user_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of ConversationText."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the ConversationText object (in Admin site etc.)."""
        return f"{self.user_id}"


class Notification(models.Model):
    # Fields
    match_id = models.ForeignKey(Matches, on_delete=models.PROTECT)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.PROTECT)
    new_match = models.BooleanField()
    new_convo = models.BooleanField()
    seen = models.BooleanField()

    # Metadata
    class Meta: 
        ordering = ['match_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Notification."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Notification object (in Admin site etc.)."""
        return f"{self.match_id}"


class Survey(models.Model):
    # Fields
    conversation_id = models.ForeignKey(Conversation, on_delete=models.PROTECT)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    answer1 = models.IntegerField()
    answer2 = models.IntegerField()
    answer3 = models.IntegerField()

    # Metadata
    class Meta: 
        ordering = ['conversation_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Survey."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Survey object (in Admin site etc.)."""
        return f"{self.conversation_id}"


class Reports(models.Model):
    # Fields
    conversationtext_id = models.ForeignKey(ConversationText, on_delete=models.PROTECT)
    user_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    why_report = models.TextField()

    # Metadata
    class Meta: 
        ordering = ['conversationtext_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Reports."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Reports object (in Admin site etc.)."""
        return f"{self.conversationtext_id}"



