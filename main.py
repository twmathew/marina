#Thomas Mathew
#CS 496
# [imports]
from google.appengine.ext import ndb
import webapp2
import json

#following google cloud reference material, define Boat template
#specifically, "Entity Property Reference"
class Boat(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()
    length = ndb.IntegerProperty()
    at_sea = ndb.BooleanProperty()

#Slip Template
class Slip(ndb.Model):
    number = ndb.IntegerProperty()
    current_boat = ndb.StringProperty()
    arrival_date = ndb.StringProperty()

#Slip Query definition.
def slip_query(boatId):
    #Goal is to find and return a Slip that holds the boat with the given parameter ID
    qry = Slip.query(Slip.current_boat == boatId)
    for slips in qry.fetch(1):
        slipGet = ndb.Key(urlsafe=id).get()
        return slipGet


#Boat handler. 
class BoatHandler(webapp2.RequestHandler):
    #Define POST 
    def post(self):
        boat_data = json.loads(self.request.body)
      #  boat_id = Key(urlsafe=string)
        #now take the loaded json and make a boat and put it. Starts at sea
        new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_sea=True)
        #new_boat.put()
        new_boat.put()
        #make a self link. 2nd line gives a self property so that the key is in the URL
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
        #add id to the properties
        boat_dict['id'] = new_boat.key.urlsafe()
        #next line for debugging purposes
        self.response.write(json.dumps(boat_dict))

    #Define GET
    def get(self, id=None):
        #if an id exists...
        if id:
            boatGet = ndb.Key(urlsafe=id).get()
            #add self link again so we get the id along with everything else
            boatDict = boatGet.to_dict()
            boatDict['self'] = "/boats/" + id
            boatDict['id'] = id
            #testing
            self.response.write(json.dumps(boatDict))
        else:
             #Here we will GET all boats.
             #create an array
             boat_dicts =[]
             #create a query
             boatQuery = Boat.query()
             #Use query to Fetch
             boat_query_return_list = boatQuery.fetch(100, keys_only=False)
             #Loop through everything we just fetched. GEt the info for each boat and ID as well.
             for boat in boat_query_return_list:
                     boat_dict = boat.to_dict()
                     boat_dict['id'] = boat.key.urlsafe()
                     #add to the array we defined before
                     boat_dicts.append(boat_dict)

             #dump/print the array
             self.response.write(json.dumps(boat_dicts))
   

    #Define DELETE
    def delete(self, id=None):
        if id:
            boatKey = ndb.Key(urlsafe=id)
            boatKey.delete()
            
            
        
    #Define PATCH. Used to update information of an existing boat.
    def patch(self, id=None):
        if id:
            #get the PATCH input, and the current boat at the ID
            patch_data = json.loads(self.request.body)
            curr_boat = ndb.Key(urlsafe=id).get()
            #if a field exists, update, otherwise do nothing, leaving the current data alone
            if 'at_sea' in patch_data:
                curr_boat.at_sea = patch_data['at_sea']
            if 'length' in patch_data:
                curr_boat.length = patch_data['length']
            if 'type' in patch_data:
                curr_boat.type = patch_data['type']
            if 'name' in patch_data:
                curr_boat.name = patch_data['name']
        #Put, to apply changes
            curr_boat.put()

    #define PUT. Used to overwrite a boat with a new one
    #It will operate very similar to POST, but it will take user input for the at_sea variable and ID    
    def put(self, id=None):
        if id:
            boat_data = json.loads(self.request.body)
            #now take the loaded json and make a boat and put it. Starts at sea
            new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_sea=boat_data['at_sea'], id=boat_data['id'])
            #delete the previous boat
            boatToDeleteKey = ndb.Key(urlsafe=id)
            boatToDeleteKey.delete()
            #overwrite
            new_boat.put()
            #make a self link. 2nd line gives a self property so that the key is in the URL
            boat_dict = new_boat.to_dict()
            boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
            #next line for debugging purposes
            self.response.write(json.dumps(boat_dict))

    

