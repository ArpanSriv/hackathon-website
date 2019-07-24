class ProgressUtils:
    __instance = None

    progress = {
        'some_random_id': '20',
    }

    @staticmethod
    def get_instance():
        if ProgressUtils.__instance is None:
            ProgressUtils()
        return ProgressUtils.__instance

    def __init__(self):
        if ProgressUtils.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProgressUtils.__instance = self

    ##### CRUD START HERE #####

    @staticmethod
    def update_progress(progress_id, new_progress):
        if progress_id not in ProgressUtils.progress:
            raise Exception("Progress not initialized.")

        ProgressUtils.progress[progress_id] = new_progress

        return ProgressUtils.progress[progress_id]

    @staticmethod
    def init_progress(progress_id):
        print("Initializing Progress....")

        if progress_id not in ProgressUtils.progress:
            ProgressUtils.progress[progress_id] = 0

        else:
            raise Exception("Progress already initialized.")

        return ProgressUtils.progress[progress_id]

    @staticmethod
    def get_progress(progress_id):
        if progress_id not in ProgressUtils.progress:
            print("Progress not initialized.")
            return 100

        else:
            # print("RETURNING PROGRESS : " + ProgressUtils.progress[progress_id])
            return ProgressUtils.progress[progress_id]

    @staticmethod
    def remove_progress(progress_id):
        if progress_id in ProgressUtils.progress:
            del ProgressUtils.progress[progress_id]

    def set_error_progress(self, progress_id):
        if progress_id in ProgressUtils.progress:
            ProgressUtils.progress[progress_id] = -1
