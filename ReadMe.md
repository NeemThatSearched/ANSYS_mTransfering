Наша база(тк пишем мы надеюсь на питоне):

pip install ansys-dpf-core


В main пока что програмный тест, потом надо будет написать миниприложуху с выбором файла и отображением инфы и тд и тп
План у нас примерно следующий:

1. Сбор данных из проектов ансиса в текст(json)
2. Форматировка в проекты проги какой то там от бауманки
3. Граф дизайн приложухи, чтобы запускать через екзешник, а не через хуйню каку то(консоль)

В main.py мы будем прописывать приложуху и взаимодействие между проектами
В module_ansys.py мы прописываем функции взаимодействия с ансисом(капитан очевидность)
В module_bmstu.py очевидно пишем че то там к бауманской проге
Ну а materials.json пока что будет использоваться для записи свойств материалов, потому что я думаю нам обоим лень будет искать+качать бауманскую всю эту хуйню.


ВАЖНАЯ ХУЙНЯ: АНСИС НАДО УСТАНОВИТЬ, НЕТО НИЧЕ ОКАЗЫВАЕТСЯ РАБОТАТ НЕ БУДЕТ, там есть халявная версия для студентов, вопрос лишь какая нам нужна