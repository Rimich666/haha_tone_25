from repository import base
from repository.exception import exception


def select_user(name):
    base.check_IAM()
    return base.pool.execute_with_retries(
        f"SELECT id, name FROM users WHERE name = '{name}';",
    )[0]


def insert_user(name):
    base.check_IAM()
    user = select_user(name)
    if user.rows:
        return user
    return base.pool.execute_with_retries(
        f"""
            INSERT INTO users (expire_at, updated_on, name) 
            VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), '{name}') RETURNING id, name;
        """,
    )[0]


@exception()
def insert_audio(word, file_name):
    base.check_IAM()
    return base.pool.execute_with_retries(
        f"""
            INSERT INTO audio (de, file_path) 
            VALUES ('{word}', '{file_name}');
        """,
    )[0]


def insert_new_words(words):
    base.check_IAM()
    values = ', '.join(list(map(
        lambda item: f"(CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('{item[0]}'), Utf8('{item[1]}'))", words)))
    return base.pool.execute_with_retries(
        f"""
            INSERT INTO words (de, ru, expire_at, updated_on)
                SELECT l.de as de, l.ru as ru, l.expire as expire_at, l.updated as updated_on
                FROM words
                RIGHT JOIN
                    (SELECT DISTINCT * FROM
                    (VALUES {values}) AS X(expire, updated, de, ru)) as l
                ON (words.de = l.de AND words.ru = l.ru)
                WHERE id ISNULL
            RETURNING id, de;
        """,
    )[0]


@exception(ret_count=2)
def create_list(words, user, name, count):
    base.check_IAM()
    values = ', '.join(list(map(lambda item: f"('{item[0]}', '{item[1]}')", words)))
    tx = base.session.transaction().begin()

    list_id = tx.execute(
        f"""
        INSERT INTO user_lists (expire_at, updated_on, user_id, name, count) 
            VALUES  (CurrentUtcDatetime(), CurrentUtcDatetime(), {user}, '{name}', {count})
            RETURNING id;
        """
    )[0].rows[0]['id']

    query = f"""INSERT INTO user_words (word_id, list_id)
                SELECT id as word_id, {list_id} as list_id
                FROM words
                INNER JOIN
                    (SELECT DISTINCT * FROM
                    (VALUES {values}) AS X(de, ru))
                    as l
                ON (words.de = l.de AND words.ru = l.ru)
            RETURNING word_id;"""

    head = tx.execute(query)[0].rows[:3]
    tx.commit()
    return list_id, head


def select_without_file(words):
    base.check_IAM()
    values = ', '.join(list(map(lambda item: f"('{item['id']}', Utf8('{item['de']}'))", words)))
    return base.pool.execute_with_retries(
        f"""
            SELECT l.id as id, l.de as de FROM audio 
            RIGHT JOIN  
                (SELECT DISTINCT id, de FROM
                (VALUES {values}) AS X(id, de)) as l
            ON audio.de = l.de
            WHERE file_path ISNULL;     
        """)[0].rows


def select_lists(user):
    user_id = insert_user(user).rows[0].id
    return select_lists_by_id(user_id)


def select_lists_by_id(user_id):
    base.check_IAM()
    lists = base.pool.execute_with_retries(
        f"""
            SELECT id, name FROM user_lists WHERE user_id = {user_id};
        """, )
    return lists[0].rows, user_id


def get_list_id(user, name):
    base.check_IAM()
    res = base.pool.execute_with_retries(f"""
    SELECT id, is_loaded FROM user_lists WHERE user_id in 
        (SELECT id FROM users WHERE name = '{user}')
        AND name = '{name}';""", )[0].rows
    return (False, False) if not res else (res[0].id, res[0].is_loaded)


@exception()
def get_list_info(user, name):
    base.check_IAM()
    res = base.pool.execute_with_retries(f"""
    SELECT * FROM (
        SELECT id, is_loaded, count
        FROM user_lists 
        WHERE user_id in 
            (SELECT id FROM users WHERE name = '{user}')
                AND name = '{name}'
            ) as l
        LEFT JOIN
        (SELECT list_id, COUNT(id) as learned
        FROM user_words 
        WHERE learned
        GROUP BY list_id) as c
        ON l.id = c.list_id;""", )[0].rows
    return (False, False, 0, 0) if not res else \
        (res[0].id, res[0].is_loaded, res[0].count, res[0].learned)


def select_free_names(names):
    base.check_IAM()
    values = ', '.join(list(map(lambda name: f"('{name}')", names))) if names else "('')"
    result = base.pool.execute_with_retries(f"""
    SELECT name FROM (SELECT DISTINCT * FROM
        (VALUES {values}) AS X(color))
        as l
        RIGHT JOIN colors
        ON l.color = colors.name
        WHERE color ISNULL
    """)
    return [row.name for row in result[0].rows]


