import json
import math

import requests


class Vehicle:
    def __init__(self,  name, model, year, color, price, latitude, longitude, id=None):
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.id = id

    def __repr__(self):
        return f'{self.name} {self.model} {self.year} {self.color} {self.price}'


class VehicleDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(json_dict: dict):
        new_vehicle = Vehicle(
            json_dict.get('name'),
            json_dict.get('model'),
            json_dict.get('year'),
            json_dict.get('color'),
            json_dict.get('price'),
            json_dict.get('latitude'),
            json_dict.get('longitude'),
            json_dict.get('id'),
        )
        return new_vehicle


class VehicleManager:
    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self) -> list[Vehicle]:
        return requests.get(self.url).json(cls=VehicleDecoder)

    def get_vehicle(self, id: int) -> Vehicle:
        url = f'{self.url}{id}/'
        return requests.get(url).json(cls=VehicleDecoder)

    @classmethod
    def check_vehicle_with_params(cls, params: dict, vehicle: Vehicle):
        for param in params.keys():
            if params[param] == getattr(vehicle, param):
                continue
            else:
                return False
        return True

    def filter_vehicles(self, params: dict) -> list[Vehicle]:
        vehicles = self.get_vehicles()
        filter_vehicles = []
        for vehicle in vehicles:
            if self.check_vehicle_with_params(params=params, vehicle=vehicle):
                filter_vehicles.append(vehicle)
        return filter_vehicles

    def add_vehicle(self, new_vehicle: Vehicle) -> None:
        requests.post(self.url, json=new_vehicle.__dict__)
        print(f'{new_vehicle.name} {new_vehicle.model} has added')

    def update_vehicle(self, id: int, new_vehicle_info: Vehicle) -> None:
        url = f'{self.url}{id}/'
        requests.put(url, json=new_vehicle_info.__dict__)
        print(f'{new_vehicle_info.name} {new_vehicle_info.model} has updated')

    def delete_vehicle(self, id: int) -> None:
        url = f'{self.url}{id}/'
        requests.delete(url)
        print(f'Vehicle with id {id} has deleted')

    def get_distance(self, id1: int, id2: int) -> float:
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        x1 = float(vehicle1.latitude)
        x2 = float(vehicle2.latitude)
        y1 = float(vehicle1.longitude)
        y2 = float(vehicle2.longitude)
        trapezoid_side = abs((x1 - x2) * 111.1)
        trapezoid_top_base = abs(y1 - y2) * 111.3 * math.cos(max(x1, x2) * math.pi / 180)
        trapezoid_bottom_base = abs(y1 - y2) * 111.3 * math.cos(min(x1, x2) * math.pi / 180)
        trapezoid_height = math.sqrt(trapezoid_side ** 2 - ((trapezoid_bottom_base - trapezoid_top_base) * 0.5) ** 2)
        trapezoid_dioganal = math.sqrt(trapezoid_height ** 2 +
                                       (trapezoid_top_base + (trapezoid_bottom_base - trapezoid_top_base) * 0.5) ** 2)
        return trapezoid_dioganal

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        vehicles = self.get_vehicles()
        reference_vehicle = self.get_vehicle(id)
        distances_to_reference_vehicle = {}
        for vehicle in vehicles:
            if vehicle.id != reference_vehicle.id:
                distances_to_reference_vehicle[vehicle] = self.get_distance(id, vehicle.id)
        return sorted(distances_to_reference_vehicle.items(), key=lambda item: item[1])[0][0]


# manager = VehicleManager(url='http://127.0.0.1:8000/vehicle/')
# print(manager.get_vehicles())
# print(manager.get_vehicle(id=2))
# print(manager.filter_vehicles({'year': 2011, 'color': 'gray'}))
# manager.add_vehicle(new_vehicle=Vehicle(name='Chevrolette', model='Niva', year='2011', color='pink', price='7000',
#                                         latitude='61.235308', longitude='69.728326'))
# manager.update_vehicle(id=16, new_vehicle_info=Vehicle(name='Chevrolette', model='Niva', year='2011', color='pink',
#                                                        price='9500', latitude='61.235308', longitude='69.728326'))
# manager.delete_vehicle(17)
# print(manager.get_distance(id1=2, id2=3))
# print(manager.get_nearest_vehicle(3))
