import PySimpleGUI as sg
import informationfind as info


names = ['1.  У зелёной грязной лужи', '2.  Песня бывшего простого школьника', '3.  Почему же я физиком не стал', '4.  Реет как знамя над “Интегралом”',
'5.  Светило в небе солнышко', '6.  Виноватый ли я', '7.  Господа зондера', '8.  Непрощальная песня о КЛШ', '9.  Друг мой', '10. Старые раны', '11. Гоп-стоп',
'12. Песня про КЛШ', '13. 25 августа 1985 года', '14. Едет крыша', '15. Песня ветеранов', '16. Песня зондеров', '17. Когда воротимся мы в Школу',
'18. Бродит август по лету', '19. Приветственная песня КЛШ', '20. Песенка зондеров, сочинённая зондерами в 1988 году', '21. Песенка зондеров, сочинённая зондерами в 1990 году',
'22. Господа зондера', '23. Ничего на свете лучше нету', '24. Посвящение', '25. Воспоминание о будущем лете', '26. Что тебе снится, Летняя Школа',
'27. Песня Московской Коллаборации о Красноярской Летней Школе', '28. Слава Биохиму!', '29. День Физмата', '30. КЛШ', '31. Расцветай', '32. Медиана (Песня вожатых команды сигма)',
'33. Зондер (Песенка зондера)', '34. Фанат работы над собой', '35. Канкебан, стойка короля, железный палец, КЛШ', '36. Я сотрудник', '37. От сосны до сосны',
'38. 10 лет в КЛШ', '39. Летнешкольница', '40. Общепит', '41. Мегавольт', '42. Физматик', '43. Блюз старого человека', '44. Песня про директора', '45. Так это же Садовский',
'46. Космический Ламзин', '47. Момент на массу', '48. У нас была Школа', '49. Юбилейная', '50. Атланты КЛШ', '51. Ты, Диана, пожалуйста, нас прости', '0.  Благодарности']


filenames = []
for pos in range(len(names)):
    file = names[pos]
    filenames.append('Песни КЛШ\\' + file + '.txt')
    names[pos] = file[4:]
test = info.InformationFind(filenames)


def main_window():
    # sg.ChangeLookAndFeel('GreenTan')
    layout = [
        [sg.Text('“Что ни слово — то песня или инфопоиск”', size=(37, 1), justification='center', font=("Helvetica", 20), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Запишите поисковый запрос', size=(55, 1), justification='center', font=("Helvetica", 15))],
        [sg.InputText('', size=(85, 1))],
        [sg.Submit('Поиск', tooltip='Нажмите для поиска'), sg.Cancel('Закрыть', tooltip='Нажмите чтобы закрыть программу')]]
    window = sg.Window('“Что ни слово — то песня или инфопоиск”', layout, default_element_size=(40, 1), grab_anywhere=False)
    while True:
        event, values = window.read()
        if event != 'Поиск' or event == 'Поиск' and values[0] != '':
            break
    window.close()
    if event == 'Поиск':
        find_window(values[0])


def find_window(text):
    result = test.files_with_text(text, info.PHARSE_QUERY)
    layout = [
        [sg.Text('Запрос: ' + text, size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)]]
    for file in result:
        if text.lower() == 'инфопоиск' and names[filenames.index(file)] == names[-1] or text.lower() != 'инфопоиск' and names[filenames.index(file)] != names[-1]:
            layout.append([sg.Submit(names[filenames.index(file)])])
        if len(layout) > 10:
            break
    if len(layout) == 1:
        layout.append([sg.Text('По вашему запросу ничего не найдено (((', size=(60, 1), justification='center', font=("Helvetica", 12))])
    layout.append([sg.Submit('Поиск', tooltip='Нажмите чтобы вернуться к поиску'), sg.Cancel('Закрыть', tooltip='Нажмите чтобы закрыть программу')])
    window = sg.Window('Запрос: ' + text, layout, default_element_size=(40, 1), grab_anywhere=False)
    while True:
        event, values = window.read()
        if event in names:
            open_window(event)
        elif event == 'Поиск':
            window.close()
            main_window()
            break
        else:
            window.close()
            break


def open_window(file):
    with open(filenames[names.index(file)], 'r') as fd:
        text = fd.read()
    out_text = [text[0:900], text[900:1800], text[1800:]]
    layout0 = [[sg.Text(out_text[0], justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)]]
    layout1 = [[sg.Text(out_text[1], justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)]]
    layout2 = [[sg.Text(out_text[2], justification='center', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)]]
    if file == names[-1]:
        layout0 = [[sg.Text(out_text[0], justification='left', font=("Helvetica", 10), relief=sg.RELIEF_RIDGE)]]
    if out_text[1] != '':
        window = sg.Window(file + ' (1)', layout0, default_element_size=(40, 1), grab_anywhere=False)
        window.read()
        window.close()
        window = sg.Window(file + ' (2)', layout1, default_element_size=(40, 1), grab_anywhere=False)
        window.read()
        window.close()
        if out_text[2] != '':
            window = sg.Window(file + ' (3)', layout2, default_element_size=(40, 1), grab_anywhere=False)
            window.read()
            window.close()
    else:
        window = sg.Window(file, layout0, default_element_size=(40, 1), grab_anywhere=False)
        window.read()
        window.close()


try:
    main_window()
except Exception as e:
    print(e)
