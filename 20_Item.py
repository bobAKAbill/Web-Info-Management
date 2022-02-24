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
        ret = [[train_people[j][i] for j in range(len(train_people))] for i in range(len(train_people[0]))]
        return ret

def testing_matrix(fp_test, k):#fp_test is the filename, rated is the number of movies the users have rated
        #This function will return the list of stuff that we need to write to the file
        training_list = training_matrix()#200*1000, training data
        test_list = testing_read(fp_test)
        print(len(training_list))
        print(len(training_list[0]))


#Need to generate the list of users and movie rankings to do cosine similarity on, will make it look like training matrix
        test_matrix = []#Matrix just like the training matrix, 200*1000
        temp_matrix = []
        test_tuple = [0]*1000#For all movies
        return_matrix = []#Matrix value to return
        prev_user = test_list[0][0]
        counter = 0
        
        for i in test_list:
                test_tuple[i[1]-1] = i[2]
                if(prev_user != i[0]):
                        temp_matrix.append(test_tuple)
                        test_tuple = [0]*1000
                        counter += 1
                prev_user = i[0]
        temp_matrix.append(test_tuple)#Since the for loop leaves one set out for some reason?

        test_matrix = [[temp_matrix[j][i] for j in range(len(temp_matrix))] for i in range(len(temp_matrix[0]))]

#Need to increase size of the test matrix because its lists are 100 elts long and they need to be 200 for the cosine
        for i in range(len(test_matrix)):
                for j in range(len(test_matrix[i-1])):
                        test_matrix[i-1].append(0)

                
#Need to compare the ratings of our users with the training matrix
        weights = []#Weights for all of the users in the training matrix compared to our testing users, 100 entries
                        #Each index in weights has 200 entries for the similarity to each other user
        weight_u = []#Temp tuple to append stuff
        count = 0#Count of all users that have rated MID

        for i in range(len(test_matrix)):
                for t in range(len(training_list)):
                        if(sum(test_matrix[i-1]) == 0):
                                tup = (0, t-1)
                                weight_u.append(tup)
                        else:
                                tup = (spatial.distance.cosine(test_matrix[i-1], training_list[t-1]), t-1)
                                weight_u.append(tup)
                weights.append(weight_u)
                weight_u = []
        print(len(weights[0]))
        print(len(weights))


#Need to get k neighbors
        for i in range(len(weights)):
                weights[i].sort(reverse = True)

                       
#Now need to get the ratings for all of the 0 rankings in test_list
        base = test_list[0][0]+1
        for u in test_list:#For all of our testing movies
                #print(u[0])
                if(u[2] == 0):#If we need to get a rating for u[1] = MID
                        #print(weights[u[0]-200])
                        for i in range(k):#For every elt in that users array, need to add their ranking for MID*weight
                                #print(u[0]-200, i, u[1])#Print UID-200, round thru loop, MID
                                #print(u[1]-1)
                                if(weights[u[1]-1][i][0] != 0):
                                        for l in range(len(training_list[u[1]])):
                                                weight = weights[u[1]][i][0] * training_list[u[1]][l]
                                                #weight = weights[(u[0]-base)][i][0]*training_list[i][u[1]-1]
                                                weight_u.append(weight)
                                                count = count + weights[u[1]][i][0]

                        if(count != 0):
                                #print(weight_u)
                                sum_u = sum(weight_u)
                                #print(weight_u)
                                weight_u = []
                                #print(u, sum_u)
                                u[2] = sum_u/count
                                count = 0
                                return_matrix.append(u)
                        else:#If count == 0
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
        fp = open("item20.txt", "w")
        train_matrix = training_matrix()
        result_matrix = testing_matrix("testing20.txt", 50)

#My code into a new text file
        print(len(result_matrix))
        for i in range(len(result_matrix)):
                fp.write(str(result_matrix[i][0]))
                fp.write(" ")
                fp.write(str(result_matrix[i][1]))
                fp.write(" ")
                if(int(round(result_matrix[i][2])) == 0):
                        result_matrix[i][2] = 1
                elif(int(round(result_matrix[i][2])) == 6):
                        result_matrix[i][2] = 6
                fp.write(str(int(round(result_matrix[i][2]))))
                fp.write("\n")


if __name__ == "__main__":
        main()
