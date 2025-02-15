from malaya_speech.supervised import classification
from malaya_speech.utils import describe_availability
from herpetologist import check_type
import logging

logger = logging.getLogger(__name__)

_availability = {
    'vggvox-v2': {
        'Size (MB)': 31.1,
        'Quantized Size (MB)': 7.92,
        'Accuracy': 0.9509,
    },
    'deep-speaker': {
        'Size (MB)': 96.9,
        'Quantized Size (MB)': 24.4,
        'Accuracy': 0.9315,
    },
}

labels = [
    'angry',
    'disgust',
    'fear',
    'happy',
    'sad',
    'surprise',
    'neutral',
    'not an emotion',
]


def available_model():
    """
    List available emotion detection deep models.
    """
    logger.info('last accuracy during training session before early stopping.')

    return describe_availability(_availability)


@check_type
def deep_model(model: str = 'vggvox-v2', quantized: bool = False, **kwargs):
    """
    Load emotion detection deep model.

    Parameters
    ----------
    model : str, optional (default='vggvox-v2')
        Check available models at `malaya_speech.emotion.available_model()`.
    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.supervised.classification.load function
    """

    model = model.lower()
    if model not in _availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.emotion.available_model()`.'
        )

    settings = {
        'vggvox-v2': {'concat': False},
        'deep-speaker': {'voice_only': False},
    }

    return classification.load(
        model=model,
        module='emotion',
        extra=settings[model],
        label=labels,
        quantized=quantized,
        **kwargs
    )
