import os


class FolderFinder:

    @staticmethod
    def check_if_exists(dirname, files_location):
        for root, dirs, files in os.walk(files_location):
            if dirname in dirs:
                return os.path.join(root, dirname)

        return False

    @staticmethod
    def get_files_from_directory(directory):
        return os.listdir(directory)

    @staticmethod
    def check_file_json_format(filename):
        if not filename.endswith(".json"):
            raise Exception("invalid document type found inside folder. (" + os.path.splitext(filename)[1] +
                            " instead of .JSON for document " + os.path.splitext(filename)[0] + ")")
