# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# from django.db import transaction
# from .models import TeacherCourseAssignment, BatchCourseTeacherAssignment, Teacher

# @receiver(post_delete, sender=TeacherCourseAssignment)
# @receiver(post_delete, sender=BatchCourseTeacherAssignment)
# def delete_orphan_teacher(sender, instance, **kwargs):
#     teacher = instance.Teacher_ID

#     def delete_if_orphan():
#         if not TeacherCourseAssignment.objects.filter(Teacher_ID=teacher).exists() and \
#            not BatchCourseTeacherAssignment.objects.filter(Teacher_ID=teacher).exists():
#             teacher.delete()

#     transaction.on_commit(delete_if_orphan)
