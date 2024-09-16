import React from 'react';
import { Typography } from "@mui/material";
import BookData from '../Data.json';
import SearchComponent from "../components/Services/index";
import Ind from '../components/Main/index';
import Draw from '../components/Main/Drawer';
import image from '../images/pred.jpg';
export default function Services() {

    return(
        <>
        <Ind/>
        <Draw/>
        <Typography
  variant="h3"
  component="h1"
  sx={{
    position: "absolute",
    top: 100,
    left: 0,
    width: "100%",
    textAlign: "center",
    color: "#042C30",
    animation: "pulse 2s infinite",
    height: "100%",
      }}
>
  Welcome to my website! Please feel free to search for any company's stock you want to buy or sell by entering its name in the search bar.
</Typography>


        <SearchComponent data={BookData}/>
        <img src={image} alt="Description de l'image"  style={{width: '70%', height: "58%",  position:"absolute"  , left:"17%" , bottom:"2%"}} />
        </>
    );
    }
