from django.db import models
from django.conf import settings


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


class UserProfile(models.Model):
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
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.TextField(choices=GENDER_CHOICES)
    political_status = models.TextField(choices=POLITICAL_CHOICES)

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
    VIEW_CHOICES = (("Very Liberal", "Very Liberal"),
                    ("Slightly liberal", "Slightly Liberal"),
                    ("Neutral", "Neutral"),
                    ("Slightly Conservative", "Slightly Conservative"),
                    ("Very Conservative", "Very Conservative"))

    # Fields
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    view = models.TextField(choices=VIEW_CHOICES)
    progress = models.IntegerField()
    interest_other_side = models.BooleanField()

    # Metadata
    class Meta:
        ordering = ['topic_id']

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
    user1_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user1_id"
    )
    user2_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user2_id"
    )
    topic1_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic1", null = True)
    topic2_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic2", null = True)
    topic3_id = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="match_topic3", null = True)
    conversation_phase = models.IntegerField()
    question_idx = models.IntegerField()
    user1_skip = models.BooleanField()
    user2_skip = models.BooleanField()
    match_time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField()

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


class ConversationText(models.Model):
    # Fields
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    match_id = models.ForeignKey(Matches, on_delete=models.PROTECT)
    question_id = models.ForeignKey(Question, on_delete = models.PROTECT, null = True)
    convo_time = models.DateTimeField(auto_now_add=True)
    response = models.TextField()
    seen = models.BooleanField()

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
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    match_id = models.ForeignKey(Matches, on_delete=models.PROTECT)
    new_match = models.BooleanField()
    new_convo = models.BooleanField()
    seen = models.BooleanField()

    # Metadata
    class Meta: 
        ordering = ['user_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Notification."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Notification object (in Admin site etc.)."""
        return f"{self.user_id}"


class Survey(models.Model):
    # Fields
    match_id = models.ForeignKey(Matches, on_delete=models.PROTECT)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    answer1 = models.IntegerField()
    answer2 = models.IntegerField()
    answer3 = models.IntegerField()

    # Metadata
    class Meta: 
        ordering = ['match_id']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Survey."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Survey object (in Admin site etc.)."""
        return f"{self.match_id}"


class Reports(models.Model):
    # Fields
    conversationtext_id = models.ForeignKey(ConversationText, on_delete=models.PROTECT)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
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



