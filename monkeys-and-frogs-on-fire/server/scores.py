from typing import Any, Dict

from frost.ext import Cog
from frost.server import auth_required, Status
from frost.server.database import managed_session

from server.models import Score


class Scores(Cog, route='scores'):

    @auth_required
    def new(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        score = data['score']

        with managed_session() as session:
            score = Score(score=score, user_id=id_)
            session.add(score)

        kwargs['client_send']({
            'headers': {
                'path': 'scores/post_new',
                'status': Status.SUCCESS.value
            }
        })

    @auth_required
    def get_top_ten(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        with managed_session() as session:
            scores = session.query(Score).order_by(Score.score.desc()).limit(10).all()

            kwargs['client_send']({
                'headers': {
                    'path': 'scores/post_top_ten',
                    'status': Status.SUCCESS.value
                },
                'scores': [
                    {
                        'score': score.score,
                        'username': score.user.username,
                        'user_id': score.user.id
                    } for score in scores
                ]
            })
