# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache

from confluent_kafka import Producer
from pydantic import json

from config.kafka import get_producer
from .contracts import ILaquesisService
from ..domain import Piece


class LaquesisService(ILaquesisService):
    """
    LaquesisService is the service that segments the clippings, saving the relationship
    between the segmented image and its respective field in the database.
    """

    def __init__(self, producer: Producer) -> None:
        """
        LaquesisService constructor.

        ----------
        Parameters
        ----------
        producer : Producer
            The producer to be used to send the message to the segment queue.
        """
        self.producer = producer

    @classmethod
    @lru_cache
    def instance(cls, producer: Producer | None = None) -> 'LaquesisService':
        """
        instance returns a new LaquesisService instance.

        ----------
        Parameters
        ----------
        producer : Producer | None
            The producer to be used to send the message to the segment queue.

        -------
        Returns
        -------
        LaquesisService
            a new LaquesisService instance.
        """
        return cls(producer or get_producer('ares'))

    def segment(self, plot: Piece) -> None:
        """
        segment is responsible for segmenting the piece.

        ----------
        Parameters
        ----------
        plot : Piece
            The piece to be segmented.

        """
        data = {
            'id': str(plot.id),
            'path': plot.file.get_location(),
        }

        self.producer.produce('add_piece_to_segment', json.dumps(data).encode('utf-8'))
        self.producer.poll()
        self.producer.flush()
