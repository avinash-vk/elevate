export default {
    dashboard: "/",
    profile:"/profile",
    signin:"/signin",
    signup:"/signup",
    landing:"/landing",
    forgotPassword:'/forgotPassword',
    admintrack:"/admintrack",
    adminartist:"/adminartist",
    favourites: "/favourites",
    artists: "/artist",
    artist:"/artist/:id",
    songs:"/songs",
    history:"/history",
    playlist:"/playlist/:id",
    queue:'/queue',
    searchResult:'/searchResult',

    // route generator functions
    genPlaylist:(id)=>`/playlist/${id}`,
    genArtist:(id)=>`/artist/${id}`
}