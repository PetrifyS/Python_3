class Game():
    def __init__(self):
        self.candle = "There is a candle nearby."
        self.lantern = "There is a empty lantern nearby."
        self.pawn = "There is a pawn nearby."
        self.lamp = "There is a lamp nearby."
        self.inv = []
        self.oldinv = []
        self.lat = False
        self.room2 = False
        self.start()

    def taking(self, obj):
        take = "take " + obj
        grab = "grab " + obj
        taking = [take, grab]
        return taking

    def heavy(self):
        print("That is too heavy for you to take.")
        self.choice()

    def throwing(self, obj):
        drop = "drop " + obj
        throw = "throw " + obj
        throwing = [throw, drop]
        return throwing

    def direction(self, direction):
        go = "go " + direction
        head = "head " + direction
        move = "move " + direction
        walk = "walk " + direction
        abrevation = direction[0]
        walking = [go, head, move, walk, abrevation]
        return walking

    def start(self):
        self.room = 1
        self.print_room()
        self.choice()

    def print_room(self):
        if self.room == 1:
            print("You are in a room.")
            if "lamp" in self.inv:
                print("There is an exit to the south.")
            if "candle" not in self.inv and "lamp" not in self.inv and self.lat == False:
                print(self.candle)
            if "lantern" not in self.inv and "lamp" not in self.inv and self.lat == False:
                print(self.lantern)
            if "lamp" not in self.inv and self.lat == True:
                print(self.lamp)
            if "pawn" not in self.inv:
                print(self.pawn)
        if self.room == 2:
            print("You are in a bare room with a table.")
            print("There are exits to the north and to the east.")


    def choice(self):
        self.decision = input("> ")
        #if staments that will always be needed
        #if stament just needed in room1

        #other if staments

        if self.decision in self.throwing("candle"):
            self.throw("candle")
        elif self.decision in self.taking("lantern"):
            self.take("lantern")
        elif "candle" in self.inv and "lantern" not in self.inv:
            print("You hands keep burning and you die from blood loss.")
            self.kill()
        elif self.decision in self.taking("candle"):
            self.take("candle")
        elif self.decision in self.taking("pawn") and "pawn" not in self.oldinv:
            self.take("pawn")
        elif self.decision in self.taking("lamp"):
            self.take("lamp")

        elif self.decision in self.throwing("candle"):
            self.throw("candle")
        elif self.decision in self.throwing("lantern"):
            self.throw("lantern")
        elif self.decision in self.throwing("lamp"):
            self.throw("lamp")
        elif self.decision in self.throwing("pawn"):
            self.throw("pawn")
        elif self.decision == "i" or self.decision == "inventory":
            self.checkinv()
        elif self.decision == "l" or self.decision == "look":
            self.print_room()
            self.choice()
        elif self.decision == "kill":
            self.kill()

        elif self.decision in self.direction("south") and self.room == 1:
            if "lamp" in self.inv:
                self.room = 2
                if self.room2 == False:
                    print("After exiting the room, you feel kinda've dizzy and fall to the ground.")
                    print("You wake up to find that your lantern is still lighted.")
                    print("You don't know how long you have been out,")
                    print("but looking around you can see a bare room with a table in the center.")
                    print("There are two exits, one to the north and one towards the east.")
                    self.room2 = True
                    self.choice()
                else:
                    self.choice()
            else:
                print("You walked into a hole in the ground and died.")
                self.kill()
        #if staments just needed in room2

        elif self.decision in self.direction("north") and self.room == 2:
            if "lamp" in self.inv:
                self.room = 1
                self.choice()
            else:
                print("You walked into a hole in the ground and died.")
                self.kill()
        elif self.decision in self.taking("table") and self.room == 2:
            self.heavy()

        elif self.decision == "help":
            print("This is a text based adventure game made by Peter Scholtens.")
            print("The object of this game is to find the chess board and all its missing pieces.")
            print("You can use 'take' and 'grab' to take things.")
            print("To head in a direction type 'go', 'head', 'move', 'walk'")
            print("or the first letter of the direction to head that way.")
            print("Type 'i' or 'inventory' to check your inventory.")
            print("Type 'l' or 'look' to look around or at items.")
            print("Good luck!")
            self.choice()
        else:
            print("I do not understand.")
            self.choice()

    def take(self, obj):
        if obj not in self.inv:
            if obj == "candle" or obj == "lantern":
                if "lamp" not in self.inv and self.lat == False:
                    if obj == "candle":
                        self.inv.append("candle")
                        print("Taken.")
                        if "lantern" not in self.inv:
                            print("Ok now you can see that there is a exit to the south,")
                            print("but you are burning your hands...")
                            self.choice()
                        elif "lantern" in self.inv:
                            print("You put the candle into the lantern and start a flame.")
                            print("Immediately you can see there is an exit to the south.")
                            self.inv.remove("candle")
                            self.inv.remove("lantern")
                            self.inv.append("lamp")
                            self.lat = True
                            self.choice()
                    elif obj == "lantern":
                        self.inv.append("lantern")
                        print("Taken.")
                        if "candle" not in self.inv:
                            print("You can't see")
                            self.choice()
                        elif "candle" in self.inv:
                            print("Quickly you put the candle into the empty lantern and")
                            print("notice that your hands aren't too badly burnt. You have saved your life.")
                            print("The light spreads around the room and you realize that to the south is an exit.")
                            self.inv.remove("candle")
                            self.inv.remove("lantern")
                            self.inv.append("lamp")
                            self.lat = True
                            self.choice()
                else:
                    print("That no longer exists.")
                    self.choice()
            elif obj == "lamp" and self.lat == True:
                self.inv.append("lamp")
                print("Taken.")
                self.choice()
            elif obj == "pawn":
                self.inv.append("pawn")
                print("Taken.")
                print("Congratulations, you have found your first pawn.")
                self.choice()
            else:
                print("That doesn't exists.")
                self.choice()


        else:
            print("You already have that in your inventory.")
            self.choice()

    def throw(self, obj):
        if obj in self.inv:
            if obj == "candle":
                self.inv.remove("candle")
                print("Thrown.")
                self.choice()
            elif obj == "lantern":
                self.inv.remove("lantern")
                print("Thrown.")
                self.choice()
            elif obj == "lamp":
                self.inv.remove("lamp")
                print("Thrown.")
                self.choice()
            elif obj == "pawn":
                self.inv.remove("pawn")
                self.oldinv.append("thrownpawn")
                print("Thrown.")
                self.choice()
        else:
            print("You do not have that in your inventory.")
            self.choice()


    def checkinv(self):
        print("You have %s in your inventory." % (self.inv))
        print("You had %s in your inventory." % (self.oldinv))
        self.choice()

    def kill(self):
        print("Would you like to play again? y/n")
        kill = input("> ")
        if kill == "y":
            print("Restarting......")
            g = Game()

g = Game()
