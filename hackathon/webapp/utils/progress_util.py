
progress = {
    'some_random_id': '20',
}


def update_progress(progress_id, new_progress):
    if progress_id not in progress:
        raise Exception("Progress not initialized.")

    progress[progress_id] = new_progress

    return progress[progress_id]


def init_progress(progress_id):
    if progress_id not in progress:
        progress[progress_id] = 0

    else:
        raise Exception("Progress already initialized.")

    return progress[progress_id]


def get_progress(progress_id):
    if progress_id not in progress:
        # print("Progress not initialized.")
        return 100

    else:
        return progress[progress_id]


def remove_progress(progress_id):
    if progress_id in progress:
        del progress[progress_id]