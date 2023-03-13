import numpy as np
from sklearn import linear_model
from evaluation_improvements.metric_distributions import *
from evaluation_improvements.metric_inverse import *
import random
from datetime import datetime
import uuid
from app import session
from database import *
from sqlalchemy import text

def executeText(query):
    try:
        response = session.execute(text(query)).mappings().all()

        formatted = [[v for v in r.values()] for r in response]

        return formatted
    except:
        return

def evaluation(projectID, evalType):
    # try:

    temp1 = "CREATE VIEW testview as select * from crosstab('select project_id, metric_id, metric_value from metric_assignment order by 1,2') as"
    temp2= ' ct("project_id" int, "metric0" real, "metric1" real, "metric2" real, "metric3" real, "metric4" real, "metric5" real, "metric6" real, "metric7" real, "metric8" real, "metric9" real, "metric10" real, "metric11" real, "metric12" real);'
    tempString = temp1+temp2

    executeText("DROP VIEW IF EXISTS testview CASCADE;")
    executeText(tempString)
    session.commit()

    record = executeText("SELECT * from testview;")
    tableData = np.array(record)

    #Index of current project
    inputProjectIndex = (np.where(tableData[:, 0] == projectID))[0][0]

    #Storing current project metrics
    testMetrics = tableData[inputProjectIndex][1:12]

    #Deleting row to train the model with other projects
    tableData = np.delete(tableData, inputProjectIndex, axis=0)

    X = tableData[:, [1,2,3,4,5,6,7,8,9,10,11]]
    y = tableData[:, 12]

    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    
    print()
    testArray = np.array(testMetrics).reshape(1,-1)
    linearRegression = regr.predict(testArray)[0]
    print(linearRegression)

    evalID = str(uuid.uuid4().fields[-1])[:6]
    currentTime = datetime.now()
    if (linearRegression<25):
        evalLabel = "Failing"
    elif (linearRegression<50):
        evalLabel = "At Risk"
    elif (linearRegression<75):
        evalLabel = "Showing Symptoms"
    else:
        evalLabel = "Successful"

    #Deleting pre-existing evaluation if present then storing current evaluation
    executeText("delete from metric_assignment where project_id={} and metric_id=11".format(projectID))
    executeText("insert into metric_assignment values('{}','{}','{}')".format(11,projectID,linearRegression))
    executeText("insert into project_evaluation values('{}','{}','{}','{}','{}','{}')".format(evalID, projectID, currentTime, evalType, evalLabel, linearRegression))
    session.commit()


    #Improvement Metrics Code
    data = MetricInverse()

    ideal_probability = min(linearRegression + 15, 100)
    prob_range = [max(0,ideal_probability-2.5), min(100, ideal_probability+2.5)]
    metric = [[0]*12 for i in range(5)]

    #Creating 5 project with ideal probability
    for x in range(5):
        arr = [random.uniform(prob_range[0],prob_range[1]) for _ in range(12)]
        
        metric[x][0] = data.TTR0_inverse(arr[0])
        metric[x][1] = data.CR1_inverse(arr[1])
        metric[x][2] = data.TS2_inverse(arr[2])
        metric[x][3] = data.M3_inverse(arr[3])
        metric[x][4] = data.SPI4_inverse(arr[4])
        metric[x][5] = data.CPI5_inverse(arr[5])
        metric[x][6] = data.CQ6_inverse(arr[6])
        metric[x][7] = data.CRF7_inverse(arr[7])
        metric[x][8] = data.DF8_inverse(arr[8])
        metric[x][9] = data.TSR9_inverse(arr[9])
        metric[x][10] = data.CC10_inverse(arr[10])

        tempReshape = np.array(metric[x][0:11]).reshape(1,-1)
        metric[x][11] = regr.predict(tempReshape)[0]

    Euclidean_distance = [0] * 5

    #Calculating euclidean distance between input project and the 5 created and choosing the closest
    for i in range(5):
        Euclidean_distance[i] = np.linalg.norm(np.array(testMetrics) - np.array(metric[i][0:11]))
    
    ideal_project_index = (Euclidean_distance.index(min(Euclidean_distance)))
    ideal_project = metric[ideal_project_index][0:11]

    #Calculating difference in each metric
    difference = [0]*11

    #Weights assigned to each metric based on importance to evaluation
    list_of_weights = [1.5,1,1,1,2,2,1.5,1,1,1.5,1]

    for i in range(11):
        difference[i] = ((ideal_project[i] - testMetrics[i]) / ideal_project[i])*100*list_of_weights[i]

    increasing_metrics = [1,3,4,5,6,7,8,9,10]
    decreasing_metrics = [0]

    for i in range(11):
        change = round(((ideal_project[i] - testMetrics[i])/testMetrics[i])*100,2)
        if change < 0 and increasing_metrics.count(i) == 0:
            executeText("insert into improvement_metrics values('{}','{}','{}','{}')".format(i, evalID, -1, round(ideal_project[i],2)))
        elif change > 0 and decreasing_metrics.count(i) == 0:
            executeText("insert into improvement_metrics values('{}','{}','{}','{}')".format(i, evalID, 1, round(ideal_project[i],2)))
        else:
            executeText("insert into improvement_metrics values('{}','{}','{}','{}')".format(i, evalID, 0, testMetrics[i]))
        session.commit()


    # except:
    #     print("Error while connecting to PostgreSQL")
