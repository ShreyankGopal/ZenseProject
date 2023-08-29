import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QTAgg')
from io import BytesIO
import base64

from .models import Quiz, Results  # Make sure to import the appropriate models


def get_graph(username):
    quizzes = Quiz.objects.all()
    results = Results.objects.filter(user=username)
    dict_items = {}

    for q in quizzes:
        for res in results:
            if res.quiz == q:
                dict_items[q.topic] = res.totalmarks

    x = list(dict_items.keys())
    y = list(dict_items.values())

    plt.bar(x, y)
    plt.xlabel("Quizzes")  # Set the x-axis label
    plt.ylabel("Your marks for each quiz")
    plt.title("Quiz Performance")

    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

    plt.tight_layout()  # Adjust layout for better spacing
    buffer=BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64
    
def get_piechart(username):
    quizzes = Quiz.objects.all()
    results = Results.objects.filter(user=username)
    dict_items = {}

    for q in quizzes:
        for res in results:
            if res.quiz == q:
                dict_items[q.topic] = res.totalmarks
   
    x = list(dict_items.keys())
    y = list(dict_items.values())
    plt.style.use('_mpl-gallery-nogrid')
    plt.figure(figsize=(8, 6))
    plt.clf()
    wedges=plt.pie(y,labels=x,radius=3, center=(4, 4),autopct="%1.1f%%",
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
    plt.legend(wedges, x, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    buffer=BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

# Call the function with a username

