import random


class Creature:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        return self.hp > 0


class Station(Creature):
    def __init__(self, name, hp=100):
        super().__init__(name, hp)
        self.day = 1
        self.resources = {'scrap': 50, 'energy': 100}


        self.protocols = [
            {
                'name': 'Аварійний щит',
                'min_save': 10,
                'max_save': 15,
                'chance': 0.9
            },
            {
                'name': 'Маневр ухилення',
                'min_save': 20,
                'max_save': 40,
                'chance': 0.4
            },
            {
                'name': 'Лазерне збиття',
                'min_save': 50,
                'max_save': 80,
                'chance': 0.15
            },
        ]

    def next_day(self):
        self.day += 1
        self.resources['scrap'] += 20
        print(f"✅ Ми пережили ще один день! Настав день {self.day}")

class Monster(Creature):
    def __init__(self, station_day):
        monster_data = [
              {'name': 'Метеоритний дощ',
              'hp': 30,
              'damage': 10
               },
              {'name': 'Космічне сміття',
              'hp': 50,
              'damage': 18
              },
              {'name': 'Сонячний спалах',
              'hp': 80,
              'damage': 25
              },
              {'name': 'Ворожий дрон',
              'hp': 120,
              'damage': 45
              },
        ]

        monster = random.choice(monster_data)
        multiplier = 1 + (station_day - 1) * 0.2

        super().__init__(monster['name'], int(monster['hp'] * multiplier))
        self.power = int(monster['damage'] * multiplier)


# =======Гра=======
print('⚔️ Вітаємо у грі "Space-Battles ООП" ⚔️')

player_name = input("👨‍✈️ Введіть ім'я Капітана: ")
station = Station(player_name)
print(f"Капітан {station.name} починає службу! 🚀")

while station.is_alive() and station.day <= 10:
    enemy = Monster(station.day)
    print(f"⚠️ На шляху загроза: {enemy.name}👹")
    print(f"Її здоров'я: {enemy.hp}❤️")
    print(f"Її сила: {enemy.power}💪")

    while enemy.is_alive() and station.is_alive():
        print(f"Ваше здоров'я (HP): {station.hp}❤️")
        print('Що будеш робити?')

        for i, p in enumerate(station.protocols):
            print(f"{i + 1}. {p['name']} ({p['min_save']}|{p['max_save']}) Шанс: {p['chance']}")

        print("4. Ремкомплект 🛠️")
        print("5. Прийняти удар 🛸")

        try:
            choice = int(input("Ваш вибір⚔️: "))
        except:
            choice = 5


        if 1 <= choice <= 3:
            protocol = station.protocols[choice - 1]
            if random.random() <= protocol['chance']:
                dmg = random.randint(protocol['min_save'], protocol['max_save'])
                enemy.hp -= dmg
                print(f"✨ Успіх! {protocol['name']} послабив загрозу на {dmg}!")
            else:
                print("❌ Протокол не спрацював!")

        elif choice == 4:

            print(f"🛡️ Капітан {station.name} вирішив Полатати корпус станції!")

        elif choice == 5:

            print(f"🛡️ Капітан {station.name} вирішив прийняти удар на корпус станції!")

        if enemy.is_alive():
            damage = enemy.power
            station.hp -= damage
            print(f"💥 {enemy.name} завдав станції {damage} шкоди!")

    if station.is_alive():
        print(f"🏁 Загроза {enemy.name} подолана!")
        station.next_day()


print('⚔️ ГРУ ЗАВЕРШЕНО! ⚔️')
if station.is_alive() and station.day > 10:
    print(f"🌟 ПЕРЕМОГА! Капітан {station.name} врятував станцію!")
else:
    print(f"💀 Капітан {station.name} протримався до {station.day} дня! 💀")