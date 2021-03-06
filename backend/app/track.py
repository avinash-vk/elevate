from firebase import firebase

firestore = firebase.FirestoreController()

class Track(object):
    def __init__(self,tname,artist,aname,genre,desc,coverurl,mp3fileurl='',duration=0,plays=0,tid=""):
        self.tname=tname
        self.artist=artist
        self.aname=aname
        self.genre=genre
        self.desc=desc
        self.coverurl=coverurl
        self.mp3fileurl=mp3fileurl
        self.plays=plays
        self.duration=duration
        self.tid=tid
        
    @classmethod
    def fromDB(cls,tid):
        trackData = firestore.getTrack(tid)
        return cls(trackData['tname'],trackData['artist'],trackData['aname'],trackData['genre'],trackData['desc'],trackData['coverurl'],trackData['mp3fileurl'],trackData['plays'],trackData['duration'],trackData['tid'])
    
    def save(self):
        return firestore.addNewTrack(self)

    def data(self):
        return {'tname':self.tname,'artist':self.artist,'aname':self.aname,'genre':self.genre,'desc':self.desc,'coverurl':self.coverurl,'mp3fileurl':self.mp3fileurl,'plays':self.plays,'duration':self.duration,'tid':self.tid}
    
    def addPlay(self):
        return firestore.addPlay(self.tid)

    def retrieveArtist(self):
        return firestore.retrieveTrackArtist(self.tid)

    def update(self,tid):
        return firestore.updateTrack(self,tid)

    def delete(self):
        firestore.deleteTrack(self.tid)


class TrackManager(object):
    def __init__(self):
        pass

    def addNewTrack(self,tnm,artist,aname,genre,desc,coverurl,mp3fileurl,duration):
        newTrack=Track(tnm,artist,aname,genre,desc,coverurl,mp3fileurl,duration)
        return newTrack.save()
        
    def getTrack(self,tid):
        return Track.fromDB(tid)
    
    def getTrackData(self,tid):
        track = Track.fromDB(tid)
        return track.data()

    def retrieveTrackArtist(self,tid):
        track = Track.fromDB(tid)
        track.retrieveArtist()
        return firestore.retrieveTrackArtist(tid)
    
    def updateTrack(self,tid,tnm,artist,aname,genre,desc,coverurl):
        updatedTrack=Track(tnm,artist,aname,genre,desc,coverurl)
        updatedTrack.update(tid)

    def deleteTrack(self,tid):
        track = Track.fromDB(tid)
        track.delete()
        
    def getTracks(self,uid):
        return firestore.getTracks(uid)

    def getTracksByArtist(self,aid):
        return firestore.getTracksByArtist(aid)
    
    def getAllTracks(self):
        return firestore.getAllTracks()
