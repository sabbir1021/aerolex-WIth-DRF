SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@gmail.com
SUPERUSER_PASSWORD=admin
AGENT_NAME='Aerolex UK'
PHONE_NUMBER='01758514752'
COUNTRY='uk'
EMAIL='admin@gmail.com'
CURRENCY='pound'
PASSWORD='sabbireti1021'
UNIQUE_IDENTIFIER='147852369'
PAYMENT_POLICY='credit'
AGENT_TYPE_USER='country_user'
AGENT_TYPE='country_agent'

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py shell -c "from agent.models import Agent; agent = Agent.objects.create(name='$AGENT_NAME', phone_number='$PHONE_NUMBER', country='$COUNTRY', email='$EMAIL',currency='$CURRENCY',unique_identifier='$UNIQUE_IDENTIFIER', payment_policy='$PAYMENT_POLICY', agent_type='$AGENT_TYPE');from django.contrib.auth import get_user_model; User= get_user_model(); user = User.objects.create_superuser(email='$EMAIL', password='$PASSWORD',agent=agent,user_type='$AGENT_TYPE_USER',phone_number='$PHONE_NUMBER');"
