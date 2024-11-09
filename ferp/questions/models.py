from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    QUESTION_TYPES = [
        ('short', 'Short Answer'),
        ('medium', 'Medium Answer'),
        ('long', 'Long Answer'),
        ('mcq', 'Multiple Choice Question'),
    ]

    LEARNING_LEVELS = [
        ('remembering', 'Remembering'),
        ('application', 'Application'),
        ('evaluation', 'Evaluation'),
    ]

    DIFFICULTY_LEVELS = [
        ('simple', 'Simple'),
        ('moderate', 'Moderate'),
        ('complex', 'Complex'),
    ]

    VERIFICATION_STATUS = [
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    qn_id = models.BigAutoField(primary_key=True)
    qn_title = models.TextField()
    option_1 = models.CharField(max_length=200, blank=True, null=True)
    option_2 = models.CharField(max_length=200, blank=True, null=True)
    option_3 = models.CharField(max_length=200, blank=True, null=True)
    option_4 = models.CharField(max_length=200, blank=True, null=True)
    correct_ans = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Specify the correct answer if question type is MCQ"
    )
    subject = models.CharField(max_length=50)
    qn_area = models.CharField(max_length=10, choices=QUESTION_TYPES,blank=True)
    faculty = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='questions_uploaded',null=True, blank=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='moderated_questions', null=True, blank=True)
    learning_level = models.CharField(max_length=20, choices=LEARNING_LEVELS,blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS,blank=True)
    time_required = models.IntegerField(help_text="Time required to solve the question")
    verification_status = models.CharField(max_length=15, choices=VERIFICATION_STATUS, default='not_verified')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically set moderator to faculty if not provided
        if not self.moderator:
            self.moderator = self.faculty
        # Ensure correct answer is only set for MCQ type questions
        if self.qn_area != 'mcq':
            self.correct_ans = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.qn_title} - {self.subject}"