@exception()
def select_words_list(list_id, is_processed=None):
    base.check_IAM()
    processed_string = '' if is_processed is None else f'AND is_processed {'' if is_processed else 'ISNULL'}'
    query = f"""
    SELECT ru, w.de as de, w.id as id, audio_id, is_processed, file_path, learned 
    FROM audio
    RIGHT JOIN 
        (SELECT ru, de, ids.id as id, audio_id, is_processed, learned 
        FROM words 
        RIGHT JOIN 
            (SELECT id, word_id, is_processed, audio_id, learned 
            FROM user_words 
            WHERE list_id = {list_id} 
                {processed_string}
             ) as ids
        ON words.id = ids.word_id) as w
    ON audio.de = w.de
    WHERE NOT (file_path ISNULL);
    """
    res = base.pool.execute_with_retries(query)
    return res[0].rows


@exception()
def set_audio_ids(audio_ids):
    base.check_IAM()
    audio, processed = (zip(*map(
        lambda item: (f"WHEN {item[0]} THEN Utf8('{item[1]}')", f"WHEN {item[0]} THEN {item[2]}"), audio_ids)))

    base.pool.execute_with_retries(
        f"""
        UPDATE user_words 
        SET audio_id = CASE id
            {'\n'.join(audio)}
            ELSE audio_id END,
        is_processed = CASE id
            {'\n'.join(processed)}
            ELSE is_processed END;
        """
    )


@exception()
def set_audio_id(*args, is_processed=False):
    base.check_IAM()
    query_text = f"""
        UPDATE user_words 
        SET audio_id = '{args[1]}'{', is_processed = True' if is_processed else ''} 
        WHERE id = {args[0]} RETURNING id;
    """ if len(args) == 2 else f"""
        UPDATE user_words 
        SET audio_id = '{args[2]}'{', is_processed = True' if is_processed else ''} 
        WHERE word_id = {args[0]} AND list_id = {args[1]} RETURNING id;
    """
    res = base.pool.execute_with_retries(query_text)[0].rows
    return res[0].id == id if res else False


@exception()
def set_is_processed(id):
    base.check_IAM()
    return base.pool.execute_with_retries(
        f"""
        UPDATE user_words SET is_processed = True WHERE id = {id} RETURNING id;""")[0].rows


@exception()
def get_file_path(word):
    base.check_IAM()
    return base.pool.execute_with_retries(
        f"SELECT file_path FROM audio WHERE de = '{word}';",
    )[0].rows


@exception()
def get_added_words(list_id, is_exists):
    base.check_IAM()
    condition = f" AND audio_id IS NOT NULL" if is_exists else ""
    return base.pool.execute_with_retries(
        f"""SELECT id, audio_id 
        FROM user_words 
        WHERE list_id = {list_id} 
        AND is_processed ISNULL{condition};""",
    )[0].rows


def get_words_by_id(ids):
    base.check_IAM()
    value = f"( {', '.join(ids)} )"
    return base.pool.execute_with_retries(
        f"SELECT id, de FROM words WHERE id IN {value};",
    )[0].rows


@exception()
def get_list_is_loaded(id):
    base.check_IAM()
    res = base.pool.execute_with_retries(
        f"SELECT id, is_loaded FROM user_lists WHERE id = {id};"
    )[0].rows
    return (res[0].id, res[0].is_loaded) if res else (None, None)


@exception()
def set_list_is_loaded(id, is_loaded):
    base.check_IAM()
    res = base.pool.execute_with_retries(f"""
        UPDATE user_lists SET is_loaded = {is_loaded} WHERE id = {id} RETURNING id, is_loaded;
    """)[0].rows
    return (res[0].id, res[0].is_loaded) if res else (None, None)


@exception()
def set_created_list(list_id):
    base.check_IAM()
    res = base.pool.execute_with_retries(f"""
        UPDATE user_lists SET is_created = TRUE WHERE id = {list_id} RETURNING id, is_loaded;
    """)


@exception()
def get_created_list(list_id):
    base.check_IAM()
    return base.pool.execute_with_retries(f"""
        SELECT is_created FROM user_lists WHERE id = {list_id};
    """)[0].rows[0].is_created


def reset_list_is_loaded(list_id):
    base.check_IAM()
    tx = base.session.transaction().begin()
    tx.execute(
        f"UPDATE user_words SET audio_id = NULL WHERE list_id = {list_id};"
    )
    tx.execute(
        f"UPDATE user_lists SET is_loaded = NULL WHERE id = {list_id};"
    )
    tx.commit()


def reset_words_learning(list_id):
    base.check_IAM()
    base.pool.execute_with_retries(f"""
        UPDATE user_words SET learned = FALSE WHERE list_id = {list_id};
    """)


@exception()
def set_is_learn(id):
    base.check_IAM()
    query = f"""
        UPDATE user_words SET learned = TRUE WHERE id = {id};
    """
    base.pool.execute_with_retries(query)


def select_all_audio():
    base.check_IAM()
    return base.pool.execute_with_retries(
        f"SELECT audio_id FROM user_words WHERE audio_id NOTNULL;",
    )[0].rows
