def form_unread_message(len_msg):
    last_num = len_msg % 10
    msg_sending = "сообщений"
    news_msg = "новых"
    if last_num == 1 and len_msg != 11:
       news_msg = "новое"
       msg_sending = "сообщение"
    elif last_num in [2, 3, 4]:
      msg_sending = "сообщения"
    return news_msg, msg_sending