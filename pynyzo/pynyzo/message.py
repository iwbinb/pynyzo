"""
Message ancestor class for Nyzo messages
"""

from abc import ABC, abstractmethod
from pynyzo.helpers import base_app_log
from pynyzo.messagetype import MessageType
from pynyzo.messageobject import MessageObject
from time import time

__version__ = '0.0.1'


class Message(ABC):
    """Abstract Ancestor for all messages."""

    # slots for private vars, to spare ram
    __slots__ = ('_applog', '_timestamp', '_type', '_content', '_sourceNodeIdentifier', '_sourceNodeSignature', '_valid',
                 '_sourceIpAddress')

    # Static class variables
    maximumMessageLength = 4194304  # 4MB
    whitelist = dict()
    disallowedNonCycleTypes = (MessageType.NewBlock9, MessageType.BlockVote19, MessageType.NewVerifierVote21,
                               MessageType.MissingBlockVoteRequest23, MessageType.MissingBlockRequest25)

    # We do not broadcast any messages to the full mesh from the broadcast method. We do, however, use the full mesh
    # as a potential pool for random requests for the following types. This reduces strain on in-cycle verifiers.
    fullMeshMessageTypes = (MessageType.BlockRequest11, MessageType.BlockWithVotesRequest37)

    def __init__(self, a_type: MessageType, content: MessageObject, app_log:object, sourceNodeIdentifier: bytes=None,
                 sourceNodeSignature: bytes=None, sourceIpAddress: bytes=None, timestamp: int=0):
        """This is the constructor for a new message originating from this system AND from the outside,
        depending on the params."""
        self.app_log = base_app_log(app_log)
        self._type = a_type
        self._content = content
        self._valid = True

        if sourceNodeIdentifier is None:
            # From our system
            self._timestamp = int(time()*1000)
            # TODO
            self.app_log.error("TODO: Handle verifier")
            # self._sourceNodeIdentifier = Verifier.getIdentifier();
            # self._sourceNodeSignature = Verifier.sign(getBytesForSigning());
        else:
            # From another system
            self._timestamp = timestamp
            self._sourceNodeIdentifier = sourceNodeIdentifier
            self._sourceNodeSignature = sourceNodeSignature
            self._sourceIpAddress = sourceIpAddress
            # TODO: Verify the source signature.
            self.app_log.error("TODO: Verify source signature")
            # self._valid = SignatureUtil.signatureIsValid(sourceNodeSignature, getBytesForSigning(), sourceNodeIdentifier);
            if not self._valid:
                self.app_log.warning(f"message of type {self._type.name} is not valid")  # Temp log
                # TODO
                # self.app_log.warning(f"message from {PrintUtil.compactPrintByteArray(sourceNodeIdentifier)} of type {self._type.name} is not valid, content is {content}"
                # self.app_log.warning(f"signature is {ByteUtil.arrayAsStringWithDashes(sourceNodeSignature)}")

    @abstractmethod
    def to_string(self) -> str:
        """String view of the message for log/print"""
        pass

    def get_timestamp(self) -> int:
        return self._timestamp

    def get_type(self) -> MessageType:
        return self._type

    def get_content(self) -> MessageObject:
        return self._content

    def get_source_node_identifier(self) -> bytes:
        return self._sourceNodeIdentifier

    def get_source_node_signature(self) -> bytes:
        return self._sourceNodeSignature

    def is_valid(self) -> bool:
        return self._valid

    def get_source_ip_address(self) -> bytes:
        return self._sourceIpAddress

    def sign(self, private_seed: bytes) -> None:
        # TODO
        self.app_log.error("TODO: Message.sign()")
        # self._sourceNodeIdentifier = KeyUtil.identifierForSeed(private_seed);
        # self._sourceNodeSignature = SignatureUtil.signBytes(self.get_bytes_for_signing(), private_seed);

