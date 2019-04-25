import SingleQuestionChecker
import FileManager
import json
import re
import os


question_id_regex = re.compile(r"(\d)-(\d+)")


class Checker:

    questions_location = None
    files_location = None
    single_question_checker = SingleQuestionChecker.Checker()
    file_manager = FileManager.FolderFinder()

    def __init__(self, questions_location, files_location):
        self.questions_location = questions_location
        self.files_location = files_location

    def validate_data(self):

        if not os.path.exists(self.questions_location):
            raise Exception("Invalid questions file location.")

        if not os.path.exists(self.files_location):
            raise Exception("Invalid documents location folder.")

        if not self.questions_location.endswith(".json"):
            raise Exception("Invalid question file format.")

        questions_json = json.loads(open(self.questions_location, "r").read())

        for key in questions_json.keys():

            try:
                try:
                    question = dict()
                    question[key] = questions_json[key]

                    subtask = question_id_regex.match(key).group(1)
                    document_folder = question_id_regex.match(key).group(2)

                    if not self.file_manager.check_if_exists(document_folder, self.files_location):
                        raise Exception("document with ID = "
                                        + str(document_folder)
                                        + ", subtask " + subtask
                                        + ", has no directory associated.")

                    self.single_question_checker.check_question_valid(json.dumps(question))

                    for file in self.file_manager.get_files_from_directory(os.path.join(self.files_location,
                                                                                        document_folder)):
                        try:
                            self.file_manager.check_file_json_format(file)
                        except Exception as e:
                            print("Problem encountered for question with ID = " + document_folder + ": " + str(e))

                except Exception as e:
                    raise e

            except Exception as e:
                print("Problem encountered: " + str(e))
