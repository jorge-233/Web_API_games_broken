from fastapi import HTTPException
from sqlmodel import Session, select

from models.game import Game
from schemas.game import GameCreate


def create_game(game_data: GameCreate, session: Session):
    game = Game(
        title=game_data.title,
        genre=game_data.genre,
        platform=game_data.platform,
        stock=game_data.stock,
        active=game_data.active
    )

    session.add(game)

    # CORREGIDO: faltaba session.commit(). Sin él, el objeto no es
    # persistente y session.refresh() lanzaba InvalidRequestError (500).
    session.commit()

    session.refresh(game)

    return game


def list_games(session: Session):
    statement = select(Game)
    return session.exec(statement).all()


def get_game(game_id: int, session: Session):
    game = session.get(Game, game_id)

    # CORREGIDO: antes se devolvía session.get() directamente. Si el ID
    # no existía devolvía None y la API fallaba. Ahora responde 404.
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


def delete_game(game_id: int, session: Session):
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    session.delete(game)

    # CORREGIDO: faltaba session.commit(). Sin él, el DELETE respondía
    # "Game deleted" pero el registro seguía en SQLite.
    session.commit()

    return {"message": "Game deleted"}
