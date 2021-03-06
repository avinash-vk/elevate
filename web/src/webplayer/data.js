const userData = {
    uid:'tgsiMMRg2Ed4zcsJOrkHj9L8z8l1',
    email:'avinash2000vk@gmail.com',
    displayName:'avinash vk',
    likedSongs:[ 1 ],
    recommendations:[],
    playlists:[
        {
            pid:1,
            tracks:[1,2],
            pname:'Hype',
        }
    ],
    history:[2]
}

const tracks = [
    {
        tid:1,
        tname: "Dreams",
        aname: "NF",
        aid:1,
        time: 223,
        plays:12,
        coverUrl: "https://images.genius.com/02543f01dfa688d0e7de36632a1cd58b.1000x1000x1.jpg",
        link:'https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_1MG.mp3'
    },
    {
        tid:2,
        tname: "Layers",
        aname: "NF",
        aid:1,
        time: 200,
        plays:6,
        coverUrl: "https://images.genius.com/c1d6d5b577205c6454f665dedee3f774.1000x563x1.png",
        link: "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3"
    },
    {
        tid:3,
        tname: "Treat you better",
        aname: "Shawn mendes",
        aid:2,
        time: 300,
        plays:3,
        coverUrl: "https://images.genius.com/bf004d7c1ba188cb06c28e8966788a6d.1000x1000x1.jpg",
        link: "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_2MG.mp3"
    },
]

const artists = [
    {
        aid:1,
        aname:'NF',
        artistProfile:'https://kgo.googleusercontent.com/profile_vrt_raw_bytes_1587515314_10149.jpg'
    },
    {
        aid:2,
        aname:'Shawn Mendes',
        artistProfile:'https://gossipgist.com/uploads/25048/mendes.png'
    }
]

export default {
    userData,
    artists,
    tracks
}