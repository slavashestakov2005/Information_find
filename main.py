import help
import informationfind as info


def main():
    help.start()
    # filenames = [r'corpus\pg135.txt', r'corpus\pg76.txt', r'corpus\pg5200.txt']
    filenames = [r'my_corpus\test3.txt', r'my_corpus\test.txt', r'my_corpus\test2.txt']
    test = info.InformationFind(filenames)
    typ = input()
    if typ == 'word':
        result = test.files_with_text(input())
    elif typ == 'or':
        result = test.files_with_text(input(), info.OR_QUERY)
    elif typ == 'and':
        result = test.files_with_text(input(), info.AND_QUERY)
    else:
        result = test.files_with_text(input(), info.PHARSE_QUERY)
    print(result)
    help.finish()


try:
    main()
except Exception as e:
    print(e)
