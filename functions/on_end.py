from foundation import db_connection,history_cursor,db_history
async def on_end(db):
    try :
        db_connection.commit()
        db_connection.close()

        db_history.commit()
        db_history.close()
        print('-----------------------------\nConnection closed...\nBot is off')
    except Exception as ex:
        print('Something wrong with connection close...\n',ex)