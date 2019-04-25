import MultipleQuestionsChecker

if __name__ == '__main__':
    question_checker = MultipleQuestionsChecker.Checker("D:\\Facultate\\Facultate_Anul_III_Semestrul_II\\IILN"
                                                        "\\Laboratories\\Introduction-to-Natural-Language-Engineering"
                                                        "\\Validator\\test_folder\\questions.json",
                                                        "D:\\Facultate\\Facultate_Anul_III_Semestrul_II\\IILN"
                                                        "\\Laboratories\\Introduction-to-Natural-Language-Engineering"
                                                        "\\Validator\\test_folder\\documents")

    try:
        question_checker.validate_data()
    except Exception as e:
        print(str(e))
