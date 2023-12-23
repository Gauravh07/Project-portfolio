from Book import Book
 # To complete



class Inventory:
    def __init__(self):
        self.books=[]
    def initialize(self):
        book1=Book("A Brief History of Time","Stephen Hawking",10.17,"GV5N32M9")
        book2=Book("The Alchemist","P. Coelho",6.99,"TR3FL0EW") 
        book3=Book("Thus Spoke Zarathustra.","F. Nietzsche",7.81,"F2O9PIE9")  
        book4=Book("Jonathan Livingston Seagull","R. Bach",6.97,"R399CED1")
        book5=Book("The Time Machine ","H. G. Wells",5.95,"6Y9OPL87")
        book6=Book("Introduction to Programming in Python","R. Sedgewick",69.99,"5T3RRO90")
        book7=Book("Atoms of Silence ","H. Reeves",28.02,"3W2TB162")
        book8=Book("2001: A Space Odyssey","A. C. Clarke ",8.99,"TU2RL012") 
        book9=Book("20,000 Leagues under the Sea" ,"J. Verne",5.99,"JI2PL986 ")
        book10=Book("Les Miserables","V. Hugo ",9.98,"VC5CE249 ")
        self.books=[book1,book2,book3,book4,book5,book6,book7,book8,book9,book10]
    def __str__(self):
        inventorystr =""
        for i in range(len(self.books)):
            inventorystr= inventorystr+"%s-%s \n"%(i+1,self.books[i])
        return inventorystr
    
 
    def info(self):
        totalbooks=len(self.books)
        totalprice=0
        maxprice=self.books[0].price
        for book in self.books:
            totalprice=totalprice+book.price
            if book.price>maxprice:
                maxprice=book.price 
        print("#Items : %s"%totalbooks)
        print("Total price $%s"%totalprice)
        print('Most expensive item at $%s'%maxprice) 


    def search(self,keyword):
        found=False
        i=0
        
        for x in self.books:
            i=i+1
            if keyword in x.title:
                print(i,'-',x)
                found=True
                
                    
        if found==False:
            print("no book found")    


    def add(self,book=None):
        if book is None:
            title=input("Add new title:")
            author=input("Enter Author name")
            price=float(input("Add price"))
            reference=input("Enter Reference number: ")
            newbook=Book(title,author,price,reference)
            self.books.append(newbook)
        else:
            self.books.append(book)    

       
    
    def delete(self):
        x=int(input('Enter the ID of the book to be deleted'))
        del self.books[x-1]


    def adjust_price(self,x):
        for y in self.books:
            y.price=y.price+(y.price*x/100)

    def id_book(self,id):
        y=0
        for x in self.books:
            y=y+1
            if y==id:
                return x
        return None    