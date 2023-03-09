from rest_framework import mixins, generics, viewsets
from rest_framework.decorators import action
from django.shortcuts import render
from sudoku import SudokuHandler
import numpy as np

class SudokuViewSet(viewsets.GenericViewSet):

	# def get_queryset(self):
	# 	pass
	#
	# def get_serializer_class(self):
	# 	pass

	@action(detail=False, methods=['get'])
	def sudoku(self, request):
		sudoku = SudokuHandler()
		sudoku.generate(size=9)
		sudoku.prepare_for_solving(difficulty=2)
		return render(request, 'Sudoku/sudoku.html', context={'grid': sudoku.user_grid.tolist(),
															  'completed_grid': sudoku.completed_grid.tolist()})

	@action(detail=False, methods=['post'])
	def send_result(self, request):
		result = request.data['result']



