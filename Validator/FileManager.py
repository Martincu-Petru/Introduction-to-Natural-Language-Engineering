import os


class FolderFinder:

    @staticmethod
    def check_if_exists(dirname, files_location):
        for root, dirs, files in os.walk(files_location):
            if dirname in dirs:
                return os.path.join(root, dirname)

        return False
