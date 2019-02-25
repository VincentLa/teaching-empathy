from django.db import models


class Topic(models.Model):
    # Fields
    name = models.TextField()
    category = models.TextField()
    literature_review = models.TextField()

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


class User(models.Model):
    # Fields
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.TextField()
    political_status = models.TextField()
    interested_topics = models.ForeignKey(Topic, on_delete=models.PROTECT)  # Not sure what to do for data model where users indicate multiple topics

    # Metadata
    class Meta: 
        ordering = ['last_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of User."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the User object (in Admin site etc.)."""
        return f"{self.name} {self.last_name}"


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
