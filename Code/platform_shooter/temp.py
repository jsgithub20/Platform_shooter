class Animal:
    def __init__(self,name,age,weight):
        self.name=name
        self.age=age
        self.weight=weight


class Dog(Animal):
    def __init__(self,name,age,weight,owner):
        super().__init__(name,age,weight)
        self.owner=owner


class NewDog(Animal):
    def __init__(self,name,age,weight,owner):
        Animal.__init__(self, name,age,weight)
        self.owner = owner


class Cat(Animal):
    def __init__(self, name,age,weight,sound):
        super().__init__(name, age, weight)
        self.sound = sound


d1=Dog('小白','2','20','小黑')
d2=Dog('小白','2','20','小黑')

c1 = Cat("meow1", "2", "4", "meow")

print('%s的主人是%s'%(d2.name,d2.owner))#小白的主人是小黑

print(f"{c1.name} is a cat, and she makes sound of '{c1.sound}'")