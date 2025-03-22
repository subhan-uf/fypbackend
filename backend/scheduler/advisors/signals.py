# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# from .models import TimetableHeader, TimetableDetail, Generation

# @receiver(post_delete, sender=TimetableHeader)
# def delete_generation_when_header_deleted(sender, instance, **kwargs):
#     gen_id = instance.Generation_id  # use the FK field, not reverse lookup
#     if gen_id:
#         Generation.objects.filter(pk=gen_id).delete()

# @receiver(post_delete, sender=TimetableDetail)
# def delete_generation_when_detail_deleted(sender, instance, **kwargs):
#     gen = instance.Timetable_ID.Generation
#     from .models import TimetableHeader
#     # only delete if no other headers reference it
#     if not TimetableHeader.objects.filter(Generation=gen).exists():
#         gen.delete()
