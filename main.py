from flask import Flask, request, render_template
from flask import Response
from flask_cors import cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
from predictFromModel import prediction

app = Flask(__name__)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('login.html')


@app.route("/", methods=['POST'])
@cross_origin()
def predictRouteClient():
    if request.method == 'POST':
        try:
            path = request.form['Prediction Path']
            pred_val = pred_validation(path)  # object initialization
            pred_val.prediction_validation()  # calling the prediction_validation function
            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()

        except ValueError:
            return Response("Error Occurred! %s" % ValueError)
        except KeyError:
            return Response("Error Occurred! %s" % KeyError)
        except Exception as e:
            return Response("Error Occurred! %s" % e)

    return render_template('results.html')
@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:

        path = request.json['Prediction Path']
        train_valObj = train_validation(path)  # object initialization
        train_valObj.train_validation()  # calling the training_validation function
        trainModelObj = trainModel()  # object initialization
        trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")


if __name__ == "__main__":
    app.run(debug=True)

