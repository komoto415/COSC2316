def get_face_frequencies_from_card_hand(hand):
    face_frequencies = {}
    for faces in hand:
        face_frequencies[faces] = face_frequencies.get(faces, 0) + 1

    return face_frequencies

def discard_all_cards_with_face(hand, face):
    assert face in [card.face_str() for card in hand]
    for card in hand:
        if card.face_str() == face:
            hand.remove(card)

def discard_four_of_a_kind_with_face(hand, face):
    assert hand.hand_as_faces().count(face) == 4

    cards_with_face_found = 0
    while cards_with_face_found < 4:
        for card in hand:
            if card.face == face:
                cards_with_face_found += 1
                hand.remove(card)

def get_all_cards_with_face(hand, face):
    return [card for card in hand if card.face_str() == face]

# def get_n_cards_with_face(hand, face, n):
#     cards_with_face = []
#     while len(cards_with_face) < n
#     # for card in
#     return [card for card in hand if card.face_str() == face]

def give_up_all_cards_with_face(hand, face):
    give_up = get_all_cards_with_face(hand, face)
    discard_all_cards_with_face(hand, face)
    return give_up

def group_by_frequency_max_4(hand):
    face_frequencies = get_face_frequencies_from_card_hand(hand)
    groups = ([], [], [], [])

    for face, frequency in face_frequencies.items():
        groups[frequency - 1].append(face)

    return groups

def get_four_of_a_kind_faces(hand):
    face_frequencies = get_face_frequencies_from_card_hand(hand)
    four_of_a_kinds = []
    for face, frequency in face_frequencies.items():
        if frequency % 4 == 0 and frequency != 0:
            for _ in range(frequency // 4):
                four_of_a_kinds.append(face)

    return four_of_a_kinds

# def found_four_of_a_kind_of_face(hand, face):
#     face_frequencies = get_face_frequencies_from_card_hand(hand)
#     return face in face_frequencies
