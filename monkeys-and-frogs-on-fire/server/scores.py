from typing import Any, Dict

from frost.ext import Cog
from frost.server import auth_required, logger, Status
from frost.server.database import managed_session, User

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
            s = Score(score=score, user_id=id_)
            session.add(s)

            kwargs['client_send']({
                'headers': {
                    'path': 'scores/post_new',
                    'status': Status.SUCCESS.value
                }
            })

            user = session.query(User).filter(User.id == id_).first()
            logger.info(f'User "{user.username}" sent a new score of {score}')

    @auth_required
    def get_top(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        with managed_session() as session:
            scores = session.query(Score).order_by(Score.score.asc()).limit(10).all()

            kwargs['client_send']({
                'headers': {
                    'path': 'scores/post_top',
                    'status': Status.SUCCESS.value
                },
                'scores': [
                    {
                        'score': score.score,
                        'username': session.query(User).filter(User.id == score.user_id).first().username,
                        'user_id': score.user_id,
                        'timestamp': str(score.timestamp)
                    } for score in scores
                ]
            })

            user = session.query(User).filter(User.id == id_).first()
            logger.info(f'User "{user.username}" was sent the top ten scores')
