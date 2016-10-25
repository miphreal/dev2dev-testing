from datetime import timedelta
from django.contrib.auth import login, authenticate
from django.utils import timezone
from rest_framework import serializers, viewsets, mixins, permissions

from my_prj.polls.models import Question, Choice


class LoginView(viewsets.GenericViewSet):
    class Validator(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    serializer_class = Validator

    def create(self, request, *args, **kwargs):
        from rest_framework import response, status

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        login(request=request, user=user)
        return response.Response({}, status=status.HTTP_201_CREATED)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'votes')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')

    class Meta:
        model = Question
        fields = ('created', 'updated', 'question_text', 'pub_date', 'id', 'choices')


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        now = timezone.now()
        return Question.objects.filter(pub_date__range=(now - timedelta(days=30), now))


class VoteValidator(serializers.Serializer):
    id = serializers.ReadOnlyField()
    choice_text = serializers.ReadOnlyField()
    votes = serializers.ReadOnlyField()

    def save(self):
        from django.db.models import F

        choice = self.instance
        choice.votes = F('votes') + 1
        choice.save()

        self.instance = Choice.objects.get(pk=choice.pk)


class VoteViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = VoteValidator
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Choice.objects.filter(question_id=self.kwargs['question_id'])
