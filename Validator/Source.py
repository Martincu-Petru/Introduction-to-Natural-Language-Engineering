import QuestionChecker

if __name__ == '__main__':
    question_checker = QuestionChecker.QuestionChecker()
    try:
        question_checker.check_question_valid(open("test_question.json").read())
    except Exception as e:
        print("Problem ancountered: " + str(e))
    else:
        print("Question is valid!")
