"""
Прототип — это порождающий паттерн проектирования, который позволяет копировать объекты, не вдаваясь в подробности их реализации.


Проблема:
У вас есть объект, который нужно скопировать. Как это сделать? Нужно создать пустой объект такого же класса, 
а затем поочерёдно скопировать значения всех полей из старого объекта в новый.

Прекрасно! Но есть нюанс. Не каждый объект удастся скопировать таким образом, ведь часть его состояния может быть приватной, 
а значит — недоступной для остального кода программы.

Но есть и другая проблема. Копирующий код станет зависим от классов копируемых объектов. Ведь, чтобы перебрать все поля объекта, 
нужно привязаться к его классу. Из-за этого вы не сможете копировать объекты, зная только их интерфейсы, а не конкретные классы.


Решение
Паттерн Прототип поручает создание копий самим копируемым объектам. Он вводит общий интерфейс для всех объектов,
 поддерживающих клонирование. Это позволяет копировать объекты, не привязываясь к их конкретным классам. Обычно такой интерфейс имеет всего один метод clone.
 
 
 +
 Позволяет клонировать объекты, не привязываясь к их конкретным классам.
 Меньше повторяющегося кода инициализации объектов.
 Ускоряет создание объектов.
 Альтернатива созданию подклассов для конструирования сложных объектов.
 
 -
 Сложно клонировать составные объекты, имеющие ссылки на другие объекты.
 
 
 Отношения с другими паттернами
Многие архитектуры начинаются с применения Фабричного метода (более простого и расширяемого через подклассы) и эволюционируют 
в сторону Абстрактной фабрики, Прототипа или Строителя (более гибких, но и более сложных).

Классы Абстрактной фабрики чаще всего реализуются с помощью Фабричного метода, хотя они могут быть построены и на основе Прототипа.

Если Команду нужно копировать перед вставкой в историю выполненных команд, вам может помочь Прототип.

Архитектура, построенная на Компоновщиках и Декораторах, часто может быть улучшена за счёт внедрения Прототипа.
 Он позволяет клонировать сложные структуры объектов, а не собирать их заново.

Прототип не опирается на наследование, но ему нужна сложная операция инициализации. Фабричный метод, наоборот, 
построен на наследовании, но не требует сложной инициализации.

Снимок иногда можно заменить Прототипом, если объект, состояние которого требуется сохранять в истории, довольно простой,
 не имеет активных ссылок на внешние ресурсы либо их можно легко восстановить.

Абстрактная фабрика, Строитель и Прототип могут быть реализованы при помощи Одиночки.
"""

import copy


class Registrar:
    _STORAGE = {}

    @staticmethod
    def register(id, object):
        Registrar._STORAGE[id] = object

    @staticmethod
    def copy(id):
        return copy.copy(Registrar._STORAGE[id])

    @staticmethod
    def deepcopy(id):
        return copy.deepcopy(Registrar._STORAGE[id])



class Prototype:
    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)


if __name__ == '__main__':


    class SomeComponent:
        """
        Python provides its own interface of Prototype via `copy.copy` and
        `copy.deepcopy` functions. And any class that wants to implement custom
        implementations have to override `__copy__` and `__deepcopy__` member
        functions.
        """

        def __init__(self, some_int, some_list_of_objects, some_circular_ref):
            self.some_int = some_int
            self.some_list_of_objects = some_list_of_objects
            self.some_circular_ref = some_circular_ref

        def __copy__(self):
            """
            Create a shallow copy. This method will be called whenever someone calls
            `copy.copy` with this object and the returned value is returned as the
            new shallow copy.
            """
            new = self.__class__(
                self.some_int, self.some_list_of_objects, self.some_circular_ref
            )
            new.__dict__.update(self.__dict__)

            # The new object has a new list of objects but with same
            # objects(shared).
            new.some_list_of_objects = copy.copy(self.some_list_of_objects)
            new.some_circular_ref = copy.copy(self.some_circular_ref)
            return new

        def __deepcopy__(self, memo={}):
            """
            Create a deep copy. This method will be called whenever someone calls
            `copy.deepcopy` with this object and the returned value is returned as
            the new deep copy.

            What is the use of the argument `memo`? Memo is the dictionary that is
            used by the `deepcopy` library to prevent infinite recursive copies in
            instances of circular references. Pass it to all the `deepcopy` calls
            you make in the `__deepcopy__` implementation to prevent infinite
            recursions.
            """
            new = self.__class__(
                self.some_int, self.some_list_of_objects, self.some_circular_ref
            )
            new.__dict__.update(self.__dict__)

            # The new object has a new list of objects with different copy of those
            # objects.
            new.some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
            new.some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)
            return new


    class A(Prototype):
        def __init__(self):
            self.l = [1, 2, 3, 4]
            self.d = {
                "1": 1,
                "2": [1, 2, 3, 4],
                "3": 1,
                "4": 1,
            }

        def __str__(self):
            return "self.l = {}, self.d = {}".format(self.l, self.d)