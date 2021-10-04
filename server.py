from app import create_app, socketio 
from app.models import Money

app = create_app('development')

@socketio.on('send_data')
def receive_data(data):
    if not data['data']:
        socketio.emit('message', 'error integer')
        return False 

    if data['type'] == 'income':
        mon = Money(income=data['data'])
        print(data)
        mon.save()
        print(Money.query.all())
        socketio.emit('message','income added')
    elif data['type'] == 'outcome':
        mon = Money(outcome=data['data'])
        mon.save()
        socketio.emit('message','data added')
    
    
if __name__ == '__main__':
    socketio.run(app, debug=True)

