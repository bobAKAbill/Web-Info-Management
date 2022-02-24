from scipy import spatial
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
#        #rated_list = []
#        #not_rated_list = []

#        for i in test_list:
#                if i[2] != 0:
#                        rated_list.append(i)#Adds [UID, MID, rating] to rated_list when rating != 0
#                else:
#                        not_rated_list.append(i)#Does above for rating == 0

#Need to generate the list of users and movie rankings to do cosine similarity on, will make it look like training matrix
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
        weights = []#Weights for all of the users in the training matrix compared to our testing users, 100 entries
                        #Each index in weights has 200 entries for the similarity to each other user
        weight_u = []#Temp tuple to append stuff
        count = 0#Count of all users that have rated MID
        
        for user in test_matrix:#For each user
                for t in range(len(training_list)):#And each user in the testing list
                        tup = (spatial.distance.cosine(user, training_list[t]), t)
                        weight_u.append(tup)#Cosine similarity
                weights.append(weight_u)
                weight_u = []
        #print(len(weights[0]))
        #print(len(weights))

#K nearest neighbors
        for i in range(len(weights)):
                weights[i].sort(reverse = True)

#Now need to get the ratings for all of the 0 rankings in test_list
        base = test_list[0][0]+1
        for u in test_list:#For all of our testing users
                #print(u[0])
                if(u[2] == 0):#If we need to get a rating for u[1] = MID
                        #print(weights[u[0]-200])
                        for i in range(k):#For every elt in that users array, need to add their ranking for MID*weight
                                #print(u[0]-200, i, u[1])#Print UID-200, round thru loop, MID
                                if(training_list[i][u[1]-1] != 0):
                                        weight = weights[(u[0]-base)][i][0]*training_list[i][u[1]-1]
                                        weight_u.append(weight)
                                        count = count + weights[(u[0]-base)][i-1][0]

                        if(count != 0):
                                sum_u = sum(weight_u)
                                #print(weight_u)
                                weight_u = []
                                #print(u, sum_u)
                                u[2] = sum_u/count
                                count = 0
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
        fp = open("cosine10.txt", "w")
        train_matrix = training_matrix()
        result_matrix = testing_matrix("testing10.txt", 10)

        print(len(result_matrix))
        for i in range(len(result_matrix)):
                fp.write(str(result_matrix[i][0]))
                fp.write(" ")
                fp.write(str(result_matrix[i][1]))
                fp.write(" ")
                if(int(round(result_matrix[i][2])) == 6):
                        result_matrix[i][2] = 5
                elif(int(round(result_matrix[i][2])) == 0):
                        result_matrix[i][2] = 1
                fp.write(str(int(round(result_matrix[i][2]))))
                fp.write("\n")
        

if __name__ == "__main__":
        main()
