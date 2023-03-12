from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sudoku import SudokuHandler
from .serializers import ResultSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Difficulty, Results
import json


def prepare_sudoku_context(size: int, difficulty_setting: float):
	"""
	Based on sudoku configuration params (difficulty_setting and size), prepare context containing sudoku data which
	will be used by UI.
	:param difficulty_setting:
	:param size:
	:return:
	"""
	sudoku = SudokuHandler()
	sudoku.generate(size=size)
	difficulty = calculate_difficulty(size=size, difficulty_setting=difficulty_setting)
	sudoku.prepare_for_solving(cells_to_remove=difficulty)
	context = {'grid': sudoku.user_grid.tolist(),
			   'completed_grid': sudoku.completed_grid.tolist()}
	return context


def calculate_difficulty(size: int, difficulty_setting: float):
	"""
	Sudoku package defines difficulty as number of fields which should be removed from grid. Since we define it as %
	of the grid which should be removed, conversion is perfomed here.
	:param size:
	:param difficulty_setting:
	:return:
	"""
	difficulty = int(size ** 2 * difficulty_setting)
	return difficulty


class SudokuViewSet(viewsets.GenericViewSet):
	"""
	ViewSet for displaying sudoku to user as well as related highscores tables.
	"""

	@action(detail=False, methods=['get'])
	def sudoku_game(self, request):
		"""
		Displays sudoku game view.
		:param request:
		:return:
		"""
		difficulties = [value[0] for value in Difficulty.objects.values_list('Option')]
		context = {'difficulties': difficulties}
		return render(request, 'Sudoku/sudoku.html', context=context)

	@action(detail=False, methods=['post'])
	def send_result(self, request):
		"""
		Process completed game results from frontend and parse them to database.
		:param request:
		:return:
		"""
		data = json.loads(request.data['result'])
		if request.user.is_authenticated:
			data['UserId'] = request.user
		result = ResultSerializer(data=data)
		if result.is_valid():
			result.save()
			return Response(status=status.HTTP_200_OK)
		error = result.errors.values()
		data = {"error": error}
		return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False, methods=['get'])
	def generate_new(self, request):
		"""
		Creates new sudoku and sends corresponding data to UI.
		:param request:
		:return:
		"""
		difficulty_option = request.query_params['Difficulty']
		difficulty_setting = Difficulty.objects.filter(Option=difficulty_option).values('FieldsToRemove')[0][
			'FieldsToRemove']
		size = int(request.query_params['Size'])
		context = prepare_sudoku_context(difficulty_setting=difficulty_setting, size=size)
		return Response(data=context)

	@action(detail=False, methods=['get'], url_path=r'leaderboards-view/(?P<difficulty>[\w-]+)')
	def leaderboards_view(self, request, difficulty: str = None):
		"""
		Renders UI which displays best scores.
		:param request:
		:param difficulty:
		:return:
		"""
		difficulties = [value[0] for value in Difficulty.objects.values_list('Option')]
		results_query = Results.objects.filter(Difficulty__Option=difficulty).order_by('Duration')
		top_results = ResultSerializer(results_query.all()[:10], many=True)
		leaderboards = [values for values in top_results.data]
		return render(request, 'Sudoku/leaderboards.html', context={'difficulties': difficulties,
																	'leaderboards': leaderboards,
																	'difficulty': difficulty})
