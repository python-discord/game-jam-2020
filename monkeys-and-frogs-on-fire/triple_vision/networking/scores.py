from typing import Any, Dict

from frost.client.events import EventStatus
from frost.client.objects import Memory
from frost.ext import Cog


class Scores(Cog, route='scores'):

    def post_new(data: Dict[str, Any]) -> None:
        EventStatus.new_score = data['headers']['status']

    def post_get_top(data: Dict[str, Any]) -> None:
        Memory.scores = data['scores']
        EventStatus.get_top_scores = data['headers']['status']
