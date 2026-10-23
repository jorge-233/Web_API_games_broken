# Respuestas del parcial

1. ¿Qué error encontraste en la validación de `stock`?

En `schemas/game.py` el campo `stock` tenía `ge=0`, así que aceptaba el valor 0. Lo cambié a `ge=1` y ahora `stock: 0` se rechaza con 422. El error estaba en la capa Schema, que es la que valida los datos.

2. ¿Qué hacía que un juego pareciera creado pero no quedara persistido?

En `create_game` (capa Service) se hacía `session.add(game)` y luego `session.refresh(game)` sin `session.commit()`. Sin el commit no existe la fila en SQLite, y `refresh` fallaba con `InvalidRequestError: not persistent within this Session`. Agregué `session.commit()` entre `add` y `refresh`.

3. ¿Qué problema tenía el endpoint que lista juegos?

En `routers/games.py`, `GET /games` declaraba `response_model=GameResponse`, que representa un solo objeto, pero el service devuelve una lista. Lo cambié a `response_model=list[GameResponse]`. El error estaba en la capa Router.

4. ¿Cómo solucionaste la consulta de un ID inexistente?

`get_game` devolvía `session.get(Game, game_id)` directamente, que retorna `None` si el ID no existe. Ahora, en el Service, si el resultado es `None` se lanza `HTTPException(status_code=404, detail="Game not found")`.

5. ¿Por qué DELETE podía responder correctamente y aun así no eliminar el registro de SQLite?

Porque `delete_game` hacía `session.delete(game)` sin `session.commit()`. El borrado quedaba solo en la sesión, que se cierra al terminar la petición, y nunca se escribía en la base. La API respondía "Game deleted" pero el registro seguía en SQLite. Agregué `session.commit()` después de `session.delete(game)`.