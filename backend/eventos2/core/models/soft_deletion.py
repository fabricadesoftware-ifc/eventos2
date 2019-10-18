from django.db import models
from django.utils import timezone


class SoftDeletableQuerySet(models.QuerySet):
    def delete(self):
        count = self.update(deleted_on=timezone.now())
        return count, {self.model._meta.label: count}

    def undelete(self) -> int:
        return self.update(deleted_on=None)

    def hard_delete(self):
        return super().delete()


class AvailableObjectsManager(models.Manager):
    def get_queryset(self) -> SoftDeletableQuerySet:
        return SoftDeletableQuerySet(self.model, using=self._db).filter(
            deleted_on__isnull=True
        )


class SoftDeletableModel(models.Model):
    objects = SoftDeletableQuerySet.as_manager()
    available_objects = AvailableObjectsManager()

    deleted_on = models.DateTimeField(null=True, blank=True)

    def delete(self):
        count = 1 if self.deleted_on is None else 0
        self.deleted_on = timezone.now()
        self.save()
        return count, {self._meta.label: count}

    def undelete(self) -> int:
        count = 1 if self.deleted_on is not None else 0
        self.deleted_on = None
        self.save()
        return count

    def hard_delete(self):
        return super().delete()

    class Meta:
        abstract = True
