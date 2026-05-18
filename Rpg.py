import random
from calendar import day_name
from encodings import palmos
from select import select

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
        self.money = 10000

        self.skills = [
            {
                'name': 'Швидкій удар',
                'min_dmg': 1000,
                'max_dmg': 1500,
                'chance': 0.9
            },
            {
                'name': 'потужний удар',
                'min_dmg': 25,
                'max_dmg': 40,
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
            self.potions -= 1

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
        print(f"УВАГА! На рівні {self.level} на тебе чекає бос!⚠️")
        boss = Boss(self.level)

        while boss.is_alive() and self.is_alive():
            print(f"БИТВА З БОСОМ: {boss.name}")
            print(f"{self.name}: {self.hp}❤️  |  {boss.name}: {boss.hp}❤️")

            for index, skill in enumerate(self.skills):
                print(f"{index + 1}. {skill['name']} ({skill['min_dmg']}-{skill['max_dmg']})")

            try:
                choice = int(input("Твій хід⚔️: "))
                if 1 <= choice <= len(self.skills):
                    skill = self.skills[choice - 1]
                    if random.random() <= skill['chance']:
                        dmg = random.randint(skill['min_dmg'], skill['max_dmg'])
                        boss.hp -= dmg
                        print(f"💥 Ти влучив! Урону нанесно: {dmg}")
                    else:
                        print("💨 Промах!")


                if boss.is_alive():
                    boss_dmg = random.randint(int(boss.power * 0.8), int(boss.power * 1.2))
                    self.hp -= boss_dmg
                    print(f"👹 {boss.name} вдарив тебе на {boss_dmg} урону!")

            except ValueError:
                print("Введіть число!")

        if self.is_alive():
            print(f"🏆Ти подолав боса {boss.name}!")
            print("Твій шлях продовжується")
        else:
            print(f"💀 Босс {boss.name} виявився сильнішим")


class Monster(Creature):
    def __init__(self, player_level):
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
        multiplier = 1 + (player_level - 1) * 0.2

        super().__init__(monster['name'], int(monster['hp'] * multiplier))

        self.power = int(monster['damage'] * multiplier)

class Boss(Monster):
    def __init__(self, player_level):
        boss_data = [
            {
                'name': 'Зомбі',
                'hp': 250,
                'damage': 50
            },
            {
                'name': 'Орк-БОСС',
                'hp': 350,
                'damage': 65
            },
            {
                'name': 'Король-БОСС',
                'hp': 450,
                'damage': 80
            }
        ]

        boss = random.choice(boss_data)
        multiplier = 1 + (player_level - 2) * 0.3

        Creature.__init__(self, boss['name'], int(boss['hp'] * multiplier))

        self.power = int(boss['damage'] * multiplier)



class Event:
    def __init__(self, name,  description):
        self.name = name
        self.description = description

    def trigger(self, player):
        print('-----------------------')
        print(f'⚔️Подія: {self.name}. {self.description}⚔️')

class Shop:
    def __init__(self, shop_name):
        self.shop_name = shop_name

        self.product = [
            {
                'name': 'Щит',
                'price': 150,
                'type': 'shield',
            },
            {
                'name': 'Зілля',
                'price': 100,
                'type': 'potions',
            },
        ]


    def start(self):
        while True:
            print(f"Вітаємо в магазині {self.shop_name}!")
            print(f"Ваш баланс: {player.money} золота 💰")
            print("Доступні товари:")
            for index, item in enumerate(self.product):
                print(f"{index + 1}. {item['name']} | {item['price']} золота")
                print(f"{len(self.product) + 1}. Вийти з магазину")

            try:
                choice = int(input("Що бажаєте придбати? ")) - 1

                if choice == len(self.product):
                    print("Дякуємо за візит!")
                    return

                item = self.product[choice]

                if player.money >= item['price']:
                    player.money -= item['price']
                    print(f" Ви купили {item['name']}!")

                    if item['type'] == 'potions':
                        player.potions += 1
                    elif item['type'] == 'shield':
                        player.max_hp += 10
                        player.hp += 10

                else:
                    print("У вас недостатньо золота!")
            except ValueError:
                print("Невірний вибір")
                continue



class ShopEvent(Event):
    def __init__(self):
        super().__init__('Магазин', 'Можна купувати зілля,щит')
        self.shop = Shop('Магазин чогось!')

    def trigger(self, player):
        super().trigger(player)
        self.shop.start()


class TrainerEvent(Event):
    def __init__(self):
        super().__init__('Тренер  фехтування⚔️',
                         'Ви зурстріли тренера, що може навчити вас новому!💪')

        self.skills = [
            {
                'name': 'Гарантований удар',
                'min_dmg': 5,
                'max_dmg': 10,
                'chance': 1.0
            },
            {
                'name': 'Удар з ноги',
                'min_dmg': 20,
                'max_dmg': 30,
                'chance': 0.6
            },
            {
                'name': 'Удар Смерті',
                'min_dmg': 80,
                'max_dmg': 120,
                'chance': 0.05
            },
        ]

    def trigger(self, player):
        super().trigger(player)

        print('Навички на вибір:')
        for index, skill in enumerate(self.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}) Шанс: {skill['chance']}')

        player_choice = int(input('Вам вибір:'))
        new_skill = self.skills[player_choice - 1]
        player.skills.append(new_skill)
        print('Навички отримано!💪')


class UpgradeEvent(Event):
    def __init__(self):
        super().__init__('Ви знайшли Точильний камінь💎',
                         'Ви знайши камінь, що допоможе покращити одни з скілів!')


    def trigger(self, player):
        super().trigger(player)

        print('Навички на вибір:')
        for index, skill in enumerate(player.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}) Шанс: {skill['chance']}')

        player_choice = int(input('Вам вибір:'))
        upgrade_skill = player.skills[player_choice - 1]
        upgrade_skill['chance'] += 0.05
        print(f'Тепер навик {upgrade_skill['name']} має шанс: {upgrade_skill['chance']}')






