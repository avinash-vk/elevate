import React from 'react';
import {useHistory} from 'react-router-dom';
import {
    Grid,
    Button,
    Slide
} from '@material-ui/core';
import { makeStyles } from "@material-ui/core/styles";
import waveform from '../assets/waveform.svg'
import AuthLayout from '../Layout/AuthLayout';

const useStyles = makeStyles(() => ({
    heading1:{
        fontWeight:'bold',
        fontSize:64,
        marginTop:20,
        marginBottom:50,
        lineHeight:"64px"
    },
    heading2:{
        fontWeight:'bold',
        fontSize:36
    },
    info:{
        fontWeight:500,
        fontSize:24,
        color:"#ABABAB",
        width:"80%"
    },
    btn:{
        backgroundColor: "#EF757D",
        padding:"4%",
        paddingTop:"1%",
        paddingBottom:"1%",
        borderRadius:20,
        textTransform:"none",
        fontSize:18,
        color:"#FFF",
        fontWeight:400,
        fontFamily:"Poppins",
    },
    "@keyframes strike":{
        '0%': { 
            width:0
        },
        '100%': { 
            width:'100%'
        }
    },
    magicText:{
        "&::after":{
            borderBottom: '0.125em solid black',
            borderRadius:100,
            content:'""',
            left:0,
            position:'absolute',
            right:0,
            top:'50%',
            animation:"$strike 2s linear"
        },
        lineHeight:'1em',
        position:'relative',
    }
  }));
  
const Landing = () => {
    const classes = useStyles();
    const history = useHistory();
    return (
            <AuthLayout>
                <Slide
                    in={true}
                    timeout={1500}
                    direction="up"
                ><div style={{display:"flex",flexDirection:"column",height:"80%"}}>
                    <Grid item>
                        <img src={waveform} height="90%" />
                    </Grid>
                    <Grid item style={{flex:1}}>
                        <h1 className = {classes.heading1}>
                            Play your feel<br/>
                            <text className = {classes.heading2}>
                                Its simply <span className={classes.magicText}>magic</span> <span style={{color:"#EF757D"}}>music</span>.
                            </text>
                        </h1>
                        <p className = {classes.info}>
                            Access a large set of non copyright songs directly from the artists on your web browser.
                        </p>
                    </Grid>
                    <Grid item>
                        <Button className = {classes.btn} onClick={()=>{history.push('/signin')}}>
                            Get Started
                        </Button>
                </Grid> </div>
                </Slide>
            </AuthLayout> 
    );
}

export default Landing;