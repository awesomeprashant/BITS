from csv import reader
import time as t

class citizenRecord:
    def __init__(self,name,date,citId):
        self.citId = citId
        self.name = name
        self.date = date
        self.left = None
        self.right = None

    def __eq__(self, other):
        if(isinstance(other,citizenRecord) and isinstance(self,citizenRecord) ):
            return self.date == other.date

    def __lt__(self, other):
        if(isinstance(other,citizenRecord) and isinstance(self,citizenRecord)):
            return self.date < other.date

class citizenRecordQueue:
   
    def __init__(self,maxsize):
        self.preFix = 1
        self.maxsize = maxsize
        self.size = 0
        self.crQueue =  [citizenRecord]*(self.maxsize+1)
        self.FRONT = 1
        self.outFilePath = "outputPS06a.txt"
    
    #Arr[(i -1) / 2] returns its parent node.
    #Arr[(2 * i) + 1] returns its left child node.
    #Arr[(2 * i) + 2] returns its right child node.

    # Function to return the position of
    # parent for the node currently
    # at pos
    def parent(self, pos):
        if pos//2 <= 0:
            return 1
        else:
            return pos//2
    
    # Function to return the position of
    # the left child for the node currently
    # at pos
    def leftChild(self, pos):
        return 2 * pos
  
    # Function to return the position of
    # the right child for the node currently
    # at pos
    def rightChild(self, pos):
        return (2 * pos) + 1
    
    # Function that returns true if the passed
    # node is a leaf node
    def isLeaf(self, pos):
        return pos*2 > self.size
    
    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.crQueue[fpos], self.crQueue[spos] = self.crQueue[spos], self.crQueue[fpos]
            
        
    # Function to insert a node into the heap
    def enqueueCitizen(self, citizen):
        
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.crQueue[self.size] = citizen
        current = self.size
        
        while self.crQueue[current] < self.crQueue[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)

        
    # Function to print the contents of the heap
    def Print(self):
        #print(self.size)
        try:
            for i in range(1, (self.size//2)+1):
                #print(i)
                print(" PARENT : "+ str(self.crQueue[i].citId)+" LEFT CHILD : "+ 
                                str(self.crQueue[2 * i ].citId)+" RIGHT CHILD : "+
                                str(self.crQueue[2 * i+1].citId))
        except AttributeError:
            print('No element at specified index')  
    
    # Function to heapify the node at pos
    def minHeapify(self, pos):
        #print(self.size)
        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if (
                (
                 isinstance(self.crQueue[self.leftChild(pos)],citizenRecord) and 
                 self.crQueue[pos] > self.crQueue[self.leftChild(pos)] )
                
                or 
                
                (isinstance(self.crQueue[self.rightChild(pos)],citizenRecord) and 
                 self.crQueue[pos] > self.crQueue[self.rightChild(pos)])
            ):
  
                # Swap with the left child and heapify
                # the left child
                if self.crQueue[self.leftChild(pos)] < self.crQueue[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
  
                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
    
    def minHeap(self):
        #print(self.size)
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
    
    def printQueue(self):
        for i in range(1,self.size+1):
            print(" name : " + self.crQueue[i].name)
            print(" date : " + self.crQueue[i].date)
            print(" id : " + self.crQueue[i].citId)
            
            if (isinstance(self.crQueue[self.leftChild(i)],citizenRecord)):
                self.crQueue[i].left = self.crQueue[self.leftChild(i)].citId
            else:
                self.crQueue[i].left = None
             
            if (isinstance(self.crQueue[self.rightChild(i)],citizenRecord)):
                self.crQueue[i].right = self.crQueue[self.rightChild(i)].citId
            else:
                self.crQueue[i].right = None
                
           
            if(self.crQueue[i].left is None):
                print(" left  is None")
            else:
                print(" left  is : " + str(self.crQueue[i].left))
            if(self.crQueue[i].left is None):
                print(" right is None")
            else:
                print(" right is : " + str(self.crQueue[i].right))
            
    
  
    
    def nextCitizen(self):
        if(self.size<1):
            print("Next Patient Not Available")
        else:    
            print("nextCitizen: 1" )
            print("Next citizen for vaccination is: " + self.crQueue[1].citId + " " + self.crQueue[1].name)
            self._dequeueCitizen(self.crQueue[1].citId)
            print("Vaccination Completed for : " + self.crQueue[1].citId)
    
    # Function to remove and return the minimum
    # element from the heap
    # Find Index of Node to be deleted and replace it with last node and delete last node
    # As tree is not min heap. Heapify it again
    def _dequeueCitizen(self, citId):
        #self.remove()
        last = self.crQueue[self.size]
        #print(last.name)
        nodeIndex = self.findNodeIndex(citId)
        #print(nodeIndex)
        
        if(nodeIndex!=-1):
            self.crQueue[nodeIndex]=last
            del(self.crQueue[self.size])  
            self.size-= 1
            self.minHeapify(self.FRONT)
        
        
    def registerCitizen(self, name, date):
        citId = str(self.preFix)+str(date).strip()
        cr = citizenRecord(name,date,citId)
        self.enqueueCitizen(cr)
    
    def findNodeIndex(self,citId):
        for i in range(1,self.size+1):
            print(self.crQueue[i].citId)
            if(self.crQueue[i].citId==citId):
                return i
        return -1
            
            
    def readFile(self,inFilePath):
        with open(inFilePath, 'r') as read_obj:
            csv_reader = reader(read_obj)
            row_count=0
            for row in csv_reader:
            # row variable is a list that represents a row in csv
                if(str(row[0]).find(":")>0):
                    citizenName = (str(row[0]).split(":")[1]).strip()
                else:
                    citizenName = str(row[0]).strip()
                vaccinationDate = row[1]
                #print(citizenName,vaccinationDate)
                self.registerCitizen(citizenName,vaccinationDate)
                row_count+=1
            self.writeFile(self.outFilePath,"No of citizens added: " + str(row_count) +"\n", "w")
            
    
    def writeFile(self, outFilePath, outString, mode):
        f = open(outFilePath, mode)
        f.write(outString)
        f.close()
        
    def outputQueue(self):
        self.writeFile(self.outFilePath,"Refreshed Queue : \n","a")
        for i in range(1,self.size+1):
            self.writeFile(self.outFilePath, self.crQueue[i].citId + ", ","a")
            self.writeFile(self.outFilePath, self.crQueue[i].name + "\n","a")
    def sortQueue(self):
        temp=[citizenRecord]*self.size
        j = 0
        for i in range(1,self.size+1):
            temp[j] = self.crQueue[i]
            j += 1
        temp.sort()
        
        j=0
        for i in range(1,self.size+1):
            self.crQueue[i] = temp[j]
            j +=1
        

# Driver code
if __name__ == '__main__':
	
    print("Initialized VaccinationQueue: ")
    crq = citizenRecordQueue(10)
    t.sleep(3)
    
    print("Loading inputPS06a.txt data into VaccinationQueue... ")
    crq.readFile("inputPS06a.txt")
    t.sleep(3)
    
    print("Heapify VaccinationQueue as min heap based on date... ")
    crq.minHeap()
    crq.printQueue()
    t.sleep(3)
    
    print("Sort VaccinationQueue... ")
    crq.sortQueue()
    t.sleep(3)
    
    print("Output VaccinationQueue to File outputPS06a.txt ... ")
    crq.outputQueue()
    t.sleep(3)
    
    print("Register new  Patient and update the VaccinationQueue ... ")
    crq.readFile("inputPS06b.txt")
    t.sleep(3)
    
    print("Heapify VaccinationQueue as min heap based on date... ")
    crq.minHeap()
    crq.printQueue()
    t.sleep(3)
    
    print("Sort VaccinationQueue... ")
    crq.sortQueue()
    t.sleep(3)
    
    print("Output VaccinationQueue to File outputPS06a.txt ... ")
    crq.outputQueue()
    t.sleep(3)

    print("Next Patient to be vaccinated .. ")
    crq.nextCitizen()
    t.sleep(3)
    
    print("Print Refreshed Queue... ")
    crq.printQueue()
