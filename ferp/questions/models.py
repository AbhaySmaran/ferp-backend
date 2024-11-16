from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    qn_id = models.BigAutoField(primary_key=True)
    qn_title = models.CharField(max_length=100)
    qn_area = models.TextField()
    qn_type = models.CharField(max_length = 250)
    option_1_number = models.PositiveSmallIntegerField(default=1) 
    option_1_value = models.CharField(max_length=200, blank=True, null=True)
    option_2_number = models.PositiveSmallIntegerField(default=2) 
    option_2_value = models.CharField(max_length=200, blank=True, null=True)
    option_3_number = models.PositiveSmallIntegerField(default=3)
    option_3_value = models.CharField(max_length=200, blank=True, null=True)
    option_4_number = models.PositiveSmallIntegerField(default=4) 
    option_4_value = models.CharField(max_length=200, blank=True, null=True)
    
    correct_ans = models.PositiveSmallIntegerField(blank=True,null=True)
    subject = models.CharField(max_length=50)
    
    faculty = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='questions_uploaded',null=True, blank=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='moderated_questions', null=True, blank=True)
    learning_level = models.CharField(max_length=20,blank=True)
    difficulty_level = models.CharField(max_length=20,blank=True)
    time_required = models.IntegerField(help_text="Time required to solve the question")
    verification_status = models.CharField(max_length=15, default='not_verified')
    status = models.CharField(max_length=10, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically set moderator to faculty if not provided
        if not self.moderator:
            self.moderator = self.faculty
        # Ensure correct answer is only set for MCQ type questions
        if self.qn_type != 'mcq':
            self.correct_ans = None
        super().save(*args, **kwargs)

    def get_correct_answer_value(self):
        options = {
            1: self.option_1_value,
            2: self.option_2_value,
            3: self.option_3_value,
            4: self.option_4_value,
        }
        return options.get(self.correct_ans)

    def __str__(self):
        return f"{self.qn_title} - {self.subject}"
