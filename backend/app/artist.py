from firebase import firebase;

class Artist(object):
    def __init__(self,aname):
        self.aname=aname
          
    def getTracks(self):
        #return tracks by this artist 
        pass

class ArtistManager(object):
    def __init__(self):
        pass

    def addNewArtist(self,anm):
        newArtist=Artist(anm)
        controller=firebase.FirestoreController()
        controller.addNewArtist(newArtist)

    def deleteArtist(self,id):
        controller=firebase.FirestoreController()
        controller.deleteArtist(id)
        
    def getArtists(self):
        controller=firebase.FirestoreController()
        return controller.getArtists()