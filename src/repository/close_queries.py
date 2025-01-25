from repository import base


def select_audio_for_clearn(lists):
    base.check_IAM()
    queries = "\nUNION\n".join([
        f"""
            (SELECT id FROM user_words
            WHERE list_id = {id} AND audio_id NOTNULL
            LIMIT 3)
        """ for id in lists])

    query = f"""
        SELECT id, audio_id
        FROM user_words
        WHERE id NOT IN (
        {queries}
        )
    """
    return base.pool.execute_with_retries(query)[0].rows


def clear_audio_id(ids, lists):
    base.check_IAM()
    tx = base.session.transaction().begin()
    tx.execute(
        f"UPDATE user_words SET audio_id = NULL WHERE id IN {ids};"
    )
    tx.execute(
        f"UPDATE user_lists SET is_loaded = FALSE WHERE id IN {lists};"
    )
    tx.commit()
