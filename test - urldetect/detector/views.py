from django.shortcuts import render
import numpy as np
from .create_feature import create
from django.http import HttpResponse
from .train import model_load
import matplotlib.pyplot as plt

def index(request):
    if request.method == 'POST':

        url = request.POST['web_url']
        print(url)
        if not url == "" or url == None:
            if "http://" in url or "https://" in url:
                print(url)
                featureset = create(url)
                if type(featureset) is list:
                    model = model_load('model.pickle')
                    prediction = model.predict_proba(np.array([featureset]))
                    print(prediction)
                    unsafe_pred = float(prediction[0][0] * 100)
                    safe_pred = float(prediction[0][1] * 100)
                    left = [1, 2]
                    height = [safe_pred,unsafe_pred]
                    tick_label = ['good', 'bad']
                    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green', 'red'])
                    plt.xlabel('x - axis')
                    plt.ylabel('y - axis')
                    plt.text(2.5, 80, 'Bad URL')
                    plt.text(2.5, 90, 'Good URL')
                    plt.axhline(y=90, color='orange', ls='--')
                    plt.axhline(y=80, color='red', ls='--')
                    plt.title('URL Behavior Graph(Prediction %)')
                    plt.show()


                    if safe_pred > 80 and safe_pred < 90:
                        print(safe_pred)
                        color = "orange"
                        msg = "This Website may be Suspecious"
                    elif safe_pred >= 90:
                        color = "green"
                        msg = "This website is safe with {}% chances ".format(int(safe_pred))
                    else:
                        color = "red"
                        msg = "This website is unsafe. report it or do not visit this site"
                    # unsafe_prob = prediction[0]
                    # safe_prob = prediction[1]

                    return render(request, 'detector/index.html',
                                  {'url': url, 'prediction': prediction[0], 'msg': msg, 'color': color})


            else:
                print(type(url))
                color = 'black'
                msg = "Please Enter a Valid Url with (HTTP/HTTPS) token"
                return render(request, 'detector/index.html', {'msg': msg, 'color': color})


        else:
            msg = "Please Enter Some url in Field"

            return render(request, 'detector/index.html', {'msg': msg})


    else:
        return render(request, 'detector/index.html')





