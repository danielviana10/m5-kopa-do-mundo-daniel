from rest_framework import status
from django.forms import model_to_dict
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from teams.models import Team
from utils import data_processing
from exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)  # noqa


class TeamView(APIView):
    def post(self, req: Request) -> Response:
        try:
            data_processing(req.data)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError,
        ) as error:
            return Response(
                {"error": error.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )

        created_team = Team.objects.create(**req.data)
        response_data = model_to_dict(created_team)
        return Response(response_data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        all_teams = Team.objects.all()
        return Response(
            [model_to_dict(team) for team in all_teams], status.HTTP_200_OK
        )  # noqa


class TeamDetailView(APIView):
    def delete(self, req: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )  # noqa
        found_team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, req: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )  # noqa
        return Response(model_to_dict(found_team), status.HTTP_200_OK)

    def patch(self, req: Request, team_id: int) -> Response:
        data_to_update = req.data
        try:
            found_team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )  # noqa
        for key, value in data_to_update.items():
            setattr(found_team, key, value)
        found_team.save()
        return Response(model_to_dict(found_team), status.HTTP_200_OK)
