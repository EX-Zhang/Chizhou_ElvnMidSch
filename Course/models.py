# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    course_id = models.IntegerField(db_column='Course_ID', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField(db_column='Student_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'application'
        unique_together = (('course_id', 'student_id'),)


class Comment(models.Model):
    course_id = models.IntegerField(db_column='Course_ID', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField(db_column='Student_ID')  # Field name made lowercase.
    course_date = models.DateField(db_column='Course_Date')  # Field name made lowercase.
    absent = models.IntegerField(db_column='Absent', blank=True, null=True)  # Field name made lowercase.
    attend = models.TimeField(db_column='Attend', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    parent_available = models.IntegerField(db_column='Parent_Available', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('course_id', 'student_id', 'course_date'),)


class Course(models.Model):
    course_id = models.AutoField(db_column='Course_ID', primary_key=True)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    course_info = models.TextField(db_column='Course_Info', blank=True, null=True)  # Field name made lowercase.
    teacher_id = models.CharField(db_column='Teacher_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    course_place = models.CharField(db_column='Course_Place', max_length=255, blank=True, null=True)  # Field name made lowercase.
    course_time = models.CharField(db_column='Course_Time', max_length=255, blank=True, null=True)  # Field name made lowercase.
    available_date = models.DateField(db_column='Available_Date', blank=True, null=True)  # Field name made lowercase.
    total_num = models.IntegerField(db_column='Total_Num', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course'
