from rest_framework import mixins, generics, viewsets
from rest_framework.decorators import action
from django.shortcuts import render
from sudoku import SudokuHandler
import numpy as np
from .serializers import ResultSerializer, DifficultySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Difficulty
import json

class SudokuViewSet(viewsets.GenericViewSet):

	# def get_queryset(self):
	# 	pass
	#
	# def get_serializer_class(self):
	# 	pass

	@action(detail=False, methods=['get'])
	def sudoku(self, request):
		difficulties = [value[0] for value in Difficulty.objects.values_list('Option')]
		sudoku = SudokuHandler()
		sudoku.generate(size=9)
		sudoku.prepare_for_solving(difficulty=2)
		return render(request, 'Sudoku/sudoku.html', context={'grid': sudoku.user_grid.tolist(),
															  'completed_grid': sudoku.completed_grid.tolist(),
															  'difficulties': difficulties})

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
		sudoku = SudokuHandler()
		sudoku.generate(size=size)
		difficulty = int(size**2 * difficulty_setting)
		sudoku.prepare_for_solving(difficulty=difficulty)
		return Response(data={'grid': sudoku.user_grid.tolist(),
								'completed_grid': sudoku.completed_grid.tolist()})
