import random

#######Executive Summary######
'''
1. 3 დამხმარე ფუნქცია: #1 დასტის შემქმნელი, #2 ქულების გამომთვლელი, და #3 მოთამაშის ბანქოს და ჯამური ქულების მაჩვენებელი ფუნქციები.
 
2. 1 მთავარი ფუნქცია, რომლის ლოგიკაა: #1 მოთამაშეების სახელების შეყვანა; #2 5 ბანქოს დარიგება და მე-3 დამხმარე ფუნქციის გამოყენება და დაპრინტვა;
#3 ბანქოს შეცვლის შეთავაზება; #4 ქულების თანმიმდევრობით დალაგება და უმცირესი ქულის მქონე მოთამაშის გაგდება; #5 თამაში გრძელდება იქამდე სანამ 1 მოთამაშე არ დარჩება.
 
3. კოდი მოდიფიცირებულია პოტენციურ error-თან გასამკლავებლად, რის დემონსტრირებას კოდის გაშვებისას შემოგთავაზებთ.
 
'''

# ვქმნით ცვლადებს ფერებისა და მნიშვნელობების მიხედვით, რათა შევქმნათ დასტა/კომბინაციები
SUITS = ['S', 'H', 'D', 'C']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'J', 'Q', 'K']

# ფუნქცია ქმნის დასტას, ზემოთ ცვლადებში არსებული მნიშვნელობათა კომბინაციებით
def create_shuffled_deck():
    deck = [value + suit for value in VALUES for suit in SUITS] * 4
    random.shuffle(deck)  # კომბინაციებს ვურევთ, ანუ ვჩეხავთ კარტს
    return deck
 
# ვითვლით ქულებს
def calculate_score(hand):
    points, suit_count, value_count = 0, {suit: 0 for suit in SUITS}, {}
    for card in hand:
        value, suit = card[:-1], card[-1] # მოთამაშის კარტებისგან ვაცალკევებთ მნიშვნელობასა და ფერს
        points += int(value) if value.isdigit() else {'J': 11, 'Q': 12, 'K': 13, 'A': 20}[value] # ვითვლით ქულებს და პროგრამას ვეუბნებით ნახატებიანი კარტების მნიშვნელობას
        suit_count[suit] += 1 # ვითვლით ფერების რაოდენობას
        value_count[value] = value_count.get(value, 0) + 1 # ვითვლით მნიშვნელობათა რაოდენობებს
    return points, max(suit_count.values()), max(value_count.values()) # ფუნქცია აბრუნებს ქულებს
 
# გვიჩვენებს მოთამაშეების სახელს, რა კარტები უჭირავთ ხელში და რა ქულის ექვივალენტია ჯამურად ეს კარტები.
def display_players(players):
    for player in players:
        print(f"{player['name']}: {player['hand']} (Points: {player['points']})")
 
 
def main():
    # შეგვყავს მოთამაშეების სახელები key-დ, ვქმნით ველიუ ინფუთს: სიას - კარტებისთვის და  ქულებისთვის
    players = [{'name': input(f"Enter player {i+1} name: "), 'hand': [], 'points': 0} for i in range(3)]
    deck = create_shuffled_deck()
 
    # პროგრამა მუშაობს მანამ სანამ არ გამოვლინდება გამარჯვებული (დარჩება ერთი მოთამაშე)
    while len(players) > 1:
        for player in players:
            player['hand'] = [deck.pop() for _ in range(5)] # ვარიგებთ 5 კარტს თითოეულისთვის
            player['points'], player['max_suit'], player['max_value'] = calculate_score(player['hand']) # ვითვლით ქულებს
       
        display_players(players) #გვაჩვენებს მოთამაშეების სახელს, მათ ხელში არსებულ კარტებს და მათ ქულებს
       
        # მოთამაშეებს აქვთ უფლება 1 კარტი შეცვალონ ერთხელ
        for player in players:
            while True:
                yes_or_no = input(f"{player['name']}, replace a card? (yes/no): ").lower()
                if yes_or_no == 'yes':
                    card_to_replace = input(f"Enter card to replace: ").upper()
                    if card_to_replace in player['hand']:
                        player['hand'].remove(card_to_replace) # შეცვლი მოთამაშის კარტს
                        new_card = deck.pop() # იღებს დასტიდან ახალ კარტს
                        player['hand'].append(new_card) # აძლევს მეხუთე კარტად ახალ კარტს
                        player['points'], player['max_suit'], player['max_value'] = calculate_score(player['hand']) # რეკალკულირება
                        break  
                    else:
                        print(f"Card {card_to_replace} is not in your hand. Try again.") # არასწორი კარტის შემთხვევაში თავიდან ვეკითხებით
                elif yes_or_no == 'no':
                    break
                else:
                    print("Please try again and write yes or no")
 
        display_players(players) # გვაჩვენებს განახლებულ მონაცემებს
 
        players.sort(key=lambda x: (x['points'], x['max_suit'], x['max_value'])) # ქულების ზრდის მიხედვით ალაგებს მოთამაშეებს
        loser = players.pop(0) # სიის თავში მყოფს გააგდებს, ანუ ყველაზე ნაკლები ქულის მქონეს. (ამოიღებს სიიდან და შემცირდება მოთამაშეთა რაოდენობა)
        print(f"{loser['name']} is eliminated!") # პროგრამა გვაჩვენებს გავარდნილს
        random.shuffle(deck)
 
    print(f"\nThe winner is {players[0]['name']}!") # გამარჯვებულს გვიჩვენებს
 
# პროგრამის გაშვება.
if __name__ == "__main__":
    main()