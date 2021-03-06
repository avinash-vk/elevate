import React,{useContext,useEffect, useState} from 'react';
import API from "../api"
import {useAuth} from '../firebase/provider'
import {AddTrack,CreatePlaylist} from '../components/Modals';
import {default as Loader} from '../components/Loader';
import StatusAlert from '../components/StatusAlert';

export const PlayerContext = React.createContext();
export const usePlayer = () => {
    return useContext(PlayerContext);
}

export const PlayerProvider = ({children}) => {
    const [statusAlert,setStatusAlert] = useState('');
    
    const {currentUser} = useAuth()
    
    // state to make sure all of user data loads before app is shown to users
    const [globalLoad, setGlobalLoad] = useState(true);

    // ids of all the likedSongs by user
    const [likedSongs,setLikedSongs] = useState([])

    // all the playlists of the user
    const [playlists, setPlaylists] = useState([]);

    // ids of all of the user's history
    const [history, setHistory] = useState([]);

    // song queue of the current session
    const [songQueue, setSongQueue] = useState([]);

    // current song index that's being played from the queue
    const [currIndex, setCurrIndex] = useState(-1);

    // audio handles the current song that's being played
    const [audio,setAudio] = useState(new Audio());

    // flag to check whether a song is being played or not.
    const [playing, setPlaying] = useState(false);
    const toggle = () => setPlaying(!playing);

    let trackLogs = [];

    // modal indicators for the addtrack and addplaylist
    const [modal, setModal] = React.useState(0);
    const [tid, setTid] = React.useState();
    const handleClose = () => setModal(0);

    const [tracks, setTracks] = useState([]);
    const [artists, setArtists] = useState([]);
    const [popularityRecommendations,setPopRecommendations]= useState([]);
    const [userRecommendations,setUserRecommendations]=useState([]);

    const userInit = async () => {
        let data = await API.getUserData(currentUser.uid)
        setPlaylists(data.playlists)
        setHistory(data.history)
        setLikedSongs(data.likedSongs)
        let tracks = (await API.getAllTracks()).data
        setTracks(tracks);
        let artists = (await API.getArtists()).data
        setArtists(artists);
        let popRecommendations = (await API.getPopularityRecommendations(currentUser.uid, 5)).data
        setPopRecommendations(popRecommendations);
        let userRecommendations = (await API.getUserRecommendations(currentUser.uid, 10)).data
        setUserRecommendations(userRecommendations);
    }

    // Event to load all of the user data on the frontend on the first load.
    useEffect(()=>{
        userInit().then(()=>{
            setGlobalLoad(false);
        }).catch( err => {
            console.log(err)
            setGlobalLoad(false);
        })
    },[])

    // event to trigger pause/play in the music player.
    useEffect(() => {
        playing ? audio && audio.play() : audio && audio.pause();
      },
      [playing]
    );
    
    // event to set songs source as the current index changes.
    useEffect(()=>{
        if ( songQueue.length>0 && currIndex != -1 && songQueue[currIndex]){
            audio.setAttribute('src', songQueue[currIndex].mp3fileurl)
            setAudio(audio);
            if (!(songQueue[currIndex].tid in trackLogs)){
                trackLogs.push(songQueue[currIndex].tid);
                API.updatePlay(songQueue[currIndex].tid);
            }
            updateHistory(songQueue[currIndex]);
        }
    },[currIndex])

    // event to stop playing the music once the music ends.
    useEffect(() => {
        if (audio){
            audio.addEventListener('loadeddata',()=>setPlaying(true));
            audio.addEventListener('ended', () => setPlaying(false));
            return () => {
                audio.removeEventListener('ended', () => setPlaying(false));
            };
        }
    }, [audio]);
    
    const handleAddTrack = (tid) => {
        setTid(tid)
        setModal(1)
    }
    const handleCreatePlaylist = (event) => {
        setModal(2)
    }

    const nextSong = () => {
        if (songQueue.length-1 === currIndex) return;
        setCurrIndex(currIndex+1);
        setPlaying(false);
    }

    const prevSong = () => {
        if (currIndex == 0) return;
        setCurrIndex(currIndex-1);
        setPlaying(false);
    }

    const seek = () => {

    }

    //EP added
    const setLike = (tid,action) => {
        if(action==1){
            API.setLike({"uid":currentUser.uid,"tid":tid,"action":"like"})
            likedSongs.push(tid);
            
        }else{
            API.setLike({"uid":currentUser.uid,"tid":tid,"action":"unlike"})
            likedSongs.splice(likedSongs.indexOf(tid),1);
        }
        let newLikedSongs = [...likedSongs]
        setLikedSongs(newLikedSongs)
    }

    //EP added
    const getSongsForPlaylist = (playlist) => {
        return new Promise((res,rej)=>res(tracks.filter(track => playlist.tracks.includes(track.tid))))
       /*return API.getPlaylistTracks(playlist).then(res => {
            return res.data.tracks
        })*/
    }

    //EP added
    const getFavouritesForUser = () => {
        /*return API.getUserFavourites(currentUser.uid).then(res =>{
            return res.data
        })*/
        return new Promise((res,rej)=>res(tracks.filter(track => likedSongs.includes(track.tid))))
    }

    //EP added
    const getHistoryForUser = () => {
        return tracks.filter(track => history.includes(track.tid))
        /*
        return API.getUserHistory(currentUser.uid).then(res =>{
            return res.data
        })
        return new Promise((res,rej) => {
            try{
                let t = tracks.filter(track => history.includes(track.tid))
                res(t)
            }catch(err){
                rej(err)
            }
        })*/
    }

    const updateHistory = (track) => {
        
        let newHistory = history.filter(currTrack => currTrack.tid!=track.tid);
        newHistory.push(track.tid);
        setHistory([...newHistory]);
        API.updateHistory({"uid":currentUser.uid, "trackId":track.tid})
    }

    const getTopSongs = () => {
        return new Promise((res,rej) => {
            try{
                let t = tracks.sort((a,b) => a.plays<b.plays?1:-1)
                res(t)
            }catch(err){
                rej(err)
            }
        })
    }

    //EP added
    const addPlaylist = (playlist) => {
        API.createPlaylist(playlist).then(async res => {
            //console.log(res.pid)
            playlist['pid']=res.pid
            playlist['tracks']=[]
            const toAdd={
                "pid":res.pid,
                "uid":currentUser.uid,
                "action":"addPlaylist"
            }
            playlists.push(playlist);
            let newPlaylists = playlists;
            setPlaylists(newPlaylists);
            //console.log(toAdd)
            await API.addPlaylistToUser(toAdd)
            setModal(0)
            setStatusAlert('Playlist created!');
        })
        
    }
    //EP added
    const addTrack = (tid, pid) => {
        let temptrack = {
            "tid" : tid,
            "pid" : pid,
            "action" : "addTrack"
        }
        API.addTrackToPlaylist(temptrack)
        let ps = playlists.map(playlist => {
            if(playlist.pid == pid){
                playlist.tracks.push(tid);
            }
            return playlist
        })
        setPlaylists(ps);
        setModal(0);
        setStatusAlert('Track added to playlist!');
    }

    const playNow = (track) => {
        setCurrIndex(songQueue.indexOf(track));
        setPlaying(false);
    }

    const addToQueue = (track) => {
        songQueue.push(track);
        if (currIndex === -1){
            setCurrIndex(0);
        }
        setSongQueue([...songQueue]);
        setStatusAlert('Song added to queue!');
    }   

    //EP added
    const getArtists = () => {
        return new Promise((res,rej) => res(artists))/*API.getArtists().then(data => {
            console.log(data.data)
            return data.data
          })*/
        //return []
    }
    //EP added
    const getTracks = () => {
        return API.getTracks(currentUser.uid).then(data =>{
            return data.data
          })
    }
    //EP added
    const getTracksForArtist = (aid) => {
        /*
        return API.getTracksByArtist(aid).then(data =>{
            return data.data
          })
        */
          return new Promise((res,rej) => {
            try{
                let t = tracks.filter(track => track.artist === aid)
                console.log(tracks)
                console.log(t)
                res(t)
            }catch(err){
                rej(err)
            }
        })
        //return trackList.filter(track => track.aid == aid);
    }

    
    return (
        <PlayerContext.Provider
            value = {{
                nextSong,
                prevSong,
                seek,
                setLike,
                playNow,
                songQueue,
                addToQueue,
                setSongQueue,
                playlists, 
                setPlaylists,
                history,
                setHistory,
                likedSongs, 
                setLikedSongs,
                currIndex, 
                setCurrIndex,
                getSongsForPlaylist,
                getFavouritesForUser,
                getHistoryForUser,
                updateHistory,
                getTopSongs,
                addPlaylist,
                addTrack,
                handleAddTrack,
                handleCreatePlaylist,
                audio,
                setAudio,
                playing,
                setPlaying,
                toggle,
                getArtists,
                getTracks,
                getTracksForArtist,
                tracks,
                artists,
                userRecommendations,
                popularityRecommendations,
                setStatusAlert
            }}
        >
            {
                globalLoad? <Loader/>
                :children
            }
            <StatusAlert statusAlert = {statusAlert} closeStatusAlert={()=>setStatusAlert('')} />
            <AddTrack handleClose={handleClose} open={modal===1} tid={tid} />
            <CreatePlaylist handleClose={handleClose} open={modal===2} />
        </PlayerContext.Provider>
    );
}