#======= Гра
print('⚔️Вітаємо у грі "OOP-Battles"⚔️')

player_name = input("🤴Введіть ім'я свого героя:👑")
player = Player(player_name)
events = [TrainerEvent(), UpgradeEvent(), ShopEvent()]
print(f'{player.name} починає пригоди! 🏇')

while player.is_alive():
    enemy  = Monster(player.level)
    print(f'На шляху стоїть {enemy.name}👹')
    print(f"Його здоров'я: {enemy.hp}❤️")
    print(f'Його сила: {enemy.power}💪')

    while enemy.is_alive() and player.is_alive():
        print('===================================')
        print(f"{player.name} - {player.hp}❤️ | {enemy.name} - {enemy.hp}❤️")
        print('Що будеш робити?')

        for index, skill in enumerate(player.skills):
            print(f'{index + 1}. {skill['name']} ({skill['min_dmg']}|{skill['max_dmg']}) Шанс: {skill['chance']}')

        healt_index = index + 2
        relax_index = index + 3
        shop_index = index + 4

        print(f'{healt_index} Полікуватись❤️')
        print(f'{relax_index} Пропустити🦥')
        print(f'{shop_index} Магазин🏪')

        try:
            player_choice = int(input('Ваш вибір⚔️:'))
        except ValueError:
            print('Ви ввели не число')
            continue

        if 1 <= player_choice <= len(player.skills):
            select_skill = player.skills[player_choice - 1]

            if random.random() <= select_skill['chance']:
                print('Попав💪')
                damage = random.randint(select_skill['min_dmg'], select_skill['max_dmg'])
                print(f'Ворог отривам {damage} урону!🩸')
                enemy.hp -= damage
            else:
                print('Ворог ухильнувся💨')
        elif player_choice == healt_index:
            player.heal()
        elif player_choice == relax_index:
            print('Ви вирішили відпочити посеред бою🧘')
            player.hp += 10
        elif player_choice == shop_index:
            shop = Shop("Лавка")
            shop.start()

        if enemy.is_alive():
            damage = random.randint(int(enemy.power * 0.8), int(enemy.power * 1.2))
            print(f"Здоров'я ворога: {enemy.hp}❤️")
            print(f'Ворог Атакає!👹 {damage} Наніс урону!')
            player.hp -= damage

    if player.is_alive():
        print('Монстра переможено!💀⚔️')
        gain_xp = random.randint(40 , 70)
        player.gain_exp(gain_xp)
        player.potions += 1
        gold = random.randint(10, 30)
        player.money += gold
        print(f'Ти отривам {gain_xp} досвіду!💥, та {gold} золота, та одне зілля!')

        if random.random() <= 0.5:
            ev = random.choice(events)
            ev.trigger(player)





print('⚔️Гру Завершино!⚔️')
print(f'💀{player.name} протривамався до {player.level} рівню!💀')
