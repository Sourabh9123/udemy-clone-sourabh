from rest_framework.serializers import ModelSerializer
from students.models import Learner




class LearnerSerializer(ModelSerializer):
    class Meta:
        model = Learner
        feilds = "__all__"