import matplotlib.pyplot as plt
from.models import Results,Quiz
import io
import base64
def get_graph(username):
    quiz=Quiz.objects.all()
    results=Results.objects.filter(user=username)
    dict_items={}
    for q in quiz:
        for res in results:
            if res.quiz==q:
                dict_items['f{q.topic}']=res.totalmarks
    x=list(dict_items.keys())
    y=list(dict_items.values())
    plt.bar(x, y)
    plt.xticks("Quizzes")
    plt.ylabel("Your marks for each quiz")
    plt.title("Statistics")
    
    plt.show()
    

