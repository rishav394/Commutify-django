import bcrypt


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def convert_tuple_list_to_unique_list(tuple_list: list) -> list:
    return list(
        set(
            [item for sublist in map(lambda x: list(x), tuple_list) for item in sublist]
        )
    )
