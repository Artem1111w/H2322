import random
from encodings import palmos

class Creature:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        return self.hp > 0


class Player(Creature):
    def __init__(self, name, hp=100):
        super().__init__(name, hp)
        self.level = 1
        self.exp = 0
        self.potions = 3

        self.skills = [
            {
                'name': 'Швидкій удар',
                'min_dmg': 10,
                'max_dmg': 15,
                'chance': 0.9
            },
            {
                'name': 'потужний удар',
                'min_dmg': 40,
                'max_dmg': 25,
                'chance': 0.4
            },
            {
                'name': 'Удар в серце',
                'min_dmg': 60,
                'max_dmg': 80,
                'chance': 0.15
            },
        ]

    def heal(self):
        if self.potions > 0:
            amount = 40 + (self.level * 5)
            print(f'Ти вилікувався на {amount} HP!❤️')

            self.hp += amount

            if self.hp > self.max_hp:
                self.hp = self.max_hp

            print(f'В тебе зараз: {self.hp}❤️')
        else:
            print('В тебе більше немає хілок🧪')

    def gain_exp(self, amount):
        self.exp += amount
        print(f'Ти отримав: {amount}exp💥')

        if self.exp >= 100:
            self.new_level()

    def new_level(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 20
        self.hp = self.max_hp
        print('НОВИЙ РІВЕНЬ!🍾')
        print(f'Твій рівень тепер: {self.level}')
        print(f"Твоє здоров'я: {self.max_hp}")


class Monster(Creature):
    def __init__(self, palyer_level):
        monster_data = [
            {
                'name': 'Гоблін',
                'hp': 30,
                'damage': 5
            },
            {
                'name': 'Орк-Боксер',
                'hp': 60,
                'damage': 12
            },
            {
                'name': 'Орк з сокирою',
                'hp': 90,
                'damage': 20
            },
            {
                'name': 'Мертвий Король',
                'hp': 150,
                'damage': 40
            },
        ]

        monster = random.choice(monster_data)
        multiplier = 1 + (palyer_level - 1) * 0.2

        super().__init__(monster['name'], int(monster['hp'] * multiplier))

        self.power = int(monster['damage'] * multiplier)


#======= Гра
print('⚔️Вітаємо у грі "OOP-Battles"⚔️')

player_name = input("🤴Введіть ім'я свого героя:👑")
player = Player(player_name)
print(f'{player.name} починає пригоди! 🏇')

while player.is_alive():
    enemy  = Monster(player.level)
    print(f'На шляху стоїть {enemy.name}👹')
    print(f"Його здоров'я: {enemy.hp}❤️")
    print(f'Його сила: {enemy.power}💪')

    while enemy.is_alive() and player.is_alive():
        print(f"Здоров'я: {player.hp}❤️")

        print('Що будеш робити?')

        for index, skill in enumerate(player.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}) Шанс: {skill['chance']}')

        print('4. Полікуватись❤️')
        print('5. Пропустити🦥')

        player_choice = int(input('Ваш вибір⚔️:'))

        #перевірка вибору атаки або лікування
        #контр-атака ворога (якщо живий )


print('⚔️Гру Завершино!⚔️')
print(f'💀{player.name} протривамався до {player.level} рівню!💀')
