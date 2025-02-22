def message_handler(user_act=None, message=None):
    if user_act == 'start':
        return ('Привет!💙\nЯ чат-бот вашего любимого заведения. Рад познакомиться с вами сегодня.',
                'Давайте вместе организуем ваше идеальное пребывание в нашем уютном хостеле всего за 4⃣ шага.',
                '1⃣ Для начала, скажите мне, пожалуйста, в какие даты вы планируете у нас остановиться?\n\n'
                '📆 Укажите даты в формате:\n\n❗дд.мм.гг – дд.мм.гг❗\n\n, одним сообщением, где первая дата – '
                'предпочитаемая для заезда, вторая – для выезда.')

    if user_act == 'dates':
        return ('2⃣ Отлично, сколько гостей будет в вашей компании? 👔\n\n❗Необходимо указать только число❗\n\n'
                'Просим обратить ваше внимание, что проживать в нашем заведении могут только дети возрастом '
                'начиная 📌от 14 лет📌 и старше.')

    if user_act == 'dates_mistake':
        return ('Ваше сообщение не соответствует формату. Пожалуйста, пришлите даты еще раз, придерживаясь '
                'формата:\n\nдд.мм.гг – дд.мм.гг')

    if user_act == 'persons':
        return ('3⃣ Скажите, пожалуйста, соотношение мужчин и женщин в вашей группе?\n\n👫 Укажите в формате:\n\n'
                '❗Число мужчин / число женщин❗\n\n, например, 4 мужчин/2 женщин. Если персон какого-то пола не '
                'заезжает, укажите 0.')

    if user_act == 'persons_mistake':
        return ('Ваше сообщение не соответствует формату. Пожалуйста, пришлите количество человек еще раз, '
                'придерживаясь формата:\n\nТолько число.')

    if user_act == 'genders':
        return ('4⃣ Есть ли у вас предпочтения в выборе комнаты? Предлагаем Вам ознакомиться со списком и прайсом.\n\n'
                '🏡 Выбранные Вами желаемые комнаты укажите в формате, ❗который указан в списке❗\n\n, например, 4-ех '
                'женский. Напишите, "желаемых комнат нет", если предпочтений не имеется.')

    if user_act == 'genders_mistake':
        return ('Ваше сообщение не соответствует формату. Пожалуйста, пришлите соотношение человек еще раз, '
                'придерживаясь формата:\n\nЧисло мужчин / Число женщин.')

    if user_act == 'rooms':
        return ('Спасибо, я внимательно все записал. Проверьте, пожалуйста, '
                'правильность введенных данных:\n\n'
                '📆 Даты: {}\n'
                '👔 Количество персон: {}\n'
                '👫 Мужчины и женщины: {}\n'
                '🏡 Комнаты: {}\n')

    if message == '📆 изменить даты':
        return 'Хорошо, отправьте верные даты, соблюдая данный формат:\n\n❗дд.мм.гг – дд.мм.гг❗'

    if message == '👔 изменить число персон':
        return 'Хорошо, отправьте число человек, которое должно заехать.'

    if message == '👫 изменить соотношение':
        return 'Хорошо, отправьте верное соотношение, соблюдая данный формат:\n\n❗Число мужчин / число женщин❗'

    if message == '🏡 изменить комнаты':
        return ('Хорошо, отправьте верную комнату (верные комнаты), в которой Вы бы предпочли проживать в '
                'нашем заведении.')

    if user_act == 'all_right':
        return ('Прежде чем отправить заявку на проживание в нашем заведении, мы хотели бы обратить ваше внимание на '
                'важные правила, которые необходимо соблюдать во время вашего пребывания.\n\n✅ Пожалуйста, '
                'ознакомьтесь с полным списком правил проживания и подтвердите свое согласие.',
                '🌎 ПРАВИЛА ВНУТРЕННЕГО РАСПОРЯДКА «НАЗВАНИЕ ЗАВЕДЕНИЯ» 🌎\n\n1⃣  Чистота и порядок!\n• Убирать и '
                'мыть за собой посуду и кухонные принадлежности;\n• Поддерживать порядок в комнатах;\n• Не оставлять '
                'свои личные вещи в местах общего пользования;\n • Не хранить и не употреблять продукты питания в '
                'комнатах.\n2⃣  Уважение!\n• Соблюдать режим тишины с 24:00 до 07:00;\n• Использовать стиральную '
                'машину с 09:00 до 21:00.\n\n🚫 КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО 🚫\n• Курение, употребление и распространение '
                'наркотических веществ, употребление алкоголя - выселение;\n• Проявление агрессии и всех признаков '
                'насилия к окружающим;\n• Хранение взрывчатых и легко воспламеняющихся веществ, оружия, наркотиков, '
                'ртути, химических и радиоактивных веществ;\n• Приглашение на территорию хостела посторонних гостей, '
                'продажа своих услуг или товаров.\n\n⏰ ПРАВИЛА ЗАЕЗДА И ВЫЕЗДА ⏰\n• Заезд возможен после 13:00, '
                'выезд в 12:00;\n• Раннее заселение или поздний выезд возможны✅, при наличии свободных мест. Стоит '
                'учесть, что услуга оплачивается отдельно за дополнительную плату;\n• В случае выезда раньше '
                'оплаченной даты, администрация не возвращает денежные средства, внесенные за проживание;\n• Гость '
                'обязан заранее предупредить о продлении брони. В случае неоплаты до 12:00, администрация вправе '
                'заселить другого гостя.\n\nНам будет очень жаль, но ради душевного спокойствия наших гостей и, '
                'конечно, персонала хостела, администрация оставляет за собой право на выселение любого проживающего '
                'в случае нарушения общественного порядка и правил проживания, без возврата денежных средств.')

    if message == 'прочитал(а) и принимаю правила':
        return ('Я отправил эту информацию своим коллегам. Она поможет им подобрать для вас самые комфортные '
                'условия проживания.',
                'Время ожидания ответа на заявку:\n\n⏰ Варьируется от 2 до 15 минут в дневное время.\n\nПосле, '
                'оператор подключится в чат, чтобы начать организацию вашей поездки.')

    if message == 'позвать оператора':
        return 'Направил Вашу просьбу коллегам, скоро оператор подключится в чат ⏰'