#Slip handler. 
class SlipHandler(webapp2.RequestHandler):

    #Define POST 
    def post(self):
        slip_data = json.loads(self.request.body)
      #  boat_id = Key(urlsafe=string)
        #now take the loaded json and make a slip and put it. All new slips are empty, so set current boat to null by leaving it blank
        new_slip = Slip(number=slip_data['number'])
        new_slip.put()
        #make a self link. 2nd line gives a self property so that the key is in the URL
        slip_dict = new_slip.to_dict()
        slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
        #add id to the properties
        slip_dict['id'] = new_slip.key.urlsafe()
        #next line for debugging purposes
        self.response.write(json.dumps(slip_dict))

    #Define GET
    def get(self, id=None):
        #if an id exists...
        if id:
            slipGet = ndb.Key(urlsafe=id).get()
            #add self link again so we get the id along with everything else
            slipDict = slipGet.to_dict()
            slipDict['self'] = "/slips/" + id
            slipDict['id'] = id
            #testing
            self.response.write(json.dumps(slipDict))
        else:
             #Here we will GET all slips.
             #create an array
             slip_dicts =[]
             #create a query
             slipQuery = Slip.query()
             #Use query to Fetch
             slip_query_return_list = slipQuery.fetch(100, keys_only=False)
             #Loop through everything we just fetched. GEt the info for each slip and ID as well.
             for slip in slip_query_return_list:
                     slip_dict = slip.to_dict()
                     slip_dict['id'] = slip.key.urlsafe()
                     #add to the array we defined before
                     slip_dicts.append(slip_dict)

             #dump/print the array
             self.response.write(json.dumps(slip_dicts))

    #Define DELETE
    def delete(self, id=None):
        if id:
            slipKey = ndb.Key(urlsafe=id)
            slipKey.delete()
            
            
    #Define PATCH. Used to update information of an existing slip.
    def patch(self, id=None):
        if id:
            #get the PATCH input, and the current slip at the ID
            patch_data = json.loads(self.request.body)
            current_slip = ndb.Key(urlsafe=id).get()
            #if a field exists, update, otherwise do nothing, leaving the current data alone
            if 'number' in patch_data:
                current_slip.number = patch_data['number']
            if 'arrival_date' in patch_data:
                current_slip.arrival_date = patch_data['arrival_date']
            if 'current_boat' in patch_data:
                current_slip.current_boat = patch_data['current_boat']
                
        #Put, to apply changes
            current_slip.put()

    #define PUT. Used to overwrite a slip with a new one
    #It will operate very similar to POST, but it will take user input for the ID    
    def put(self, id=None):
        if id:
            slip_data = json.loads(self.request.body)
            #now take the loaded json and make a slip and put it. 
            new_slip = Slip(number=slip_data['number'], arrival_date=slip_data['arrival_date'], current_boat=slip_data['current_boat'], id=slip_data['id'])
            #delete the previous slip
            slipToDeleteKey = ndb.Key(urlsafe=id)
            slipToDeleteKey.delete()
            #overwrite
            new_slip.put()
            #make a self link. 2nd line gives a self property so that the key is in the URL
            slip_dict = new_slip.to_dict()
            slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
            #next line for debugging purposes
            self.response.write(json.dumps(slip_dict))

#Slip handler. 
class DockingHandler(webapp2.RequestHandler):
    def put(self, id=None):
        #Define PUT, to dock a boat
        #Boat will be assigned to a slip, the user's inputs which slip.
        #User provides the slip, the date of arrival and the boat's ID
        #If the slip is occupied the server should return an Error 403 Forbidden message
        if id:
            dock_data = json.loads(self.request.body)
            #Want to get the boat and the slip
            boatId = dock_data['boat_id']
            boatGet = ndb.Key(urlsafe=boatId).get()
            slipId = dock_data['slip_id']
            slipDate = dock_data['arrival_date']
            slipGet = ndb.Key(urlsafe=slipId).get()
            #Now do the stuff to dock, If the slip is empty
            if slipGet.current_boat:
                nothing = 1
            else:
                slipGet.current_boat = boatId
                slipGet.arrival_date = slipDate
                boatGet.at_sea = False
                #save changes
                slipGet.put()
                boatGet.put()
                #make a self link. 2nd line gives a self property so that the key is in the URL
                slip_dict = slipGet.to_dict()
                slip_dict['self'] = '/slips/' + slipGet.key.urlsafe() + '/boat/'

    
    def delete(self, id=None):
        #Define DELETE, to have a boat depart
        #Causes slip to become empty
        #Sets the ship to be "At sea"
        if id:
            #Get the slip
            slipGet = ndb.Key(urlsafe=id).get()
            #get the boat
            boatId = slipGet.current_boat
            boatGet = ndb.Key(urlsafe=boatId).get()
            #Now make the changes needed
            boatGet.at_sea = True
            slipGet.current_boat = "null"
            #save changes
            boatGet.put()
            slipGet.put()



# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write("This is the Marina page")
# [END main_page]


# [START app]

# Stuff for Webapp 2 so it can handle PATCH
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

#This part determines how all the URL routes are handled
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boats', BoatHandler),
    ('/boats/(.*)', BoatHandler),
    ('/slips', SlipHandler),
    ('/slips/(.*)/boat', DockingHandler),
    ('/slips/(.*)', SlipHandler)
], debug=True)
# [END app]
