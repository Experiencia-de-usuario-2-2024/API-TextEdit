from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def analyze_sentiment(self):
        response = self.client.post("/sentiment", json={"text": "Estoy muy feliz hoy."})
        print(f"Sentiment response: {response.json()}")

    @task(1)
    def analyze_emotions(self):
        response = self.client.post("/emotions", json={"texto": "Me siento un poco triste."})
        print(f"Emotion response: {response.json()}")

    @task(1)
    def classify_text(self):
        response = self.client.post("/classify", json={"texto": "No estoy seguro de lo que estás diciendo."})
        print(f"Classification response: {response.json()}")

    @task(1)
    def analyze_disagreement(self):
        response = self.client.post("/desacuerdos", json={"texto": "Creo que la tierra es plana y otros dicen que es redonda."})
        print(f"Disagreement response: {response.json()}")

    @task(1)
    def create_commitment(self):
        response = self.client.post("/compromiso", json={"texto": "Juan va a enviar el informe mañana en la oficina."})
        print(f"Commitment response: {response.json()}")

    @task(1)
    def redact_commitment(self):
        response = self.client.post("/redactar-compromiso", json={"texto": "Voy a entregar el proyecto el viernes en la sala de juntas."})
        print(f"Redacted commitment response: {response.json()}")

class MyUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

