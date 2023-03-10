from rest_framework import mixins, generics, viewsets
from rest_framework.decorators import action
from django.shortcuts import render
from sudoku import SudokuHandler
import numpy as np
from .serializers import ResultSerializer, DifficultySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Difficulty, Results
import json


def prepare_sudoku_context(difficulty, size):
	sudoku = SudokuHandler()
	sudoku.generate(size=size)
	sudoku.prepare_for_solving(difficulty=2)
	context = {'grid': sudoku.user_grid.tolist(),
			   'completed_grid': sudoku.completed_grid.tolist()}
	return context


class SudokuViewSet(viewsets.GenericViewSet):

	@action(detail=False, methods=['get'])
	def sudoku(self, request):
		size = 9
		difficulties = [value[0] for value in Difficulty.objects.values_list('Option')]
		difficulty_option = difficulties[0]
		context = prepare_sudoku_context(difficulty=difficulty_option, size=size)
		context['difficulties'] = difficulties
		return render(request, 'Sudoku/sudoku.html', context=context)

	@action(detail=False, methods=['post'])
	def send_result(self, request):
		result = ResultSerializer(data=request.data)
		if result.is_valid():
			result.save()
			return Response(status=status.HTTP_200_OK)
		error = result.errors.values()
		data = {"error": error}
		return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False, methods=['get'])
	def generate_new(self, request):
		difficulty_option = request.query_params['Difficulty']
		difficulty_setting = Difficulty.objects.filter(Option=difficulty_option).values('FieldsToRemove')[0]['FieldsToRemove']
		size = int(request.query_params['Size'])
		difficulty = int(size**2 * difficulty_setting)
		context = prepare_sudoku_context(difficulty=difficulty, size=size)
		return Response(data=context)

	@action(detail=False, methods=['get'], url_path=r'leaderboards-view/(?P<difficulty>[\w-]+)')
	def leaderboards_view(self, request, difficulty=None):
		difficulties = [value[0] for value in Difficulty.objects.values_list('Option')]
		leaderboards = [values for values in
						ResultSerializer(Results.objects.filter(Difficulty__Option=difficulty).order_by('Duration').all(),
										 many=True).data]
		return render(request, 'Sudoku/leaderboards.html', context={'difficulties': difficulties,
																	'leaderboards': leaderboards,
																	'difficulty': difficulty})
