

from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> None:
        mes = asdict(self)
        return self.MESSAGE.format(*mes.values())


"""Информационное сообщение о тренировке."""


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    M_IN_H: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:

        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return NotImplementedError('не получилось рассчитать каллории')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    run_calorie_1 = 18
    run_calorie_2 = 20

    def get_spent_calories(self) -> float:

        return ((self.run_calorie_1
                * self.get_mean_speed()
                - self.run_calorie_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.M_IN_H)


class SportsWalking(Training):
    walk_calorie_1: float = 0.035
    walk_calorie_2: float = 2
    walk_calorie_3: float = 0.029

    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.walk_calorie_1
                * self.weight
                + (self.get_mean_speed() ** self.walk_calorie_2 // self.height)
                * self.walk_calorie_3 * self.weight)
                * self.duration
                * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    swim_calorie_1 = 1.1
    swim_calorie_2 = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.len_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.len_pool * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.swim_calorie_1)
                * self.swim_calorie_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pam_train = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in pam_train:
        return pam_train[workout_type](*data)



def main(training: Training) -> None:
    """Главная функция."""
    message_trainig = training.show_training_info()
    print(message_trainig.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
