import json
from .constants import RateModel, expectedRateModelKeys
from .exceptions import AcrossException


def parse_and_return_rate_model_from_string(rate_model_string: str) -> RateModel:
    """Helper method that returns parsed rate model from string, or throws.

    Args:
        rate_model_string (str): Stringified rate model to parse.

    Returns:
        RateModel: Rate model object. Must conform to `expectedRateModelKeys` format.
    
    Raises:
        AcrossException:
            - Rate model does not contain all expected keys. 
            - Rate model contains unexpected keys.
    """
    rateModelFromEvent = json.loads(rate_model_string)

    # Rate model must contain the exact same keys in `expectedRateModelKeys`.
    for key in expectedRateModelKeys:
        if key not in rateModelFromEvent:
            raise AcrossException(
                f"Rate model does not contain all expected keys. "
                "Expected keys: [{expectedRateModelKeys}], actual keys: [{rateModelFromEvent.keys()}]"
            )
    for key in rateModelFromEvent:
        if key not in expectedRateModelKeys:
            raise AcrossException(
                f"Rate model contains unexpected keys. "
                "Expected keys: [{expectedRateModelKeys}], actual keys: [{rateModelFromEvent.keys()}]"
            )

    return {
        "UBar": int(rateModelFromEvent["UBar"]),
        "R0": int(rateModelFromEvent["R0"]),
        "R1": int(rateModelFromEvent["R1"]),
        "R2": int(rateModelFromEvent["R2"]),
    }
