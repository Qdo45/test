
import pandas as pd
from datetime import timedelta, datetime
import xml.etree.cElementTree as ET
from flask import Flask, make_response, jsonify, request

def sort_date_end(date):
	return date.get('date_end')
def sort_date_start(date):
	return date.get('date_start')

app = Flask(__name__)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/openfile')

def openfile():
	try:
		filename = request.files['file']
		start_date = request.form.get('start_date', None)
		end_date = request.form.get('end_date', None)
		if (start_date is None and end_date is not None   )   or  (end_date is None and start_date is not None   ):
			persons_days={'error': 'Задайте дату начала и окончания или не передавайте ключи start_date и end_date'}
			return  persons_days
		person = request.form.get('person',None)
		persons = []
		persons_finish = []
		persons_score = []
		persons_days = []
		file = request.files['file']
		if ('file' not in request.files) or (file.filename == ''):
			persons_days={'error': 'Файл не найден '}
			return  persons_days

		tree = ET.ElementTree(file=filename)
		root = tree.getroot()
		dlina = len(root)
		for child_of_root in range(0,dlina):
			date_start = pd.to_datetime(root[child_of_root][0].text , format='%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y')
			time_start = pd.to_datetime(root[child_of_root][0].text).strftime('%H:%M:%S')
			date_end = pd.to_datetime(root[child_of_root][1].text, format='%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y')
			time_end = pd.to_datetime(root[child_of_root][1].text).strftime('%H:%M:%S')
			persons += [{
				'person': root[child_of_root].attrib['full_name'],
				'date_start': date_start,
				'time_start': time_start,
				'date_end': date_end,
				'time_end': time_end
			}]

		if ((start_date is None) and (end_date is None)):
			persons.sort(key=sort_date_end)
			end_date=persons[(persons.__len__())-1]['date_end']
			persons.sort(key=sort_date_start)
			start_date = persons[0]['date_start']
			if (start_date >end_date ):
				persons_days={'error': 'Дата начала больше даты окончания'}
				return  persons_days

		for kk in range(0, persons.__len__()):
			if ((pd.to_datetime(persons[kk]['date_start'], format='%d-%m-%Y').strftime('%d-%m-%Y')) > (pd.to_datetime(end_date, format='%d-%m-%Y').strftime('%d-%m-%Y'))):
				break
			start_date = pd.to_datetime(persons[kk]['date_start'], format='%d-%m-%Y').strftime('%d-%m-%Y')
			if ( pd.to_datetime(persons[kk]['date_start'], format='%d-%m-%Y').strftime('%d-%m-%Y') == pd.to_datetime(start_date, format='%d-%m-%Y').strftime('%d-%m-%Y')):
				if (persons[kk]['date_end'] != persons[kk]['date_start']):
					score_date_start = pd.to_datetime(start_date, format='%d-%m-%Y')
					score_date_rabota = pd.to_datetime(persons[kk]['date_end'], format='%d-%m-%Y') - pd.to_datetime(persons[kk]['date_start'],format='%d-%m-%Y')
					score_date_rabota = score_date_rabota.days + 1
					for vv in range(0, score_date_rabota):
						if vv == 0:
							score_for_days_hour =  datetime.strptime("23:00:00","%H:%M:%S") -  datetime.strptime(persons[kk]['time_start'],"%H:%M:%S")
							score_for_days_hour = score_for_days_hour + timedelta(hours=1)
							score_for_days_hour = pd.to_datetime(score_for_days_hour, format='%H:%M:%S').strftime('%H:%M:%S')
						else:
							if vv == (score_date_rabota-1):
								score_for_days_hour = time_end
							else:
								score_for_days_hour = "24:00:00"
						persons_finish += [
									{ 'person': persons[kk]['person'],
									  'date_start': pd.to_datetime(score_date_start, format='%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y'),
									  'score_date_sotrudnik':  score_for_days_hour
									}]
						if ( pd.to_datetime(score_date_start, format='%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y') ) == ( pd.to_datetime(end_date, format='%d-%m-%Y').strftime('%d-%m-%Y') ) :
							break
						score_date_start = pd.to_datetime(score_date_start, format='%d-%m-%Y') + timedelta(1)

				else:
					score_for_days_hour =  datetime.strptime(persons[kk]['time_end'],'%H:%M:%S')-datetime.strptime(persons[kk]['time_start'],'%H:%M:%S')
					persons_finish += [
							{'person': persons[kk]['person'],
							 'date_start': pd.to_datetime(start_date, format='%d-%m-%Y').strftime('%d-%m-%Y'),
							 'score_date_sotrudnik': pd.to_datetime(score_for_days_hour, format='%H:%M:%S').strftime('%H:%M:%S'),
							 }]


		score_date_start = pd.to_datetime(start_date, format='%d-%m-%Y')
		score_date_rabota = pd.to_datetime(end_date, format='%d-%m-%Y') - pd.to_datetime(start_date, format='%d-%m-%Y')
		score_date_rabota = score_date_rabota.days

		for tt in range(0,score_date_rabota+1):
			score_for_days_hour = 0
			for kk in range(0, persons_finish.__len__()):
				if (pd.to_datetime(persons_finish[kk]['date_start'], format='%d-%m-%Y').strftime('%d-%m-%Y') == pd.to_datetime(score_date_start, format='%d-%m-%Y').strftime('%d-%m-%Y')):
					if persons_finish[kk]['score_date_sotrudnik'] == "24:00:00":
						score_for_days_hour = 86400 + score_for_days_hour
					else:
						z = persons_finish[kk]['score_date_sotrudnik']
						date = datetime.strptime(z, "%H:%M:%S")
						z2 = date.hour * 60 * 60 + date.minute *60 + date.second
						score_for_days_hour = z2 + score_for_days_hour
			persons_score += [
					{'date_start': pd.to_datetime(score_date_start, format='%d-%m-%Y').strftime('%d-%m-%Y'),
					 'score_date_sotrudnik': score_for_days_hour
					 }]
			score_date_start = pd.to_datetime(score_date_start, format='%d-%m-%Y') + timedelta(1)

		if (person is None) or (person =="False") or (person!='True'):
			for kk in range(0, persons_score.__len__()):
				seconds = persons_score[kk]['score_date_sotrudnik']
				days = str (seconds//86400)
				hours = str((seconds % 86400 ) // 3600)
				minut = str(((seconds % 86400 ) % 3600) // 60)
				second = str(((seconds % 86400 ) % 3600) % 60)
				if int(days)<10:
					days='0'+str(days)
				if int(hours) < 10:
					hours = '0' + str(hours)
				if int(minut) < 10:
					minut = '0' + str(minut)
				if int(second) < 10:
					second = '0' + str(second)
				persons_days+= [{"Дата":persons_score[kk]['date_start'],"Кол-во часов в эту дату":"Дней: "+days+" Чесов: "+hours+" Минут: "+minut+" Секунд: "+second}]
				# Тут надо перевести секунды в дни часы секунды минуты
		if person =="True":
			persons_finish.sort(key=sort_date_start)
			score_date_start = pd.to_datetime(start_date, format='%d-%m-%Y')
			for tt in range(0, score_date_rabota + 1):
				persons_kesh = []
				for kk in range(0, persons_finish.__len__()):

					if (pd.to_datetime(persons_finish[kk]['date_start'], format='%d-%m-%Y').strftime('%d-%m-%Y') == pd.to_datetime(score_date_start, format='%d-%m-%Y').strftime('%d-%m-%Y')):
						persons_kesh+= [{"Работник":persons_finish[kk]['person'],"Время работы": persons_finish[kk]['score_date_sotrudnik']}]
				persons_days +=  [{"Дата":pd.to_datetime(score_date_start, format='%d-%m-%Y').strftime('%d-%m-%Y'),"Работники":persons_kesh}]
				score_date_start = pd.to_datetime(score_date_start, format='%d-%m-%Y') + timedelta(1)

	except :
		persons_days = {'error': 'Ошибка с датами'}

	return jsonify( persons_days )


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')