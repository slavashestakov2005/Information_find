import informationfind as info
def main():
    filenames = [r'corpus\pg135.txt', r'corpus\pg76.txt', r'corpus\pg5200.txt']
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


try:
    main()
except Exception as e:
    print(e)