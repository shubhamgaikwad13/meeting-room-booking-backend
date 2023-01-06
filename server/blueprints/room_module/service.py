from ...utils import field_must_be_type, field_required
from .constant import *

RoomFields = {
    'title': {'is_required': True, 'type': str},
    'type': {'is_required': True, 'type': str},
    'capacity': {'is_required': True, 'type': int},
    'description': {'is_required': True, 'type': str},
    'has_microphone': {'is_required': True, 'type': bool},
    'has_projector': {'is_required': True, 'type': bool},
    'has_speakers': {'is_required': True, 'type': bool},
    'has_whiteboard': {'is_required': True, 'type': bool},
    'created_by': {'is_required': True, 'type': str},
    'updated_by': {'is_required': False, 'type': str}
}

