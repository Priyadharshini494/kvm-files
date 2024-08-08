from ... import aiotools

from ...yamlconf import Option

from ...validators.basic import valid_number
from ...validators.basic import valid_int_f0

from .pwm import Plugin as PwmPlugin


# =====
class Plugin(PwmPlugin):
    def __init__(  # pylint: disable=super-init-not-called,too-many-arguments
        self,
        instance_name: str,
        notifier: aiotools.AioNotifier,

        chip: int,
        period: int,
        duty_cycle_min: int,
        duty_cycle_max: int,
        angle_min: float,
        angle_max: float,
        angle_push: float,
        angle_release: float,
    ) -> None:

        angle_push = min(max(angle_push, angle_min), angle_max)
        angle_release = min(max(angle_release, angle_min), angle_max)

        duty_cycle_per_degree = (duty_cycle_max - duty_cycle_min) / (angle_max - angle_min)

        duty_cycle_push = int(duty_cycle_per_degree * (angle_push - angle_min) + duty_cycle_min)
        duty_cycle_release = int(duty_cycle_per_degree * (angle_release - angle_min) + duty_cycle_min)

        super().__init__(
            instance_name=instance_name,
            notifier=notifier,

            chip=chip,
            period=period,
            duty_cycle_push=duty_cycle_push,
            duty_cycle_release=duty_cycle_release,
        )

    @classmethod
    def get_plugin_options(cls) -> dict:
        valid_angle = (lambda arg: valid_number(arg, min=-360.0, max=360.0, type=float))
        return {
            "chip":           Option(0,        type=valid_int_f0),
            "period":         Option(20000000, type=valid_int_f0),
            "duty_cycle_min": Option(1000000,  type=valid_int_f0),
            "duty_cycle_max": Option(2000000,  type=valid_int_f0),
            "angle_min":      Option(0.0,      type=valid_angle),
            "angle_max":      Option(180.0,    type=valid_angle),
            "angle_push":     Option(100.0,    type=valid_angle),
            "angle_release":  Option(120.0,    type=valid_angle),
        }

    def __str__(self) -> str:
        return f"Servo({self._instance_name})"

    __repr__ = __str__
