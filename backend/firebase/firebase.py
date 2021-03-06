import os

from firebase_admin import firestore

class FirestoreController:
    def __init__(self):
        self.db = firestore.client()

    def getUser(self, uid):
        return self.db.collection('users').document(uid).get().to_dict()
        
    def saveUser(self, user):
        self.db.collection('users').document(user.uid).set(user.data())

    def deleteUser(self, uid):
        self.db.collection('users').document(uid).delete()

    def userAdminStatus(self,uid):
        user=self.db.collection('users').document(uid).get().to_dict()
        if "superUser" in user:
            if(user["superUser"]):
                return True
            else:
                return False
        else:
            return False

    def getUserFavourites(self,uid):
        tracks_ref = self.db.collection(u'tracks')
        likedSongs=self.db.collection(u'users').document(uid).get().to_dict()['likedSongs']
        tracks = tracks_ref.stream()
        trackarr=[]
        for track in tracks:
            t=track.to_dict()
            if t['tid'] in likedSongs:
                t=track.to_dict()
                #t['aname']=FirestoreController().retrieveTrackArtist(t['tid'])
                trackarr.append(t)
        return {"data":trackarr}

    def getUserHistory(self,uid):
        tracks_ref = self.db.collection(u'tracks')
        history=self.db.collection(u'users').document(uid).get().to_dict()['history']
        tracks = tracks_ref.stream()
        trackarr=[]
        for track in tracks:
            t=track.to_dict()
            #t['aname']=FirestoreController().retrieveTrackArtist(t['tid'])
            if t['tid'] in history:
                trackarr.append(t)
        return {"data":trackarr}

    def addNewTrack(self,track):
        doc_ref = self.db.collection(u'tracks').document()
        tid=doc_ref.id
        doc_ref.set({
            u'tname': track.tname,
            u'artist': track.artist,
            u'aname':track.aname,
            u'genre': track.genre,
            u'desc': track.desc,
            u'coverurl': track.coverurl,
            u'mp3fileurl': track.mp3fileurl,
            u'duration':track.duration,
            u'plays':track.plays,
            u'tid':tid
        })
        return doc_ref.id

    def updateTrack(self,track,tid):
        self.db.collection('tracks').document(tid).update({'tname':track.tname,'aname':track.aname,'artist':track.artist,'desc':track.desc,'coverurl':track.coverurl})

    def getTracks(self,uid):
        tracks_ref = self.db.collection(u'tracks')
        #likedSongs=self.db.collection(u'users').document(uid).get().to_dict()['likedSongs']
        tracks = tracks_ref.stream()
        trackarr=[]
        for track in tracks:
            t=track.to_dict()
            '''
            if t['tid'] in likedSongs:
                t['like']=1
            else:
                t['like']=0
            '''
            #t['aname']=FirestoreController().retrieveTrackArtist(t['tid'])
            trackarr.append(t)
        return {"data":trackarr}
        
    def getTracksByArtist(self,aid):
        tracks_ref = self.db.collection(u'tracks')
        tracks_ref=tracks_ref.where(u'artist',u'==',aid)
        tracks = tracks_ref.stream()
        trackarr=[]
        for track in tracks:
            t=track.to_dict()
            #t['aname']=FirestoreController().retrieveTrackArtist(t['tid'])
            trackarr.append(t)
        return {"data":trackarr}

    def deleteTrack(self,id):
        doc_ref=self.db.collection(u'tracks').document(id)
        if doc_ref.get().exists:
            doc_ref.delete()
        else:
            return {'error':"Track doesn't exist"}

    def getTrack(self,tid):
        doc_ref = self.db.collection(u'tracks').document(tid)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {'error':'Document not found,Missing track'}

    def retrieveTrackArtist(self,tid):
        track = self.db.collection(u'tracks').document(tid).get().to_dict()
        artist = self.db.collection(u'artists').document(track['artist']).get().to_dict()
        return artist['aname']

    def getAllTracks(self):
        tracks = self.db.collection('tracks').stream()
        return [track.to_dict() for track in tracks]
    
    #Artist controller functions
    def addNewArtist(self,artist):
        doc_ref = self.db.collection(u'artists').document()
        aid=doc_ref.id
        doc_ref.set({
            u'aname': artist.aname,
            u'photo': artist.photo,
            u'aid':aid
        })
        return aid

    def getArtist(self,aid):
        doc_ref = self.db.collection(u'artists').document(aid)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {'error':'Document not found,Missing artist'}


    def getArtists(self):
        artists_ref = self.db.collection(u'artists')
        artists = artists_ref.stream()
        artistarr=[]
        for artist in artists:
            artistarr.append(artist.to_dict())
        return {"data":artistarr}
        
    def deleteArtist(self,id):
        doc_ref=self.db.collection(u'artists').document(id)
        if doc_ref.get().exists:
            doc_ref.delete()
        else:
            return {'error':"Artist doesn't exist"}

    def updateArtist(self,artist,aid):
        self.db.collection('artists').document(aid).update({'aname':artist.aname,'photo':artist.photo})

    #playlist controller functions

    def getPlaylist(self,pid):
        doc_ref = self.db.collection(u'playlists').document(pid)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {'error':'Document not found,Missing playlist'}

    def getPlaylistTracks(self,pid):
        playlist_ref = self.db.collection(u'playlists').document(pid).get()
        if playlist_ref.exists:
            playlist_ref=playlist_ref.to_dict()
            tids=playlist_ref['tracks']
            tracks=[]
            i=0
            while(1):
                if i+10<=len(tids):
                    temp_ref=self.db.collection(u'tracks').where(u'tid','in',tids[i:i+10])
                    temp=temp_ref.stream()
                    for t in temp:
                        tracks.append(t.to_dict())
                else:
                    temp_ref=self.db.collection(u'tracks').where(u'tid','in',tids[i:len(tids)])
                    temp=temp_ref.stream()
                    for t in temp:
                        tracks.append(t.to_dict())
                    break
                i=i+10
            res = {
                "pname":playlist_ref['pname'],
                "pid":pid,
                "tracks":tracks
            }
            return {"data":res}
        else:
            return {'error':'Document not found,Missing Playlist'}

    def savePlaylist(self,playlist):
        doc_ref = self.db.collection('playlists').document()
        pd=playlist.data()
        pd['pid']=doc_ref.id
        doc_ref.set(pd)
        return doc_ref.id

    def updatePlaylist(self,playlist,pid):
        doc_ref = self.db.collection('playlists').document(pid)
        doc_ref.set(playlist.data())

    def deletePlaylist(self,pid):
        doc_ref=self.db.collection(u'playlists').document(pid)
        if doc_ref.get().exists:
            doc_ref.delete()
        else:
            return {'error':"Playlist doesn't exist"}

    def getTopSongs(self,limit=20):
        tracks = self.db.collection('tracks').order_by('plays',direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [track.to_dict() for track in tracks]
    
    def getAllSongs(self):
        tracks = self.db.collection('tracks').stream()
        return [track.to_dict() for track in tracks]
    
    def getAllUsers(self):
        users = self.db.collection('users').stream()
        return [user.to_dict() for user in users]
    
    def getMultipleSongs(self, trackIds):
        tracks = self.db.collection('tracks').where('tid', 'in', trackIds).stream()
        return [track.to_dict() for track in tracks]
    
    def addPlay(self,tid):
        self.db.collection('tracks').document(tid).update({'plays':firestore.Increment(1)})