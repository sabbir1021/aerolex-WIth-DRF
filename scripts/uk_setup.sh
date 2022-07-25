
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py shell -c "from agent.models import Agent; agent = Agent.objects.create(name='Admin', phone_number='01758514752', country='uk', email='admin@gmail.com',currency='pound');from django.contrib.auth import get_user_model; User= get_user_model(); user = User.objects.create_superuser(email='admin@gmail.com', password='sabbireti1021',agent=agent);"
