
import json
import logging
import configure
import urlparse
from flask import Flask, request
from flask_uwsgi_websocket import GeventWebSocket

from .message_distributor import MessageDistributor
from .listener import Listener
from .storage import MessageStorageMemory
from .path import PathConverter, Path
from .data_pack import DataPack
from .formats import FormatConverter

logger = logging.getLogger(__name__)

app =  Flask("piriti")

logger.info("Piriti app started")

#websocket = GeventWebSocket(app)

message_distributor = MessageDistributor()

storage = MessageStorageMemory()

app.url_map.converters['path'] = PathConverter
app.url_map.converters['format'] = FormatConverter

storage.store(DataPack(Path('/magrathea/helene'), {'muha': 42}))

@app.route("/data/<format:formatter>/", methods = ["POST"])
@app.route("/data/<format:formatter>/<path:path>", methods = ["POST"])
def post_data(formatter, path = Path()):
    raw_data = request.get_data()

    logger.debug("Data received (%s)", len(raw_data))

    data = formatter.deserialize(raw_data)

    data_pack = DataPack(path, data)

    storage.store(data_pack)

    message_distributor.dispatch(data_pack)

    return "OK"

@app.route("/data/<format:formatter>/", methods = ["GET"])
@app.route("/data/<format:formatter>/<path:path>", methods = ["GET"])
def get_data(formatter, path = Path()):
    raw_data_list = storage.fetch(path)
    if len(raw_data_list) == 0:
        return "data not found", 404
    data_list = []
    for raw_data in raw_data_list:
        data_list.append(raw_data.as_dict)

    return formatter.serialize(data_list)

#@websocket.route('/listen/<format:formatter>')
#@websocket.route('/listen/<format:formatter>/<path:path>')
def listen(ws, formatter, path = Path()):

    listener = Listener(ws, formatter.serializer)

    message_distributor.register(path, listener)

    while True:
        message = ws.receive()
        if not ws.connected:
            break

    message_distributor.unregister(listener)
