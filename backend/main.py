# importing flask and other dependencies
from flask import Flask,request,jsonify
from mutagen.mp3 import MP3

#configurations and environment setup
from dotenv import load_dotenv
load_dotenv()
from firebase import config
import os


# importing other modules from the app for functionalities
from app.users import UserManager
from app.track import TrackManager
from app.artist import ArtistManager
from app.playlist import PlaylistManager
from app.recommender.popularityRecommender import PopularityRecommender
from app.recommender.userRecommender import UserRecommender
from utils import fileUploader

# enabling cors
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# initialising manager objects
trackManager=TrackManager()
artistManager=ArtistManager()
userManager = UserManager()
playlistManager = PlaylistManager()
popularityRecommender = PopularityRecommender()
userRecommender = UserRecommender()

class APIServer:
    '''
        This class controls all of the API routing and running of the flask server.
    '''
    def __init__(self,port):
        self.port = port

    def start(self):
        if __name__ == '__main__':
            app.run(port = self.port,debug=True)
    
    def returnErrorMessage(self,e):
        print(e)
        response_msg=jsonify({"error":"400","message":"Bad request,"+str(e)}),400
        return response_msg

    # testing server status
    @app.route('/ping')
    def test():
        return 'pong'

    # Checking if the user is admin or not.
    @app.route('/user/adminstat',methods=['GET'])
    def userAdminStatus():
        uid = request.args.get('uid')
        admin = userManager.userAdminStatus(uid)
        return {"admin":admin}
    
    # User endpoints

    # create user api
    @app.route('/user/create',methods=['POST'])
    def createUser():
        if request.method == 'POST':
            try:
                userManager.createUser( request.json['uid'], request.json['email'], request.json['displayName'])
                return {"message":"success"},200
            except Exception as e:
                self.returnErrorMessage(e)
    
    # update user endpoint
    @app.route('/user/update')
    def updateUser():
        if request.method == 'POST':
            try:
                userManager.updateUser(request.json.uid, request.json.email, request.json.displayName)
                return {"message":"success"},200
            except Exception as e:
                self.returnErrorMessage(e)
    
    # get user endpoint
    @app.route('/user')
    def getUser():
        uid = request.args.get('uid')
        res = userManager.getUserData(uid)
        plist=[]
        for pid in res['playlists']:
            pdata=playlistManager.getPlaylistData(pid)
            plist.append(pdata)
        res['playlists']=plist
        return res

    # top songs recommendations endpoint
    @app.route('/user/top')
    def getPopularityRecommendations():
        uid = request.args.get('uid')
        limit = int(request.args.get('limit'))
        popularityRecommender.create(uid)
        recommendations = popularityRecommender.recommend(limit);
        return {"data":recommendations}
    
    # user recommendations endpoint 
    @app.route('/user/recommend')
    def getUserRecommendations():
        uid = request.args.get('uid')
        limit = int(request.args.get('limit'))
        userRecommender.create(uid)
        recommendations = userRecommender.recommend(limit);
        return {"data":recommendations}

    # manages user like/unlike a track
    @app.route('/user/like',methods=['POST'])
    def setLike():
        try:
            uid = request.json.get('uid')
            trackId = request.json.get('tid')
            action = request.json.get('action')
            user = userManager.getUser(uid)
            if (action=='like'):
                user.likeSong(trackId)
            else:
                user.unLikeSong(trackId)
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)
        
    # manages add/remove playlist for user
    @app.route('/user/playlists',methods=['POST'])
    def managePlaylist():
        try:
            uid = request.json.get('uid')
            playlistId = request.json.get('pid')
            action = request.json.get('action')
            user = userManager.getUser(uid)
            if (action=='addPlaylist'):
                user.addPlaylist(playlistId)
            else:
                user.removePlaylist(playlistId)
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)

    # updates user history
    @app.route('/user/history',methods=['POST'])
    def manageHistory():
        try:
            uid = request.json.get('uid')
            trackId = request.json.get('trackId')
            user = userManager.getUser(uid)
            user.addToHistory(trackId)
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)

    # delete user endpoint
    @app.route('/user/delete')
    def deleteUser():
        if request.method == 'POST':
            try:
                userManager.deleteUser(request.json.get('uid'))
                return {"message":"success"},200
            except Exception as e:
                self.returnErrorMessage(e)
    
    # get a list of all liked songs
    @app.route('/user/tracks/favourites',methods=['GET'])
    def getUserFavourites():
        try:
            uid=request.args.get('uid')
            return userManager.getUserFavourites(uid),200
        except Exception as e:
            self.returnErrorMessage(e)

    # get all of user history songs
    @app.route('/user/tracks/history',methods=['GET'])
    def getUserHistory():
        try:
            uid=request.args.get('uid')
            return userManager.getUserHistory(uid),200
        except Exception as e:
            self.returnErrorMessage(e)

    # track endpoints

    # add track to db
    @app.route('/addtrack',methods=['POST'])
    def addTrack():
        if request.method == 'POST':
            try:
                tnm=request.form['tname']
                artist=request.form['artist']
                aname=request.form['aname']
                genre=request.form['genre']
                desc=request.form['desc']
                cover=request.files['cover']
                mp3file=request.files['mp3file']
                if cover and fileUploader.allowed_file_cover(cover.filename):
                    pass
                else:
                    raise Exception('Invalid file type for image!')
                
                if mp3file and fileUploader.allowed_file_track(mp3file.filename):
                    pass
                else:
                    raise Exception('Invalid file type for track!')
                #Something happens here
                uploader=fileUploader.FileUploader()
                upload_folder ="app\\uploads"
                cover.save(os.path.join(upload_folder,cover.filename))
                coverurl = uploader.uploaderimg(os.path.join(upload_folder,cover.filename),cover)
                filepath=os.path.join(upload_folder,mp3file.filename)
                mp3file.save(filepath)
                mp3fileurl = uploader.uploadertrack(filepath,mp3file)
                audio = MP3(filepath)
                audio_info = audio.info    
                duration = int(audio_info.length)
                tid=trackManager.addNewTrack(tnm=tnm,artist=artist,genre=genre,desc=desc,coverurl=coverurl,mp3fileurl=mp3fileurl,duration=duration,aname=aname)
                response_msg=jsonify({"status":"200 ok","message":"successfully added track","tid":str(tid)}),200
                return response_msg 
            except Exception as e:
                self.returnErrorMessage(e)

    #get all tracks for user as per liked/unliked
    @app.route('/gettracks',methods=['GET'])
    def getTracks():
        try:
            uid=request.args.get('uid')
            return trackManager.getTracks(uid),200
        except Exception as e:
            self.returnErrorMessage(e)

    # get all tracks by artist
    @app.route('/tracks/artist',methods=['GET'])
    def getTracksByArtist():
        try:
            aid = request.args.get('aid')
            return trackManager.getTracksByArtist(aid),200
        except Exception as e:
            self.returnErrorMessage(e)

    # get particular track
    @app.route('/track',methods=['GET'])
    def getTrack():
        try:
            tid=request.args.get('tid')
            res=trackManager.getTrackData(tid)
            #res['aname']=trackManager.retrieveTrackArtist(tid)
            return res
        except:
            response_msg=jsonify({"error":"400","message":"Bad request"}),400
            return response_msg

    # update a particular track
    @app.route('/track/update',methods=['POST'])
    def updateTrack():
        #updating mp3 not added
        if request.method == 'POST':
            try:
                tid = request.args.get('tid')
                trackManager.updateTrack(tid=tid,tnm=request.json.get("tname"),artist=request.json.get("artist"), aname=request.json.get("aname"),genre=request.json.get("genre"), desc=request.json.get("desc"), coverurl=request.json.get("coverurl"))
                return {"message":"successfully updated track"},200
            except Exception as e:
                self.returnErrorMessage(e)

    # delete a particular track
    @app.route('/track/delete',methods=['POST'])
    def deleteTrack():
        try:
            trackManager.deleteTrack(request.json.get('tid'))
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)


    #artist endpoints

    @app.route('/addartist',methods=['POST'])
    def addArtist():
        try:
            anm=request.json.get('aname')
            photo=request.json.get('photo')
            aid=artistManager.addNewArtist(anm=anm,photo=photo)
            response_msg=jsonify({"status":"200 ok","message":"successfully created artist","aid":str(aid)}),200
            return response_msg

        except Exception as e:
            self.returnErrorMessage(e)

    
    @app.route('/artist',methods=['GET'])
    def getArtist():
        aid=request.args.get('aid')
        return artistManager.getArtistData(aid)

    @app.route('/getartists',methods=['GET'])
    def getArtists():
        try:
            return artistManager.getArtists(),200
        except Exception as e:
            self.returnErrorMessage(e)
    
    @app.route('/artist/delete',methods=['POST'])
    def deleteArtist():
        try:
            artistManager.deleteArtist(request.json.get('aid'))
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)

    @app.route('/artist/update',methods=['POST'])
    def updateArtist():
        if request.method == 'POST':
            try:
                aid = request.args.get('aid')
                artistManager.updateArtist(aid=aid, anm=request.json.get("aname"),photo=request.json.get("photo"))
                return {"message":"successfully updated artist"},200
            except Exception as e:
                self.returnErrorMessage(e)


    #playlist endpoints

    @app.route('/playlist/create',methods=['POST'])
    def createPlaylist():
        if request.method == 'POST':
            try:
                pid=playlistManager.createPlaylist(request.json['uid'], request.json['pname'])
                return {"pid":pid},200
            except Exception as e:
                self.returnErrorMessage(e)

    @app.route('/playlist/delete',methods=['POST'])
    def deletePlaylist():
        try:
            playlistManager.deletePlaylist(request.json.get('pid'))
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)

    @app.route('/playlist',methods=['GET'])
    def getPlaylist():
        try:
            pid=request.args.get('pid')
            return playlistManager.getPlaylistData(pid),200
        except Exception as e:
            self.returnErrorMessage(e)

    @app.route('/playlist/tracks',methods=['GET'])
    def getPlaylistTracks():
        try:
            pid=request.args.get('pid')
            return playlistManager.getPlaylistTracks(pid),200
        except Exception as e:
            self.returnErrorMessage(e)

    # manages add/remove playlist for user
    @app.route('/user/playlist/tracks',methods=['POST'])
    def managePlaylistTracks():
        try:
            tid = request.json.get('tid')
            pid = request.json.get('pid')
            action = request.json.get('action')
            playlist = playlistManager.getPlaylist(pid)
            if (action=='addTrack'):
                playlist.addSong(pid,tid)
            else:
                playlist.removeSong(pid,tid)
            return {"message":"success"},200
        except Exception as e:
            self.returnErrorMessage(e)

    @app.route('/tracks/all')
    def getAllTracks():
        try:
            tracks = trackManager.getAllTracks()
            return {'data':tracks}
        except Exception as e:
            self.returnErrorMessage(e)
    
    @app.route('/tracks/updateplay', methods=['POST'])
    def updatePlay():
        try:
            tid = request.args.get('tid')
            track = trackManager.getTrack(tid)
            track.addPlay()
            return {"msg":"success"}
        except Exception as e:
            self.returnErrorMessage(e)

# starting the server on port 5000
server = APIServer(port = 5000)
server.start()

