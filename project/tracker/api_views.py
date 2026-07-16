from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Skill, PracticeLog
from django.contrib.auth.models import User
from .serializers import UserSerializer, SkillSerializer, PracticeLogSerializer
from django.db.models import Avg
from django.shortcuts import get_object_or_404


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return Skill.objects.filter(user_id=user_id)
        return super().get_queryset()


class PracticeLogViewSet(viewsets.ModelViewSet):
    queryset = PracticeLog.objects.all()
    serializer_class = PracticeLogSerializer

    def get_queryset(self):
        skill_id = self.request.query_params.get('skill')
        if skill_id:
            return PracticeLog.objects.filter(skill_id=skill_id)
        return super().get_queryset()


class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'detail': 'user param required'}, status=status.HTTP_400_BAD_REQUEST)
        skills = Skill.objects.filter(user_id=user_id)
        total_skills = skills.count()
        avg_strength = 0
        if total_skills > 0:
            strengths = [s.get_strength_score() for s in skills]
            avg_strength = sum(strengths) / total_skills
        recent_logs = PracticeLog.objects.filter(skill__user_id=user_id).order_by('-practice_date')[:10]
        recent = PracticeLogSerializer(recent_logs, many=True).data
        return Response({'total_skills': total_skills, 'average_strength': avg_strength, 'recent_logs': recent})
