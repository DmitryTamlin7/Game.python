import random

suits = ('Червы', 'Бубны', 'Пики', 'Трефы')
ranks = ('Двойка', 'Тройка', 'Четвёрка', 'Пятерка', 'Шестёрка', 'Семёрка', 'Восьмёрка', 'Девятка', 'Десятка', 'Валет', 'Дама', 'Король', 'Туз')
values = {'Двойка':2, 'Тройка':3, 'Четвёрка':4, 'Пятерка':5, 'Шестёрка':6, 'Семёрка':7, 'Восьмёрка':8, 'Девятка':9, 'Десятка':10, 'Валет':10, 'Дама':10, 'Король':10, 'Туз':11}

playing = True

class Card:
    
    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank
        
    
    def __str__(self):
        return  self.rank + '-' + self.suit 
        


class Deck:
    
    def __init__(self):
        self.deck = []  # начинаем с пустого списка
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) 
    
    def __str__(self):
        deck_comp = ''  # начинаем с пустой строки
        for card in self.deck:
            deck_comp += '\n '+card.__str__() 
        return 'В колоде находятся:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card



class Hand:
    def __init__(self):
        self.cards = []  # начинаем с пустого списка, так же, как и в классе Deck 
        self.value = 0   # начинаем со значения 0
        self.aces = 0    # добавляем атрибут, чтобы учитывать тузы
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Туз':
            self.aces += 1
        pass
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
        pass


class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('Ставка? '))
        except ValueError:
            print('число только целое')
        else:
            if chips.bet > chips.total:
                print("Большая ставка, твой баланс ",chips.total)
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
    pass

def hit_or_stand(deck,hand):
    global playing  # для контроля цикла while
    while True:
        x = input("ВОзьмите карту или останьтесь при себе. h = взять карту s = остаться")
        if x[0].lower() == 'h':
            hit(deck, hand)
            
        elif x[0].lower() == 's':
            print('Игра диллера')
            playing = False
            
        else: 
            print('попробуй еще раз')
            continue
        break

    
    


def show_some(player,dealer):
    print("\nКарты Дилера:")
    print(" <карта скрыта>")
    print('',dealer.cards[1])  
    print("\nКарты Игрока:", *player.cards, sep='\n ')
    
   
    
def show_all(player,dealer):
    print('\nКарты диллера', *dealer.cards, sep='\n ')
    print('карты диллера = ', dealer.value )
    print('\nкарты игрока', *player.cards, sep='\n ')
    print('Карты игрока = ', player.value )
    
   
def player_busts(player,dealer,chips):
    print('игрок превысил 21')
    chips.lose_bet()
    pass

def player_wins(player,dealer,chips):
    print('Игрок победил')
    chips.win_bet()
    pass

def dealer_busts(player,dealer,chips):
    print('Диллер превысил 21')
    chips.win_bet()
    pass
    
def dealer_wins(player,dealer,chips):
    print('Диллер победил')
    chips.lose_bet()
    pass
    
def push():
    print('ничья')
    pass









while True:

    # Напишите приветственное сообщение
    print('Добро пожаловать в игру Блекджэк! Постарайтесь приблизиться к сумме 21 как можно ближе, не превышая её!\n\
    Дилер берёт дополнительные карты до тех пор, пока не получит сумму больше 17. Туз считается как 1 или 11.')

    
    # Создайте и перемешайте колоду карт, выдайте каждому Игроку по две карты
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())


    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())


    # Установите количество фишек Игрока
    player_chips = Chips()

    # Спросите у Игрока его ставку
    take_bet(player_chips)
          

    
    # Покажите карты (но оставьте одну и карт Дилера скрытой)

    show_some(player_hand,dealer_hand)

    
    while playing:  # помните, это переменная из нашей функции hit_or_stand 
        
        # Спросите Игрока, хочет ли он взять дополнительную карту или остаться при текущих картах

        hit_or_stand(deck,player_hand)
        
        
        # Покажите карты (но оставьте одну и карт Дилера скрытой)

        show_some(player_hand,dealer_hand)
 
        
        # Если карты Игрока превысили 21, запустите player_busts() и выйдите из цикла (break)
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # Если карты Игрока не превысили 21, перейдите к картам Дилера и берите доп. карты до суммы карт >=17
    if player_hand.value < 21:
        while dealer_hand.value < 17 :
            hit(deck, dealer_hand)
    
        # Показываем все карты
        show_all(player_hand,dealer_hand)

    
        # Выполняем различные варианты завершения игры
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value > player_hand.value:
            player_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else: push(dealer_hand, player_hand)

    # Сообщить Игроку сумму его фишек 
    print('Сумма фишек', player_chips.total)
    
    # Спросить его, хочет ли он сыграть снова
    new_game = input("Хотите ли сыграть снова? Введите 'y' или 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Спасибо за игру!")
        break