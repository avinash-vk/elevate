const ENDPOINT = process.env.NODE_ENV === 'production' ? "https://elevate-music-api.herokuapp.com" : "http://localhost:5000"
let URLS;
const playlistURL = {
    createPlaylist:()=>`${ENDPOINT}/playlist/create`,
    addPlaylistToUser:()=>`${ENDPOINT}/user/playlists`,
    addTrackToPlaylist:()=>`${ENDPOINT}/user/playlist/tracks`,
    getPlaylistTracks:(id)=>`${ENDPOINT}/playlist/tracks?pid=${id}`
}

const userURL = {
    createUser: `${ENDPOINT}/user/create`,
    userAdminStatus:(id)=>`${ENDPOINT}/user/adminstat?uid=${id}`,
    getUserData : (id) => `${ENDPOINT}/user?uid=${id}`,
    setLike : () => `${ENDPOINT}/user/like`,
    getUserFavourites : (uid) => `${ENDPOINT}/user/tracks/favourites?uid=${uid}`,
    getUserHistory : (uid) => `${ENDPOINT}/user/tracks/history?uid=${uid}`,
    updateHistory: () => `${ENDPOINT}/user/history`
}

const adminURL = {
    createTrack:()=>`${ENDPOINT}/addtrack`,
    createArtist:()=>`${ENDPOINT}/addartist`
}

const artistURL = {
    getArtists:()=>`${ENDPOINT}/getartists`
}

const tracksURL = {
    getTracks:(id)=>`${ENDPOINT}/gettracks?uid=${id}`,
    getTracksByArtist:(aid)=>`${ENDPOINT}/tracks/artist?aid=${aid}`,
    getAllTracks:()=>`${ENDPOINT}/tracks/all`,
    updatePlay:(tid)=>`${ENDPOINT}/tracks/updateplay?tid=${tid}`
}

const recommenderURL ={
    getPopularity:(uid, limit) => `${ENDPOINT}/user/top?uid=${uid}&limit=${limit}`,
    getUserRecommendations: (uid, limit) => `${ENDPOINT}/user/recommend?uid=${uid}&limit=${limit}`
}
export default URLS = {
    ...playlistURL,
    ...userURL,
    ...adminURL,
    ...artistURL,
    ...tracksURL,
    ...recommenderURL
}