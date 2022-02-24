from scipy import spatial
from scipy import stats
from statistics import mean
import math
import numpy as np

def training_matrix():#Reads training matrix and makes the data, 200*1000
        train_people = []
        fp_train = open("train.txt").read().splitlines()

        for l in fp_train:

                train_tuple = []

                for i in l.split():
                        train_tuple.append(int(i))

                train_people.append(train_tuple)
        return train_people

def testing_matrix(fp_test, k):#fp_test is the filename, rated is the number of movies the users have rated
        #This function will return the list of stuff that we need to write to the file
        training_list = training_matrix()#200*1000, training data
        test_list = testing_read(fp_test)


        iuf = [0,]*1000#For all 1000 movies
#Need numbers for IUF
        for i in range(len(training_list)):#Runs 200 times
                for j in range(len(training_list[i])):#Runs 1000 times for every user
                        if(training_list[i-1][j-1] != 0):
                                iuf[j] += 1
        for i in range(len(iuf)):
                iuf[i] = math.log( ( 200 / (iuf[i]+1) ) )
                

#Need to generate the list of users and movie rankings to do pearson similarity on, will make it look like training matrix
        test_matrix = []#Matrix just like the training matrix, 200*1000
        test_tuple = [0]*1000#For all movies
        return_matrix = []#Matrix value to return
        prev_user = test_list[0][0]
        counter = 0
        
        for i in test_list:
                test_tuple[i[1]-1] = i[2]
                if(prev_user != i[0]):
                        test_matrix.append(test_tuple)
                        test_tuple = [0]*1000
                        counter += 1
                prev_user = i[0]
        test_matrix.append(test_tuple)#Since the for loop leaves one set out for some reason?
                               
                
#Need to compare the ratings of our users with the training matrix
        correlations = []#Weights for all of the users in the training matrix compared to our testing users, 100 entries
                        #Each index in weights has 200 entries for the similarity to each other user
        top_u = []#Temp tuple to append stuff
        count = 0#Count of all users that have rated MID
        
        for user in test_matrix:#For each user
                for t in range(len(training_list)):#And each user in the testing list
                        tup = ( abs(stats.pearsonr(user, training_list[t-1])[0]), t-1)
                        top_u.append(tup)#Correlation between u and t
                correlations.append(top_u)
                top_u = []

#K neighbors
        for i in range(len(correlations)):
                correlations[i].sort(reverse = True)

#Calculate the means for all of the users given rankings
        means = []
        mean_u = []

        for u in test_list:
                if(u[2] != 0):#If there's a given ranking
                        mean_u.append(u[2])
                if(u[2] == 0 and len(mean_u) != 0):#If we've passed the given rankings
                        means.append(mean(mean_u))
                        mean_u = []

#Now need to get the ratings for all of the 0 rankings in test_list
        base = test_list[0][0]+1
        correl_sum = 0
        for u in test_list:#For all of our testing users
                #print(u[0])    
                if(u[2] == 0):#If we need to get a rating for u[1] = MID
                        #print(weights[u[0]-200])
                        for i in range(k):#For every elt in that users array, need to add their ranking for MID*weight
                                #print(u[0]-200, i, u[1])#Print UID-200, round thru loop, MID
                                if(training_list[i-1][u[1]-1] != 0):
                                        ave_i = mean(training_list[i-1])#Mean of train_users rankings
                                        top = correlations[(u[0]-base)][i-1][0] * (training_list[i-1][u[1]-1] - ave_i) * iuf[u[1]-1]
                                        top_u.append(abs(top))
                                        count = count + top

                        if(count != 0):
                                #print(correl_u)
                                sum_u = sum(top_u)
                                top_u = []
                                for i in range(k):
                                        if (correl_sum == 0):
                                                correl_sum = sum(np.sum(correlations[(u[0]-base)], axis=0))
                                        else:
                                                break
                                correl_u = []
                                #print(u, sum_u)
                                u[2] = (sum_u/correl_sum) + means[(u[0]-base)]
                                count = 0
                                correl_sum = 0
                                return_matrix.append(u)
                        else:
                                u[2] = 3
                                return_matrix.append(u)
        return return_matrix
                        


def testing_read(fp_test):#Pull in all of the data from our test file
        
        with open(fp_test) as fp:
                test = []
                for l in fp:
                        test.append([int(i) for i in l.split()])
        return test

def main():
        fp = open("IUF20.txt", "w")
        train_matrix = training_matrix()
        result_matrix = testing_matrix("testing20.txt", 5)

#My code into a new text file
        for i in range(len(result_matrix)):
                fp.write(str(result_matrix[i-1][0]))
                fp.write(" ")
                fp.write(str(result_matrix[i-1][1]))
                fp.write(" ")
                if(result_matrix[i-1][2] > 5):
                        result_matrix[i-1][2] = 5
                elif(result_matrix[i-1][2] < 1):
                        result_matrix[i-1][2] = 1
                fp.write(str(int(round(result_matrix[i-1][2]))))
                fp.write("\n")


if __name__ == "__main__":
        main()
