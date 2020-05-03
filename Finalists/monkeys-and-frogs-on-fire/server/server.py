from pathlib import Path

from frost import FrostServer

from server.scores import Scores


class Server(FrostServer):

    def __init__(self, file: str) -> None:
        db = Path('pyfrost.sqlite3')
        if not db.exists():
            from server.utils import init_db
            init_db()

        # Load up our cog
        Scores()

        super().__init__(file)
