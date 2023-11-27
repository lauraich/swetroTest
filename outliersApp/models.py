from django.db import models
from import_export import resources

# Create your models here.
""" class UserRegistry(models.Model):
    RegistryId =  models.IntegerField(null=False)
    UserId = models.IntegerField(null=False)
    StartTimeInSeconds = models.BigIntegerField(null=True)
    DurationInSeconds = models.IntegerField(null=True)
    DistanceInMeters = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    Steps = models.IntegerField(null=True)
    AverageSpeedInMetersPerSecond = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    AveragePaceInMinutesPerKilometer = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    TotalElevationGainInMeters = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    AverageHeartRateInBeatsPerMinute = models.IntegerField(null=True)

class RegistryResource(resources.ModelResource):

    class Meta:
        model = UserRegistry
        import_id_fields = ["RegistryId"]
        skip_unchanged = True
        use_bulk = True """
